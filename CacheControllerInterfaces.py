from InterconnectInterfaces import Interconnect
from MessageInterfaces import *

class StoreQueueEntry:
    def __init__(self, age, data, address) -> None:
        self.age = age 
        self.data = data 
        self.address = address



class LoadQueueEntry:
    def __init__(self, age, address) -> None:
        self.age = age 
        self.address = address


class CacheStateEntry:
    def __init__(self, address, data, state) -> None:
        self.address = address 
        self.data = data 
        self.state = state
 

class CacheController:
    def __init__(self, identifier, clock) -> None:
        self.cacheState = {}
        self.identifier = identifier
        self.loadQueue = []
        self.storeQueue = []
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
            self.onDataRespStore(message)
        
        
        
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
        self.cacheState[message.address].data = self.storeQueue[0].data
        self.cacheState[message.address].state = 'M'
        self.state = 'READY'
        # delete the entry of the oldest pending store as it is successfully processed.
        del self.storeQueue[0]
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
            self.storeQueue.append(StoreQueueEntry(self.clock.counter, data, address))
            self.state = 'BUSY'
