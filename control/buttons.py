#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 3/3/18

from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from functools import partial
from collections import namedtuple


class ButtonsLayout(GridLayout):

    state_file = 'state.txt'
    Buttons = namedtuple('Buttons', ['start', 'pause', 'stop'])

    def __init__(self, **kwargs):
        super(ButtonsLayout, self).__init__(**kwargs)
        self.logger = self._initialize_logger()
        self.button_props = self._setup_buttons()
        self.buttons = self.Buttons(*self._make_buttons())
        self.state = 'stop'
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
                'disabled': False
            },
            'pause': {
                'type': ToggleButton,
                'color': [0.7, 0.7, 0.7, 1],
                'disabled': True
            },
            'stop': {
                'type': Button,
                'color': [0.88, 0.2, 0.2, 1],
                'disabled': True
            }
        }

        return button_props

    def _make_button(self, text):
        button = self.button_props[text]['type'](text=text.upper(), background_normal='', background_color=self.button_props[text]['color'])
        button.bind(on_press=self.pressed)
        self.logger.info('{} button created'.format(text))

        return button

    def _make_buttons(self):
        return tuple(self._make_button(name) for name in self.Buttons._fields)

    def _write_state(self):
        self.logger.info("writing state '{}' to file".format(self.state))

        with open(self.state_file, 'w') as fyle:
            fyle.write('{}\n'.format(self.state))

    def _update_state(self, state):
        self.state = state.lower()
        self.logger.info("state updated to '{}'".format(self.state))
        self._write_state()

    def _change_text(self, text):
        self.buttons.pause.text = 'RESUME' if text == 'PAUSE' else 'PAUSE'
        self.logger.info("changed PAUSE button text to '{}'".format(self.buttons.pause.text))

    def _set_disabled(self, button):
        button.disabled = self.button_props[button.text.lower()]['disabled']

    def _flip_disableds(self):
        for key in self.button_props.keys():
            self.button_props[key]['disabled'] = not self.button_props[key]['disabled']
            self._set_disabled(getattr(self.buttons, key))

    def initialize_disabled(self, button, dt):
        '''according to kivy dt stands for 'deltatime' and is needed for a Clock callback'''

        self._set_disabled(button)

    def pressed(self, instance):
        '''
        initially tried sending socket messages using our send.py module, i.e.:
        self.sender.send_msg('127.0.0.1', instance.text)

        this code works fine, but so far unable to implement it concurrently in main.py
        '''

        txt = instance.text
        self.logger.info('{} button pressed'.format(txt))
        self._update_state(txt)

        if txt in ['PAUSE', 'RESUME']:
            self._change_text(txt)
        elif txt == 'START' or txt == 'STOP':
            self._flip_disableds()


class ButtonsApp(App):

    def build(self):
        layout = ButtonsLayout(cols=3, spacing=30, padding=30, row_default_height=150)

        # Make the background gray:
        with layout.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=(800, 600), pos=layout.pos)

            for button in layout.buttons:
                layout.add_widget(button)

                # since creating a button with disabled = True in ButtonsLayout didn't work,
                # we schedule disabled to be set in the future after build returns
                # partial is used since the function itself must be passed as an argument
                Clock.schedule_once(partial(layout.initialize_disabled, button), 0.1)

        return layout


if __name__ == '__main__':
    ButtonsApp().run()
