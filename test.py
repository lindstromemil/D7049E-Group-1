from communication.messageHandling import MessageHandling
from communication.message import Message
import time
import logging

from communication.bullet import Bullet
from audio_module.audioHandeler import Sound
from input_module.inputManager import InputListener
from physics.physics import Physics
from render_module.render import Render

from concurrent.futures import ThreadPoolExecutor


def main():

    setup = Render()
    setup.setup(setup)
    setup.run()

    #sound = Sound('audio_module\\Sounds\\')
    #message_handler.add_component(sound)

#     message_handler = MessageHandling()

#     messaging_pool = ThreadPoolExecutor()
#     messaging_pool.submit(message_handler.handle_messages)

#     physics_engine = Physics()

#     #physics_pool = ThreadPoolExecutor()
#     #physics_pool.submit(physics_engine.setup)
#     messaging_pool.submit(physics_engine.setup)

#     render_engine = Render()
#     #messaging_pool.submit(render_engine.setup)
#     #messaging_pool.submit(render_engine.run)
#     #render_engine.run()

#     input_manager = InputListener(physics_engine.id, render_engine.id)
#     #input_manager = InputListener(physics_engine.id, 1000000000)

#     #listner_pool = ThreadPoolExecutor()
#     messaging_pool.submit(input_manager.mouse)

#     message_handler.add_component(input_manager)
#     message_handler.add_component(physics_engine)
#     message_handler.add_component(render_engine)


#     messaging_pool.submit(loop, (physics_engine, input_manager))

#     render_engine.setup()
#     render_engine.run()


# def loop(physics_engine: Physics, input_manager: InputListener):
#     while True:
#         start = time.time()
#         #physics_engine.start()
#         physics_engine.start
#         input_manager.checkInput
#         print(max(1./60 - (time.time() - start), 0))
#         time.sleep(max(1./240 - (time.time() - start), 0))

if __name__ == "__main__":
    main()


