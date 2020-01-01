import csv
from typing import NamedTuple, Optional, Dict, Tuple, Set
from enum import Enum
from moneyed import Money, PLN
from datetime import date


class Category(NamedTuple):
    id: int
    name: str
    parent: Optional['Category']

    def parents(self) -> Set['Category']:
        """ Zwraca zbiór kategorii nadrzednych oraz samej siebie. """
        if self.parent is not None:
            return self.parent.parents().union([self])
        return {self}


class Size(Enum):
    ONE_SIZE = 0
    XS = 1
    S = 2
    M = 3
    L = 4
    XL = 5


class Sex(Enum):
    UNISEX = 0
    WOMAN = 1
    MAN = 2


class Product(NamedTuple):
    id: str
    name: str
    size: Size
    sex: Sex
    color: str
    categories: Tuple[Category, ...]
    delivery_time: float

    @property
    def all_categories(self) -> Set[Category]:
        return set().union(*[cat.parents() for cat in self.categories])

    def __repr__(self):
        return f'Product({self.id})'


class OperationType(Enum):
    RESUPPLY = 1
    SALE = 2


class Operation(NamedTuple):
    id: int
    date: date
    type: OperationType
    product: Product
    quantity: int
    price: Money

    @property
    def total_price(self) -> Money:
        return self.price * self.quantity


class Warehouse:
    """ Class that stores and manages available data. """
    
    def __init__(self):
        """ Creates empty warehouse """
        self.categories: Dict[int, Category] = {}
        self.products: Dict[str, Product] = {}
        self.operations: Dict[int, Operation] = {}
        
    def load_categories(self, path: str):
        """ Loads catories from given CSV file """
        with open(path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=';')
            # skip header 
            next(csv_reader)
            
            for row in csv_reader:
                if row[2] == 'NULL':
                    p = None
                else:
                    p = self.categories[int(row[2])]
                
                self.categories[int(row[0])] = Category(int(row[0]), row[1], p)
                                       
    def load_products(self, path: str):
        """ Loads products from given CSV file """
        with open(path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=';')
            # skip header 
            next(csv_reader)
            
            for row in csv_reader:
                size = Size[row[2].upper()]
                sex = Sex[row[3].upper()]
                categories = tuple(
                    self.categories[int(c)]
                    for c in row[5].split(';')
                )
                
                self.products[row[0]] = Product(row[0], row[1], size, sex, row[4].lower(), categories, float(row[6]))
                
    def load_operations(self, path: str):
        """ Loads operations from given CSV file """
        with open(path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=';')
            # skip header 
            next(csv_reader)
            
            for row in csv_reader:
                operation_type = OperationType[row[2].upper()]
                operation_date = date.fromisoformat(row[1])
                product = self.products[row[3]]
                price = Money(row[5], PLN)
                
                self.operations[int(row[0])] = Operation(int(row[0]), operation_date, operation_type, product, int(row[4]), price)
                
    def load(self, path_categories: str, path_products: str, path_operations: str):
        """ Loads warehouse data from given files """
        self.load_categories(path_categories)
        self.load_products(path_products)
        self.load_operations(path_operations)

    def get_category_by_name(self, name: str) -> Optional[Category]:
        """ Returns category base on given name """
        for cat in self.categories.values():
            if cat.name.lower() == name.lower():
                return cat
