from datetime import datetime, date
from typing import List, Dict

from moneyed import Money, PLN

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
    """ Funkcja zwracająca wszytskie operacje dla podanego produktu. """
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


def get_income(date_from: date, date_to: date, wh: Warehouse) -> Money:
    """
    Zwraca przychód na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :return: suma przychodow za dany okres
    """
    return sum((
            op.total_price
            for op in wh.operations.values()
            if date_from <= op.date < date_to and op.type == OperationType.SALE
        ),
        Money(0, PLN)
    )


def get_costs(date_from: date, date_to: date, wh: Warehouse) -> Money:
    """
    Zwraca koszty na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :return: suma kosztow za dany okres
    """
    return sum((
            op.total_price
            for op in wh.operations.values()
            if date_from <= op.date < date_to and op.type == OperationType.RESUPPLY
        ),
        Money(0, PLN)
    )


def get_sales(date_from: date, date_to: date, wh: Warehouse) -> int:
    """
    Zwraca ilosc sprzedanych towarow na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :return: ilosc sprzedanych towarow za dany okres
    """
    return sum(
        op.quantity
        for op in wh.operations.values()
        if date_from <= op.date < date_to and op.type == OperationType.SALE
    )


def get_resupply(date_from: date, date_to: date, wh: Warehouse) -> int:
    """
    Zwraca ilosc zamowionych towarow na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :return: ilosc zamowionych towarow za dany okres
    """
    return sum(
        op.quantity
        for op in wh.operations.values()
        if date_from <= op.date < date_to and op.type == OperationType.RESUPPLY
    )


def get_balance(date_from: date, date_to: date, wh: Warehouse) -> Money:
    """
    Zwraca bilans na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :return: bilans za dany okres
    """
    return get_income(date_from, date_to, wh) - get_costs(date_from, date_to, wh)


def get_products_balance(date_from: date, date_to: date, wh: Warehouse) -> int:
    """
    Zwraca bilans produktow na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :return: bilans produktow za dany okres
    """
    return get_resupply(date_from, date_to, wh) - get_sales(date_from, date_to, wh)
