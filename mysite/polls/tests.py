from datetime import date
from django.test import TestCase
from .google_chart import google_graph


class GoogleGraphTest(TestCase):

    pizza_col_def = [("Topping", "string"), ("Slices", "number"), ("BornDate", "date")]

    pizza_rows = [
        ("Mushrooms", 3, date(2010, 11, 30)),
        ("Onions", 3, date(2010, 11, 30)),
        ("Olives", 3, date(2010, 11, 30)),
        ("Zucchini", 3, date(2010, 11, 30))
    ]

    def setUp(self):
        self.gtable = google_graph.GoogleGraph({"title": "Pizza Chart"}, self.pizza_col_def)
        for row in self.pizza_rows:
            self.gtable.add_row(row)

    def test_title(self):
        self.assertEqual(self.gtable.header["title"], "Pizza Chart")

    def test_col_def(self):
        c = 0
        for col in self.pizza_col_def:
            self.assertEqual(self.gtable.cols[c]["label"], col[0])
            self.assertEqual(self.gtable.cols[c]["type"], col[1])
            c += 1

    def test_rows(self):
        r = 0
        for row in self.pizza_rows:
            self.assertEqual(self.gtable.get_rc_value(r, 0), row[0])
            self.assertEqual(self.gtable.get_rc_value(r, 1), row[1])
            r += 1