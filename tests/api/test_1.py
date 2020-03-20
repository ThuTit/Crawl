from datetime import datetime
import random

import requests

from settings import PCR_URL_TEST1

url = PCR_URL_TEST1 + 'schedulers'


def test_create():
    for i in range(10):
        _json = {
            "name": "Thu test pcr 82 " + str(i),
            "taskId": 1,
            "sellerId": 1,
            "active": random.choice([True, False]),
            "scheduleType": "WEEKLY",
            "startDate": "2020-02-28",
            "scheduleTime": "15:12",
            "settings": {
                "repeat_days": [
                    0,
                    1,
                    2,
                    3, 4, 5, 6
                ]
            },
            "variables": {
                # "template": "send_email_compare_price",
                "shop_ids": [55, 54, 52, 53, 51],
                "category_ids": ["01-N001", "01-N001-01", "01-N001-01-01", "01-N001-01-01-01", "01-N001-01-01-02", "01-N001-01-02", "01-N001-01-02-01", "01-N001-01-02-02", "01-N001-02", "01-N001-02-01", "01-N001-02-01-01", "01-N001-02-01-02", "01-N001-02-02", "01-N001-02-02-01", "01-N001-02-02-02", "01-N001-03", "01-N001-03-01"],
                "subject": "Thu test pcr 82 " + str(i),
                "receivers": [
                    "thu.nt1@teko.vn"
                ]
            }
        }
        requests.post(url=url, json = _json)

