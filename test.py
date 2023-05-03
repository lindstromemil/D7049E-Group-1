from communication.messageHandling import MessageHandling
from communication.message import Message
import time
import logging

from communication.bullet import Bullet
#from input_module.inputManager import InputListener

def main():
    message_handler = MessageHandling()
    logger = logging.getLogger()


    bullet = Bullet()

    #input_manager = InputListener()

    message_handler.add_component(bullet)
    #message_handler.add_component(input_manager)
    
    #message = Message("object", 0, "explode")
    while True:
        pass
        # logger.info("hej")
        # time.sleep(1)
        # message_handler.add_message(message)


if __name__ == "__main__":
    main()


