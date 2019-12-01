from datetime import datetime
from collections import defaultdict
from operator import attrgetter
from typing import List, Dict

from storage.warehouse import Warehouse, Product, Operation, OperationType, Sex, Size
import matplotlib.pyplot as plt

""" Funkcje stanu magazynu """


def stock_statuses_for_general_product(id_prefix: str, wh: Warehouse) -> Dict[Product, int]:
    """ Funkcja zwracająca ilość w magazynie dla produktów, których id zaczynających się na wpisaną wartość. """
    return {
        prod: stock_status_for_product(prod, wh)
        for prod in get_products_starting_with(id_prefix, wh)
    }


def stock_status_for_product(prod: Product, wh: Warehouse) -> int:
    """ Funkcja zwracająca ilość w magazynie podanego produktu. """
    count = 0
    for operation in get_product_operations(prod, wh):

        # skip operations in future
        if operation.date > datetime.now():
            continue

        if operation.type == OperationType.RESUPPLY:
            count += operation.quantity
        elif operation.type == OperationType.SALE:
            count -= operation.quantity
    return count


def get_product_operations(prod: Product, wh: Warehouse) -> List[Operation]:
    """ Funkcja zwracająca wszytskie operacje dla podanego produktu.  """
    return [
        op
        for op in wh.operations.values()
        if op.product == prod
    ]


def get_products_starting_with(id_prefix: str, wh: Warehouse) -> List[Product]:
    """ Funkcja zwracająca wszystkie produkty których id zaczyna się od podanej wartości. """
    return [
        prod
        for prod in wh.products.values()
        if prod.id.startswith(id_prefix)
    ]


def plot_stock_by_color(id_prefix: str, wh: Warehouse):
    stock = stock_statuses_for_general_product(id_prefix, wh)
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


def plot_stock_by_size(id_prefix: str, wh: Warehouse):
    stock = stock_statuses_for_general_product(id_prefix, wh)
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


def plot_stock_statuses_for_general_product(id_prefix: str, wh: Warehouse):
    x = stock_statuses_for_general_product(id_prefix, wh).keys()
    y = stock_statuses_for_general_product(id_prefix, wh).values()

    plt.bar(x, y)
    plt.show()