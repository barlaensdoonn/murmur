#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 2/11/18

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle


class ButtonsApp(App):

    def setup_buttons(self):
        '''setup button properties'''

        self.button_props = {
            'start': {
                'type': Button,
                'color': [0.2, 0.8, 0.2, 1],
                'callback': self.callback
            },
            'pause': {
                'type': ToggleButton,
                'color': [0.7, 0.7, 0.7, 1],
                'callback': self.change_text
            },
            'stop': {
                'type': Button,
                'color': [0.88, 0.2, 0.2, 1],
                'callback': self.callback
            }
        }

    def _make_button(self, text):
        button = self.button_props[text]['type'](text=text.upper(), background_normal='', background_color=self.button_props[text]['color'])
        button.bind(on_press=self.button_props[text]['callback'])

        return button

    def callback(self, instance):
        print('button {} pressed'.format(instance.text))

    def change_text(self, event):
        self.pause_button.text = 'RESUME' if event.text == 'PAUSE' else 'PAUSE'

    def build(self):
        # Set up the layout:
        layout = GridLayout(cols=3, spacing=30, padding=30, row_default_height=150)

        # Make the background gray:
        with layout.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=(800, 600), pos=layout.pos)

        # set button properties and make buttons
        self.setup_buttons()
        self.start_button = self._make_button('start')
        self.pause_button = self._make_button('pause')
        self.stop_button = self._make_button('stop')

        layout.add_widget(self.start_button)
        layout.add_widget(self.pause_button)
        layout.add_widget(self.stop_button)

        return layout


if __name__ == '__main__':
    ButtonsApp().run()
