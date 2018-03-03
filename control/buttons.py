#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 3/2/18

import sys
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle


class ButtonsLayout(GridLayout):

    state_file = 'state.txt'

    def __init__(self, **kwargs):
        super(ButtonsLayout, self).__init__(**kwargs)
        self.logger = self._initialize_logger()
        self.button_props = self._setup_buttons()
        self.start_button = self._make_button('start')
        self.pause_button = self._make_button('pause')
        self.stop_button = self._make_button('stop')
        self.state = 'start'
        self._write_state()

    def _initialize_logger(self):
        Logger.info('* * * * * * * * * * * * * * * * * * * *')
        Logger.info('kivy logger instantiated')

        return Logger

    def _setup_buttons(self):
        '''setup button properties'''

        button_props = {
            'start': {
                'type': Button,
                'color': [0.2, 0.8, 0.2, 1],
                'callback': self.pressed
            },
            'pause': {
                'type': ToggleButton,
                'color': [0.7, 0.7, 0.7, 1],
                'callback': self.change_text
            },
            'stop': {
                'type': Button,
                'color': [0.88, 0.2, 0.2, 1],
                'callback': self.pressed
            }
        }

        return button_props

    def _make_button(self, text):
        button = self.button_props[text]['type'](text=text.upper(), background_normal='', background_color=self.button_props[text]['color'])
        button.bind(on_press=self.button_props[text]['callback'])
        self.logger.info('{} button created'.format(text))

        return button

    def _write_state(self):
        self.logger.info("writing state '{}' to file".format(self.state))

        with open(self.state_file, 'w') as fyle:
            fyle.write('{}\n'.format(self.state))

    def pressed(self, instance):
        '''
        initially tried sending socket messages using our send.py module, i.e.:
        self.sender.send_msg('127.0.0.1', instance.text)

        this code works fine, but so far unable to implement it concurrently in main.py
        '''

        self.logger.info('{} button pressed'.format(instance.text))
        self.state = instance.text.lower()
        self.logger.info("set state to '{}'".format(self.state))
        self._write_state()

        if instance.text == 'STOP':
            sys.exit()

    def change_text(self, instance):
        self.pressed(instance)
        self.pause_button.text = 'RESUME' if instance.text == 'PAUSE' else 'PAUSE'


class ButtonsApp(App):

    def build(self):
        layout = ButtonsLayout(cols=3, spacing=30, padding=30, row_default_height=150)

        # Make the background gray:
        with layout.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=(800, 600), pos=layout.pos)

            layout.add_widget(layout.start_button)
            layout.add_widget(layout.pause_button)
            layout.add_widget(layout.stop_button)

            return layout


if __name__ == '__main__':
    ButtonsApp().run()
