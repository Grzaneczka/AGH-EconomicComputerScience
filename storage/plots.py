from collections import defaultdict
from datetime import date
from operator import attrgetter
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta

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

    if not stock:
        return plot_error('Brak produktów spełniających kryteria')

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

    if not stock:
        return plot_error('Brak produktów spełniających kryteria')

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

    plt.plot(years, costs, c='r', label='Koszty')
    plt.plot(years, incomes, c='g', label='Przychody')
    plt.plot(years, balance, c='b', label='Bilans (dochód)')
    plt.title('Roczne przychody oraz koszty')
    plt.ylabel('Wielkość [PLN]')
    plt.xlabel("Rok")
    plt.xticks(years)
    plt.legend()


def plot_yearly_products_balance(year_from: int, year_to: int, wh: Warehouse):
    """ Wyświetla wykres dostaw i sprzedazy na przestrzeni lat """

    years = list(range(year_from, year_to+1))
    sales = [analysis.get_sales(date(y, 1, 1), date(y+1, 1, 1), wh) for y in years]
    resupply = [analysis.get_resupply(date(y, 1, 1), date(y+1, 1, 1), wh) for y in years]
    balance = [analysis.get_products_balance(date(y, 1, 1), date(y+1, 1, 1), wh) for y in years]

    plt.plot(years, sales, c='r', label='Sprzedaż')
    plt.plot(years, resupply, c='g', label='Dostawy')
    plt.plot(years, balance, c='b', label='Balans ilości produktów')
    plt.title('Roczne sprzedaże oraz dostawy produktów ')
    plt.ylabel('Ilość [sztuka]')
    plt.xlabel("Rok")
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

    if all(v == 0 for v in y):
        return plot_error('Brak danych spełniających kryteria')

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Przychody w różnych okresach ')
    plt.ylabel('Przychody [PLN]')


def plot_costs_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla koszty dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_costs(d1, d2, wh, **kwargs).amount for d1, d2 in periods]

    if all(v == 0 for v in y):
        return plot_error('Brak danych spełniających kryteria')

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Koszty w różnych okresach')
    plt.ylabel('Koszty [PLN]')


def plot_sales_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla ilość sprzadanych towarów dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_sales(d1, d2, wh, **kwargs) for d1, d2 in periods]

    if all(v == 0 for v in y):
        return plot_error('Brak danych spełniających kryteria')

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Sprzedaż w różnych okresach')
    plt.ylabel('Sprzedaż')


def plot_resupply_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla ilość zamówionych przedmiotów dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_resupply(d1, d2, wh, **kwargs) for d1, d2 in periods]

    if all(v == 0 for v in y):
        return plot_error('Brak danych spełniających kryteria')

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Dostawy w różnych okresach')
    plt.ylabel('Dostawy')


def plot_balance_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla balans dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_balance(d1, d2, wh, **kwargs).amount for d1, d2 in periods]

    if all(v == 0 for v in y):
        return plot_error('Brak danych spełniających kryteria')

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Balans (dochód) w różnych okresach')
    plt.ylabel('Balans [PLN]')


def plot_products_balance_periods(periods: List[Tuple[date, date]], wh: Warehouse, **kwargs):
    """
    Wyświetla dochód dla poszczególnych okresów.

    :param periods: okresy w postaci listy tupli dat od do
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """
    x = [f'{d1.isoformat()}\n{d2.isoformat()}' for d1, d2 in periods]
    y = [analysis.get_products_balance(d1, d2, wh, **kwargs) for d1, d2 in periods]

    if all(v == 0 for v in y):
        return plot_error('Brak danych spełniających kryteria')

    bars = plt.bar(x, y)

    # plot numbers
    for rect in bars:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

    plt.title('Products balance in different periods')
    plt.ylabel('Products balance')


def plot_forecast_income(analyse_months: int, season: int, forecast_months: int, wh: Warehouse, **kwargs):
    """
    Wyświetla prognozę na podstawie danych.

    :param analyse_months: ilość miesięcy w tył branych pod uwagę
    :param season: długość okresu w miesiącach
    :param forecast_months: ilość prognozowanych miesięcy
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """

    # check parameters
    if analyse_months <= 2 * season:
        return plot_error('Błędna kombinacja parametrów')

    # get dates
    d = date(date.today().year, date.today().month, 15)
    dates = [d + relativedelta(months=i) for i in range(-analyse_months, forecast_months)]

    # get data
    data = [float(d.amount) for d in analysis.get_monthly_incomes(analyse_months, wh, **kwargs)]

    # get forecast
    try:
        forecast = analysis.forecast_values(data, forecast_months, season)
    except:
        return plot_error('Brak danych')

    # setup figure
    fig = plt.gcf()
    ax = fig.subplots()

    # plot data
    ax.plot(dates[:analyse_months], data, label='historia')

    # plot forecast
    ax.plot(dates[analyse_months-1:], [data[-1]] + forecast, label='prognoza')

    # format the ticks
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.grid(True, axis='x', which='major', linewidth=2, alpha=0.8)
    ax.grid(True, axis='x', which='minor', linewidth=1, alpha=0.2)
    ax.set_ylim(bottom=0)
    ax.set_ylabel('Wielkość [PLN]')

    ax.legend()


def plot_forecast_sales(analyse_months: int, season: int, forecast_months: int, wh: Warehouse, **kwargs):
    """
    Wyświetla prognozę na podstawie danych.

    :param analyse_months: ilość miesięcy w tył branych pod uwagę
    :param season: długość okresu w miesiącach
    :param forecast_months: ilość prognozowanych miesięcy
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    """

    # check parameters
    if analyse_months <= 2 * season:
        return plot_error('Błędna kombinacja parametrów')

    # get dates
    d = date(date.today().year, date.today().month, 15)
    dates = [d + relativedelta(months=i) for i in range(-analyse_months, forecast_months)]

    # get data
    data = [float(d) for d in analysis.get_monthly_sales(analyse_months, wh, **kwargs)]

    # plot forecast
    try:
        forecast = np.rint(analysis.forecast_values(data, forecast_months, season))
    except:
        return plot_error('Brak danych')

    # setup figure
    fig = plt.gcf()
    ax = fig.subplots()

    # plot data
    ax.plot(dates[:analyse_months], data, label='historia')

    # plor forecast
    ax.plot(dates[analyse_months-1:], [data[-1]] + forecast.tolist(), label='prognoza')

    # format the ticks
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.grid(True, axis='x', which='major', linewidth=2, alpha=0.8)
    ax.grid(True, axis='x', which='minor', linewidth=1, alpha=0.2)
    ax.set_ylim(bottom=0)
    ax.set_ylabel('Ilość [sztuka]')
    ax.legend()


# ========================================================
#  UTILITY
# ========================================================
def plot_error(msg: str):
    """ Wyświetla pusty wykres z tekstem na środku. """
    plt.text(
        0.5, 0.5,
        msg,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=12,
    )
    plt.axis('off')
