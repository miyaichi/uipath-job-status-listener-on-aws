# -*- coding: utf-8 -*-
import datetime
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


def scheduled_handler_wrapper(func):
    def decorate(event, context):
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        log.debug("Received event {}".format(json.dumps(event)))

        try:
            minutes = int(os.environ["interval"])
        except:
            response = {"statusCode": 200, "body": "interval not found"}
            return response

        end = datetime.datetime.now().replace(second=0, microsecond=0)
        start = end - datetime.timedelta(minutes=minutes)
        filter = "StartTime ge {}Z and StartTime lt {}Z".format(
            start.isoformat(), end.isoformat())
        log.debug("Job filter: {}".format(filter))

        joblist, message = uipath.jobs(filter)
        if joblist is not None:
            log.debug("Job list {}".format(json.dumps(joblist)))
            message = func(joblist)

        response = {"statusCode": 200, "body": message}
        return response

    return decorate


def verify_signature(secret, msg, signature):
    mac = hmac.new(secret, msg=msg, digestmod=sha256)
    return hmac.compare_digest(str(mac.digest()), str(signature))


def webhook_handler_wrapper(func):
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

        if payload["Type"] not in [
                "job.faulted", "job.completed", "job.stopped"
        ]:
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


@scheduled_handler_wrapper
def backlog_scheduled_handler(joblist):
    import handlers.backlog
    response = handlers.backlog.scheduled_handler(joblist)
    return response


@webhook_handler_wrapper
def backlog_webhook_handler(event, context):
    import handlers.backlog
    response = handlers.backlog.webhook_handler(payload)
    return response


@scheduled_handler_wrapper
def chatwork_scheduled_handler(joblist):
    import handlers.chatwork
    response = handlers.chatwork.scheduled_handler(joblist)
    return response


@webhook_handler_wrapper
def chatwork_webhook_handler(payload):
    import handlers.chatwork
    response = handlers.chatwork.webhook_handler(payload)
    return response


@scheduled_handler_wrapper
def google_hangouts_scheduled_handler(joblist):
    import handlers.google_hangouts
    response = handlers.google_hangouts.scheduled_handler(joblist)
    return response


@webhook_handler_wrapper
def google_hangouts_webhook_handler(payload):
    import handlers.google_hangouts
    response = handlers.google_hangouts.webhook_handler(payload)
    return response


@scheduled_handler_wrapper
def google_spreadsheet_scheduled_handler(joblist):
    import handlers.google_spreadsheet
    response = handlers.google_spreadsheet.scheduled_handler(joblist)
    return response


@webhook_handler_wrapper
def google_spreadsheet_webhook_handler(joblist):
    import handlers.google_spreadsheet
    response = handlers.google_spreadsheet.webhook_handler(joblist)
    return response


@scheduled_handler_wrapper
def jira_scheduled_handler(joblist):
    import handlers.jira
    response = handlers.jira.scheduled_handler(joblist)
    return response


@webhook_handler_wrapper
def jira_webhook_handler(payload):
    import handlers.jira
    response = handlers.jira.webhook_handler(payload)
    return response


@scheduled_handler_wrapper
def redmine_scheduled_handler(joblist):
    import handlers.redmine
    response = handlers.redmine.scheduled_handler(joblist)
    return response


@webhook_handler_wrapper
def redmine_webhook_handler(payload):
    import handlers.redmine
    response = handlers.redmine.webhook_handler(payload)
    return response


@scheduled_handler_wrapper
def servicenow_scheduled_handler(joblist):
    import handlers.servicenow
    response = handlers.servicenow.scheduled_handler(joblist)
    return response


@webhook_handler_wrapper
def servicenow_webhook_handler(payload):
    import handlers.servicenow
    response = handlers.servicenow.webhook_handler(payload)
    return response


@scheduled_handler_wrapper
def slack_scheduled_handler(joblist):
    import handlers.slack
    response = handlers.slack.scheduled_handler(joblist)
    return response


@webhook_handler_wrapper
def slack_webhook_handler(payload):
    import handlers.slack
    response = handlers.slack.webhook_handler(payload)
    return response


@scheduled_handler_wrapper
def wrike_scheduled_handler(joblist):
    import handlers.wrike
    response = handlers.wrike.scheduled_handler(joblist)
    return response


@webhook_handler_wrapper
def wrike_webhook_handler(payload):
    import handlers.wrike
    response = handlers.wrike.webhook_handler(payload)
    return response
