import collections
from abc import ABC, abstractmethod
import sys

from shopping_cart_interface import IShoppingCart
from pricer import Pricer
from format import Format

class ShoppingCart(IShoppingCart):
    """
    Implementation of the shopping tills in our supermarket.
    """
    def __init__(self, pricer: Pricer, format: Format):
        self.pricer = pricer
        self._contents: dict = collections.OrderedDict()
        self.format = format
        self.total = 0
        self.scan_id = 0

    def add_item(self, item_type: str, number: int):
        # adds new item to cart
        # making an assumption that when asked to ensure items are printed in
        # the order they are scanned that items of the same type will be printed
        # on sperate lines rather than updated if scanned at different times
        self._contents[self.scan_id] = {"item_type" : item_type,
                                    "number" : number}
        self.scan_id += 1

    def print_receipt(self):
        for item in self._contents.items():
            item_type = item[1]["item_type"]
            amount = item[1]["number"]
            price = self.pricer.get_price(item_type)
            self.format.get_format(item_type, amount, price)
            self.total += (price*amount)
        print (f"total - {self.total}")
        

class ShoppingCartCreator(ABC):
    """
    Interface for the ShoppingCart creator.
    The creation process will be delegated to the subclasses of this class.
    """
    @abstractmethod
    def factory_method(self, format_option) -> ShoppingCart:
        # return the ShoppingCart object
        pass

    def operation(self, format_option: int = 1) -> ShoppingCart:
        # Here more operations can be performed on the ShoppingCart object
        # returns ShoppingCart object
        return self.factory_method(format_option)

class ShoppingCartConcreteCreator(ShoppingCartCreator):
    """
    Concrete class for the ShoppingCart creator.
    Implements the factory_method
    """
    def factory_method(self, format_option) -> ShoppingCart:
        # returns ShoppingCart object
        return ShoppingCart(Pricer(), Format(format_option))


