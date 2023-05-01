from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

import queue

class InputListener:
    def __init__(self, queue):
        self.queue = queue

    def addToQueue(self, key):
        self.queue.put(key)

    def on_press(key):
        try:
            print('key {0} pressed'.format(key))
        except AttributeError:
            print('special key {0} pressed'.format(key))

    def on_release(key):
        print('{0} released'.format(key))

    def on_move(x, y):
        print("Mouse moved to ({0} : {1})".format(x, y))

    def on_click(x, y, button, pressed):
        if pressed:
            print("{0} clicked at ({1} : {2})".format(button, x, y))

    def on_scroll(x, y, dx, dy):
        print("Mouse scrolled at ({0} : {1}) ({2} : {3})".format(x, y, dx, dy))

    keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
    mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()
