# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import json
import logging
import urllib
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from elogger.config import secret
from elogger.constants import LOG_TYPE_DAY_LOG

logger = logging.getLogger(__name__)

class Integration:
    def get_month_logs(self, username, year, month, callback):
        return callback({})

    def put_day_log(self, id, username, year, month, day, content, callback):
        return callback(True)


class DummyIntegration(Integration):
    dummy_data = {
        2011: {12: {
            '11': 'test',
            '12': 'test',
            '13': 'test',
            '14': 'test',
        }
        },
        2012: {1: {
            '1': 'test',
            '2': 'test',
            '5': 'test',
            '6': 'test',
        }
        }
    }

    def get_month_logs(self, username, year, month, callback):
        callback(
            self.dummy_data.get(year, {}).get(month, {})
        )

    def put_day_log(self, id, username, year, month, day, content, callback):
        if year not in self.dummy_data:
            self.dummy_data[year] = {}
        if month not in self.dummy_data[year]:
            self.dummy_data[year][month] = {}

        self.dummy_data[year][month][day] = content
        return callback(True)


class ParseIntegration(Integration):
    http_client = AsyncHTTPClient()
    api_host = 'https://api.parse.com/1/'

    def __init__(self, app_id, api_key):
        self.api_header = {
            "X-Parse-Application-Id": app_id,
            "X-Parse-REST-API-Key": api_key,
            "Content-Type": "application/json"
        }

    def put_day_log(self, id, userid, year, month, day, content, callback):
        """
        create or update day log
        """
        url, method = ('%s/classes/DayLog/%s' % (self.api_host, id), 'PUT' ) if id\
        else ('%s/classes/DayLog' % self.api_host, 'POST')
        request = HTTPRequest(
            url=url,
            headers=self.api_header,
            method=method,
            body=json.dumps(dict(
                userid=userid,
                year=year,
                month=month,
                day=day,
                content=content
            )),
        )

        def _get_response(response):
            # TODO handle errors
            if id:
                callback(id)
            else:
                result = json.loads(response.body)
                callback(result['objectId'])

        self.http_client.fetch(request, callback=_get_response)


    def get_month_logs(self, userid, year, month, callback):
        params = urllib.urlencode({"where": json.dumps({
            'userid': userid,
            'year': year,
            'month': month,

        })})
        url = '%s/classes/DayLog?%s' % (self.api_host, params)
        request = HTTPRequest(url=url, headers=self.api_header, method='GET')
        def _on_response(response):
            day_logs = {}
            for log in json.loads(response.body)['results']:
                day = log['day']
                if day not in day_logs:
                    day_logs[day] = []
                day_logs[day].append(dict(
                    content=log['content'],
                    id=log['objectId'],
                    title='',
                    type=LOG_TYPE_DAY_LOG
                ))
            return day_logs

        self.http_client.fetch(request,
            callback=lambda response: callback(_on_response(response))
        )



def get_integration():
#    return  DummyIntegration()
    return ParseIntegration(secret.PARSE_APPLICATION_ID, secret.PARSE_REST_API_KEY)

integration = get_integration()