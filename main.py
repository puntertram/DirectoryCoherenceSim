from MemoryControllerInterfaces import MemoryController
from ClockInterfaces import Clock 
from DirectoryControllerInterfaces import DirectoryController
from CacheControllerInterfaces import CacheController
from InterconnectInterfaces import Interconnect



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

        



