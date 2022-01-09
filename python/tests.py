import unittest

from shopping_cart import ShoppingCartConcreteCreator
from test_utils import Capturing

class ShoppingCartAddTest(unittest.TestCase):
    def setUp(self):
        self.cart =  ShoppingCartConcreteCreator().operation()
    
    def test_add_item(self):
        self.cart.add_item("apple", 2)
        self.assertEqual({0:{"item_type" : "apple",
                             "number" : 2}}, self.cart._contents)
    
    def test_update_item(self):
        self.cart.add_item("apple", 4)
        self.cart.add_item("apple", 2)
        self.assertEqual({0:{"item_type" : "apple",
                             "number" : 4},
                          1:{"item_type" : "apple",
                             "number" : 2}}, self.cart._contents)
    
    def test_add_multiple_items(self):
        self.cart.add_item("apple", 2)
        self.cart.add_item("banana", 3)
        self.cart.add_item("strawberries", 10)
        self.assertEqual({0:{"item_type" : "apple",
                             "number" : 2},
                          1:{"item_type" : "banana",
                             "number":3},
                          2:{"item_type" : "strawberries",
                             "number" : 10}}, 
                         self.cart._contents)
    
        
    def tearDown(self) -> None:
        super(ShoppingCartAddTest, self).tearDown()
        
class ShoppingCartReceiptTest(unittest.TestCase):
    
    def setUp(self):
        self.cartItems = {0:{"item_type" : "apple",
                             "number" : 2},
                          1:{"item_type" : "banana",
                             "number" : 3}}
        
    def test_print_receipt_default(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc._contents =self.cartItems
        
        applePrice = sc.pricer.get_price("apple")
        bananaPrice = sc.pricer.get_price("banana")
        
        with Capturing() as output:
            sc.print_receipt()
            
        self.assertEqual(f"apple - 2 - {applePrice}", output[0])
        self.assertEqual(f"banana - 3 - {bananaPrice}", output[1])
    
    def test_print_receipt_price_first(self):
        sc = ShoppingCartConcreteCreator().operation(2)
        sc._contents =self.cartItems
        
        applePrice = sc.pricer.get_price("apple")
        
        with Capturing() as output:
            sc.print_receipt()
            
        self.assertEqual(f"{applePrice} - apple - 2", output[0])
    
    def test_print_receipt_item_first(self):
        sc = ShoppingCartConcreteCreator().operation(1)
        sc._contents =self.cartItems
        
        applePrice = sc.pricer.get_price("apple")
        
        with Capturing() as output:
            sc.print_receipt()
            
        self.assertEqual(f"apple - 2 - {applePrice}", output[0])
    
    def test_doesnt_explode_on_mystery_item(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc.add_item("pear", 5)
        with Capturing() as output:
            sc.print_receipt()
        self.assertEqual("pear - 5 - 0", output[0])
    
    def tearDown(self) -> None:
        super(ShoppingCartReceiptTest, self).tearDown()
    
class ShoppingCartTotalTest(unittest.TestCase):
    
    def setUp(self):
        self.cart =  ShoppingCartConcreteCreator().operation()
        self.cart.add_item("apple", 2)
    
    def test_print_total(self):
        
        with Capturing() as output:
            self.cart.print_receipt()
        self.assertEqual("total - 200", output[-1])
    
    def test_print_total_update_item(self):
        self.cart.add_item("apple", 1)
        with Capturing() as output:
            self.cart.print_receipt()
        self.assertEqual("total - 300", output[-1])
    
    
    def test_print_total_multi_items(self):
        self.cart.add_item("banana", 1)
        with Capturing() as output:
            self.cart.print_receipt()
        self.assertEqual("total - 400", output[-1])
    
    def test_print_total_foreign_item(self):
        self.cart.add_item("pear", 1)
        with Capturing() as output:
            self.cart.print_receipt()
        self.assertEqual("total - 200", output[-1])
    
    def tearDown(self) -> None:
        super(ShoppingCartTotalTest, self).tearDown()

unittest.main(exit=False)
