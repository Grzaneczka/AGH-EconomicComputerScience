from collections import defaultdict
from datetime import datetime
from operator import attrgetter

import matplotlib.pyplot as plt

from storage import analysis
from storage.analysis import stock_statuses_for_general_product
from storage.warehouse import Warehouse


def plot_stock_by_color(id_prefix: str, wh: Warehouse, time: datetime = None):
    """ Wyswietla wykresy (po kolorach) statusu produktow zaczynajacych sie od podanego id """
    stock = stock_statuses_for_general_product(id_prefix, wh, time=time)
    sexes = sorted({p.sex for p in stock.keys()}, key=attrgetter('value'))
    colors = sorted({p.color for p in stock.keys()})

    # create plot
    fig, axes = plt.subplots(nrows=len(colors), ncols=len(sexes), figsize=(12, 8), sharex='all', sharey='all', squeeze=False)

    # set cols titles
    for ax, sex in zip(axes[0], sexes):
        ax.set_title(sex.name)

    # set rows titles
    for ax, color in zip(axes[:, 0], colors):
        ax.set_ylabel(color, size='large')

    # plot data
    for row, color in zip(axes, colors):
        for ax, sex in zip(row, sexes):

            # collect data
            data = defaultdict(int)
            for prod, count in stock.items():
                if prod.color == color and prod.sex == sex:
                    data[prod.size.name] += count

            # if there is no data skip
            if not data:
                continue

            # plot bars
            bars = ax.bar(*zip(*data.items()))

            # plot numbers
            for rect in bars:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

            # disable ticks
            ax.set_yticks([])

    fig.tight_layout()
    plt.show()


def plot_stock_by_size(id_prefix: str, wh: Warehouse, time: datetime = None):
    """ Wyswietla wykresy (po rozmiarach) statusu produktow zaczynajacych sie od podanego id """
    stock = stock_statuses_for_general_product(id_prefix, wh, time=time)
    sexes = sorted({p.sex for p in stock.keys()}, key=attrgetter('value'))
    sizes = sorted({p.size for p in stock.keys()}, key=attrgetter('value'))

    # create plot
    fig, axes = plt.subplots(nrows=len(sizes), ncols=len(sexes), figsize=(12, 8), sharex='all', sharey='all', squeeze=False)

    # set cols titles
    for ax, sex in zip(axes[0], sexes):
        ax.set_title(sex.name)

    # set rows titles
    for ax, size in zip(axes[:, 0], sizes):
        ax.set_ylabel(size.name, size='large')

    # plot data
    for row, size in zip(axes, sizes):
        for ax, sex in zip(row, sexes):

            # collect data
            data = defaultdict(int)
            for prod, count in stock.items():
                if prod.size == size and prod.sex == sex:
                    data[prod.color] += count

            # if there is no data skip
            if not data:
                continue

            # plot bars
            bars = ax.bar(*zip(*data.items()))

            # plot numbers
            for rect in bars:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

            # disable ticks
            ax.set_yticks([])

    fig.tight_layout()
    plt.show()


def plot_stock(id_prefix: str, wh: Warehouse, time: datetime = None):
    """ Wyswietla wykresy (typ wybrany automatycznie) statusu produktow zaczynajacych sie od podanego id """
    if id_prefix[0] in ['T', 'Q', 'C']:
        plot_stock_by_size(id_prefix, wh, time)
    else:
        plot_stock_by_color(id_prefix, wh, time)


def plot_yearly_balance(year_from: int, year_to: int, wh: Warehouse):
    """ Wyświetla wykres kosztow i dochodów na przestrzeni lat """
    x = list(range(year_from, year_to + 1))
    costs = [analysis.get_year_costs(year, wh).amount for year in x]
    incomes = [analysis.get_year_income(year, wh).amount for year in x]
    balance = [analysis.get_year_balance(year, wh).amount for year in x]

    plt.plot(x, costs, c='r', label='Costs')
    plt.plot(x, incomes, c='g', label='Incomes')
    plt.plot(x, balance, c='b', label='Balances')
    plt.title('Yearly incomes and costs')
    plt.legend()
    plt.show()


def plot_yearly_products_balance(year_from: int, year_to: int, wh: Warehouse):
    """ Wyświetla wykres dostaw i sprzedazy na przestrzeni lat """
    x = list(range(year_from, year_to + 1))
    sales = [analysis.get_year_sales(year, wh) for year in x]
    resupply = [analysis.get_year_resupply(year, wh) for year in x]
    balance = [analysis.get_year_products_balance(year, wh) for year in x]

    plt.plot(x, sales, c='r', label='Sales')
    plt.plot(x, resupply, c='g', label='Resupplies')
    plt.plot(x, balance, c='b', label='Balances')
    plt.title('Yearly products resupplies and sales')
    plt.legend()
    plt.show()
