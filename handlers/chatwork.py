import json
import os
import requests


def post_message(body):
    api_token = os.environ["api_token"]
    room_id = os.environ["room_id"]

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-ChatWorkToken": api_token
    }
    response = requests.post(
        "https://api.chatwork.com/v2/rooms/{}/messages".format(room_id),
        headers=headers,
        params={"body": body})
    return response


def scheduled_handler(joblist):
    for job in joblist:
        release_name = job["ReleaseName"]
        info = job["Info"]
        state = job["State"]

        response = post_message("[info][title]{} {}.[/title]{}[/info]".format(
            release_name, state, info))
        if response.status_code != 200:
            return response.text

    return _("{} messages sent").format(len(joblist))


def webhook_handler(payload):
    type = payload["Type"]
    process_key = payload["Job"]["Release"]["ProcessKey"].encode("utf-8")
    info = payload["Job"]["Info"].encode("utf-8")
    machine_name = payload["Job"]["Robot"]["MachineName"].encode("utf-8")

    response = post_message(
        "[info][title]{} {}.[/title]{}\n\nMachine Name: {}[/info]".format(
            process_key, " ".join(type.split(".")), info, machine_name))
    if response.status_code != 200:
        return response.text

    return _("{} messages sent").format(1)