# coding:utf-8
import gettext
import json
import os
import requests


def post_message(process_name, state, info, machine_name):
    webhook_url = os.environ["incomming_webhook_url"]

    (process_name, state, info, machine_name) = map(
        lambda s: s.encode("utf-8"), (process_name, state, info, machine_name))

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
                "{} {}".format(process_name, state.lower()),
                "color":
                color,
                "fields": [{
                    "title":
                    "{} {}".format(process_name, state.lower()),
                    "value":
                    info
                }],
                "footer":
                "Machine Name: {}".format(machine_name)
            }]
        }))
    return response


def scheduled_handler(joblist):
    for job in joblist:
        response = post_message(job["ReleaseName"], job["State"], job["Info"],
                                job["HostMachineName"])
        if response.status_code != 200:
            return response.text

    return _("{} messages sent").format(len(joblist))


def webhook_handler(payload):
    job = payload["Job"]
    response = post_message(job["Release"]["ProcessKey"], job["State"],
                            job["Info"], job["Robot"]["MachineName"])
    if response.status_code != 200:
        return response.text

    return _("{} messages sent").format(1)
