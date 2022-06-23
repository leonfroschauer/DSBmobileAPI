import json

import requests

from .timetable_objects import Plan, Posting, News


class DSB:
    BASE_ULR = "https://mobileapi.dsbcontrol.de/"

    def __init__(self, username: str, password: str):
        self._username: str = username
        self._password: str = password

        self.__token = None

    def get_plans(self, plan_mapping: dict = {}) -> list:
        raw_data = self.__get_raw_data("dsbtimetables")
        return [Plan(data, plan_mapping) for data in raw_data]

    def get_news(self) -> list:
        raw_data = self.__get_raw_data("newstab")
        return [News(data) for data in raw_data]

    def get_postings(self) -> list:
        raw_data = self.__get_raw_data("dsbdocuments")
        return [Posting(data) for data in raw_data]

    _get_raw_plan_data = lambda self: self.__get_raw_data(endpoint="dsbtimetables")
    _get_raw_news_data = lambda self: self.__get_raw_data(endpoint="newstab")
    _get_raw_posting_data = lambda self: self.__get_raw_data(endpoint="dsbdocuments")

    def __get_raw_data(self, endpoint: str) -> list:
        req = requests.get(self.BASE_ULR + endpoint, params={"authid": self._authentication_token()})
        return json.loads(req.text)

    def _authentication_token(self) -> str:
        if self.__token:
            return self.__token
        self.__token = self.__request_new_token()
        return self.__token

    def __request_new_token(self) -> str:
        params = {
            "user": self._username,
            "password": self._password,
            "bundleid": "de.heinekingmedie.dsbmobile",
            "appversion": 35,
            "osversion": 22,
        }
        req = requests.get(self.BASE_ULR + "authid?pushid", params=params)
        return json.loads(req.content)
