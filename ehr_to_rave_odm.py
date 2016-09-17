# -*- coding: utf-8 -*-
import config

__author__ = 'isparks'

from rwslib.builders import *
from rwslib import RWSConnection
from rwslib.rws_requests import PostDataRequest, SubjectDatasetRequest
from datetime import datetime
from random import choice
from string import ascii_letters

def get_subject_data(study_uuid, subject_uuid):
    connection = RWSConnection(config.USERNAME, config.PASSWORD)
    data = connection.send_request(SubjectDatasetRequest())


class Folder(object):
    def __init__(self, oid, repeat=None):
        self.oid = oid
        self.repeat = repeat
        self.forms = {}


class Form(object):
    def __init__(self, oid, repeat=None):
        self.oid = oid
        self.repeat = repeat
        self.records = {}  # Keyed on context item or None.

    def add_field(self, row):
        field_oid = row['field_oid']
        value = row.get('value', None)
        measurement_unit = row.get('measurement_unit', None)
        specify_value = row.get('specify_value', None)
        context_field_oid = row.get('log_context_field', None)
        context_field_value = row.get('log_context_value', None)
        raw_value = row.get('esource_value')

        # Is this the value that we're using to find the log form by context? I.e. unique identifying field.
        is_context = field_oid == context_field_oid

        # Is it a new value we want to add?
        is_new = row.get('is_new', False)

        record = self.records.setdefault(context_field_value, Record())
        f = Field(field_oid, value, specify_value, measurement_unit, raw=raw_value,
                  context_item=is_context, is_new=is_new)

        # Did we see the context field? If we didn't we will have to add it later
        record.has_context_field = record.has_context_field or is_context

        # Note that the record takes the last field oid and value it is passed
        record.context_field_oid = context_field_oid
        record.context_field_value = context_field_value

        record.fields.append(f)


class Record(object):
    def __init__(self):
        self.fields = []
        self.has_context_field = False
        self.context_field_oid = None
        self.context_field_value = None


class Field(object):
    def __init__(self, oid, value, specify_value, measurement_unit, raw, context_item=False, is_new=False):
        self.oid = oid
        self.value = value
        self.specify_value = specify_value
        self.measurement_unit = measurement_unit
        self.context_item = context_item
        self.raw = raw # unadulterated eSource value
        self.is_new = is_new  # On a context item, are we seeking to update or add this?


def make_odm(study_oid, environment, site_oid, subject_oid, mapping,
             retrieved_datetime, transfer_user, transfer_identifier, freeze=True):
    """Receives a mapping like:

       [
         dict(folder_oid="SCRN", form_oid="DM", field_oid="SEX", value="M", cdash_domain="DM", cdash_element="SEX"),
         dict(folder_oid="SCRN", form_oid="DM", field_oid="DOB", value="1965-02-09", cdash_domain="DM",
           cdash_element="DOB"),
         ...
       ]

       Unpacks this into a ODM Message broken up by [folder][form][record][field]

    """
    # Sort unstructured dicts into hierarchy of objects to send
    folders = {}  # Map of folders to forms to records to fields
    for row in mapping:
        folder_oid = row.get('folder_oid', 'SUBJECT')

        folder = folders.get(folder_oid, False)
        if not folder:
            folder = Folder(folder_oid)
            folders[folder_oid] = folder

        form_oid = row.get('form_oid')

        form = folder.forms.get(form_oid, False)
        if not form:
            form = Form(form_oid)
            folder.forms[form_oid] = form

        # add_field sorts into appropriate records
        form.add_field(row)

    # Now loop through our structure and build ODM
    study_events = []
    for folder_oid in folders:
        folder = folders[folder_oid]

        study_event = StudyEventData(folder.oid, study_event_repeat_key=None)  # TODO: Folder repeat key?
        study_events.append(study_event)

        # Loop through forms in folder
        for form_oid in folder.forms:
            form = folder.forms[form_oid]

            # Add formdata to study event
            formdata = FormData(form.oid, transaction_type="Update")
            study_event << formdata

            # Loop through records we gathered
            for record_context in form.records:
                record = form.records[record_context]

                params = {}
                if record_context is not None:
                    # Log line?
                    params['oid'] = "{0}_LOG_LINE".format(form_oid)

                ig = ItemGroupData()

                # Add itemgroupdata to formdata
                formdata << ig

                # Add all items to itemgroupdata along with external audits to show where they came from
                for field in record.fields:
                    transaction_type = None
                    if field.context_item:

                        if field.is_new:
                            ig.transaction_type = 'Upsert'
                        else:
                            # We want to do a seek an update
                            transaction_type = "Context"
                            ig.transaction_type = 'Update'
                        ig.item_group_repeat_key = '@CONTEXT'
                    ehr_message = "Import from EHR: EHR Source Value %s -> Submitted value: %s" % (field.raw, field.value)
                    item_data = ItemData(field.oid,
                                         field.value,
                                         specify_value=field.specify_value,
                                         transaction_type=transaction_type,
                                         freeze=freeze)(
                            AuditRecord(used_imputation_method=False,
                                        identifier=transfer_identifier,
                                        include_file_oid=False)(
                                    UserRef(transfer_user),
                                    LocationRef(site_oid),
                                    ReasonForChange(ehr_message),
                                    # Any string, just becomes part of documentation in Audit trail
                                    DateTimeStamp(retrieved_datetime)

                            )
                    )

                    # Measurement unit related to this value?
                    if field.measurement_unit is not None:
                        item_data << MeasurementUnitRef(field.measurement_unit)

                    # Add to itemgroup
                    ig << item_data

                # In context update situation we need to pass the value of the conext field with transaction type
                # of context. So if that is not one of the fields passed in we need to include it for this record
                if not record.has_context_field and record_context is not None:
                    # create the itemdata element, add the mdsol:Freeze attribute
                    ig << ItemData(record.context_field_oid, record.context_field_value, transaction_type="Context",
                                   freeze=freeze)
                    ig.item_group_repeat_key = '@CONTEXT'

    odm = ODM("EHRImport")(
            ClinicalData(study_oid, environment)(
                    SubjectData(site_oid, subject_oid, transaction_type="Update", subject_key_type='SubjectUUID')(*study_events)
            )
    )
    return odm



def audit_id():
    """

    :return: An audit ID, a (hopefully) unique string of characters acceptable as an external audit ID to Rave.
             I don't think this is required but it's good to have the traceability from Rave data back to the
             EHR import/transaction that sent it.
    """
    ret = []
    for i in range(15):
        ret.append(choice(ascii_letters))
    return 'audit_{0}'.format(''.join(ret))


if __name__ == '__main__':
    mapping_values = [

        dict(folder_oid="SCREEN", form_oid="DM", field_oid="BRTHDTC", value="01 JAN 1980"),
        # NB. Need to know date format
        dict(folder_oid="SCREEN", form_oid="DM", field_oid="SEX", value="MALE"),  # Male
        dict(folder_oid="SCREEN", form_oid="DM", field_oid="RACE", value="5", specify_value="Mixed Race"),
        # 3=White 5=Other Specify
        dict(folder_oid="VISIT01", form_oid="VS", field_oid="PULSE", value="82"),
        dict(folder_oid="VISIT01", form_oid="VS", field_oid="TEMP", value="33.1", measurement_unit="Celsius"),

        # For AE's going to use AEACNOTH as a context value for now. Later we'll need a surrogate. AEACNOTH is just a handy text field.
        dict(folder_oid="SUBJECT", form_oid="AE", field_oid="AETERM", value="AE 1", log_context_field="AEACNOTH",
             log_context_value="XX1"),
        dict(folder_oid="SUBJECT", form_oid="AE", field_oid="AESTDTC", value="02 Jan 1970",
             log_context_field="AEACNOTH", log_context_value="XX1"),

        # This is a context field. When is_new = True the record get inserted. If is_new = True then it's used to identify the record to update
        dict(folder_oid="SUBJECT", form_oid="AE", field_oid="AEACNOTH", value="XX1", log_context_field="AEACNOTH",
             log_context_value="XX1", is_new=False),

        dict(folder_oid="SUBJECT", form_oid="AE", field_oid="AETERM", value="AE 3", log_context_field="AEACNOTH",
             log_context_value="XX3"),
        dict(folder_oid="SUBJECT", form_oid="AE", field_oid="AESTDTC", value="03 Feb 1981",
             log_context_field="AEACNOTH", log_context_value="XX3"),
        dict(folder_oid="SUBJECT", form_oid="AE", field_oid="AEACNOTH", value="XX3", log_context_field="AEACNOTH",
             log_context_value="XX3", is_new=True),
        # Must send a line like this if you want to CREATE a record.

    ]

    odm = make_odm("Mediflex", "Dev", "MDSOL", "222 IJS", mapping_values, datetime.now(), "EHR Import User", audit_id())
    request = PostDataRequest(str(odm))

    print(str(odm))

    rave = RWSConnection('innovate', 'username', 'password')
    print(rave.send_request(request))
