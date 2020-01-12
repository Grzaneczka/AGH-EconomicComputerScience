from storage.analysis import *
from storage.predictions import *
import unittest
from unittest.mock import patch
import os
os.getcwd()


wh = Warehouse()
wh.load('./categories_test.csv','./products_test.csv','./operations_test.csv')
load_stocktaking('./stocktaking_test.csv')

class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.date_from = date.fromisoformat('2017-01-01')
        self.date_to = date.fromisoformat('2018-01-01')
        self.list_of_colors = [(39, 'black')]
        self.list_of_sizes = [(39, Size(2))]
        self.name = 'Bluza z nadrukiem Harry Potter'
        self.inv = './stocktaking_test.csv'

    def test_get_statuses(self):
        self.assertListEqual(list(get_statuses(wh, None).values()),[47, 38, 43, -1])
        self.assertListEqual(list(get_statuses(wh, self.date_to).values()),[29, 20, 29, -1])
        self.assertListEqual(list(get_statuses(wh, date.fromisoformat('2011-01-01')).values()), [0,0,0,0])

    def test_get_products(self):
        self.assertEqual(len(get_products(wh,['B'],self.name,[wh.categories[4], wh.categories[13]],'white', [Size.XS], [Sex.MAN])), 1)
        self.assertEqual(len(get_products(wh, ['B'], self.name, None, 'white', None, None)), 2)
        self.assertEqual(len(get_products(wh,None, None, None, None, None, None)),4)
        self.assertEqual(len(get_products(wh,None,None, None,['white','red'], [Size.XS, Size.L], [Sex.MAN])), 1)
        self.assertEqual(len(get_products(wh, None, None, None, ['purple', 'yellow'], [Size.S, Size.L], [Sex.WOMAN, Sex.MAN])), 0) #wrong colors


    def test_get_income(self):
        self.assertEqual(get_income(self.date_from,self.date_to, wh), Money(4680.00, PLN))
        self.assertEqual(get_income(self.date_to,self.date_from, wh), Money(0, PLN))

    def test_get_costs(self):
        self.assertEqual(get_costs(self.date_from, self.date_to, wh), Money(2800.00, PLN))
        self.assertEqual(get_costs(self.date_to, self.date_from, wh), Money(0, PLN))

    def test_get_sales(self):
        self.assertEqual(get_sales(self.date_from, self.date_to, wh), 39)
        self.assertEqual(get_sales(self.date_to, self.date_from, wh), 0)

    def test_get_resupply(self):
        self.assertEqual(get_resupply(self.date_from, self.date_to, wh), 40)
        self.assertEqual(get_resupply(self.date_to, self.date_from, wh), 0)

    def test_get_balance(self):
        self.assertEqual(get_balance(self.date_from, self.date_to, wh), Money(1880.00, PLN))
        self.assertEqual(get_balance(self.date_to, self.date_from, wh), Money(0, PLN))

    def test_get_products_balance(self):
        self.assertEqual(get_products_balance(self.date_from, self.date_to, wh), 1)
        self.assertEqual(get_products_balance(self.date_to, self.date_from, wh), 0)

    def test_get_best_selling_colors(self):
        self.assertListEqual(get_best_selling_colors(self.date_from, self.date_to,wh), self.list_of_colors)
        self.assertListEqual(get_best_selling_colors(self.date_to, self.date_from, wh), [])

    def test_get_best_selling_sizes(self):
        self.assertListEqual(get_best_selling_sizes(self.date_from, self.date_to, wh), self.list_of_sizes)
        self.assertListEqual(get_best_selling_sizes(self.date_to, self.date_from, wh), [])

    def test_compare_with_stocktaking(self):
        self.assertListEqual(list(compare_with_stocktaking(self.inv,wh).values()),[0,-2,3,2])

    def test_get_monthly_incomes(self):
        self.assertEqual(get_monthly_incomes(3, wh),[Money(1400.00, PLN),Money(1400.00, PLN),Money(2100.00, PLN)])
        self.assertEqual(get_monthly_incomes(0, wh),[])
        self.assertEqual(get_monthly_incomes(-1, wh), [])

    def test_get_monthly_sales(self):
        self.assertEqual(get_monthly_sales(3, wh),[10,10,15])
        self.assertEqual(get_monthly_sales(-1, wh), [])

    def test_get_months_for_supples(self):
        with patch('storage.analysis.forecast_values', return_value=[4.,4.,4.,4.,4.,4.]) as mock:
            assert get_months_for_supplies("BHaP01MWhi",4, wh) == 1

        with patch('storage.analysis.forecast_values', return_value=[4.,4.,4.,4.,4.,4.]) as mock:
            assert get_months_for_supplies("BHaP01MWhi",200, wh) == '>6'

        with patch('storage.analysis.forecast_values', return_value=[4.,4.,4.,4.,4.,4.]) as mock:
            assert get_months_for_supplies("BHaP01MWhi",0, wh) == 0

        with patch('storage.analysis.forecast_values', return_value=[4.,4.,4.,4.,4.,4.]) as mock:
            assert get_months_for_supplies("BHaP01MWhi",-2, wh) == 0

        with patch('storage.analysis.forecast_values', return_value=[0.,0.,0.,0.,0.,0.]) as mock:
            assert get_months_for_supplies("BHaP01MWhi", 10, wh) == '>6'

        with patch('storage.analysis.forecast_values', return_value=None) as mock:
            assert get_months_for_supplies("BHaP01MWhi", 10, wh) == 'brak danych'



if __name__ == '__main__':
    unittest.main()
