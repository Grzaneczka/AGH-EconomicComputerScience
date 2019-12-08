import csv
from collections import defaultdict
from datetime import date
from typing import List, Tuple, Dict

from moneyed import Money, PLN

from storage.warehouse import Warehouse, Product, Operation, OperationType, Category, Size, Sex


def get_statuses(wh: Warehouse, time: date = None, **kwargs):
    """
    Zwraca status produktow spelniajacych kryteria.

    :param wh: magazyn
    :param time: data dnia dla którego jest sprawdzany status
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    :return: ilość produktu w magazynie dla każdego produktu
    """
    return {
        prod: stock_status_for_product(prod, wh, time=time)
        for prod in get_products(wh, **kwargs)
    }


def stock_status_for_product(prod: Product, wh: Warehouse, time: date = None) -> int:
    """ Funkcja zwracająca ilość w magazynie podanego produktu. """
    if time is None:
        time = date.today()

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


def get_products(wh: Warehouse,
                 id_prefixes: List[str] = None,
                 names: List[str] = None,
                 categories: List[Category] = None,
                 colors: List[str] = None,
                 sizes: List[Size] = None,
                 sexes: List[Sex] = None):
    """
    Zwraca wszystkie produkty z magazynu które spełniają podane warunki.
    Jeżeli któryś warunek nie zostanie podany to z domysłu akceptuje on wszystko.

    :param wh: magazyn
    :param id_prefixes: lista akceptowanych prefixów id
    :param names: lista akceptowanych nazw produktow
    :param categories: lista akceptowanych kategorii produktow
    :param colors: lista akceptowanych kolorów produktow
    :param sizes: lista akceptowanych rozmiarów produktow
    :param sexes: lista akceptowanych płci produktow
    :return: produkty które spełniaja podane warunki
    """

    products = wh.products.values()
    if id_prefixes:
        products = filter(lambda p: any(p.id.startswith(prefix) for prefix in id_prefixes), products)
    if names:
        products = filter(lambda p: p.name in names, products)
    if colors:
        products = filter(lambda p: p.color in colors, products)
    if sizes:
        products = filter(lambda p: p.size in sizes, products)
    if sexes:
        products = filter(lambda p: p.sex in sexes, products)
    if categories:
        products = filter(lambda p: all(cat in p.all_categories for cat in categories), products)

    return list(products)


def get_income(date_from: date, date_to: date, wh: Warehouse, **kwargs) -> Money:
    """
    Zwraca przychód na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    :return: suma przychodow za dany okres
    """
    products = get_products(wh, **kwargs)
    return sum((
            op.total_price
            for op in wh.operations.values()
            if date_from <= op.date < date_to and op.type == OperationType.SALE and op.product in products
        ),
        Money(0, PLN)
    )


def get_costs(date_from: date, date_to: date, wh: Warehouse, **kwargs) -> Money:
    """
    Zwraca koszty na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    :return: suma kosztow za dany okres
    """
    products = get_products(wh, **kwargs)
    return sum((
            op.total_price
            for op in wh.operations.values()
            if date_from <= op.date < date_to and op.type == OperationType.RESUPPLY and op.product in products
        ),
        Money(0, PLN)
    )


def get_sales(date_from: date, date_to: date, wh: Warehouse, **kwargs) -> int:
    """
    Zwraca ilosc sprzedanych towarow na dany domknięto-otwarty okres.

    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    :return: ilosc sprzedanych towarow za dany okres
    """
    products = get_products(wh, **kwargs)
    return sum(
        op.quantity
        for op in wh.operations.values()
        if date_from <= op.date < date_to and op.type == OperationType.SALE and op.product in products
    )


def get_resupply(date_from: date, date_to: date, wh: Warehouse, **kwargs) -> int:
    """
    Zwraca ilosc zamowionych towarow na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    :return: ilosc zamowionych towarow za dany okres
    """
    products = get_products(wh, **kwargs)
    return sum(
        op.quantity
        for op in wh.operations.values()
        if date_from <= op.date < date_to and op.type == OperationType.RESUPPLY and op.product in products
    )


def get_balance(date_from: date, date_to: date, wh: Warehouse, **kwargs) -> Money:
    """
    Zwraca bilans na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    :return: bilans za dany okres
    """
    return get_income(date_from, date_to, wh, **kwargs) - get_costs(date_from, date_to, wh, **kwargs)


def get_products_balance(date_from: date, date_to: date, wh: Warehouse, **kwargs) -> int:
    """
    Zwraca bilans produktow na dany domknięto-otwarty okres
    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :param kwargs: kryteria przy wybieraniu produktow (patrz get_products())
    :return: bilans produktow za dany okres
    """
    return get_resupply(date_from, date_to, wh, **kwargs) - get_sales(date_from, date_to, wh, **kwargs)


def get_best_selling_colors(date_from: date, date_to: date, wh: Warehouse) -> List[Tuple[int, str]]:
    """
    Zwraca posortowaną ilość sprzedanych sztuk w danym okresie dla poszczególnych kolorów.

    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :return: posortowana lista tupli w formacie: (ilosc, kolor)
    """
    data = defaultdict(int)

    for op in wh.operations.values():
        if date_from <= op.date < date_to and op.type == OperationType.SALE:
            data[op.product.color] += op.quantity

    data = [(count, color) for color, count in data.items()]
    return sorted(data, reverse=True)


def get_best_selling_sizes(date_from: date, date_to: date, wh: Warehouse) -> List[Tuple[int, Size]]:
    """
    Zwraca posortowaną ilość sprzedanych sztuk w danym okresie dla poszczególnych rozmiarów.

    :param date_from: data poczatkowa
    :param date_to: data koncowa
    :param wh: magazyn
    :return: posortowana lista tupli w formacie: (ilosc, rozmiar)
    """
    data = defaultdict(int)

    for op in wh.operations.values():
        if date_from <= op.date < date_to and op.type == OperationType.SALE:
            data[op.product.size] += op.quantity

    data = [(count, size) for size, count in data.items()]
    return sorted(data, reverse=True)


def compare_with_stocktaking(path: str, wh: Warehouse) -> Dict[Product, int]:
    """
    Zwraca porównanie aktualnego stanu magazynu ze stanem z inwentaryzacji.
    Inwentaryzacja w formie pliku CSV, gdzie pierwsza kolumna to id produktu a druga to zliczona liość.

    :param path: scierzka do pliku CSV
    :param wh: magazyn
    :return: słownik id-produktu: rożnica między stanem teoretycznym a rzeczywistym
    """
    stacktaking = defaultdict(int)

    # wczytywanie inwentaryzacji
    with open(path, 'r') as f:
        csv_reader = csv.reader(f, delimiter=';')
        # skip header
        next(csv_reader)

        for row in csv_reader:
            stacktaking[row[0]] = int(row[1])

    return {
        prod: count - stacktaking[prod.id]
        for prod, count in get_statuses(wh).items()
    }
