# -*- coding: utf-8 -*-
import gettext
import hmac
import json
import logging
import os
from hashlib import sha256

languages = [os.environ["language"]]
trans = gettext.translation(
    "messages", localedir="locale", languages=languages, fallback=True)
trans.install()


def monitoring(func):
    def decorate(event, context):
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        log.debug("Received event {}".format(json.dumps(event)))
        log.debug("Received body {}".format(
            json.dumps(json.loads(event["body"]))))
        response = func(event, context)
        log.debug("Response {}".format(json.dumps(response)))
        return response

    return decorate


def verify_signature(secret, msg, signature):
    mac = hmac.new(secret, msg=msg, digestmod=sha256)
    return hmac.compare_digest(str(mac.digest()), str(signature))


@monitoring
def handler(event, context):
    if os.environ["secret"] or "X-UIPATH-Signature" in event["headers"]:
        secret = os.environ["secret"]
        signature = event["headers"]["X-UIPATH-Signature"].decode('base64')
        msg = event["body"].encode('utf-8')
        if not verify_signature(secret, msg, signature):
            response = {
                "statusCode": 403,
                "body": json.dumps({
                    "error": _("Secret and Signature mismatch")
                })
            }
            return response

    payload = json.loads(event["body"])

    type = payload["Type"]
    if type not in ["job.faulted", "job.completed", "job.stopped"]:
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": _("This webhook was ignored")
            })
        }
        return response

    # something to do

    #   event_id = payload["EventId"]
    #   timestamp = payload["Timestamp"]
    #   job_id = payload["Jobs"]["Id"]
    #   job_info = payload["Jobs"]["Info"]
    #   release_id = payload["Release"]["Id"]
    #   release_key = payload["Release"]["Key"]

    response = {"statusCode": 200, "body": json.dumps({"message": json.dumps(payload)})}
    return response
