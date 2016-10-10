__author__ = 'John'

# !/usr/bin/python

import json
from datetime import date, datetime
from time import mktime

# Example of input (custom format)
pizza_col_def = [("Topping", "string"), ("Slices", "number"), ("BornDate", "date")]

pizza_rows = [
    ("Mushrooms", 3, date(2010, 11, 30)),
    ("Onions", 3, date(2010, 11, 30)),
    ("Olives", 3, date(2010, 11, 30)),
    ("Zucchini", 3, date(2010, 11, 30))
]

# Example of output (this is format for Google Graph)
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

# need to handle date for json serialization of dates and google chart
# needing date to be captured as javascript function "Date"
class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return int(mktime(obj.timetuple()))

        if isinstance(obj, date):
            ds = obj.strftime("Date(%Y,%m,%d)")
            return ds

        return json.JSONEncoder.default(self, obj)


# builds the google graph json to drive a simple n x n chart
class GoogleGraph:
    # cross reference between custom types and python types...
    column_types = {
        "number": [int, float],
        "string": [str],
        "date": [date]
    }

    def __init__(self, header, col_defs):
        self.header = header
        self.cols = []
        self.rows = []

        if not isinstance(header, dict):
            raise TypeError("GoogleGraph header is not a dictionary: {0}".format(type(header)))

        self.col_count = len(col_defs)
        for col_def in col_defs:
            # verify column type...
            if not col_def[1] in self.column_types:
                raise TypeError("Unrecognized type in GoogleGraph column: {0}".format(col_def[1]))
            self.cols.append({"id": "", "label": col_def[0], "pattern": "", "type": col_def[1]})

    def add_row(self, row):
        rw = []
        for i in range(self.col_count):
            value = row[i]
            formatted = None

            # check input data against column type...
            if not type(value) in self.column_types[self.cols[i]["type"]]:
                raise TypeError("GoogleGraph Type Should Be {0} but is {1}".format(self.cols[i]["type"], type(value)))

            # add special formatting for date...
            if self.cols[i]["type"] == "date":
                formatted = value.strftime("%m/%d/%y")
            rw.append({"v": value, "f": formatted})

        self.rows.append({"c": rw})

    # returns the value at rc
    def get_rc_value(self, r, c):
        return self.rows[r]["c"][c]["v"]

    def to_json(self):
        return json.dumps({"header": self.header, "cols": self.cols, "rows": self.rows}, cls = MyEncoder)


# Example of input data...
counts_cols = [("Date", "date"), ("Count", "number")]

count_rows = [
    (date(2010, 11, 30), 0),
    (date(2011, 11, 30), 1),
    (date(2012, 11, 30), 2),
    (date(2013, 11, 30), 3),
    (date(2014, 11, 30), 4)
]

def test2():
        gtable = GoogleGraph({"title": "Counts Chart"}, counts_cols)
        for row in count_rows:
            gtable.add_row(row)
        json = gtable.to_json()

test2()
