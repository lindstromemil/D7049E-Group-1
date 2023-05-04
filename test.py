from communication.messageHandling import MessageHandling
from communication.message import Message
import time
import logging

from communication.bullet import Bullet
from audio_module.audioHandeler import Sound
from input_module.inputManager import InputListener
from physics.physics import Physics

def main():
    message_handler = MessageHandling()
    logger = logging.getLogger()


    bullet = Bullet()

    #sound = Sound('audio_module\\Sounds\\')
    #message_handler.add_component(sound)

    physicsEngine = Physics()
    input_manager = InputListener(physicsEngine.id)
    
    message_handler.add_component(bullet)
    message_handler.add_component(input_manager)
    message_handler.add_component(physicsEngine)


    #physicsEngine.start()
    
    #message = Message("object", sound.id, "explode")
    while True:
        pass
        #logger.info("hej")
        #time.sleep(1)
        #message_handler.add_message(message)


if __name__ == "__main__":
    main()


