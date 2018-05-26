#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 5/26/18

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

    state_file = '/home/pi/gitbucket/murmur/control/state.txt'
    Buttons = namedtuple('Buttons', ['start', 'pause', 'stop', 'exit'])

    def __init__(self, **kwargs):
        super(ButtonsLayout, self).__init__(**kwargs)
        self.logger = self._initialize_logger()
        self.button_props = self._setup_buttons()
        self.buttons = self.Buttons(*self._make_buttons())
        self.state = 'pause'
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
                'disabled': False,
                'on_press': self.pressed
            },
            'pause': {
                'type': ToggleButton,
                'color': [0.7, 0.7, 0.7, 1],
                'disabled': True,
                'on_press': self.pressed
            },
            'stop': {
                'type': Button,
                'color': [0.88, 0.2, 0.2, 1],
                'disabled': True,
                'on_press': self.pressed
            },
            'exit': {
                'type': Button,
                'color': [0.88, 0.2, 0.2, 1],
                'disabled': False,
                'on_press': self.exit
            }
        }

        return button_props

    def _make_button(self, text):
        button = self.button_props[text]['type'](text=text.upper(), font_size=30, bold=True, background_normal='', background_color=self.button_props[text]['color'])
        button.bind(on_press=self.button_props[text]['on_press'])
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

    def _reset_pause_text(self):
        self.buttons.pause.text = 'PAUSE'
        self.logger.info("reset PAUSE button text to 'PAUSE'")

    def _set_disabled(self, button):
        bttn_txt = 'pause' if button.text == 'RESUME' else button.text.lower()
        button.disabled = self.button_props[bttn_txt]['disabled']

    def _flip_disableds(self):
        for key in ['start', 'pause', 'stop']:
            key = 'pause' if key == 'resume' else key
            self.button_props[key]['disabled'] = not self.button_props[key]['disabled']
            self._set_disabled(getattr(self.buttons, key))

    def _log_press(self, txt):
        self.logger.info('{} button pressed'.format(txt))

    def initialize_disabled(self, button, dt):
        '''according to kivy, 'dt' stands for 'deltatime' and is needed for a Clock callback'''
        self._set_disabled(button)

    def pressed(self, instance):
        '''
        initially tried sending socket messages using our send.py module, i.e.:
        self.sender.send_msg('127.0.0.1', instance.text)

        this code works fine, but so far unable to implement it concurrently in main.py
        '''
        txt = instance.text
        self._log_press(txt)
        self._update_state(txt)

        if txt in ['PAUSE', 'RESUME']:
            self._change_text(txt)
        else:
            self._flip_disableds()
            if txt == 'STOP':
                self._reset_pause_text()

    def exit(self, instance):
        '''callback method for exit button to shut down the app'''
        self._log_press(instance.text)
        App.get_running_app().stop()


class ButtonsApp(App):

    def build(self):
        layout = ButtonsLayout(cols=3, rows=2, rows_minimum={0: 380, 1: 50}, spacing=20, padding=20)

        # Make the background gray:
        with layout.canvas.before:
            Color(.2, .2, .2, 1)
            self.rect = Rectangle(size=(800, 480), pos=layout.pos)

            for button in layout.buttons:
                layout.add_widget(button)

                # since creating a button with disabled = True in ButtonsLayout didn't work,
                # we schedule disabled to be set in the future after build returns
                # partial is used since the function itself must be passed as an argument
                Clock.schedule_once(partial(layout.initialize_disabled, button), 0.1)

        return layout


if __name__ == '__main__':
    ButtonsApp().run()
