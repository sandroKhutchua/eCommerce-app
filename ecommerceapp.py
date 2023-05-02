import string


class Product:

    def __init__(self, name: string, price: int):
        self.name: string = name
        self.price: int = price
        self.quantity: int = 0
        self.number_of_orders: int = 0
        self.order_income: int = 0
        self.paid_for: int = 0

    def set_product_name(self, new_name: string) -> None:
        self.name = new_name

    def get_product_name(self) -> string:
        return self.name

    def set_price(self, new_price: int) -> None:
        self.price = new_price

    def get_price(self) -> int:
        return self.price

    def get_quantity(self) -> int:
        return self.quantity

    def purchase(self, quantity: int, price: int) -> None:
        self.quantity += quantity
        self.paid_for += quantity * price

    def order(self, quantity: int) -> None:
        self.number_of_orders += 1
        self.quantity -= quantity
        self.order_income += quantity * self.price

    def get_average_price(self) -> int:
        if self.quantity + self.number_of_orders == 0:
            return self.price
        return int(self.paid_for / (self.quantity + self.number_of_orders))

    def get_product_profit(self) -> int:
        return self.order_income - self.paid_for


def check_number_of_input_arguments(method_name: string, desired_num: int, product: list[string]) -> bool:
    if len(product) < desired_num:
        print(f'Not enough input arguments for {method_name}')
        return False
    if len(product) > desired_num:
        print(f'Too many input arguments for {method_name}')
        return False
    return True


class ECommerceApp:
    ILLEGAL_INT = -999999999
    ILLEGAL_STRING = ""
    ILLEGALS = {ILLEGAL_INT, ILLEGAL_STRING}

    def __init__(self):
        self.db = dict()

    def save_product(self, product: list[string]) -> None:
        if not check_number_of_input_arguments('save_product', 3, product):
            return
        if not product[2].isnumeric():
            print('Price has to be a number')
            return
        product_id = product[0]
        product_name = product[1]
        product_price = int(product[2])
        if product_id in self.db.keys():
            self.db[product_id].set_product_name(product_name)
            self.db[product_id].set_price(product_price)
        else:
            new_product = Product(product_name, product_price)
            self.db[product_id] = new_product

    def purchase_product(self, product: list[string]) -> None:
        if not check_number_of_input_arguments('purchase_product', 3, product):
            return
        product_id = product[0]
        quantity = product[1]
        price = product[2]
        if not self.product_in_catalog(product_id):
            return
        if not quantity.isnumeric():
            print('Quantity has to be a number')
            return
        if not price.isnumeric():
            print('Price has to be a number')
            return
        quantity = int(quantity)
        price = int(price)
        cur_product = self.db[product_id]
        cur_product.purchase(quantity, price)

    def order_product(self, product: list[string]) -> None:
        if not check_number_of_input_arguments('order_product', 2, product):
            return
        product_id = product[0]
        quantity = product[1]
        if not self.product_in_catalog(product_id):
            return
        if not quantity.isnumeric():
            print('Quantity hat to be a number')
            return
        quantity = int(quantity)
        cur_product = self.db[product_id]
        if cur_product.get_quantity() < quantity:
            print(f'There are only {cur_product.get_quantity()} of this product left in the catalog')
            return
        cur_product.order(quantity)

    def get_quantity_of_product(self, product: list[string]) -> int:
        if not check_number_of_input_arguments('get_quantity_of_product', 1, product):
            return ECommerceApp.ILLEGAL_INT
        product_id = product[0]
        if not self.product_in_catalog(product_id):
            return ECommerceApp.ILLEGAL_INT
        return self.db[product_id].get_quantity()

    def get_average_price(self, product: list[string]) -> int:
        if check_number_of_input_arguments('get_average_price', 1, product) == -1:
            return ECommerceApp.ILLEGAL_INT
        product_id = product[0]
        if not self.product_in_catalog(product_id):
            return ECommerceApp.ILLEGAL_INT
        return self.db[product_id].get_average_price()

    def get_product_profit(self, product: list[string]) -> int:
        if check_number_of_input_arguments('get_product_profit', 1, product) == -1:
            return ECommerceApp.ILLEGAL_INT
        product_id = product[0]
        if not self.product_in_catalog(product_id):
            return ECommerceApp.ILLEGAL_INT
        cur_product = self.db[product_id]
        return cur_product.get_product_profit()

    def get_fewest_product(self, product: list[string]) -> string:
        if len(product) > 0:
            print('get_fewest_product does not require any input arguments')
        if not self.db:
            print('There are no items at all in the catalog')
            return ECommerceApp.ILLEGAL_STRING
        name = ""
        min_quantity = 999999999
        for product_id in self.db.keys():
            cur_product = self.db[product_id]
            if cur_product.get_quantity() < min_quantity:
                name = cur_product.get_product_name()
                min_quantity = cur_product.get_quantity()
        return name

    def get_most_popular_product(self, product) -> string:
        if len(product) > 0:
            print('get_fewest_product does not require any input arguments')
        if not self.db:
            print('There are no items at all in the catalog')
            return ECommerceApp.ILLEGAL_STRING
        name = ""
        max_orders = -1
        for product_id in self.db.keys():
            cur_product = self.db[product_id]
            if cur_product.get_quantity() > max_orders:
                name = cur_product.get_product_name()
                max_orders = cur_product.get_quantity()
        return name

    def product_in_catalog(self, product_id: string) -> bool:
        if product_id not in self.db.keys():
            print('No such item in the catalog')
            return False
        return True


if __name__ == '__main__':
    my_app = ECommerceApp()
    commands = {'save_product',
                'purchase_product',
                'order_product',
                'get_quantity_of_product',
                'get_average_price',
                'get_product_profit',
                'get_fewest_product',
                'get_most_popular_product'
                }
    while True:
        inp = input().strip()
        if not inp:
            continue
        if inp == 'exit':
            break
        inp_list = inp.split()
        command = inp_list[0]
        product_info = inp_list[1:]
        if command not in commands:
            print('Unknown Command')
        else:
            res = eval('my_app.' + command + '(product_info)')
            if (res is not None) and (res not in ECommerceApp.ILLEGALS):
                print(res)
