
class Message:
    def __init__(self, type, source, destination) -> None:
        self.type = type 
        self.source = source 
        self.destination = destination

class GetSMessage(Message):
    def __init__(self, address, source, destination) -> None:
        super().__init__(type="GetS", source=source, destination=destination)
        self.address = address

class FwdGetSMessage(Message):
    def __init__(self, address, requester, source, destination) -> None:
        super().__init__(type="FwdGetS", source=source, destination=destination)
        self.address = address
        self.requester = requester
        

class CacheStateEntry:
    def __init__(self, address, data, state) -> None:
        self.address = address 
        self.data = data 
        self.state = state
    
class DirectoryStateEntry:
    def __init__(self, address, data, state, sharers) -> None:
        self.address = address 
        self.data = data 
        self.state = state 
        self.sharers = sharers 

class Interconnect:
    def __init__(self, directoryController) -> None:
        self.channel = [] 
        self.clock = 0
        self.directoryController = directoryController
    
    def nextCycle(self):
        # run the operations in this cycle and move on to the next cycle 
        pass 
    


class DirectoryController:
    def __init__(self) -> None:
        self.directoryState = {}
    def attachInterConnect(self, interconnect: Interconnect):
        self.interconnect = interconnect
    def onGetS(self, message:GetSMessage):
        try:
            directoryState = self.directoryState[message.address]
            if directoryState.state == 'M':
                # Exactly one core is holding the address block in the modified state 
                # we forward the message there 
                self.interconnect.sendMessage(FwdGetSMessage(message.address, message.requester, "Directory"))
        except KeyError:
            pass 





class CacheController:
    def __init__(self, interconnect: Interconnect) -> None:
        self.cacheState = {}
        self.interconnect = interconnect
        self.loadQueue = []
        self.storeQueue = []
        self.clock = 0
        self.state = 'READY'

    def loadData(self, address):
        try:
            data = self.cacheState[address].data
        except KeyError:
            # address does not exist in the cache; get it from the directory
            self.interconnect.sendMessage(GetSMessage(address))
            self.cacheState[address] = CacheStateEntry(address, 'X', 'IS')
            self.state = 'BUSY'

    def storeData(self, address, data):
        try:
            cacheBlockState = self.cacheState.state 
            if cacheBlockState == 'S':
                pass 
            else:
                pass 
        except KeyError:
            pass 



        



