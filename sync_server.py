from datetime import datetime
import time

import asyncio
from fhirclient.client import FHIRClient
from fhirclient.models.subscription import Subscription
from flask import Flask, request, Response
import logging


from subscriber import PseudoSubscription

SMARTSTU_OPEN = "http://localhost:9074/smartstu3/open"

app = Flask(__name__)
app.config['SECRET_KEY'] = '!secret!'
logger = app.logger

CACHE = {}


@app.route("/hook", methods=['GET', 'POST'])
def hook():
    print("Hook!: {0} => {0.method}".format(request))
    if request.method == "POST":
        print("New resource {0}".format(request.json))
    elif request.method == "GET":
        print("Processing GET Request")
    return Response(status=200)


@app.route("/subscriptions")
def subscriptions():
    if request.method == "GET":
        # firstly, get the subscriptions
        process()
        return 'OK'

def process():
    logger.info("Processing")
    APP_ID = "com.mdsol.ehr.connectathon-16.app"
    base_url = SMARTSTU_OPEN
    client = FHIRClient(settings=dict(app_id=APP_ID, api_base=base_url))
    resp = Subscription.where(struct={})
    tasks = []
    for subc in resp.perform_resources(client.server):
        tasks.append(asyncio.ensure_future(execute(subc)))
    print("Number of tasks: %s" % len(tasks))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    # for subscription in _subscriptions:
    #
    #     print("Processing {}".format(subscription.criteria))
    #     _results = execute(subscription, client)
    #     print("Result: {}".format( _results))
    #     results.extend(_results)


async def execute(subscription: Subscription) -> list:
    APP_ID = "com.mdsol.ehr.connectathon-16.app"
    base_url = SMARTSTU_OPEN
    client = FHIRClient(settings=dict(app_id=APP_ID, api_base=base_url))
    last_updated = CACHE.get(subscription.id, datetime.now())
    subs = PseudoSubscription(name=subscription.id,
                              last_updated=last_updated,
                              criteria=subscription.criteria,
                              reason=subscription.reason,
                              base_url=SMARTSTU_OPEN,
                              endpoint=subscription.channel.endpoint)
    print("Defined subscription: %s" % subs)
    results = subs.execute(client.server)
    CACHE[subscription.id] = datetime.now()
    return results


if __name__ == "__main__":
    app.run()


