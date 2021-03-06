#!/usr/bin/python3
# murmur - touch buttons
# 1/27/18
# updated: 6/17/18

from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
import subprocess
from functools import partial, wraps
from collections import namedtuple


# NOTE: this decorator is not currently working, just here for reference
def log_press(func):
    '''decorator to log which button is pressed from its callback method'''
    @wraps(func)
    def wrapper(self, instance):
        self.logger.info('{} button pressed'.format(instance.text))
        func(self)

    return wrapper


class ButtonsLayout(FloatLayout):

    state_file = '/home/pi/gitbucket/murmur/control/state.txt'
    Buttons = namedtuple('Buttons', ['start', 'pause', 'shutdown', 'exit'])
    hosts = ['pi@murmur01.local', 'pi@murmur02.local', 'pi@murmur03.local', 'pi@murmur04.local']

    def __init__(self, **kwargs):
        super(ButtonsLayout, self).__init__(**kwargs)
        self.logger = self._initialize_logger()
        self.exit_popup_buttons = self._setup_exit_popup_buttons()
        self.exit_popup = self._setup_exit_popup()
        self.start_popup_content = self._setup_start_popup_content()
        self.start_popup = self._setup_start_popup()
        self.shutdown_popup_content = self._setup_shutdown_popup_content()
        self.shutdown_popup = self._setup_shutdown_popup()
        self.button_props = self._setup_buttons()
        self.buttons = self.Buttons(*self._make_buttons())
        self.state = 'pause'
        self._write_state()

    def _initialize_logger(self):
        Logger.info('* * * * * * * * * * * * * * * * * * * *')
        Logger.info('kivy logger instantiated')

        return Logger

    def _setup_exit_popup_buttons(self):
        font_size = 20

        return {
            'exit': {
                'button': Button(text='EXIT APP', font_size=font_size),
                'on_press': self._exit_app
            },
            'reboot': {
                'button': Button(text='REBOOT', font_size=font_size),
                'on_press': self._reboot
            },
            'shutdown': {
                'button': Button(text='SHUTDOWN', font_size=font_size),
                'on_press': self._shutdown
            },
            'reboot_all': {
                'button': Button(text='REBOOT ALL', font_size=font_size),
                'on_press': self._boot_all
            },
            'shutdown_all': {
                'button': Button(text='SHUTDOWN ALL', font_size=font_size),
                'on_press': self._boot_all
            },
        }

    def _setup_start_popup_content(self):
        return {
            'button': {
                'button': Button(text='CONFIRM BLOCKS OUT', font_size=35),
                'on_press': self.pressed
            },
            'text': {
                'text': Label(text='confirm once blocks are removed from arms B, D, F, H, K, and M', font_size=20)
            }
        }

    def _setup_shutdown_popup_content(self):
        return {
            'button': {
                'button': Button(text='CONFIRM BLOCKS IN', font_size=35),
                'on_press': self.pressed
            },
            'text': {
                'text': Label(text='confirm once blocks are placed in arms B, D, F, H, K, and M', font_size=20)
            }
        }

    def _setup_exit_popup(self):
        '''
        according to kivy the popup is a special type of widget, so we just
        instantiate it here and don't need to add it to the layout in ButtonsApp
        '''
        box = BoxLayout(orientation='vertical', padding=5, spacing=10)
        for button in self.exit_popup_buttons.keys():
            box.add_widget(self.exit_popup_buttons[button]['button'])

        content = box
        exit_popup = Popup(title='touch outside this popup to cancel', content=content, size_hint=(None, None), size=(400, 460))

        for button in self.exit_popup_buttons.keys():
            self.exit_popup_buttons[button]['button'].bind(on_press=self.exit_popup_buttons[button]['on_press'])

        return exit_popup

    def _setup_start_popup(self):
        '''
        according to kivy the popup is a special type of widget, so we just
        instantiate it here and don't need to add it to the layout in ButtonsApp
        '''
        box = BoxLayout(orientation='vertical', padding=5, spacing=10)
        box.add_widget(self.start_popup_content['text']['text'])
        box.add_widget(self.start_popup_content['button']['button'])
        self.start_popup_content['button']['button'].bind(on_press=self.start_popup_content['button']['on_press'])

        content = box
        start_popup = Popup(title='initialize', content=content, size_hint=(None, None), size=(640, 260))

        return start_popup

    def _setup_shutdown_popup(self):
        '''
        according to kivy the popup is a special type of widget, so we just
        instantiate it here and don't need to add it to the layout in ButtonsApp
        '''
        box = BoxLayout(orientation='vertical', padding=5, spacing=10)
        box.add_widget(self.shutdown_popup_content['text']['text'])
        box.add_widget(self.shutdown_popup_content['button']['button'])
        self.shutdown_popup_content['button']['button'].bind(on_press=self.shutdown_popup_content['button']['on_press'])

        content = box
        shutdown_popup = Popup(title='shutdown', content=content, size_hint=(None, None), size=(600, 260))

        return shutdown_popup

    def _setup_buttons(self):
        '''
        setup button properties. 'size_hint' is a tuple formatted (x, y)
        where x and y are each a percentage that specifies how much space
        the button should use in each axis. 'pos' indicates where it is
        positioned in the layout, with (0, 0) being the bottom left corner.
        '''
        size_hint_trio = (0.29, 0.75)
        center_y_trio = 0.425

        buttons = {
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
            'shutdown': {
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
                'on_press': self.exit_popup.open
            }
        }

        return buttons

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
        for key in ['start', 'pause', 'shutdown']:
            key = 'pause' if key == 'resume' else key
            self.button_props[key]['disabled'] = not self.button_props[key]['disabled']
            self._set_disabled(getattr(self.buttons, key))

    def _log_press(self, instance):
        self.logger.info('{} button pressed'.format(instance.text))

    def _exit_app(self, instance):
        '''callback method for exit button to shut down the app'''
        self._log_press(instance)
        App.get_running_app().stop()

    def _reboot(self, instance):
        self._log_press(instance)
        subprocess.run(['sudo', 'reboot'])

    def _boot_all(self, instance):
        '''handle both reboot all and shutdown all popup button presses'''
        self._log_press(instance)
        action = 'reboot' if 'reboot' in instance.text.lower() else 'halt'

        # run action on the nodes via ssh
        for host in self.hosts:
            subprocess.run(['ssh', host, 'sudo', action])

        # run the action locally
        subprocess.run(['sudo', action])

    def _shutdown(self, instance):
        self._log_press(instance)
        subprocess.run(['sudo', 'halt'])

    def initialize_disabled(self, button, dt):
        '''according to kivy, 'dt' stands for 'deltatime' and is needed for a Clock callback'''
        self._set_disabled(button)

    def pressed(self, instance):
        '''
        initially tried sending socket messages using our send.py module, i.e.:
        self.sender.send_msg('127.0.0.1', instance.text)
        this code works fine, but so far unable to implement a listener concurrently in main.py

        instead we write the state to a file that the watchdog module is monitoring.
        '''
        self._log_press(instance)
        txt = instance.text
        self._update_state(txt)

        if txt in ['PAUSE', 'RESUME']:
            self._change_text(txt)
        elif txt in ['START', 'SHUTDOWN']:
            self._flip_disableds()
            if txt == 'START':
                self.start_popup.open()
            elif txt == 'SHUTDOWN':
                self._reset_pause_text()
                self.shutdown_popup.open()
        elif txt == 'CONFIRM BLOCKS OUT':
            self.start_popup.dismiss()
        elif txt == 'CONFIRM BLOCKS IN':
            self.shutdown_popup.dismiss()


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
                # we schedule disabled to be set in the future after build returns.
                # partial is used since the function itself must be passed as an argument
                Clock.schedule_once(partial(layout.initialize_disabled, button), 0.1)

        return layout


if __name__ == '__main__':
    ButtonsApp().run()
