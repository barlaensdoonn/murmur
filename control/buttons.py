#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 2/10/18

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle


class ButtonsApp(App):

    def set_properties(self):
        '''hold button properties'''

        self.properties = {
            'start': {
                'color': [0.2, 0.8, 0.2, 1],
                'callback': self.callback
            },
            'pause': {
                'color': [0.7, 0.7, 0.7, 1],
                'callback': self.callback
            },
            'stop': {
                'color': [0.88, 0.2, 0.2, 1],
                'callback': self.callback
            }
        }

    def _make_button(self, text):
        button = Button(text=text.upper(), background_normal='', background_color=self.properties[text]['color'])
        button.bind(on_press=self.properties[text]['callback'])

        return button

    def callback(self, instance):
        print('button {} pressed'.format(instance.text))

    def build(self):
        # Set up the layout:
        layout = GridLayout(cols=3, spacing=30, padding=30, row_default_height=150)

        # Make the background gray:
        with layout.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=(800, 600), pos=layout.pos)

        # set button properties and make buttons
        self.set_properties()
        start_button = self._make_button('start')
        pause_button = self._make_button('pause')
        stop_button = self._make_button('stop')

        layout.add_widget(start_button)
        layout.add_widget(pause_button)
        layout.add_widget(stop_button)

        return layout


if __name__ == '__main__':
    ButtonsApp().run()
