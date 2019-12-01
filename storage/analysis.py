from datetime import datetime
from typing import List, Dict

from storage.warehouse import Warehouse, Product, Operation, OperationType

""" Funkcje stanu magazynu """


def stock_statuses_for_general_product(id_prefix: str, wh: Warehouse, time: datetime = None) -> Dict[Product, int]:
    """ Funkcja zwracająca ilość w magazynie dla produktów, których id zaczynających się na wpisaną wartość. """
    return {
        prod: stock_status_for_product(prod, wh, time=time)
        for prod in get_products_starting_with(id_prefix, wh)
    }


def stock_status_for_product(prod: Product, wh: Warehouse, time: datetime = None) -> int:
    """ Funkcja zwracająca ilość w magazynie podanego produktu. """
    if time is None:
        time = datetime.now()

    count = 0
    for operation in get_product_operations(prod, wh):

        # skip operations in future
        if operation.date > time:
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
