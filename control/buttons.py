#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 1/27/18

import kivy
from kivy.app import App
from kivy.uix.button import Button


class ButtonsApp(App):

    def build(self):
        return Button(text='buttons')


if __name__ == '__main__':
    ButtonsApp().run()
