#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 2/10/18

from kivy.app import App
from kivy.uix.button import Button


class ButtonsApp(App):

    def _make_button(self, text, callback):
        button = Button(text=text)
        button.bind(on_press=callback)

        return button

    def callback(self, instance):
        print('button {} pressed'.format(instance.text))

    def build(self):
        button = self._make_button('buttons', self.callback)

        return button


if __name__ == '__main__':
    ButtonsApp().run()
