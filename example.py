from datetime import date
from pprint import pprint
from storage import warehouse, plots, analysis, predictions

wh = warehouse.Warehouse()
wh.load('data/categories.csv', 'data/products.csv', 'data/operations.csv')

print("Funkcja pomagająca w inwetaryzajci")
pprint(analysis.compare_with_stocktaking('data/stocktaking-example.csv', wh))

# Wykresy bilansów
plots.plot_yearly_products_balance(2010, 2019, wh)
plots.plot_yearly_balance(2010, 2019, wh)

# Wykresy stanu magazynu
plots.plot_stock_for_product_prefix('BHaP', wh)
plots.plot_stock_for_product_prefix('QStW', wh)


print("------------------------------------------------------------------------------------------------------")
print("Analiza który z kolorów i rozmiarów sprzedaje się najlepiej")
print(analysis.get_best_selling_colors(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
print(analysis.get_best_selling_sizes(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))

# Wykres porównujący sprzedaż kilku okresów czasu
plots.plot_sales_periods([
     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12'))], wh, id_prefixes=['BHaP'])

# Prognoza
predictions.prediction_plot(wh, None, False, True, True, False)


# Inne (nie pokazujemy)
# plots.plot_stock_by_color(wh, categories=[wh.categories[5]])
# plots.plot_stock_by_color(wh, id_prefixes=['BStW'])
# plots.plot_stock_by_size(wh, id_prefixes=['BHaP'])
# plots.plot_stock_for_category([5], wh)
# plots.plot_stock_for_category([10], wh)
# plots.plot_stock_for_category([5, 10], wh)

# print(analysis.get_sales(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_sales(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))

# print(analysis.get_resupply(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_resupply(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))

# print(analysis.get_income(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_income(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))

# print(analysis.get_costs(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_costs(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))

# print(analysis.get_balance(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_balance(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))

# print(analysis.get_products_balance(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh))
# print(analysis.get_products_balance(date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12'), wh, id_prefixes=['BHaP']))

# plots.plot_income_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])

# plots.plot_costs_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])

# plots.plot_resupply_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])

# plots.plot_balance_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])

# plots.plot_products_balance_periods([
#     (date.fromisoformat('2015-09-12'), date.fromisoformat('2016-09-12')),
#     (date.fromisoformat('2016-09-12'), date.fromisoformat('2017-09-12')),
#     (date.fromisoformat('2017-09-12'), date.fromisoformat('2018-09-12')),
# ], wh, id_prefixes=['BHaP'])
