import kivy
kivy.require('1.0.6')
from kivy.app import App
from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os

from login import Login
from registrar import Registrar
from connected import Connected

class Inicio(Screen):
    def do_inicio(self):
        app = App.get_running_app()

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'login'
    def do_registrar(self):
        app = App.get_running_app()

        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'registrar'


class InicioApp(App):

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Inicio(name='inicio'))
        manager.add_widget(Login(name='login'))
        manager.add_widget(Registrar(name='registrar'))
        manager.add_widget(Connected(name='connected'))

        return manager

if __name__ == '__main__':
    InicioApp().run()
