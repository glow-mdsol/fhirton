# -*- coding: utf-8 -*-

__author__ = 'glow'
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class ClinicalStudy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(80), index=True)
    study_name = db.Column(db.String(80), index=True)
    environment = db.Column(db.String(24))

class StudyParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rave_id = db.Column(db.Integer, db.ForeignKey('clinical_study.id'), index=True)
    subject_name = db.Column(db.String(48))
    uuid = db.Column(db.String(80), index=True)

    @classmethod
    def get_by_uuid(cls, uuid):
        return cls.query.filter(cls.uuid == uuid).first()