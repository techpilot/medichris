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

        # products = self.get_analysis()
        products = table

        col_titles = [k for k in products.keys()]
        rows_len = len(products[col_titles[0]])
        self.columns = (len(col_titles))
        # print(rows_len)
        table_data = []
        for t in col_titles:
            table_data.append(
                {'text': str(t), 'size_hint_y': None, 'height': 50, 'bcolor': (.131, .133, .255, 143)})

        for r in range(rows_len):
            for t in col_titles:
                table_data.append(
                    {'text': str(products[t][r]), 'size_hint_y': None, 'height': 30, 'bcolor': (.131, .133, .255, 143)})
        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data

    # def get_analysis(self):
    #     client = MongoClient()
    #     db_ana = client.pos
    #     analysis = db_ana.posone
    #     _sold = OrderedDict()
    #     _sold['product_name'] = {}
    #     _sold['product_qty'] = {}
    #     _sold['price'] = {}
    #     _sold['code'] = {}
    #     _sold['new_date'] = {}

    #     self.product_name = []
    #     product_qty = []
    #     price = []
    #     code = []
    #     date = []

    #     for analyse in analysis.find():
    #         name = analyse['product_name']
    #         if len(name) > 13:
    #             name = name[:13] + '...'
    #         self.product_name.append(name)
    #         product_qty.append(analyse['product_qty'])
    #         price.append(analyse['price'])
    #         code.append(analyse['code'])
    #         date.append(analyse['new_date'])
    #     # print(date)

    #     analysis_length = len(self.product_name)
    #     idx = 0
    #     while idx < analysis_length:
    #         _sold['product_name'][idx] = self.product_name[idx]
    #         _sold['product_qty'][idx] = product_qty[idx]
    #         _sold['price'][idx] = price[idx]
    #         _sold['code'][idx] = code[idx]
    #         _sold['new_date'][idx] = date[idx]

    #         idx += 1

    #     # db_ana.posone.find({}).sort('date', pymongo.DESCENDING)
    #     # print(db_ana.posone.find({}))

    #     return _sold


class DataTableApp(App):
    def build(self):

        return DataTable()


if __name__ == '__main__':
    DataTableApp().run()
