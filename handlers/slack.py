import gettext
import json
import os
import requests


def post_message(attachment):
    webhook_url = os.environ["incomming_webhook_url"]

    headers = {"Content-Type": "application/json"}
    response = requests.post(
        webhook_url, data=json.dumps({
            "attachments": [attachment]
        }))
    return response


def scheduled_handler(joblist):
    for job in joblist:
        release_name = job["ReleaseName"]
        info = job["Info"]
        state = job["State"]
        color = {
            "Faulted": "danger",
            "Successful": "good",
            "Stopped": "warning"
        }.get(state, "")

        response = post_message({
            "fallback":
            "{} {}".format(release_name, state),
            "color":
            color,
            "fields": [{
                "title": "{} {}".format(release_name, state),
                "value": info
            }],
        })
        if response.status_code != 200:
            return response.text

    return _("{} messages sent").format(len(joblist))


def webhook_handler(payload):
    type = payload["Type"]
    process_key = payload["Job"]["Release"]["ProcessKey"].encode("utf-8")
    info = payload["Job"]["Info"].encode("utf-8")
    machine_name = payload["Job"]["Robot"]["MachineName"].encode("utf-8")
    color = {
        "job.faulted": "danger",
        "job.completed": "good",
        "job.stopped": "warning"
    }.get(type, "")

    response = post_message({
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
    })
    if response.status_code != 200:
        return response.text

    return _("{} messages sent").format(1)
