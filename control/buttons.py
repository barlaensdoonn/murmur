#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 2/9/18

import kivy
from kivy.app import App
from kivy.uix.button import Button


class Buttons(object):

    def __init__(self):
        self.button = self._make_button('buttons', self.callback)

    def _make_button(self, text, callback):
        button = Button(text=text)
        button.bind(on_press=callback)

        return button

    def callback(self, instance):
        print('button {} pressed'.format(instance.text))


class MainApp(App):

    def build(self):
        buttons = Buttons()

        return buttons.button


if __name__ == '__main__':
    MainApp().run()
