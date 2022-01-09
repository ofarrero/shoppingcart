from string import Template

class Format:
    """
    a datastore for the available receipt formats in the supermarket
    """
    
    def __init__(self, format_choice:int = 1):
        self.__format_option = format_choice
        self.__options = {
            1: Template('$key - $value - $price'),
            2: Template('$price - $key - $value')
        }
    
    def get_format(self, key: str, value:int, price:int):
        # Prints the receipt in the format specified by the store
        print(
            self.__options[self.__format_option].substitute(
                key = key, value = value, price = price)
            )
        