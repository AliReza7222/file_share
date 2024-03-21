""" file custom Exception for server file """


class BlockIPException(Exception):
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
