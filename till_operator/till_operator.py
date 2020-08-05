from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.core.text import LabelBase

import re
from collections import OrderedDict
from pymongo import MongoClient
from datetime import datetime
from datetime import date
import math
import random

Builder.load_file('till_operator/operator.kv')


class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.3, .3)


class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        self.db = client.db
        self.db_ana = client.pos
        self.stocks = self.db.stocks
        self.analysis = self.db_ana.posone

        self.cart = []
        self.qty = []
        self.instock = []
        self.sold = []
        self.dbStock = []
        self.dbSold = []
        self.total_list = []
        self.ana_price_list = []
        # self.ana_disc_list = []
        self.total = 0.00  # self.ids.qty_inp.text

        self.notify = Notify()

        self.ids.cur_date.text = str(datetime.now())[:16]

    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def logout(self):
        self.parent.parent.current = 'scrn_si'

    def filter_ana(self):
        product_price = []
        product_name = []
        product_qty = []
        spinvals = []
        for product in self.stocks.find():
            product_price.append(product['product_price'])
            product_qty.append(product['in_stock'])
            name = product['product_name']
            if len(name) > 50:
                name = name[:50] + '...'
            product_name.append(name)

        for x in range(len(product_name)):
            line = ' >> '.join(
                [product_name[x], '$' + str(product_price[x]), str(product_qty[x])])
            spinvals.append(line)
        self.ids.target_product.values = spinvals

    def generateOTP(self):
        digits = "012345678957083"
        OTP = ""

        for i in range(7):
            OTP += digits[math.floor(random.random() * 15)]
        return OTP

    def update_purchases(self):
        self.pcode = self.ids.code_inp.text
        products_container = self.ids.products

        self.target_code = self.stocks.find_one(
            {'product_name': self.pcode})  # 'product_code'
        if self.target_code == None or not self.target_code:
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Product Name Empty or Incorrect[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)

        else:
            self.details = BoxLayout(size_hint_y=None, height=30,
                                     pos_hint={'top': 1})

            products_container.add_widget(self.details)

            code = Label(text=self.target_code['product_code'], size_hint_x=.2,
                         bold=True, color=(.06, .45, .45, 1))
            name = Label(text=self.pcode,
                         size_hint_x=.3, color=(.06, .45, .45, 1))
            qty = Label(text=str(self.ids.qty_inp.text),
                        size_hint_x=.1, color=(.06, .45, .45, 1))
            # disc = Label(text=str(self.ids.disc_inp.text),
            #  size_hint_x=.1, color=(.06, .45, .45, 1))
            price = Label(
                text=str(self.target_code['product_price']), size_hint_x=.1, color=(.06, .45, .45, 1))

            self.total1 = Label(text=str(float(price.text) * int(self.ids.qty_inp.text)), size_hint_x=.2,
                                color=(.06, .45, .45, 1))
            undo = Button(text='remove', size_hint_x=.1, background_color=(.06, .45, .50, 1), on_release=lambda x: (self.details.remove_widget(code), self.details.remove_widget(name), self.details.remove_widget(
                qty), self.details.remove_widget(price), self.details.remove_widget(self.total1), self.details.remove_widget(undo), self.updateList(self.pcode)))

            self.details.add_widget(code)
            self.details.add_widget(name)
            self.details.add_widget(qty)
            # self.details.add_widget(disc)
            self.details.add_widget(price)
            self.details.add_widget(self.total1)
            self.details.add_widget(undo)

            # Update Preview
            pname = name.text
            pprice = float(price.text) * int(self.ids.qty_inp.text)
            pqty = str(self.ids.qty_inp.text)

            self.total += pprice

            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t\t\t\t' + \
                str(self.total)
            self.ids.cur_product.text = pname
            self.ids.cur_price.text = str(pprice)
            preview = self.ids.receipt_preview
            prev_text = preview.text
            _prev = prev_text.find('`')
            if _prev > 0:
                prev_text = prev_text[:_prev]

            getStock = self.target_code['in_stock']
            getSold = self.target_code['sold']
            anaPrice = self.target_code['product_price']

            self.cart.append(self.pcode)
            self.qty.append(self.ids.qty_inp.text)  # 1
            self.instock.append(getStock)
            self.sold.append(getSold)
            self.ana_price_list.append(anaPrice)
            self.total_list.append(self.total1.text)

            nu_preview = '\n'.join(
                [prev_text, pname+'\tx'+pqty+'\t'+str(price.text), purchase_total])
            preview.text = nu_preview

            print(self.cart)
            print(self.qty)
            print(self.instock)
            print(self.sold)

            self.ids.qty_inp.text = str(pqty)
            self.ids.price_inp.text = str(price.text)
            self.ids.total_inp.text = str(pprice)

    def updateList(self, cartName):
        for k in range(len(self.cart)):
            if self.cart[k] == cartName:
                del self.cart[k]
                del self.qty[k]
                del self.instock[k]
                del self.sold[k]
                del self.total_list[k]
        print(self.cart)
        print(self.qty)
        print(self.instock)
        print(self.sold)

    def test(self):
        # UPDATE PRODUCT DB
        if len(self.cart) == 0 or len(self.cart) != len(self.qty) or len(self.cart) != len(self.instock) or len(self.cart) != len(self.sold):
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Nothing to sell[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)

            self.ids.products.clear_widgets()
        else:
            for j in range(len(self.cart)):
                upd_instock = int(self.instock[j]) - int(self.qty[j])
                self.dbStock.append(upd_instock)
                print('stock : ', self.dbStock)

                upd_sold = int(self.sold[j]) + int(self.qty[j])
                self.dbSold.append(upd_sold)
                print('sold : ', self.dbSold)

                self.stocks.update_one({'product_name': self.cart[j]}, {
                    '$set': {'in_stock': self.dbStock[j]}})
                print('stock upd: ', self.dbStock[j])
                self.stocks.update_one({'product_name': self.cart[j]}, {
                    '$set': {'sold': self.dbSold[j]}})
                print('sold upd: ', self.dbSold[j])
                # self.cart[j]

            for i in range(len(self.cart)):
                self.analysis.insert_one({'product_name': self.cart[i], 'product_qty': self.qty[i], 'price': self.ana_price_list[i], 'date': str(datetime.now())[
                                         :16], 'code': self.generateOTP(), 'total': self.total_list[i], 'sales_date': str(datetime.now())[:10], 'month': str(datetime.now())[:7], 'time': str(datetime.now())[11:16]})
                print(self.total_list[i])
            self.notify.add_widget(
                Label(text='[color=#00FF00][b]Successful!!![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)

            del self.cart[::]
            del self.qty[::]
            del self.instock[::]
            del self.sold[::]
            del self.dbStock[::]
            del self.dbSold[::]
            del self.ana_price_list[::]
            del self.total_list[::]

            self.ids.products.clear_widgets()
            # self.ids.receipt_preview.text.clear_widgets()

    def get_products(self):
        client = MongoClient()
        db = client.db
        products = db.stocks
        _stocks = OrderedDict()
        _stocks['product_code'] = {}
        _stocks['product_name'] = {}
        _stocks['product_price'] = {}
        _stocks['in_stock'] = {}
        _stocks['sold'] = {}
        _stocks['order'] = {}

        product_code = []
        product_name = []
        product_price = []
        in_stock = []
        sold = []
        order = []

        for product in products.find():
            product_code.append(product['product_code'])
            name = product['product_name']
            if len(name) > 10:
                name = name[:10] + '...'
            product_name.append(name)
            product_price.append(product['product_price'])
            in_stock.append(product['in_stock'])
            sold.append(product['sold'])
            order.append(product['order'])

        products_length = len(product_code)
        idx = 0
        while idx < products_length:
            _stocks['product_code'][idx] = product_code[idx]
            _stocks['product_name'][idx] = product_name[idx]
            _stocks['product_price'][idx] = product_price[idx]
            _stocks['in_stock'][idx] = in_stock[idx]
            _stocks['sold'][idx] = sold[idx]
            _stocks['order'][idx] = order[idx]

            idx += 1

        return _stocks

    def get_analysis(self):
        client = MongoClient()
        db_ana = client.pos
        analysis = db_ana.posone
        _sold = OrderedDict()
        _sold['product_name'] = {}
        _sold['product_qty'] = {}
        _sold['price'] = {}
        _sold['discount'] = {}
        _sold['date'] = {}

        product_name = []
        product_qty = []
        price = []
        discount = []
        date = []

        for analyse in analysis.find():
            name = analyse['product_name']
            if len(name) > 13:
                name = name[:13] + '...'
            product_name.append(name)
            product_qty.append(analyse['product_qty'])
            price.append(analyse['price'])
            discount.append(analyse['discount'])
            date.append(analyse['date'])

        analysis_length = len(product_name)
        idx = 0
        while idx < analysis_length:
            _sold['product_name'][idx] = product_name[idx]
            _sold['product_qty'][idx] = product_qty[idx]
            _sold['price'][idx] = price[idx]
            _sold['discount'][idx] = discount[idx]
            _sold['date'][idx] = date[idx]

            idx += 1

        return _sold


class OperatorApp(App):
    def build(self):
        return OperatorWindow()


if __name__ == "__main__":
    oa = OperatorApp()
    oa.run()
