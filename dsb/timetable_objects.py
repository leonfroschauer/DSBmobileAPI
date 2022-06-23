from datetime import datetime
from typing import List
from collections import defaultdict

from .models import Picture, Day, Entry
from bs4 import BeautifulSoup
from urllib.request import urlopen


class TimetableObject:

    def __init__(self, raw_data: dict):
        self._id: str = raw_data["Id"]
        self._title: str = raw_data["Title"]
        self._detail: str = raw_data["Detail"]
        self._tags: str = raw_data["Tags"]
        self._preview: str = raw_data["Preview"]

        self._content_type = int(raw_data["ConType"])
        self._priority = int(raw_data["Prio"])
        self._index = int(raw_data["Index"])

        self._date_published = datetime.strptime(raw_data["Date"], "%d.%m.%Y %H:%M")


class Plan(TimetableObject):

    def __init__(self, raw_data: dict, plan_mapping: dict = None):
        super().__init__(raw_data)

        self.plan_mapping = plan_mapping if plan_mapping else {}
        self._children: List[TimetableObject] = []
        self._links: List[str] = []
        for child in raw_data["Childs"]:
            self._children.append(Plan(child))
            self._links.append(child["Detail"])

        self.days = self._parse_links(self._links)

    def _parse_links(self, links: List[str]) -> List[Day]:
        plans = defaultdict(list)

        for link in links:
            entries = self.__extract_entries(link)
            if entries:
                plans[entries[0].date].extend(entries)

        days = []
        for day in plans.keys():
            days.append(Day(day, plans[day]))
        return days

    def __extract_entries(self, link: str) -> List[Entry]:
        soup = BeautifulSoup(urlopen(link), features="html.parser")
        table = soup.find_all(class_="mon_list")[0]
        rows = table.find_all("tr", {"class": "list"})

        try:
            date = soup.find("div", {"class": "mon_title"}).text.split(" ")[0]
            date = datetime.strptime(date, "%d.%m.%Y")
        except IndexError:
            date = datetime(1900, 1, 1)

        basic_entries: List[str] = [child.text for child in rows[0].findChildren()]

        entries: List[Entry] = []
        for row in rows[1:]:
            children = {}
            for key, child in zip(basic_entries, row.findChildren()):
                children[key] = child.text if child.text != "\xa0" else None
            entries.append(Entry(children, date, self.plan_mapping))
        return entries


class News(TimetableObject):

    def __init__(self, raw_data: dict):
        super().__init__(raw_data)
        self.title: str = self._title
        self.content: str = self._detail

        self._children: List[TimetableObject] = []
        for child in raw_data["Childs"]:
            self._children.append(News(child))


class Posting(TimetableObject):

    def __init__(self, raw_data: dict):
        super().__init__(raw_data)
        self.title: str = self._title

        self._children: List[TimetableObject] = []
        for child in raw_data["Childs"]:
            self._children.append(Posting(child))

        self.pictures: List[Picture] = []
        for child in self._children:
            picture = Picture(child._detail, child._title, child._preview)
            self.pictures.append(picture)

