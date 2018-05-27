#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 5/26/18

from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
import subprocess
from functools import partial
from collections import namedtuple


class ButtonsLayout(FloatLayout):

    state_file = '/home/pi/gitbucket/murmur/control/state.txt'
    Buttons = namedtuple('Buttons', ['start', 'pause', 'stop', 'exit'])

    def __init__(self, **kwargs):
        super(ButtonsLayout, self).__init__(**kwargs)
        self.logger = self._initialize_logger()
        self.popup_buttons = self._setup_popup_buttons()
        self.popup = self._setup_popup()
        self.button_props = self._setup_buttons()
        self.buttons = self.Buttons(*self._make_buttons())
        self.state = 'pause'
        self._write_state()

    def _initialize_logger(self):
        Logger.info('* * * * * * * * * * * * * * * * * * * *')
        Logger.info('kivy logger instantiated')

        return Logger

    def _setup_popup_buttons(self):
        font_size = 20

        popup_buttons = {
            'hello': {
                'button': Button(text='EXIT APP', font_size=font_size),
                'on_press': self._exit_app
            },
            'goodbye': {
                'button': Button(text='REBOOT', font_size=font_size),
                'on_press': self._reboot
            },
            'whatever': {
                'button': Button(text='SHUTDOWN', font_size=font_size),
                'on_press': self._shutdown
            }
        }

        return popup_buttons

    def _setup_popup(self):
        '''
        according to kivy the popup is a special type of widget, so we just
        instantiate it here and don't need to add it to the layout in ButtonsApp
        '''
        box = BoxLayout(orientation='vertical', padding=5, spacing=10)
        for button in self.popup_buttons.keys():
            box.add_widget(self.popup_buttons[button]['button'])

        content = box
        popup = Popup(title='what do you mean by exit', content=content, size_hint=(None, None), size=(400, 400))

        for button in self.popup_buttons.keys():
            self.popup_buttons[button]['button'].bind(on_press=self.popup_buttons[button]['on_press'])

        return popup

    def _setup_buttons(self):
        '''
        setup button properties. 'size_hint' is a tuple formatted (x, y)
        where x and y are each a percentage that specifies how much space
        the button should use in each axis. 'pos' indicates where it is
        positioned in the layout, with (0, 0) being the bottom left corner.
        '''
        size_hint_trio = (0.29, 0.75)
        center_y_trio = 0.425

        button_props = {
            'start': {
                'type': Button,
                'color': [0.2, 0.8, 0.2, 1],
                'size_hint': size_hint_trio,
                'pos_hint': {'center_x': 0.175, 'center_y': center_y_trio},
                'disabled': False,
                'on_press': self.pressed
            },
            'pause': {
                'type': ToggleButton,
                'color': [0.7, 0.7, 0.7, 1],
                'size_hint': size_hint_trio,
                'pos_hint': {'center_x': 0.5, 'center_y': center_y_trio},
                'disabled': True,
                'on_press': self.pressed
            },
            'stop': {
                'type': Button,
                'color': [0.88, 0.2, 0.2, 1],
                'size_hint': size_hint_trio,
                'pos_hint': {'center_x': 0.825, 'center_y': center_y_trio},
                'disabled': True,
                'on_press': self.pressed
            },
            'exit': {
                'type': Button,
                'color': [0.88, 0.2, 0.2, 1],
                'size_hint': (0.1, 0.1),
                'pos_hint': {'center_x': 0.1, 'center_y': 0.9},
                'disabled': False,
                'on_press': self.popup.open
            }
        }

        return button_props

    def _make_button(self, text):
        button = self.button_props[text]['type'](
            text=text.upper(), font_size=30, bold=True, size_hint=self.button_props[text]['size_hint'],
            pos_hint=self.button_props[text]['pos_hint'], background_normal='', background_color=self.button_props[text]['color']
        )
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

    def _exit_app(self, instance):
        '''callback method for exit button to shut down the app'''
        self._log_press(instance.text)
        App.get_running_app().stop()

    def _reboot(self, instance):
        self._log_press(instance.text)
        subprocess.run(['sudo', 'reboot'])

    def _shutdown(self, instance):
        self._log_press(instance.text)
        subprocess.run(['sudo', 'halt'])

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


class ButtonsApp(App):

    def build(self):
        layout = ButtonsLayout(size=(800, 480))

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
