from random import randint
class MemoryController:
    
    def __init__(self, clock, ) -> None:
        self.clock = clock
        self.memoryState = {}

    def getData(self, address):
        try:
            return self.memoryState[address]
        except KeyError:
            self.memoryState[address] = randint(1, 1000)
            return self.memoryState[address]

    def storeData(self, address):
        self.memoryState[address] = randint(1, 1000)
        