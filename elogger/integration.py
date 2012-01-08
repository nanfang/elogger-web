# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import json
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

class Integration:
    def get_month_logs(self, username, year, month, callback):
        return callback({})

    def put_day_log(self, username, year, month, day, content, callback):
        return callback(True)


class DummyIntegration(Integration):
    dummy_data = {
        2011: {12: {
            '11': 'test, 测试',
            '12': 'test, 测试',
            '13': 'test, 测试',
            '14': 'test, 测试',
            }
        }
    }

    def get_month_logs(self, username, year, month, callback):
        callback(
            self.dummy_data.get(year, {}).get(month,{})
        )

    def put_day_log(self, username, year, month, day, content, callback):
        if year not in self.dummy_data:
            self.dummy_data[year]={}
        if month not in self.dummy_data[year]:
            self.dummy_data[year][month]={}

        self.dummy_data[year][month][day]=content
        return callback(True)


class ApiIntegration(Integration):
    http_client = AsyncHTTPClient()

    def __init__(self, api_url, master_key):
        self.api_url = api_url
        self.master_key = master_key

    def get_month_logs(self, username, year, month, callback):
        self.http_client.fetch(
            HTTPRequest(
                url=self.api_url,
                auth_username=username,
                auth_password=self.master_key,
            ),
            callback=lambda response: callback(json.loads(response.body))
        )


def get_integration():
    return  DummyIntegration()

integration = get_integration()