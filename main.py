from MemoryController import MemoryController
class Message:
    def __init__(self, type, source, destination) -> None:
        self.type = type 
        self.source = source 
        self.destination = destination

class Clock:
    def __init__(self) -> None:
        self.counter = 0
    
    def tick(self):
        self.counter += 1
    
    def __str__(self) -> str:
        return f"{self.counter}"

class GetSMessage(Message):
    def __init__(self, address, source, destination) -> None:
        super().__init__(type="GetS", source=source, destination=destination)
        self.address = address
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, source={self.source}, destination={self.destination}>"

class AckMessage(Message):
    def __init__(self, address, source, destination) -> None:
        super().__init__(type="Ack", source=source, destination=destination)
        self.address = address
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, source={self.source}, destination={self.destination}>"

class GetMMessage(Message):
    def __init__(self, address, source, destination) -> None:
        super().__init__(type="GetM", source=source, destination=destination)
        self.address = address
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, source={self.source}, destination={self.destination}>"

class DataRespAckMessage(Message):
    def __init__(self, address, ack, source, destination) -> None:
        super().__init__(type="DataRespAck", source=source, destination=destination)
        self.address = address
        self.ack = ack
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, ack = {self.ack} source={self.source}, destination={self.destination}>"

class InvalidateMessage(Message):
    def __init__(self, address, requester, source, destination) -> None:
        super().__init__(type="Invalidate", source=source, destination=destination)
        self.address = address
        self.requester = requester
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, requester = {self.requester} source={self.source}, destination={self.destination}>"


class FwdGetSMessage(Message):
    def __init__(self, address, requester, source, destination) -> None:
        super().__init__(type="FwdGetS", source=source, destination=destination)
        self.address = address
        self.requester = requester
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, requester={self.requester}, source={self.source}, destination={self.destination}>"

class DataRespMessage(Message):
    def __init__(self, address, data, source, destination) -> None:
        super().__init__(type="DataResp", source=source, destination=destination)
        self.address = address
        self.data = data      
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, data={self.data}, source={self.source}, destination={self.destination}>"

class DataRespLoadMessage(Message):
    def __init__(self, address, data, source, destination) -> None:
        super().__init__(type="DataRespLoad", source=source, destination=destination)
        self.address = address
        self.data = data      
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, data={self.data}, source={self.source}, destination={self.destination}>"

class DataRespStoreMessage(Message):
    def __init__(self, address, data, source, destination) -> None:
        super().__init__(type="DataRespStore", source=source, destination=destination)
        self.address = address
        self.data = data      
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, data={self.data}, source={self.source}, destination={self.destination}>"


class UnblockMessage(Message):
    def __init__(self, address, data, source, destination) -> None:
        super().__init__(type="Unblock", source=source, destination=destination)
        self.address = address
        self.data = data
    def __str__(self) -> str:
        return f"<{self.type}Message address={self.address}, data={self.data}, source={self.source}, destination={self.destination}>"

class CacheStateEntry:
    def __init__(self, address, data, state) -> None:
        self.address = address 
        self.data = data 
        self.state = state
    
class DirectoryStateEntry:
    def __init__(self, address, data, state, dirty, sharers) -> None:
        self.address = address 
        self.data = data 
        self.state = state 
        self.dirty = dirty
        self.sharers = sharers 

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
    

         
        
        




class CacheController:
    def __init__(self, identifier, clock) -> None:
        self.cacheState = {}
        self.identifier = identifier
        self.loadQueue = {}
        self.storeQueue = {}
        self.clock = clock
        self.ackQueue = {}
        self.state = 'READY'

    def attachInterconnect(self, interconnect: Interconnect):
        self.interconnect = interconnect


    def onMessage(self, message: Message):
        if isinstance(message, FwdGetSMessage):
            self.onFwdGetS(message)
        elif isinstance(message, DataRespMessage):
            self.onDataResp(message)
        elif isinstance(message, InvalidateMessage):
            self.onInvalidate(message)
        elif isinstance(message, AckMessage):
            self.onAck(message)
        elif isinstance(message, DataRespLoadMessage):
            self.onDataRespLoad(message)
        elif isinstance(message, DataRespStoreMessage):
            self.onDataRespLoad(message)
        
        
        
    def onInvalidate(self, message:InvalidateMessage):
        print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] {message}")
        assert message.address in self.cacheState.keys(), f"{message.address} must be present in the cache."
        self.cacheState.pop(message.address)
        self.interconnect.sendMessage(AckMessage(message.address, self.identifier, message.requester))

    def onAck(self, message:AckMessage):
        print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] {message}")
        try:
            self.ackQueue[message.address] -= 1
        except KeyError:
            print(f"{message.address} must be present in the ack queue")
            exit(-1)
        if self.ackQueue[message.address] == 0:
            self.ackQueue.pop(message.address)
            self.cacheState[message.address].state = 'M'


    def loadData(self, address):
        if self.state == 'BUSY':
            print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] loadData {address} cannot be processed")
            return None 
        
        print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] loadData {address}")
        try:
            data = self.cacheState[address].data
        except KeyError:
            # address does not exist in the cache; get it from the directory
            self.interconnect.sendMessage(GetSMessage(address, self.identifier, "Directory"))
            self.cacheState[address] = CacheStateEntry(address, 'X', 'IS')
            self.state = 'BUSY'

    def onFwdGetS(self, message:FwdGetSMessage):
        print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] {message}")
        self.interconnect.sendMessage(DataRespMessage(message.address, self.cacheState[message.address].data, self.identifier, message.requester))

    def onDataRespLoad(self, message:DataRespLoadMessage):
        print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] {message}")
        self.cacheState[message.address].address = message.address
        self.cacheState[message.address].data = message.data
        self.cacheState[message.address].state = 'S'
        self.state = 'READY'
        # self.interconnect.sendMessage(UnblockMessage(message.address, message.data, self.identifier, "Directory"))

    def onDataRespStore(self, message:DataRespLoadMessage):
        print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] {message}")
        self.cacheState[message.address].address = message.address
        self.cacheState[message.address].data = message.data
        self.cacheState[message.address].state = 'M'
        self.state = 'READY'
        # self.interconnect.sendMessage(UnblockMessage(message.address, message.data, self.identifier, "Directory"))


    def onDataResp(self, message:DataRespMessage):
        print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] {message}")
        self.cacheState[message.address].address = message.address
        self.cacheState[message.address].data = message.data
        self.cacheState[message.address].state = 'S'
        self.state = 'READY'
        self.interconnect.sendMessage(UnblockMessage(message.address, message.data, self.identifier, "Directory"))



    def storeData(self, address, data):
        if self.state == 'BUSY':
            print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] storeData at {address}, data = {data} cannot be processed")
            return None 
        print(f"[Cycle {self.clock}] [CacheController {self.identifier} {self.state}] storeData at {address}, data = {data}")
        try:
            cacheBlockState = self.cacheState[address].state 
            if cacheBlockState == 'S':
                pass 
            else:
                pass 
        except KeyError:
            self.interconnect.sendMessage(GetMMessage(address, self.identifier, "Directory"))
            self.cacheState[address] = CacheStateEntry(address, 'X', 'IM')
            self.storeQueue[address] = data
            self.state = 'BUSY'


if __name__ == "__main__":
    clock = Clock()
    memoryController = MemoryController(clock)
    directoryController = DirectoryController(clock, memoryController)
    cacheController1 = CacheController("Core1", clock)
    cacheController2 = CacheController("Core2", clock)
    cacheController3 = CacheController("Core3", clock)
    
    interconnect = Interconnect(directoryController, [cacheController1, cacheController2], clock)
    while True:
        if clock.counter == 0:
            cacheController2.storeData(10, 500)
        elif clock.counter == 5:
            cacheController1.loadData(10)
        elif clock.counter == 10:
            cacheController3.storeData(10, 200)

        interconnect.nextCycle()
        choice = input("Continue?(Y)es/(N)o")
        if choice == 'N':
            exit(0)
        clock.tick()

        



