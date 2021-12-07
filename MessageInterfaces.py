class Message:
    def __init__(self, type, source, destination) -> None:
        self.type = type 
        self.source = source 
        self.destination = destination



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

   


