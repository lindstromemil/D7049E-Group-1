
import InputListener
import queue

class InputManager:
    def __init__(self):
        self.inputs = queue.Queue()
        self.InputListener = InputListener(self.inputs)

    def get_inputs(self):
        while not self.inputs.empty:
            event = self.inputs.get()
            #handle event or send it to right part
      