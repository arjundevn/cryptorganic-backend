from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

customer_table = {}
# veggies_table = {}
# fruits_table = {}
items_table = {}
initial_customer_id = 100
initial_item_id = 10
customer_item_id = dict()

# customer_table = {
#
#     11: {'name': 'Farmer 1',
#         'phone_number': 1234567890,
#         'location': 'Bangalore local'},
#
#     12: {'name': 'Farmer 2',
#         'phone_number': 5648145623,
#         'location': 'Bangalore Urban'},
#
# }


class User(BaseModel):
    name: str
    phone_number: int
    location: Optional[str] = 'NA'


class UpdateUser(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[int] = None
    location: Optional[str] = None


class Item(BaseModel):
    name: str
    quantity: float
    price_per_kilo: float
    customer_id: Optional[int] = 0


class UpdateItem(BaseModel):
    name: Optional[str] = None
    quantity: Optional[float] = None
    price_per_kilo: Optional[float] = None


""" Start: ID generator """
item_numbers = [number for number in range(11, 100)]
customer_numbers = [number for number in range(111, 999)]


def item_id_generator():

    return item_numbers.pop(0)


def customer_id_generator():

    return customer_numbers.pop(0)


""" END : ID generator """


@app.get("/customer_info/{customer_id}")
def get_customer_info(customer_id: int):
    if customer_id in customer_table:
        return customer_table[customer_id]
    return 'Customer not found!'


""" GET METHODS """


@app.get("/get_all_customer")
def get_customer_info_all():
    return customer_table


@app.get("/get_all_items")
def get_items():
    return items_table


@app.get("/customer_item_id")
def get_customer_item_id():
    return customer_item_id


@app.get("/items/customer_listings/{customer_id}")
def get_customer_listings(customer_id: int):

    if (customer_id in customer_item_id) and (len(customer_item_id[customer_id]) >= 1):
        customer_temp_table = {}
        for item_ids in customer_item_id[customer_id]:
            customer_temp_table[item_ids] = {'name': items_table[item_ids].name,
                                            'quantity': items_table[item_ids].quantity,
                                            'price_per_kilo': items_table[item_ids].price_per_kilo,
                                            }

        return customer_temp_table

    else:
        return 0



""" Add customer details to customer table """


# @app.post("/add_customer/{customer_id}")
# def add_update_customer_table(customer_id: int, user: User):
#     customer_table[customer_id] = user
#     return customer_table[customer_id]


@app.post("/add_customer")
def add_customer(user: User):
    # new user registration
    # initial customer ID: 101, 102 . . . etc
    customer_id = customer_id_generator()
    customer_table[customer_id] = user

    return customer_table[customer_id]


@app.post("/items/add_items/{customer_id}")
def add_item(customer_id: int, item: Item):

    # new item addition
    # initial item ID starts from 11

    if customer_id in customer_table:

        item_id = item_id_generator()

        if customer_id in customer_item_id.keys():
            customer_item_id[customer_id].append(item_id)
        else:
            customer_item_id[customer_id] = [item_id]

        items_table[item_id] = item
        items_table[item_id].customer_id = customer_id

        return items_table

    else:
        return {'Error': 'Customer ID does not exist'}

# @app.post("/items/add_fruits/{customer_id}")
# def add_fruits(customer_id: int, item: Item):
#
#     # new item addition
#     # initial item ID starts from 11
#     if item.name not in fruits_table[customer_id]:
#
#         item_id = initial_item_id + 1
#         fruits_table[item_id] = item
#         fruits_table[item_id]['customer_id'] = customer_id
#
#         return fruits_table
#
#     else:
#         return {'Error': 'Item already exists. Try update'}


@app.put("/items/buy/{item_id}/{buy_quantity}")
def buy_item(item_id: int, buy_quantity: float):

    if item_id in items_table:
        if items_table[item_id].quantity >= buy_quantity:

            items_table[item_id].quantity -= buy_quantity

            if items_table[item_id].quantity == 0:
                items_table.pop(item_id)

                for customer_id_list in customer_item_id.values():
                    if item_id in customer_id_list:
                        customer_id_list.remove(item_id)

            return items_table
        else:
            return {'Error': 'Specified buy quantity greater than available stock.'}

    else:
        return {'Error': 'Item does not exist'}


@app.put("/update_customer/{customer_id}")
def update_customer(customer_id: int, user: UpdateUser):

    if customer_id in customer_table:
        if user.name is not None:
            customer_table[customer_id].name = user.name

        if user.location is not None:
            customer_table[customer_id].location = user.location

        if user.phone_number is not None:
            customer_table[customer_id].phone_number = user.phone_number

    else:
        return {'Error': 'Customer ID does not exist'}
