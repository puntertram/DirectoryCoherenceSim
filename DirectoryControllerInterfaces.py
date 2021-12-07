from InterconnectInterfaces import Interconnect 
from MemoryControllerInterfaces import MemoryController 
from MessageInterfaces import *
class DirectoryStateEntry:
    def __init__(self, address, data, state, dirty, sharers) -> None:
        self.address = address 
        self.data = data 
        self.state = state 
        self.dirty = dirty
        self.sharers = sharers 

class DirectoryController:
    def __init__(self, clock, memoryController: MemoryController) -> None:
        self.directoryState = {}
        self.clock = clock
        self.memoryController = memoryController

    def attachInterconnect(self, interconnect: Interconnect):
        self.interconnect = interconnect

    def onMessage(self, message: Message):
        if isinstance(message, GetSMessage):
            self.onGetS(message)
        elif isinstance(message, UnblockMessage):
            self.onUnblock(message)
        elif isinstance(message, GetMMessage):
            self.onGetM(message)
        else:
            print("Message type not identified!!!")

    def onGetM(self, message:GetMMessage):
        print(f"[Cycle {self.clock}] [Directory] {message}")
        try:
            directoryState = self.directoryState[message.address]
            self.interconnect.sendMessage(DataRespAckMessage(message.address, directoryState.data, len(directoryState.sharers), "Directory", message.source))
            for sharer in directoryState.sharers:
                self.interconnect.sendMessage(InvalidateMessage(message.address, message.source, "Directory", sharer))
            directoryState.state = 'B'

        except KeyError:
            data = self.memoryController.getData(message.address)
            self.directoryState[message.address] = DirectoryStateEntry(message.address, data, 'M', True, set([message.source]))
            self.interconnect.sendMessage(DataRespStoreMessage(message.address, data, "Directory", message.source))


    def onGetS(self, message:GetSMessage):
        print(f"[Cycle {self.clock}] [Directory] {message}")
        try:
            directoryState = self.directoryState[message.address]
            if directoryState.state == 'M':
                # Exactly one core is holding the address block in the modified state 
                # we forward the message there 
                assert len(directoryState.sharers) == 1, "There cannot be more than 1 cores that hold the cache block in modified state."

                self.interconnect.sendMessage(FwdGetSMessage(message.address, message.source, "Directory", list(directoryState.sharers)[0]))
                directoryState.state = 'B'
        except KeyError:
            # Get the item from the main memory
            data = self.memoryController.getData(message.address) # Memory operation has latency of 0 cycles!!!
            self.directoryState[message.address] = DirectoryStateEntry(message.address, data, 'S', False, set([message.source]))
            self.interconnect.sendMessage(DataRespLoadMessage(message.address, data, "Directory", message.source))

    def onUnblock(self, message: UnblockMessage):
        print(f"[Cycle {self.clock}] [Directory] {message}")
        self.directoryState[message.address].data = message.data
        self.directoryState[message.address].dirty = True 
        self.directoryState[message.address].state = 'S'
        self.directoryState[message.address].sharers.add(message.source)
    

