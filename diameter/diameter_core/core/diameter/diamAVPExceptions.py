##
## @brief      Support classes that defines Custom Exceptions
## 
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##

class AVPParametersException(Exception):
    def __init__(self, value):
        self.message = value
        
    def __str__(self):
        return repr(self.message)
        
class UnaccettableVendorIDException(Exception):
    def __init__(self, value):
        self.message = value
        
    def __str__(self):
        return repr(self.message)
        
class InvalidAVPLengthException(Exception):
    def __init__(self, value):
        self.message = value
        
    def __str__(self):
        return repr(self.message)
        
class InvalidAVPValueException(Exception):
    def __init__(self, value):
        self.message = value
        
    def __str__(self):
        return repr(self.message)
        
class MissingMandatoryAVPException(Exception):
    def __init__(self, value):
        self.message = value
        
    def __str__(self):
        return repr(self.message)
        
class InvalidAddressTypeException(Exception):
    def __init__(self, value):
        self.message = value
        
    def __str__(self):
        return repr(self.message)
    