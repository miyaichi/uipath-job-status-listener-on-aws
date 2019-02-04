# -*- coding: utf-8 -*-
import gettext
import hmac
import json
import logging
import os
import requests
from hashlib import sha256

languages = [os.environ["language"]]
trans = gettext.translation(
    "messages", localedir="locale", languages=languages, fallback=True)
trans.install()


def verify_signature(secret, msg, signature):
    mac = hmac.new(secret, msg=msg, digestmod=sha256)
    return hmac.compare_digest(str(mac.digest()), str(signature))


def handler_wrapper(func):
    def decorate(event, context):
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        log.debug("Received event {}".format(json.dumps(event)))
        if event["body"]:
            log.debug("Received body {}".format(
                json.dumps(json.loads(event["body"]))))

        secret = os.environ["orchestrator_secret"]
        if secret or "X-UIPATH-Signature" in event["headers"]:
            signature = event["headers"]["X-UIPATH-Signature"].decode('base64')
            msg = event["body"].encode('utf-8')
            if not verify_signature(secret, msg, signature):
                response = {
                    "statusCode":
                    403,
                    "body":
                    json.dumps({
                        "error": _("Secret and Signature mismatch")
                    })
                }
                return response

        payload = json.loads(event["body"])

        if payload["Type"] not in ["job.faulted", "job.completed", "job.stopped"]:
            response = {
                "statusCode": 200,
                "body": json.dumps({
                    "message": _("This webhook was ignored")
                })
            }
            return response

        message = func(payload)

        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": message
            })
        }
        return response

    return decorate


@handler_wrapper
def slack(payload):
    webhook_url = os.environ["incomming_webhook_url"]

    type = payload["Type"]
    process_key = payload["Job"]["Release"]["ProcessKey"].encode("utf-8")
    info = payload["Job"]["Info"].encode("utf-8")
    machine_name = payload["Job"]["Robot"]["MachineName"].encode("utf-8")
    color = {
        "job.faulted": "danger",
        "job.completed": "good",
        "job.stopped": "warning"
    }.get(type, "")

    headers = {"Content-Type": "application/json"}
    response = requests.post(
        webhook_url,
        data=json.dumps({
            "attachments": [{
                "fallback":
                "{} {}".format(process_key, " ".join(type.split("."))),
                "color":
                color,
                "fields": [{
                    "title":
                    "{} {}".format(process_key, " ".join(type.split("."))),
                    "value":
                    info
                }],
                "footer":
                "Machine Name: {}".format(machine_name)
            }]
        }),
        headers=headers)
    return response.text


@handler_wrapper
def google_hangouts(payload):
    webhook_url = os.environ["incomming_webhook_url"]

    type = payload["Type"]
    process_key = payload["Job"]["Release"]["ProcessKey"].encode("utf-8")
    info = payload["Job"]["Info"].encode("utf-8")
    machine_name = payload["Job"]["Robot"]["MachineName"].encode("utf-8")

    headers = {"Content-Type": "application/json; charset=UTF-8"}
    response = requests.post(
        webhook_url,
        data=json.dumps({
            "text":
            "*{}* {}.\n{}\n\nMachine Name: {}".format(
                process_key, " ".join(type.split(".")), info, machine_name)
        }),
        headers=headers)
    return response.text
