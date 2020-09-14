from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.graphics import Color

from collections import OrderedDict
import pymongo
from pymongo import MongoClient
from utils.datatable import DataTable
from datetime import datetime
import hashlib
import math
import random


Builder.load_file('admin/admin.kv')


class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.3, .3)


class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        db = client.db

        self.users = db.users
        self.products = db.stocks
        self.analysis = db.analysis
        self.notify = Notify()

        # Display users
        content = self.ids.scrn_contents
        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

        # Display Products
        product_scrn = self.ids.scrn_product_contents
        products = self.get_products()
        prod_table = DataTable(table=products)
        product_scrn.add_widget(prod_table)

        # Display Product Analysis
        analysis_scrn = self.ids.analysis_res
        analysis = self.get_analysis()
        ana_table = DataTable(table=analysis)
        analysis_scrn.add_widget(ana_table)

    def logout(self):
        self.parent.parent.current = 'scrn_si'

    # SPINNER
    def filter_ana(self):
        product_code = []
        product_name = []
        spinvals = []
        for product in self.products.find():
            product_code.append(product['product_code'])
            name = product['product_name']
            if len(name) > 30:
                name = name[:30] + '...'
            product_name.append(name)

        for x in range(len(product_code)):
            line = ' | '.join([product_name[x], product_code[x]])
            spinvals.append(line)
        self.ids.target_product.values = spinvals

    def generateOTP(self):
        digits = "012345678957083"
        OTP = ""

        for i in range(5):
            OTP += digits[math.floor(random.random() * 15)]
            print(i)
        return OTP

    # ADD FIELDS

    def add_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name',
                               multiline=False)
        crud_last = TextInput(hint_text='Last Name', multiline=False)
        crud_user = TextInput(hint_text='User Name', multiline=False)
        crud_pwd = TextInput(hint_text='Password', multiline=False)
        crud_des = Spinner(text='Operator', values=[
                           'Operator', 'Administrator'])
        crud_submit = Button(text='Add', background_color=(0, 1, 0, 1), size_hint_x=None, width=100, on_release=lambda x: self.add_user(
            crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_name = TextInput(hint_text='Product Name', multiline=False)
        crud_price = TextInput(hint_text='Price(Naira)',
                               multiline=False, input_filter='float')
        crud_stock = TextInput(hint_text='In Stock(qty)',
                               multiline=False, input_filter='int')
        crud_sold = TextInput(hint_text='Sold(qty)',
                              multiline=False, input_filter='int')
        crud_submit = Button(text='Add', background_color=(0, 1, 0, 1), size_hint_x=None, width=100, on_release=lambda x: self.add_product(
            crud_name.text, crud_price.text, crud_stock.text, crud_sold.text))

        target.add_widget(crud_name)
        target.add_widget(crud_price)
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_submit)

    # ADD FUNCTIONS
    def add_user(self, first, last, user, pwd, des):
        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        if first == '' or last == '' or user == '' or pwd == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            self.users.insert_one({'first_name': first, 'last_name': last, 'user_name': user,
                                   'password': pwd, 'designation': des, 'date': datetime.now()})

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def killswitch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def add_product(self, name, price, stock, sold):
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        if name == '' or price == '' or stock == '' or sold == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]All Fields Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            self.products.insert_one({'product_code': self.generateOTP(), 'product_name': name,
                                      'product_price': price, 'in_stock': stock, 'sold': sold, 'order': str(datetime.now())[:10]})

        prodz = self.get_products()
        stocktable = DataTable(table=prodz)
        content.add_widget(stocktable)

    # UPDATE FIELDS
    def update_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name', multiline=False)
        crud_last = TextInput(hint_text='Last Name', multiline=False)
        crud_user = TextInput(hint_text='User Name', multiline=False)
        crud_pwd = TextInput(hint_text='Password', multiline=False)
        crud_des = Spinner(text='Operator', values=[
                           'Operator', 'Administrator'])
        crud_submit = Button(text='Update', background_color=(0, 0, 1, 1), size_hint_x=None, width=100, on_release=lambda x: self.update_user(
            crud_first.text, crud_last.text, crud_user.text, crud_pwd.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text='Product Code', multiline=False)
        crud_name = TextInput(hint_text='Product Name', multiline=False)
        crud_price = TextInput(hint_text='Price(Naira)',
                               multiline=False, input_filter='float')
        crud_stock = TextInput(hint_text='In Stock(qty)',
                               multiline=False, input_filter='int')
        crud_sold = TextInput(hint_text='Sold(qty)',
                              multiline=False, input_filter='int')
        crud_submit = Button(text='Update', background_color=(0, 0, 1, 1), size_hint_x=None, width=100, on_release=lambda x: self.update_product(
            crud_code.text, crud_name.text, crud_price.text, crud_stock.text, crud_sold.text))

        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_price)
        target.add_widget(crud_stock)
        target.add_widget(crud_sold)
        target.add_widget(crud_submit)

    # UPDATE FUNCTIONS
    def update_user(self, first, last, user, pwd, des):
        content = self.ids.scrn_contents
        content.clear_widgets()
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        if user == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Username Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            self.users.update_one({'user_name': user}, {'$set': {'first_name': first, 'last_name': last,
                                                                 'user_name': user, 'password': pwd, 'designation': des, 'date': datetime.now()}})

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def update_product(self, code, name, price, stock, sold):
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        if code == '' or name == '' or price == '' or stock == '' or sold == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Fields Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            self.products.update_one({'product_code': code}, {'$set': {'product_code': code, 'product_name': name,
                                                                       'product_price': price, 'in_stock': stock, 'sold': sold, 'order': str(datetime.now())[:10]}})

        prodz = self.get_products()
        stocktable = DataTable(table=prodz)
        content.add_widget(stocktable)

    # REMOVE/DELETE FIELDS
    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(
            hint_text='Username', multiline=False)
        crud_submit = Button(text='Delete', background_color=(1, 0, 0, 1), size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_user(crud_user.text))

        target.add_widget(crud_user)
        target.add_widget(crud_submit)

    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code', multiline=False)
        crud_submit = Button(text='Delete', background_color=(1, 0, 0, 1), size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_product(crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_submit)

    def remove_analysis_fields(self):
        target = self.ids.ops_fields_a
        target.clear_widgets()
        crud_code = TextInput(hint_text='Enter Code', multiline=False)
        crud_submit = Button(text='Delete', background_color=(1, 0, 0, 1), size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_analysis(crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_submit)

    # REMOVE/DELETE FUNCTIONS
    def remove_user(self, user):
        content = self.ids.scrn_contents
        content.clear_widgets()
        if user == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Username Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            self.users.remove({'user_name': user})

            self.notify.add_widget(
                Label(text='[color=#00FF00][b]Successfully Removed![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)

        users = self.get_users()
        userstable = DataTable(table=users)
        content.add_widget(userstable)

    def remove_product(self, code):
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        if code == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Product Code Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            self.products.remove({'product_code': code})

            self.notify.add_widget(
                Label(text='[color=#00FF00][b]Successfully Removed!![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)

        prodz = self.get_products()
        stocktable = DataTable(table=prodz)
        content.add_widget(stocktable)

    def remove_analysis(self, code):
        content = self.ids.analysis_res
        content.clear_widgets()

        if code == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]Product Code Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            self.analysis.remove({'code': code})

            self.notify.add_widget(
                Label(text='[color=#00FF00][b]Successfully Removed!!![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)

        analyse = self.get_analysis()
        ana_table = DataTable(table=analyse)
        content.add_widget(ana_table)

    # DATE FILTERS
    def dated_analysis_fields(self):
        target = self.ids.ops_fields_a
        target.clear_widgets()
        self.crud_date = TextInput(hint_text='Date', multiline=False)
        crud_submit = Button(text='Day Stats', background_color=(0, 0, 1, 1), size_hint_x=None, width=100,
                             on_release=lambda x: self.dated_analysis())

        target.add_widget(self.crud_date)
        target.add_widget(crud_submit)

    def monthd_analysis_fields(self):
        target = self.ids.ops_fields_a
        target.clear_widgets()
        self.crud_month = TextInput(hint_text='Month', multiline=False)
        crud_submit = Button(text='Month Stats', background_color=(0, 0, 1, 1), size_hint_x=None, width=100,
                             on_release=lambda x: self.monthd_analysis())

        target.add_widget(self.crud_month)
        target.add_widget(crud_submit)

    def daily_sales_fields(self):
        target = self.ids.ops_fields_a
        target.clear_widgets()
        self.crud_day = TextInput(hint_text='Input Date', multiline=False)
        crud_submit = Button(text='Sales', background_color=(1, 0, 1, 1), size_hint_x=None, width=100,
                             on_release=lambda x: self.daily_sales())

        target.add_widget(self.crud_day)
        target.add_widget(crud_submit)

    def dated_analysis(self):
        content = self.ids.analysis_res
        content.clear_widgets()

        analyse = self.dated_stats()
        ana_table = DataTable(table=analyse)
        content.add_widget(ana_table)

    def monthd_analysis(self):
        content = self.ids.analysis_res
        content.clear_widgets()

        analyse = self.monthd_stats()
        ana_table = DataTable(table=analyse)
        content.add_widget(ana_table)

    def daily_sales(self):
        content = self.ids.analysis_res
        content.clear_widgets()

        client = MongoClient()
        db_ana = client.db
        analysis = db_ana.analysis
        _sold = OrderedDict()
        _sold['total'] = {}
        _sold['sales_date'] = {}

        total = []
        date = []

        for analyse in analysis.find({'sales_date': self.crud_day.text}):
            total.append(analyse['total'])
            date.append(analyse['sales_date'])
        print(total)
        totaled = [float(i) for i in total]
        self.total_sum = sum(totaled)

        deSales = Label(text=str(self.total_sum), font_name='alpha', size_hint_x=.2,
                        bold=True, color=(.06, .45, .45, 1))

        self.ids.analysis_res.add_widget(deSales)

    def get_users(self):
        client = MongoClient()
        db = client.db
        users = db.users
        _users = OrderedDict()
        _users['first_names'] = {}
        _users['last_names'] = {}
        _users['user_names'] = {}
        _users['passwords'] = {}
        _users['designations'] = {}
        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designations = []
        for user in users.find():
            first_names.append(user['first_name'])
            last_names.append(user['last_name'])
            user_names.append(user['user_name'])
            pwd = user['password']
            if len(pwd) > 8:
                pwd = pwd[:8] + '...'
            passwords.append(pwd)
            designations.append(user['designation'])

        users_length = len(first_names)
        idx = 0
        while idx < users_length:
            _users['first_names'][idx] = first_names[idx]
            _users['last_names'][idx] = last_names[idx]
            _users['user_names'][idx] = user_names[idx]
            _users['passwords'][idx] = passwords[idx]
            _users['designations'][idx] = designations[idx]

            idx += 1

        return _users

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

    # PRODUCT ANALYSIS
    def get_analysis(self):
        client = MongoClient()
        db_ana = client.db
        analysis = db_ana.analysis
        _sold = OrderedDict()
        _sold['code'] = {}
        _sold['product_name'] = {}
        _sold['product_qty'] = {}
        _sold['price'] = {}
        _sold['sales_date'] = {}
        _sold['time'] = {}

        code = []
        self.product_name = []
        product_qty = []
        price = []
        date = []
        time = []

        for analyse in analysis.find():
            code.append(analyse['code'])
            name = analyse['product_name']
            if len(name) > 13:
                name = name[:13] + '...'
            self.product_name.append(name)
            product_qty.append(analyse['product_qty'])
            price.append(analyse['price'])
            date.append(analyse['sales_date'])
            time.append(analyse['time'])

        analysis_length = len(self.product_name)
        idx = 0
        while idx < analysis_length:
            _sold['code'][idx] = code[idx]
            _sold['product_name'][idx] = self.product_name[idx]
            _sold['product_qty'][idx] = product_qty[idx]
            _sold['price'][idx] = price[idx]
            _sold['sales_date'][idx] = date[idx]
            _sold['time'][idx] = time[idx]

            idx += 1

        return _sold

    # PRODUCT STATS FILTERS
    def dated_stats(self):
        client = MongoClient()
        db_ana = client.db
        analysis = db_ana.analysis
        _sold = OrderedDict()
        _sold['code'] = {}
        _sold['product_name'] = {}
        _sold['product_qty'] = {}
        _sold['price'] = {}
        _sold['sales_date'] = {}
        _sold['time'] = {}

        code = []
        product_name = []
        product_qty = []
        price = []
        sales_date = []
        time = []

        for analyse in analysis.find({'sales_date': self.crud_date.text}):
            code.append(analyse['code'])
            name = analyse['product_name']
            if len(name) > 17:
                name = name[:17] + '...'
            product_name.append(name)
            product_qty.append(analyse['product_qty'])
            price.append(analyse['price'])
            sales_date.append(analyse['sales_date'])
            time.append(analyse['time'])

        analysis_length = len(product_name)
        idx = 0
        while idx < analysis_length:
            _sold['code'][idx] = code[idx]
            _sold['product_name'][idx] = product_name[idx]
            _sold['product_qty'][idx] = product_qty[idx]
            _sold['price'][idx] = price[idx]
            _sold['sales_date'][idx] = sales_date[idx]
            _sold['time'][idx] = time[idx]

            idx += 1
        print(self.crud_date.text)
        return _sold

    def monthd_stats(self):

        client = MongoClient()
        db_ana = client.db
        analysis = db_ana.analysis
        _sold = OrderedDict()
        _sold['code'] = {}
        _sold['product_name'] = {}
        _sold['product_qty'] = {}
        _sold['price'] = {}
        _sold['sales_date'] = {}
        _sold['time'] = {}

        code = []
        product_name = []
        product_qty = []
        price = []
        sales_date = []
        time = []

        for analyse in analysis.find({'month': self.crud_month.text}):
            code.append(analyse['code'])
            name = analyse['product_name']
            if len(name) > 17:
                name = name[:17] + '...'
            product_name.append(name)
            product_qty.append(analyse['product_qty'])
            price.append(analyse['price'])
            sales_date.append(analyse['sales_date'])
            time.append(analyse['time'])

        analysis_length = len(product_name)
        idx = 0
        while idx < analysis_length:
            _sold['code'][idx] = code[idx]
            _sold['product_name'][idx] = product_name[idx]
            _sold['product_qty'][idx] = product_qty[idx]
            _sold['price'][idx] = price[idx]
            _sold['sales_date'][idx] = sales_date[idx]
            _sold['time'][idx] = time[idx]

            idx += 1

        return _sold

    def stats(self):
        target_product = self.ids.target_product.text
        name = target_product[:target_product.find(' | ')]

        client = MongoClient()
        db_ana = client.db
        analysis = db_ana.analysis
        _sold = OrderedDict()
        _sold['code'] = {}
        _sold['product_name'] = {}
        _sold['product_qty'] = {}
        _sold['price'] = {}
        _sold['sales_date'] = {}
        _sold['time'] = {}

        code = []
        product_name = []
        product_qty = []
        price = []
        sales_date = []
        time = []

        for analyse in analysis.find({'product_name': name}):
            code.append(analyse['code'])
            name = analyse['product_name']
            if len(name) > 17:
                name = name[:17] + '...'
            product_name.append(name)
            product_qty.append(analyse['product_qty'])
            price.append(analyse['price'])
            sales_date.append(analyse['sales_date'])
            time.append(analyse['time'])

        analysis_length = len(product_name)
        idx = 0
        while idx < analysis_length:
            _sold['code'][idx] = code[idx]
            _sold['product_name'][idx] = product_name[idx]
            _sold['product_qty'][idx] = product_qty[idx]
            _sold['price'][idx] = price[idx]
            _sold['sales_date'][idx] = sales_date[idx]
            _sold['time'][idx] = time[idx]

            idx += 1

        return _sold

    def view_stats(self):

        self.ids.analysis_res.clear_widgets()

        analysis_scrn = self.ids.analysis_res
        analysis = self.stats()
        ana_table = DataTable(table=analysis)
        analysis_scrn.add_widget(ana_table)

    def change_screen(self, instance):
        if instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        elif instance.text == 'Manage Users':
            self.ids.scrn_mngr.current = 'scrn_content'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'


class AdminApp(App):
    def build(self):

        return AdminWindow()


if __name__ == '__main__':
    AdminApp().run()
