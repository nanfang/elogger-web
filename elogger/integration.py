# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import json
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

class Integration:
    def get_month_logs(self, username,year, month, callback):
        return callback({})


class DummyIntegration(Integration):
    def get_month_logs(self, username, year, month, callback):
        callback({
            '2011-10-11':'test, 测试'
        })


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
            callback=lambda response:callback(json.loads(response.body))
        )


def get_integration():
    return  DummyIntegration()

integration = get_integration()