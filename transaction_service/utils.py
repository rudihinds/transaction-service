import json


def transpose_event(event):
    body = bytes(event).decode()
    return json.loads(body)
