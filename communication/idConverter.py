

class IdConverter():
    def __init__(self):
        self.current = {}
        self.universal = {}

    def add_ids(self, current, universal):
        self.current[current] = universal
        self.universal[universal] = current

    def get_universal_id(self, current_id):
        return self.current[current_id]
    
    def get_current_id(self, universal_id):
        return self.universal[universal_id]
    
    def get_all_current_ids(self):
        return list(self.current.items())
    
    def delete_current_id(self, current):
        self.current.pop(self.universal.pop(self.current[current]))

    def delete_universal_id(self, universal):
        self.universal.pop(self.current.pop(self.universal[universal]))