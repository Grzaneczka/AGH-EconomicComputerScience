from storage.warehouse import *
from storage.analysis import *
from storage.predictions import *
import unittest
#from unittest.mock import MagicMock

#class WarehouseTests(unittest.TestCase):
    #def test_load(self):
    # powinno zwracać błąd, jeżeli w pliku są dane nieprawidłowe (string zamiast int, lub ujemne)

class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.date_from = date.fromisoformat('2015-01-01')
        self.date_to = date.fromisoformat('2016-01-01')
        self.list_of_colors = [(3650, 'black'), (3071, 'grey'), (2879, 'white'), (1481, 'red'), (922, 'pink'), (640, 'eco'), (638, 'blue'), (524, 'green'), (296, 'light blue')]


    def test_get_income(self):
        self.assertEqual(get_income(self.date_from,self.date_to, wh), Money(1085755.00, PLN))

    def test_get_costs(self):
        self.assertEqual(get_costs(self.date_from, self.date_to, wh), Money(616750.00, PLN))

    def test_get_sales(self):
        self.assertEqual(get_sales(self.date_from, self.date_to, wh), 14101)

    def test_get_resupply(self):
        self.assertEqual(get_resupply(self.date_from, self.date_to, wh), 14250)

    def test_get_balance(self):
        self.assertEqual(get_balance(self.date_from, self.date_to, wh), Money(469005.00, PLN))

    def test_get_products_balance(self):
        self.assertEqual(get_products_balance(self.date_from, self.date_to, wh), 149)

    def test_get_best_selling_colors(self):
        self.assertListEqual(get_best_selling_colors(self.date_from, self.date_to,wh), self.list_of_colors)

    #def test_get_best_selling_sizes(self):

if __name__ == '__main__':
    unittest.main()
