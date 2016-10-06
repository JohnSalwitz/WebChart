__author__ = 'John'

# !/usr/bin/python

import json

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

# Example of input data...
col_def = [("Topping", "string"), ("Slices", "number")]

my_rows = [
    ("Mushrooms", 3),
    ("Onions", 3),
    ("Olives", 3),
    ("Zucchini", 3)
]

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
        return json.dumps({"title": self.title, "cols": self.cols, "rows": self.rows})
