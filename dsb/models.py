from datetime import datetime
from typing import List


class Picture:

    def __init__(self, photo: str, title: str, preview_url: str):
        self.photo: str = photo
        self.title: str = title
        self.preview_url: str = "https://light.dsbcontrol.de/DSBlightWebsite/Data/" + preview_url


class Entry:

    def __init__(self, raw_data: dict, date: datetime, plan_mapping: dict):
        self._raw_data = raw_data
        self.__plan_mapping = plan_mapping
        self.date = date

    def __getattr__(self, item: str):
        if item in self._raw_data.keys():
            return self._raw_data[item]

        if item in self.__plan_mapping.keys():
            if self.__plan_mapping[item] in self._raw_data.keys():
                return self._raw_data[self.__plan_mapping[item]]
        raise AttributeError(f"Entry has no attribute {item}")


class Day:

    def __init__(self, date: datetime, entries: List[Entry]):
        self.date = date
        self.entries = entries
