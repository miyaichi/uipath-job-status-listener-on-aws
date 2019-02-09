# -*- coding: utf-8 -*-
import datetime
import gettext
import json
import logging
import os
import requests
import uipath

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

        filter = "StartTime ge {}Z".format(
            (datetime.datetime.now().replace(second=0, microsecond=0) -
             datetime.timedelta(minutes=minutes)).isoformat())
        log.debug("Job filter: {}".format(filter))

        joblist, message = uipath.jobs(filter)
        if joblist is not None:
            message = func(joblist)

        response = {"statusCode": 200, "body": message}
        return response

    return decorate


@scheduled_handler_wrapper
def chatwork(joblist):
    api_token = os.environ["api_token"]
    room_id = os.environ["room_id"]

    for job in joblist:
        release_name = job["ReleaseName"]
        info = job["Info"]
        state = job["State"]

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-ChatWorkToken": api_token
        }
        response = requests.post(
            "https://api.chatwork.com/v2/rooms/{}/messages".format(room_id),
            headers=headers,
            params={
                "body":
                "[info][title]{} {}.[/title]{}[/info]".format(
                    release_name, state, info)
            })
        if response.status_code != 200:
            return response.text

    return "{} messages sent.".format(len(joblist))


@scheduled_handler_wrapper
def google_hangouts(joblist):
    webhook_url = os.environ["incomming_webhook_url"]

    for job in joblist:
        release_name = job["ReleaseName"]
        info = job["Info"]
        state = job["State"]

        headers = {"Content-Type": "application/json; charset=UTF-8"}
        response = requests.post(
            webhook_url,
            data=json.dumps({
                "text":
                "*{}* {}.\n{}".format(release_name, state, info)
            }),
            headers=headers)
        if response.status_code != 200:
            return response.text

    return "{} messages sent.".format(len(joblist))


@scheduled_handler_wrapper
def slack(joblist):
    webhook_url = os.environ["incomming_webhook_url"]

    for job in joblist:
        release_name = job["ReleaseName"]
        info = job["Info"]
        state = job["State"]
        color = {
            "Faulted": "danger",
            "Successful": "good",
            "Stopped": "warning"
        }.get(state, "")

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            webhook_url,
            data=json.dumps({
                "attachments": [{
                    "fallback":
                    "{} {}".format(release_name, state),
                    "color":
                    color,
                    "fields": [{
                        "title": "{} {}".format(release_name, state),
                        "value": info
                    }],
                }]
            }),
            headers=headers)
        if response.status_code != 200:
            return response.text

    return "{} messages sent.".format(len(joblist))
