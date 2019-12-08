from datetime import date
from pprint import pprint

from storage import warehouse, plots, analysis

wh = warehouse.Warehouse()
wh.load('data/categories.csv', 'data/products.csv', 'data/operations.csv')

# pprint(analysis.compare_with_stocktaking('data/stocktaking-example.csv', wh))
# print('\n'.join(f'{prod.id}: {count}' for prod, count in analysis.get_statuses(wh).items() if count < 0))

# plots.plot_yearly_products_balance(2010, 2019, wh)
# plots.plot_yearly_balance(2010, 2019, wh)
#
# plots.plot_stock_by_color(wh, categories=[wh.categories[5]])
# plots.plot_stock_by_color(wh, id_prefixes=['BLeZ'])
# plots.plot_stock_by_size(wh, id_prefixes=['BHaP'])
# plots.plot_stock_for_category([5], wh)
# plots.plot_stock_for_category([10], wh)
# plots.plot_stock_for_category([5, 10], wh)
# plots.plot_stock_for_product_prefix('BHaP', wh)
# plots.plot_stock_for_product_prefix('THaP', wh)

# print(analysis.get_best_selling_colors(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_best_selling_sizes(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))

# print(analysis.get_sales(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_sales(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))
#
# print(analysis.get_resupply(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_resupply(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))
#
# print(analysis.get_income(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_income(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))
#
# print(analysis.get_costs(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_costs(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))
#
# print(analysis.get_balance(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_balance(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))
#
# print(analysis.get_products_balance(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_products_balance(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))
#
# plots.plot_income_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])
#
# plots.plot_costs_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])
#
# plots.plot_sales_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])
#
# plots.plot_resupply_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])
#
# plots.plot_balance_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])
#
# plots.plot_products_balance_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])
