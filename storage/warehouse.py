import csv
from typing import NamedTuple, List, Optional, Dict
from enum import Enum
from moneyed import Money, PLN
from datetime import datetime


class Category(NamedTuple):
    id: int
    name: str
    parent: Optional['Category']


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
    categories: List[Category]
    delivery_time: float    


class OperationType(Enum):
    RESUPPLY = 1
    SALE = 2


class Operation(NamedTuple):
    id: int
    date: datetime
    type: OperationType
    product: Product
    quantity: int
    price: Money


class Warehouse:
    """ Class that stores and manages available data. """
    
    def __init__(self):
        """ Creates empty warehouse """
        self.categories: Dict[str, Category] = {}
        self.products: Dict[str, Product] = {}
        self.operations: Dict[str, Operation] = {}
        
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
                categories = [
                    self.categories[int(c)]
                    for c in row[5].split(';')
                ]
                
                self.products[row[0]] = Product(row[0], row[1], size, sex, row[4].lower(), categories, float(row[6]))
                
    def load_operations(self, path: str):
        """ Loads operations from given CSV file """
        with open(path, 'r') as f:
            csv_reader = csv.reader(f, delimiter=';')
            # skip header 
            next(csv_reader)
            
            for row in csv_reader:
                operation_type = OperationType[row[2].upper()]
                date = datetime.strptime(row[1], '%d/%m/%Y')
                product = self.products[row[3]]
                price = Money(row[5], PLN)

                self.operations[int(row[0])] = Operation(int(row[0]), date, operation_type, product, int(row[4]), price)
                
    def load(self, path_categories: str, path_products: str, path_operations: str):
        """ Loads warehouse data from given files """
        self.load_categories(path_categories)
        self.load_products(path_products)
        self.load_operations(path_operations)
