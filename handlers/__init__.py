# coding:utf-8
import datetime
import json
import os
import pytz


def dumps(data):
    data = flatten(data)
    data = timeformat(data)
    return json.dumps(
        data, ensure_ascii=False, encoding="utf-8", sort_keys=True, indent=4)


def flatten(nested_data):
    def _flatten(x, name=""):
        if type(x) is dict:
            for a in x:
                _flatten(x[a], name + a + "_")
        elif type(x) is list:
            i = 0
            for a in x:
                _flatten(a, name + str(i) + "_")
                i += 1
        else:
            flat_data[name[:-1]] = x

    flat_data = {}
    _flatten(nested_data)
    return flat_data


def timeformat(data):
    tz = os.environ["timezone"]
    for key in data.keys():
        if key.endswith("Time"):
            try:
                data[key] = datetime.datetime.strptime(
                    data[key], "%Y-%m-%dT%H:%M:%S.%fZ").replace(
                        tzinfo=pytz.timezone("UTC")).astimezone(
                            pytz.timezone(tz)).strftime("%Y-%m-%d %H:%M:%S")
            except:
                pass

    return data
