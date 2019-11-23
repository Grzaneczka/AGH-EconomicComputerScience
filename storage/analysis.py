from typing import List, Dict

from storage.warehouse import Warehouse, Product, Operation, OperationType
import matplotlib.pyplot as plt

""" Funkcje stanu magazynu - podając id """


def stock_statuses_for_general_product(id_prefix: str, wh: Warehouse) -> Dict[str, int]:
    """ Funkcja zwracająca ilość w magazynie dla produktów, których id zaczynających się na wpisaną wartość """
    return {
        id: stock_status_for_product(id, wh)
        for id in get_products_ids_starting_with(id_prefix, wh)
    }


def stock_status_for_product(id: str, wh: Warehouse) -> int:
    """ Funkcja zwracająca ilość w magazynie dla prokuktu którego id podaliśmy """
    # Sprawdza wszystkie operacje - trzeba poprawić by sprawdzał tylko do dziś
    count = 0
    for operation in get_product_operations(id, wh):
        if operation.type == OperationType.RESUPPLY:
            count += operation.quantity
        elif operation.type == OperationType.SALE:
            count -= operation.quantity
    return count


def get_product_operations(id: str, wh: Warehouse) -> List[Operation]:
    """ Funkcja zwracająca wszytskie operacje dla produktu którego id podaliśmy  """
    return [
        op
        for op in wh.operations.values()
        if op.product.id == id
    ]


def get_products_ids_starting_with(id: str, wh: Warehouse) -> List[str]:
    """ Funkcja zwracająca id wszystkich produktów zaczynających się na wpisaną wartość """
    return [
        pid
        for pid in wh.products.keys()
        if pid.startswith(id)
    ]


def plot_stock_statuses_for_general_product(id_prefix: str, wh: Warehouse):
    x = stock_statuses_for_general_product(id_prefix, wh).keys()
    y = stock_statuses_for_general_product(id_prefix, wh).values()

    plt.bar(x, y)
    plt.show()