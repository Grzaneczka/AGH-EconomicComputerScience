from collections import defaultdict
from datetime import date
from operator import attrgetter
from typing import List, Tuple

import matplotlib.pyplot as plt

from storage import analysis
from storage.analysis import get_statuses
from storage.warehouse import Warehouse


# ========================================================
#  SHORTCUTS FOR PLOTTING
# ========================================================
def plot_stock_for_category(categories: List[int], wh: Warehouse, time: date = None):
    categories = [wh.categories[i] for i in categories]
    plot_stock_by_color(wh, time, categories=categories)


def plot_stock_for_product_prefix(id_prefix: str, wh: Warehouse, time: date = None):
    if id_prefix[0] in ['T', 'Q', 'C']:
        plot_stock_by_size(wh, time, id_prefixes=[id_prefix])
    else:
        plot_stock_by_color(wh, time, id_prefixes=[id_prefix])


# ========================================================
#  COMPLEX PLOTTING
# ========================================================
def plot_stock_by_color(wh: Warehouse, time: date = None, **kwargs):
    """
    Wyswietla wykresy (po kolorach) statusu produktow spełniajacych podane kryteria.

    :param wh: magazyn
    :param time: data dnia dla którego jest sprawdzany status
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    stock = get_statuses(wh, time=time, **kwargs)
    sexes = sorted({p.sex for p in stock.keys()}, key=attrgetter('value'))
    colors = sorted({p.color for p in stock.keys()})

    # get active figure
    fig = plt.gcf()

    # create subplots
    axes = fig.subplots(nrows=len(colors), ncols=len(sexes), sharex='col', sharey='all', squeeze=False)

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


def plot_stock_by_size(wh: Warehouse, time: date = None, **kwargs):
    """
    Wyswietla wykresy (po rozmiarach) statusu produktow spełniajacych podane kryteria.

    :param wh: magazyn
    :param time: data dnia dla którego jest sprawdzany status
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    stock = get_statuses(wh, time=time, **kwargs)
    sexes = sorted({p.sex for p in stock.keys()}, key=attrgetter('value'))
    sizes = sorted({p.size for p in stock.keys()}, key=attrgetter('value'))

    # get active figure
    fig = plt.gcf()

    # create subplots
    axes = fig.subplots(nrows=len(sizes), ncols=len(sexes), sharex='col', sharey='all', squeeze=False)

    # set cols titles
    for ax, sex in zip(axes[0], sexes):
        ax.set_title(sex.name)

    # set rows titles
    for ax, size in zip(axes[:, 0], sizes):
        ax.set_ylabel(size.name, size='large')

    # plot data
    for row, size in zip(axes, sizes):
        for ax, sex in zip(row, sexes):

            # configure axis
            ax.set_yticks([])
            ax.tick_params(axis='x', rotation=45)

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

    fig.tight_layout()


def plot_yearly_balance(year_from: int, year_to: int, wh: Warehouse):
    """ Wyświetla wykres kosztow i dochodów na przestrzeni lat """

    years = list(range(year_from, year_to + 1))
    costs = [analysis.get_costs(date(y, 1, 1), date(y + 1, 1, 1), wh).amount for y in years]
    incomes = [analysis.get_income(date(y, 1, 1), date(y + 1, 1, 1), wh).amount for y in years]
    balance = [analysis.get_balance(date(y, 1, 1), date(y + 1, 1, 1), wh).amount for y in years]

    plt.plot(years, costs, c='r', label='Costs')
    plt.plot(years, incomes, c='g', label='Incomes')
    plt.plot(years, balance, c='b', label='Balances')
    plt.title('Yearly incomes and costs')
    plt.xticks(years)
    plt.legend()


def plot_yearly_products_balance(year_from: int, year_to: int, wh: Warehouse):
    """ Wyświetla wykres dostaw i sprzedazy na przestrzeni lat """

    years = list(range(year_from, year_to+1))
    sales = [analysis.get_sales(date(y, 1, 1), date(y+1, 1, 1), wh) for y in years]
    resupply = [analysis.get_resupply(date(y, 1, 1), date(y+1, 1, 1), wh) for y in years]
    balance = [analysis.get_products_balance(date(y, 1, 1), date(y+1, 1, 1), wh) for y in years]

    plt.plot(years, sales, c='r', label='Sales')
    plt.plot(years, resupply, c='g', label='Resupplies')
    plt.plot(years, balance, c='b', label='Balances')
    plt.title('Yearly products resupplies and sales')
    plt.xticks(years)
    plt.legend()


def plot_income_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla dochód dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_income(d1, d2, wh, **kwargs).amount for d1, d2 in periods]

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Income in different periods')
    plt.ylabel('Income [PLN]')


def plot_costs_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla koszty dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_costs(d1, d2, wh, **kwargs).amount for d1, d2 in periods]

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Costs in different periods')
    plt.ylabel('Costs [PLN]')


def plot_sales_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla ilość sprzadanych towarów dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_sales(d1, d2, wh, **kwargs) for d1, d2 in periods]

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Sales in different periods')
    plt.ylabel('Sales')


def plot_resupply_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla ilość zamówionych przedmiotów dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_resupply(d1, d2, wh, **kwargs) for d1, d2 in periods]

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Resupply in different periods')
    plt.ylabel('Resupply')


def plot_balance_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla balans dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_balance(d1, d2, wh, **kwargs).amount for d1, d2 in periods]

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Balance in different periods')
    plt.ylabel('Balance [PLN]')


def plot_products_balance_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla dochód dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_products_balance(d1, d2, wh, **kwargs) for d1, d2 in periods]

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Products balance in different periods')
    plt.ylabel('Products balance')
