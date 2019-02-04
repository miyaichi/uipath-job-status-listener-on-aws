# -*- coding: utf-8 -*-
import gettext
import hmac
import json
import logging
import os
import requests
import uipath
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
        if event["body"]:
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

    event_id = payload["EventId"]
    timestamp = payload["Timestamp"]
    job = payload["Job"]

    # slack post
    webhook_url = "https://hooks.slack.com/services/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"
    color = {
        "job.faulted": "#FF0000",
        "job.completed": "#00FF00",
        "job.stopped": "#FFFF00"
    }
    requests.post(
        webhook_url,
        data=json.dumps({
            "attachments": [{
                "fallback":
                type,
                "pretext":
                type,
                "color":
                color.get(type, "F0F0F0"),
                "fields": [{
                    "title": job["Release"]["ProcessKey"],
                    "value": job["Info"]
                }]
            }]
        }))

    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": json.dumps(payload)
        })
    }
    return response
