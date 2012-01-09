# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import json
import uuid
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from elogger import settings

class Integration:
    def get_month_logs(self, username, year, month, callback):
        return callback({})

    def put_day_log(self, username, year, month, day, content, callback):
        return callback(True)

    def register_user(self, user, callback):
        callback()

class DummyIntegration(Integration):
    dummy_data = {
        2011: {12: {
            '11': 'test, 测试',
            '12': 'test, 测试',
            '13': 'test, 测试',
            '14': 'test, 测试',
            }
        },
        2012: {1: {
            '1': 'test, 测试',
            '2': 'test, 测试',
            '5': 'test, 测试',
            '6': 'test, 测试',
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

    def __init__(self, api_url, admin, master_key):
        self.api_url = api_url
        self.admin = admin
        self.master_key = master_key

    def get_month_logs(self, username, year, month, callback):
        self.http_client.fetch(
            HTTPRequest(
                url='%s/daylogs?year=%s&month=%s' % (self.api_url,year, month),
                auth_username=username,
                auth_password=self.master_key,
            ),
            callback=lambda response: callback(self._on_get_logs(response))
        )

    def put_day_log(self, username, year, month, day, content, callback):
        self.http_client.fetch(
            HTTPRequest(
                method='POST',
                url='%s/daylogs' % self.api_url,
                auth_username=username,
                auth_password=self.master_key,
                body=json.dumps(dict(
                    year=year,
                    month=month,
                    day=day,
                    content=content
                ))
            ),
            callback=lambda response: callback(response.code==200)
        )

    def _on_get_logs(self, response):
        return dict([(log['day'],log['content']) for log in  json.loads(response.body)])

    def register_user(self, user, success):
        self.http_client.fetch(
            HTTPRequest(
                method="POST",
                url='%s/users' % self.api_url,
                auth_username=self.admin,
                auth_password=self.master_key,
                body=json.dumps(dict(
                    username=user['username'],
                    type='SERVER',
                    api_key='',
                )),
            ),
            callback = lambda response:success()
        )

def get_integration():
#    return  DummyIntegration()
    return ApiIntegration(settings.API_HOST, settings.ADMIN, settings.MASTER_KEY)

integration = get_integration()