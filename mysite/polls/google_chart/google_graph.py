__author__ = 'John'

# !/usr/bin/python

import json


import time
from datetime import date, datetime
from time import mktime

# Example...
data_table = {
    "cols": [
        {"id": "", "label": "Topping", "pattern": "", "type": "string"},
        {"id": "", "label": "Slices", "pattern": "", "type": "number"}
    ],

    "rows": [
        {"c": [{"v": "Mushrooms", "f": None}, {"v": 3, "f": None}]},
        {"c": [{"v": "Onions", "f": None}, {"v": 1, "f": None}]},
        {"c": [{"v": "Olives", "f": None}, {"v": 1, "f": None}]},
        {"c": [{"v": "Zucchini", "f": None}, {"v": 1, "f": None}]},
        {"c": [{"v": "Pepperoni", "f": None}, {"v": 2, "f": None}]}
    ]
}

# need to handle date for json serialization
class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return int(mktime(obj.timetuple()))

        if isinstance(obj, date):
            num = mktime(datetime.combine(obj, datetime.min.time()).timetuple())
            return int(num)

        return json.JSONEncoder.default(self, obj)


# builds the google graph json to drive a simple n x n chart
class GoogleGraph:
    def __init__(self, title, col_defs):
        self.title = title
        self.cols = []
        self.col_count = len(col_defs)
        for col_def in col_defs:
            self.cols.append({"id": "", "label": col_def[0], "pattern": "", "type": col_def[1]})
        self.rows = []

    def add_row(self, row):
        rw = []
        for i in range(self.col_count):
            rw.append({"v": row[i], "f": None})
        self.rows.append({"c": rw})

    def to_json(self):
        return json.dumps({"title": self.title, "cols": self.cols, "rows": self.rows}, cls = MyEncoder)




# Example of input data...
pizza_cols = [("Topping", "string"), ("Slices", "number")]

pizza_rows = [
    ("Mushrooms", 3),
    ("Onions", 3),
    ("Olives", 3),
    ("Zucchini", 3)
]

def test1():
        gtable = GoogleGraph("Pizza Chart", pizza_cols)
        for row in pizza_rows:
            gtable.add_row(row)
        json = gtable.to_json()
        print(json)


class Counts:
    def __init__(self, date_in, count):
        self.date_in = date_in
        self.count = count


count_rows = [
    Counts(date(2010, 11, 30), 0),
    Counts(date(2011, 11, 30), 1),
    Counts(date(2012, 11, 30), 2),
    Counts(date(2013, 11, 30), 3),
    Counts(date(2014, 11, 30), 4)
]

# Example of input data...
counts_cols = [("Date", "date"), ("Count", "number")]

def test2():
        gtable = GoogleGraph("Counts Chart", counts_cols)
        for row in count_rows:
            gtable.add_row((row.date_in, row.count))
        json = gtable.to_json()
        print(json)


test1()
test2()
