class Clock:
    def __init__(self) -> None:
        self.counter = 0
    
    def tick(self):
        self.counter += 1
    
    def __str__(self) -> str:
        return f"{self.counter}"