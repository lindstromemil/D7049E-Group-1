from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

from communication.action import Action, OnClick, OnPressed, MouseMoved
from communication.messageHandling import MessageHandling
from communication.message import Message
from communication.bullet import Bullet
from threading import Thread

import queue

class InputListener(Action):
    def __init__(self):
        super().__init__()
        self.thread = Thread(target=self.start, daemon=True)
        self.thread.start()


    def on_press(self, key):
        MessageHandling().add_message(Message("inputManager", Bullet().id, OnPressed(key)))
        # try:
        #     print('key {0} pressed'.format(key))
        # except AttributeError:
        #     print('special key {0} pressed'.format(key))

    def on_release(self, key):
        print('{0} released'.format(key))

    def on_move(self, x, y):
        pass
        #MessageHandling().add_message(Message("inputManager", Bullet().id, MouseMoved(x, y)))
        #print("Mouse moved to ({0} : {1})".format(x, y))

    def on_click(self, x, y, button, pressed):
        if pressed:
            #Message.send_message("mouseClick", [x, y, button])
            MessageHandling().add_message(Message("inputManager", Bullet().id, OnClick(x, y, button)))
            #print("{0} clicked at ({1} : {2})".format(button, x, y))

    def on_scroll(self, x, y, dx, dy):
        print("Mouse scrolled at ({0} : {1}) ({2} : {3})".format(x, y, dx, dy))

    def start(self):
        print("Starting Keyboard and Mouse Listener.....")
        keyboard_listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)
        mouse_listener = MouseListener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll) 
        print("Keyboard and Mouse Listener setup complete")
        keyboard_listener.start()
        mouse_listener.start()
        keyboard_listener.join()
        mouse_listener.join()

    def do_action(self, action):
        print(f"event '{action}' was done in inputmanager!")



      