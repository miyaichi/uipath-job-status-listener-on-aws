# coding:utf-8
import gettext
import json
import os
import requests


def post_message(process_name, state, info, machine_name):
    api_token = os.environ["api_token"]
    room_id = os.environ["room_id"]

    (process_name, state, info, machine_name) = map(
        lambda s: s.encode("utf-8"), (process_name, state, info, machine_name))

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-ChatWorkToken": api_token
    }
    response = requests.post(
        "https://api.chatwork.com/v2/rooms/{}/messages".format(room_id),
        headers=headers,
        params={
            "body":
            "[info][title]{} {}.[/title]{}\n\nMachine Name: {}[/info]".format(
                process_name, state.lower(), info, machine_name)
        })
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
