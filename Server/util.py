import json
import pickle
import numpy as np

__data_columns = None
__model = None
__town = None
__flat_model = None
__flat_type = None
__storey_range = None
__sales_month = None


def get_estimated_price(town, flat_type, storey_range, floor_area_sqm, flat_model, lease_commence_date, sales_year,
                        sales_month):

    town_index = __data_columns.index(f"town_{town}")
    flat_type_index = __data_columns.index(f"flat_type_{flat_type}")
    storey_range_index = __data_columns.index(f"storey_range_{storey_range}")
    sales_month_index = __data_columns.index(f"sales_month_{sales_month}")
    flat_model_index = __data_columns.index(f"flat_model_{flat_model}")
    floor_area_sqm_index = __data_columns.index("floor_area_sqm")
    lease_commence_date_index = __data_columns.index("lease_commence_date")
    sales_year_index = __data_columns.index("sales_year")

    x = np.zeros(len(__data_columns))
    x[floor_area_sqm_index] = floor_area_sqm
    x[lease_commence_date_index] = lease_commence_date
    x[sales_year_index] = sales_year
    if town_index >= 0:
        x[town_index] = 1
    if flat_type_index >= 0:
        x[flat_type_index] = 1
    if storey_range_index >= 0:
        x[storey_range_index] = 1
    if sales_month_index >= 0:
        x[sales_month_index] = 1
    if flat_model_index >= 0:
        x[flat_model_index] = 1

    return round(__model.predict([x])[0])




def get_categorical():
    town = [x.replace('town_', '') for x in __town]
    flat_model = [x.replace('flat_model_', '') for x in __flat_model]
    flat_type = [x.replace('flat_type_', '') for x in __flat_type]
    storey_range = [x.replace('storey_range_', '') for x in __storey_range]
    sales_month = [x.replace('sales_month_', '') for x in __sales_month]

    return town, flat_model, flat_type, storey_range, sales_month


def load_saved_resources():
    print('Loading Saved Resources...Start')
    global __data_columns
    global __town
    global __flat_model
    global __flat_type
    global __storey_range
    global __sales_month
    global __model

    with open("./Resources/columns.json", 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __town = [column for column in __data_columns if column.startswith("town_")]
        __flat_model = [column for column in __data_columns if column.startswith("flat_model_")]
        __flat_type = [column for column in __data_columns if column.startswith("flat_type_")]
        __storey_range = [column for column in __data_columns if column.startswith("storey_range_")]
        __sales_month = [column for column in __data_columns if column.startswith("sales_month_")]
    with open("./Resources/Singapore_Resale_Price_Model_lin_model.pickle", 'rb') as f:
        __model = pickle.load(f)
    print('Loading Saved Resources...Done')


if __name__ == '__main__':
    load_saved_resources()
    print(get_categorical(), '\n')
    print(get_estimated_price(town = 'ANG MO KIO', flat_type = '1 ROOM', storey_range = 'Mid-Rise', floor_area_sqm = 31.0, flat_model= 'IMPROVED', lease_commence_date = 1977, sales_year = 2025,sales_month = 'Q4'))


