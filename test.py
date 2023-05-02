from communication.messageHandling import MessageHandling
from communication.message import Message
import time
import logging

from communication.bullet import Bullet
from communication.component import Component

def main():
    message_handler = MessageHandling()
    logger = logging.getLogger()

    bullet = Bullet()

    message_handler.add_component(Component(1, bullet))
    
    message = Message("object", 1, "explode")
    while True:
        logger.info("hej")
        time.sleep(1)
        message_handler.add_message(message)


if __name__ == "__main__":
    main()



# ------------------Events------------------



# Input Manager
class OnPressed():
    def __init__(self, key):
        self.key = key
class OnClick():
    def __init__(self, xcord, ycord, button):
        self.xcord = xcord
        self.ycord = ycord
        self.button = button
class MouseMoved():
    def __init__(self, xcord, ycord):
        self.xcord = xcord
        self.ycord = ycord


