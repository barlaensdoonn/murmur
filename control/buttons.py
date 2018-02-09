#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 2/9/18

import kivy
from kivy.app import App
from kivy.uix.button import Button


class ButtonsApp(App):

    def callback(self):
        print('button pressed')

    def build(self):
        button = Button(text='buttons')
        button.bind(on_press=self.callback)

        return button


if __name__ == '__main__':
    ButtonsApp().run()
