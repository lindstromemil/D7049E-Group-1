from communication.messageHandling import MessageHandling
from communication.message import Message
import time
import logging

from communication.bullet import Bullet
from audio_module.audioHandeler import Sound
from input_module.inputManager import InputListener
from physics.physics import Physics
import threading

from concurrent.futures import ThreadPoolExecutor

def main():

    message_handler = MessageHandling()

    messaging_pool = ThreadPoolExecutor()
    messaging_pool.submit(message_handler.handle_messages)

    logger = logging.getLogger()


    bullet = Bullet()

    #sound = Sound('audio_module\\Sounds\\')
    #message_handler.add_component(sound)

    physics_engine = Physics()

    physics_pool = ThreadPoolExecutor()
    physics_pool.submit(physics_engine.setup)

    input_manager = InputListener(physics_engine.id)

    listner_pool = ThreadPoolExecutor()
    listner_pool.submit(input_manager.mouse)
    #listner_pool.submit(input_manager.keyboard)

    message_handler.add_component(bullet)
    message_handler.add_component(input_manager)
    message_handler.add_component(physics_engine)


    #physicsEngine.start()
    
    #message = Message("object", sound.id, "explode")
    #while True:
        #pass
        #logger.info("hej")
        #time.sleep(1)
        #message_handler.add_message(message)


if __name__ == "__main__":
    main()


