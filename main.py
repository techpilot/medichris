from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.text import LabelBase
import unittest

from admin.admin import AdminWindow
from signin.signin import SigninWindow
from till_operator.till_operator import OperatorWindow

LabelBase.register(name="Pacifico",
                   fn_regular="Pacifico.ttf"
                   )

LabelBase.register(name="Amita-bold",
                   fn_regular="amita-bold.ttf"
                   )

LabelBase.register(name="Opensans",
                   fn_regular="OpenSans-Regular.ttf"
                   )

LabelBase.register(name="alpha",
                   fn_regular="alpha_echo.ttf"
                   )

LabelBase.register(name="amerika",
                   fn_regular="AMERSN_.ttf"
                   )


class MainWindow(BoxLayout):

    admin_widget = AdminWindow()
    signin_widget = SigninWindow()
    operator_widget = OperatorWindow()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)


class MainApp(App):
    def build(self):

        return MainWindow()


if __name__ == '__main__':
    MainApp().run()
    # unittest.main()
