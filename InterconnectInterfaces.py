from ClockInterfaces import Clock
from MessageInterfaces import Message

class Interconnect:
    def __init__(self, directoryController, cacheControllers, clock:Clock) -> None:
        self.channel = [] 
        self.clock = clock
        self.directoryController = directoryController
        self.directoryController.attachInterconnect(self)

        self.cacheControllerDict = {}
        for cacheController in cacheControllers:
            self.cacheControllerDict[cacheController.identifier] = cacheController
            cacheController.attachInterconnect(self)
        
    def sendMessage(self, message:Message):
        self.channel.append(message)

    def nextCycle(self):
        # run the operations in this cycle and move on to the next cycle 
        if len(self.channel) == 0:
            print(f"[Cycle {self.clock}] Channel empty.")
            return None 
        message = self.channel[0]
        
        print(f"[Cycle {self.clock}][Interconnect] Processing {message}")
        del self.channel[0]
        if message.destination == 'Directory':
            self.directoryController.onMessage(message)
        else:
            self.cacheControllerDict[message.destination].onMessage(message) 
        
