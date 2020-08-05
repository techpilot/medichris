from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from pymongo import MongoClient
from collections import OrderedDict

Builder.load_string('''
<DataTable>:
    id: main_win
    RecycleView:
        viewclass: 'CustLabel'
        id: table_floor
        RecycleGridLayout:
            id: table_floor_layout
            cols: 5
            default_size: (None,250)
            default_size_hint: (1,None)
            size_hint_y: None
            height: self.minimum_height
            spacing: 5
<CustLabel@Label>:
    bcolor: (1,1,1,1)
    canvas.before:
        Color:
            rgba: root.bcolor
        Rectangle:
            size: self.size
            pos: self.pos
''')


class DataTable(BoxLayout):
    def __init__(self, table='', ** kwargs):
        super().__init__(**kwargs)

        # products = self.get_products()
        products = table

        col_titles = [k for k in products.keys()]
        rows_len = len(products[col_titles[0]])
        self.columns = (len(col_titles))
        # print(rows_len)
        table_data = []
        for t in col_titles:
            table_data.append(
                {'text': str(t), 'size_hint_y': None, 'height': 50, 'bcolor': (.06, .45, .45, 1)})

        for r in range(rows_len):
            for t in col_titles:
                table_data.append(
                    {'text': str(products[t][r]), 'size_hint_y': None, 'height': 30, 'bcolor': (.06, .25, .25, .1)})
        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data

#     def get_products(self):
#         client = MongoClient()
#         db = client.silverpos
#         products = db.stocks
#         _stocks = OrderedDict()
#         _stocks['product_code'] = {}
#         _stocks['product_name'] = {}
#         _stocks['product_weight'] = {}
#         _stocks['product_price'] = {}
#         _stocks['in_stock'] = {}
#         _stocks['sold'] = {}
#         _stocks['order'] = {}
#         _stocks['last_purchase'] = {}

#         product_code = []
#         product_name = []
#         product_weight = []
#         product_price = []
#         in_stock = []
#         sold = []
#         order = []
#         last_purchase = []

#         for product in products.find():
#             product_code.append(product['product_code'])
#             name = product['product_name']
#             if len(name) > 10:
#                 name = name[:10] + '...'
#             product_name.append(name)
#             product_weight.append(product['product_weight'])
#             product_price.append(product['product_price'])
#             in_stock.append(product['in_stock'])
#             sold.append(product['sold'])
#             order.append(product['order'])
#             last_purchase.append(product['last_purchase'])
#         # print(designations)
#         products_length = len(product_code)
#         idx = 0
#         while idx < products_length:
#             _stocks['product_code'][idx] = product_code[idx]
#             _stocks['product_name'][idx] = product_name[idx]
#             _stocks['product_weight'][idx] = product_weight[idx]
#             _stocks['product_price'][idx] = product_price[idx]
#             _stocks['in_stock'][idx] = in_stock[idx]
#             _stocks['sold'][idx] = sold[idx]
#             _stocks['order'][idx] = order[idx]
#             _stocks['last_purchase'][idx] = last_purchase[idx]

#             idx += 1

#         return _stocks


# class DataTableApp(App):
#     def build(self):

#         return DataTable()


# if __name__ == '__main__':
#     DataTableApp().run()
