from communication.messageHandling import MessageHandling
from communication.message import Message
import time
import logging

from communication.bullet import Bullet

def main():
    message_handler = MessageHandling()
    logger = logging.getLogger()

    bullet = Bullet()

    message_handler.add_component(bullet)
    
    message = Message("object", 0, "explode")
    while True:
        logger.info("hej")
        time.sleep(1)
        message_handler.add_message(message)


if __name__ == "__main__":
    main()


