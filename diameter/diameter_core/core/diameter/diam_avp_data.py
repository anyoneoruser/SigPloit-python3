'''
Created on 08 ott 2015

@author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
'''
import logging
from codecs import getencoder, getdecoder
from xdrlib import Packer, Unpacker
import socket
import struct
from .diamAVPExceptions import *
from .diamAVP import DiamAVP
from _socket import inet_ntop
from datetime import datetime
from .diamAVPCodes import DiamAVPCodes
import time
from ..commons import logErr
logging.basicConfig(format='%(levelname)s:%(message)s')

''' GENERIC AVP messages '''

utf8encoder = getencoder("utf_8")
utf8decoder = getdecoder("utf_8")

def _pack(avps):
    p = Packer()
    for a in avps:
        a.encode(p)
    return p.get_buffer()

def _pack_address(address):
    addrs=socket.getaddrinfo(address, 0)
    for a in addrs:
        if a[0]==socket.AF_INET:
            raw = socket.inet_pton(socket.AF_INET,a[4][0]);
            return struct.pack("!h4s",1,raw)
        if a[0]==socket.AF_INET6:
            raw = socket.inet_pton(socket.AF_INET6,a[4][0]);
            return struct.pack("!h16s",2,raw)
    raise InvalidAddressTypeException()

class DiamAVP_Integer32(DiamAVP):
    """32-bit signed integer AVP."""
    
    def __init__(self, avp_code, data, vendor_id=0):
        DiamAVP.__init__(self,avp_code,struct.pack("!I", data),vendor_id)
    
    def getData(self):
        """Returns the payload as a 32-bit signed value."""
        return struct.unpack("!I",self.data)[0]
    
    def setData(self,data):
        """Sets the payload to the specified 32-bit signed value."""
        self.data = struct.pack("!I",data)
    
    def __str__(self):
        return self.str_prefix__() + "\t" + str(self.getData())

    def narrow(avp):
        """Convert generic AVP to AVP_Integer32
        Raises: InvalidAVPLengthException
        """
        if len(avp.payload)!=4:
            raise InvalidAVPLengthException(avp)
        data = struct.unpack("!I",avp.payload)[0]
        a = DiamAVP_Integer32(avp.avp_code, data, avp.vendor_id)
        a.flags = avp.flags
        return a
    
    narrow = staticmethod(narrow)

class DiamAVP_Integer64(DiamAVP):
    """64-bit signed integer AVP."""
    
    def __init__(self, avp_code, data, vendor_id=0):
        DiamAVP.__init__(self,avp_code,struct.pack("!Q", data),vendor_id)
    
    def getData(self):
        """Returns the payload as a 64-bit signed value."""
        return struct.unpack("!Q",self.data)[0]
    
    def setData(self,data):
        """Sets the payload to the specified 64-bit signed value."""
        self.data = struct.pack("!Q",data)
    
    def __str__(self):
        return self.str_prefix__() + "\t" + str(self.getData())

    def narrow(avp):
        """Convert generic AVP to AVP_Integer64
        Raises: InvalidAVPLengthException
        """
        if len(avp.payload)!=8:
            raise InvalidAVPLengthException(avp)
        data = struct.unpack("!Q",avp.payload)[0]
        a = DiamAVP_Integer64(avp.avp_code, data, avp.vendor_id)
        a.flags = avp.flags
        return a
    
    narrow = staticmethod(narrow)
  
class DiamAVP_Unsigned32(DiamAVP):
    """32-bit unsigned integer AVP.
    RFC3855 describes the Unsigned32 AVP type. Python does not have an
    appropriate unsigned data type, so this class is functionally
    equivalent to AVP_Integer32
    """
    
    def __init__(self, avp_code, data, vendor_id=0):
        DiamAVP.__init__(self, avp_code, struct.pack("!I", data), vendor_id)
    
    def getData(self):
        """Returns the payload as a 32-bit unsigned value."""
        return struct.unpack("!I",self.data)[0]
    
    def setData(self, data):
        """Sets the payload to the specified 32-bit unsigned value."""
        self.data = struct.pack("!I",data)
    
    def __str__(self):
        return self.str_prefix__() + "\t" + str(self.getData())

    def narrow(avp):
        """Convert generic AVP to AVP_Unsigned32
        Raises: InvalidAVPLengthException
        """
        if len(avp.payload)!=4:
            raise InvalidAVPLengthException(avp)
        data = struct.unpack("!I",avp.payload)[0]
        a = DiamAVP_Unsigned32(avp.avp_code, data, avp.vendor_id)
        a.flags = avp.flags
        return a
    
    narrow = staticmethod(narrow)

class DiamAVP_Unsigned64(DiamAVP):
    "A Diameter Unsigned64 AVP"
    
    def __init__(self, avp_code, data, vendor_id=0):
        DiamAVP.__init__(self,avp_code,struct.pack("!Q", data),vendor_id)
    
    def getData(self):
        """Returns the payload as a 64-bit unsigned value."""
        return struct.unpack("!Q",self.data)[0]
    
    def setData(self,data):
        """Sets the payload to the specified 64-bit unsigned value."""
        self.data = struct.pack("!Q",data)
    
    def __str__(self):
        return self.str_prefix__() + "\t" + str(self.getData())

    def narrow(avp):
        """Convert generic AVP to AVP_Unsigned64
        Raises: InvalidAVPLengthException
        """
        if len(avp.payload)!=8:
            raise InvalidAVPLengthException(avp)
        data = struct.unpack("!Q",avp.payload)[0]
        a = DiamAVP_Unsigned64(avp.avp_code, data, avp.vendor_id)
        a.flags = avp.flags
        return a
    
    narrow = staticmethod(narrow) 

class DiamAVP_Float32(DiamAVP):
    """32-bit floating point AVP"""
    
    def __init__(self, avp_code, data, vendor_id=0):
        DiamAVP.__init__(self,avp_code,struct.pack("!f", data),vendor_id)
    
    def getData(self):
        """Returns the payload interpreted as a 32-bit floating point value"""
        return struct.unpack("!f",self.data)[0]
    
    def setData(self,data):
        """Sets the payload to the spcified 32-bit floating point value"""
        self.data = struct.pack("!f",data)
    
    def __str__(self):
        return self.str_prefix__() + "\t" + str(self.getData())
    
    def narrow(avp):
        """Convert generic AVP to AVP_Float32
        Raises: InvalidAVPLengthException, InvalidAVPValueException
        """
        if len(avp.payload)!=4:
            raise InvalidAVPLengthException(avp)
        try:
            data = struct.unpack("!f",avp.payload)[0]
        except struct.error:
            raise InvalidAVPValueException(avp)
        a = DiamAVP_Float32(avp.avp_code, data, avp.vendor_id)
        a.flags = avp.flags
        return a
    
    narrow = staticmethod(narrow)

class DiamAVP_Float64(DiamAVP):
    """64-bit floating point AVP"""
    
    def __init__(self,avp_code,data,vendor_id=0):
        DiamAVP.__init__(self,avp_code,struct.pack("!d", data),vendor_id)
    
    def getData(self):
        """Returns the payload interpreted as a 64-bit floating point value"""
        return struct.unpack("!d",self.data)[0]
    
    def setData(self,data):
        """Sets the payload to the spcified 64-bit floating point value"""
        self.data = struct.pack("!d",data)
    
    def __str__(self):
        return self.str_prefix__() + "\t" + str(self.getData())
    
    def narrow(avp):
        """Convert generic AVP to AVP_Float64
        Raises: InvalidAVPLengthException, InvalidAVPValueException
        """
        if len(avp.payload)!=8:
            raise InvalidAVPLengthException(avp)
        try:
            data = struct.unpack("!d",avp.payload)[0]
        except struct.error:
            raise InvalidAVPValueException(avp)
        a = DiamAVP_Float64(avp.avp_code, data, avp.vendor_id)
        a.flags = avp.flags
        return a
    
    narrow = staticmethod(narrow)    
   
class DiamAVP_UTF8String(DiamAVP):
    """AVP with UTF-8 string payload."""
    
    def __init__(self, avp_code, data="", vendor_id=0):
        DiamAVP.__init__(self,avp_code,utf8encoder(data)[0],vendor_id)
    
    def getData(self):
        """Returns the payload as a string (possibly a unicode string)"""
        return utf8decoder(self.data)[0]
    
    def setData(self,data):
        try :
            self.data = utf8encoder(data)[0]
        except Exception:
            logErr(data)
    
    def __str__(self):  
        return self.str_prefix__() + "\t" + self.getData()
    
    def narrow(avp):
        """Convert generic AVP to AVP_UTF8String
        """
        a = DiamAVP_UTF8String(avp.avp_code, vendor_id=avp.vendor_id)
        a.flags = avp.flags
        a.payload = avp.payload
        return a
    
    narrow = staticmethod(narrow)

class DiamAVP_OctetString(DiamAVP):
    """AVP containing arbitrary data of variable length."""
    
    def __init__(self,code=0,payload="",vendor_id=0):
        DiamAVP.__init__(self,code,payload,vendor_id)

class DiamAVP_DiamIdent(DiamAVP):
    """AVP containing arbitrary data of variable length."""
    
    def __init__(self,code=0,payload="",vendor_id=0):
        DiamAVP.__init__(self,code,payload,vendor_id)
       
class DiamAVP_Grouped(DiamAVP):
    """AVP grouping multiple AVPs together."""
    
    def __init__(self, avp_code, avps=[], vendor_id=0):
        DiamAVP.__init__(self,avp_code,_pack(avps),vendor_id)
    
    def getAVPs(self):
        """Returns a copy of the embedded AVPs in a list"""
        avps=[]
        u = Unpacker(self.data)
        bytes_left=len(self.data)
        while bytes_left!=0:
            sz = DiamAVP.decodeSize(u,bytes_left)
            if sz==0:
                raise InvalidAVPLengthException(self)
            a = DiamAVP(1,"")
            a.decode(u,sz)
            avps.append(a)
            bytes_left -= sz
        return avps

        
    def setAVPs(self,avps):
        """Sets the payload to a copy of the AVPs in the list"""
        self.data = _pack(avps)
    
    def __str__(self):
        #The default str(...sequence...) looks suboptimal here
        s = ""
        for a in self.getAVPs():
            if s!="": s+=', '
            s += a.str_prefix__()
        return self.str_prefix__() + "\t[" + s + "]"
    
    def narrow(avp):
        """Convert generic AVP to AVP_Float64
        Raises: InvalidAVPLengthError
        """
        avps=[]
        u = Unpacker(avp.payload)
        bytes_left=len(avp.payload)
        while bytes_left!=0:
            sz = DiamAVP.decodeSize(u,bytes_left)
            if sz==0:
                raise InvalidAVPLengthException(avp)
            a = DiamAVP(1,"")
            a.decode(u,sz)
            avps.append(a)
            bytes_left -= sz
        a = DiamAVP_Grouped(avp.avp_code, avps, avp.vendor_id)
        a.flags = avp.flags
        return a
    
    narrow = staticmethod(narrow)

class DiamAVP_Address(DiamAVP):
    """An internet address AVP.
    This class reflects the Address type AVP described in RFC3588.
    It supports both IPv4 and IPv6.
    Note: Values not conforming to RFC3588 has been seen in the wild.
    """
    
    def __init__(self, avp_code, data, vendor_id=0):
        """Constructs an AVP_Address. The address is expected to tuple (family,address)"""
        DiamAVP.__init__(self,avp_code,_pack_address(data),vendor_id)
    
    def getData(self):
        """Returns the payload as a tuple (family,address)
        Raises: InvalidAddressTypeError
        """
        if len(self.data)==2+4:
            return (socket.AF_INET,socket.inet_ntop(socket.AF_INET,self.data[2:]))
        elif len(self.data)==2+16:
            return (socket.AF_INET6,socket.inet_ntop(socket.AF_INET6,self.data[2:]))
        else:
            raise InvalidAddressTypeException(self)
        
    def setData(self,address):
        """Sets the payload. The address is expected to tuple (family,address)
        Raises: InvalidAddressTypeError
        """
        self.data = _pack_address(address)
    
    def __str__(self):
        if len(self.data)==2+4:
            return self.str_prefix__() + "\t" + inet_ntop(socket.AF_INET,self.data[2:])
        elif len(self.data)==2+16:
            return self.str_prefix__() + "\t" + inet_ntop(socket.AF_INET6,self.data[2:])
        else:
            return DiamAVP.__str__(self)
    
    def narrow(avp):
        """Convert a generic AVP to AVP_Address
        Attempts to interpret the payload as an address and returns
        an AVP_Address instance on success.
        Raises: InvalidAVPLengthError
        """
        if len(avp.data)<2:
            raise InvalidAVPLengthException(avp)
        address_family = struct.unpack("!h",avp.data[0:2])[0]
        if address_family==1:
            if len(avp.data) != 2+4:
                raise InvalidAVPLengthException(avp)
        elif address_family==2:
            if len(avp.data) != 2+16:
                raise InvalidAVPLengthException(avp)
        else:
            raise InvalidAddressTypeException(avp)
        a = DiamAVP_Address(avp.code, "0.0.0.0", avp.vendor_id)
        a.data = avp.data[:]
        a.flags = avp.flags
        return a
    
    narrow = staticmethod(narrow)

class DiamAVP_Time(DiamAVP_Unsigned32):
    """A timestamp AVP.
    AVP_Time contains a second count since 1900. You can get the raw second
    count using AVP_Unsigned32.queryValue but this class' method
    querySecondsSince1970() is probably more useful in your program.
    
    Diameter does not have any base AVPs (RFC3588) with finer granularity
    than seconds.
    """
    
    seconds_between_1900_and_1970 = ((70*365)+17)*86400
    
    def __init__(self,code,seconds_since_1970,vendor_id=0):
        DiamAVP_Unsigned32.__init__(self,code,seconds_since_1970+self.seconds_between_1900_and_1970,vendor_id)
    
    def getData(self):
        return DiamAVP_Unsigned32.queryValue(self)-self.seconds_between_1900_and_1970
    
    def setData(self,seconds_since_1970):
        DiamAVP_Unsigned32.setValue(self,seconds_since_1970+self.seconds_between_1900_and_1970)

    def narrow(avp):
        """Convert generic AVP to AVP_Float64
        Raises: InvalidAVPLengthError
        """
        if len(avp.payload)!=4:
            raise InvalidAVPLengthException(avp)
        value = struct.unpack("!I",avp.payload)[0] - DiamAVP_Time.seconds_between_1900_and_1970
        a = DiamAVP_Time(avp.code, value, avp.vendor_id)
        a.flags = avp.flags
        return a
    narrow = staticmethod(narrow)
    
    def __str__(self):
        return DiamAVP.str_prefix__(self) + " " + str(datetime.fromtimestamp(self.getData()))

class DiamAVP_Octet(DiamAVP):
    """AVP containing Generic Octects."""
    
    def __init__(self,code=0,payload='000000',vendor_id=0):
        bPayload = bytearray.fromhex(payload)
        DiamAVP.__init__(self,code,bPayload,vendor_id)
    


''' Specific AVP messages '''
class GenericAVP:
    '''
        Class that defines a Generic AVP message 
    '''
    
    def __init__(self, avp_code, data):
        '''
            Initialize the AVP message
            @param data: contains the byte code of the AVP
        '''
        self.avp_code = avp_code
        self.data = data
        self.hdata = bytearray.fromhex(data)
        self.is_vendor = False
        self.is_mandatory = False
        self.is_protected = False
                
        # analyze bytes to get infos
        (cmd_code, b2) = struct.unpack("!LL", self.hdata[:8])
        self.length = int(b2 & 0x00ffffff)
        flags = int(b2 >> 24)
        
        if cmd_code != self.avp_code:
            raise InvalidAVPValueException('The specified command code [' + str(self.avp_code) + '] is different from hex embedded command code [' + str(cmd_code) + ']')
        
        bflags = bin(flags)[2:]
        n = 8-len(bflags)
        if n > 0:
            bflags = '0'*n + bflags
        if bflags[0] == '1':
            self.is_vendor = True
        if bflags[1] == '1':
            self.is_mandatory = True
        if bflags[2] == '1':
            self.is_protected = True
        
        self.vendor_id = 0
        if self.is_vendor:
            (vi) = struct.unpack("!L", self.hdata[8:12])
            self.vendor_id = vi[0]
            
        self.pad_len = (len(self.data)/2) - self.length
                
        self.__updateFlags()
        
    ''' GETTERS & SETTERS '''
    def setAVPCode(self, val):
        self.avp_code = val
        
    def setVendorFlag(self, val):
        self.is_vendor = val
        
        self.__updateFlags()
        
    def setMandatoryFlag(self, val):
        self.is_mandatory = val
        
        self.__updateFlags()
        
    def setProtectedFlag(self, val):
        self.is_protected = val
        
        self.__updateFlags()
        
    def setFlags(self, flags):
        self.is_vendor = 'V' in flags
        self.is_mandatory = 'M' in flags
        self.is_protected = 'P' in flags
        
        self.__updateFlags()
    
    def __updateFlags(self):
        self.flags = 0x00
        self.flags += 0x80 if self.is_vendor else 0x00
        self.flags += 0x40 if self.is_mandatory else 0x00
        self.flags += 0x20 if self.is_protected else 0x00
        
    def setData(self, val):
        self.data = val
        
    def setVendorID(self, val):
        self.vendor_id = val
            
        if val is not None and val != 0:
            self.is_vendor = True
        else:
            self.is_vendor = False
            
        if self.vendor_id is None:
            self.vendor_id = 0
        if isinstance(self.vendor_id, dict) and 'value' in self.vendor_id:
            self.vendor_id = int(self.vendor_id['value'])
        if not isinstance(self.vendor_id, int):
            self.vendor_id = int(self.vendor_id)
    
    def getAVPCode(self):
        return self.avp_code
    
    def isVendor(self):
        return self.is_vendor
    
    def isMandatory(self):
        return self.is_mandatory
    
    def isProtected(self):
        return self.is_protected
    
    def getAVPLength(self):
        return self.length
    
    def getPaddingLength(self):
        return self.pad_len
    
    def getData(self):
        return self.data[:self.length]
    
    def getVendorID(self):
        return self.vendor_id
    
    def getAvp(self):
        return self.generateAVPMessage()
    
    def getPackedData(self):
        return bytearray.fromhex(self.data[:self.length])
        
    def generateAVPMessage(self):
        self.avp_code = self.data[:8]
        return bytearray.fromhex(self.data)
    
    def str_prefix__(self):
        """Return a string prefix suitable for building a __str__ result"""
        s = str(self.avp_code)
        if self.is_vendor:
            s+= ".v"
        if self.is_mandatory:
            s+= ".m"
        if self.is_protected:
            s+= ".p"
        if self.vendor_id!=0:
            s+= ":"+str(self.vendor_id)
        return s
    
    def __str__(self):
        return self.str_prefix__() + "\t0x" + self.data
        

class OriginHostAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the Origin-Host AVP message 
    '''
    
    def __init__(self, host, vendor_id=0):
        '''
            Initialize the AVP message
            @param host: [DiameterIdentity] the origin host of the message
        '''
        DiamAVP.__init__(self, DiamAVPCodes.ORIGIN_HOST, host, vendor_id)
        self.host = host
    
class OriginRealmAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the Origin-Realm AVP message 
    '''
    
    def __init__(self, realm, vendor_id=0):
        '''
            Initialize the AVP message
            @param realm: [DiameterIdentity] the origin realm of the message
        '''
        DiamAVP.__init__(self, DiamAVPCodes.ORIGIN_REALM, realm, vendor_id)
        self.realm = realm 

class AuthSessionStateAVP(DiamAVP_Integer32):
    '''
        Class that defines the Auth-Session-State AVP message 
    '''
    
    STATE_MAINTAINED        = 0
    NO_STATE_MAINTAINED     = 1
    
    def __init__(self, session_state = STATE_MAINTAINED, vendor_id=0):
        '''
            Initialize the AVP message
            @param session_state: [Enumerated] to choose between STATE_MAINTAINED and NO_STATE_MAINTAINED
        '''
        session_state = int(session_state)
        if session_state != self.STATE_MAINTAINED and \
           session_state != self.NO_STATE_MAINTAINED:
            raise AVPParametersException('Auth-Session-State AVP :: Incorrect session_state [' + str(session_state) + ']')
        
        self.session_state = session_state
        DiamAVP_Integer32.__init__(self, DiamAVPCodes.AUTH_SESSION_STATE, self.session_state, vendor_id)

class DestinationHostAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the Destination-Host AVP message 
    '''
    
    def __init__(self, host, vendor_id=0):
        '''
            Initialize the AVP message
            @param host: [DiameterIdentity] the destination host of the message
        '''
        DiamAVP.__init__(self, DiamAVPCodes.DESTINATION_HOST, host, vendor_id)
        self.host = host
    
class DestinationRealmAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the Destination-Realm AVP message 
    '''
    
    def __init__(self, realm, vendor_id=0):
        '''
            Initialize the AVP message
            @param realm: [DiameterIdentity] the destination realm of the message
        '''
        DiamAVP.__init__(self, DiamAVPCodes.DESTINATION_REALM, realm, vendor_id)
        self.realm = realm

class HostIPAddressAVP(DiamAVP_Address):
    '''
        Class that defines the Host-IP-Address AVP message 
    '''
    
    def __init__(self, ip, vendor_id=0):
        '''
            Initialize the AVP message
            @param ip: [Address] the IP of the host
        '''
        DiamAVP_Address.__init__(self, DiamAVPCodes.HOST_IP_ADDRESS, ip, vendor_id)
        self.ip = ip
    
class VendorIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines the Vendor-ID AVP message 
        the ID is a IANA "SMI Network Management Private Enterprise Codes"
            (http://www.iana.org/assignments/enterprise-numbers)
    '''
    
    def __init__(self, vid, vendor_id=0):
        '''
            Initialize the AVP message
            @param vid: [Unsigned32] a IANA "SMI Network Management Private Enterprise Codes" ID
        '''
        vid = int(vid)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.VENDOR_ID, vid, vendor_id)
        self.id = vid
    
class SupportedVendorIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Supported-Vendor-ID AVP message 
        the ID is a IANA "SMI Network Management Private Enterprise Codes"
            (http://www.iana.org/assignments/enterprise-numbers)
        this MUST not be set to 0
    '''
    
    def __init__(self, vid, vendor_id=0):
        '''
            Initialize the AVP message
            @param vid: [Unsigned32] a IANA "SMI Network Management Private Enterprise Codes" ID
        '''
        vid = int(vid)
        
        if vid == 0:
            raise UnaccettableVendorIDException('Supported-Vendor-ID MUST NOT be 0')
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SUPPORTED_VENDOR_ID, vid, vendor_id)
        self.id = vid
    
class ProductNameAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Product-Name AVP message 
    '''
    
    def __init__(self, prod_name, vendor_id=0):
        '''
            Initialize the AVP message
            @param prod_name: [UTF8String] the name of the product of the messages
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.PRODUCT_NAME, prod_name, vendor_id)
        self.prod_name = prod_name
    
class OriginStateIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Origin-State-Id AVP message 
    '''
    
    def __init__(self, origin_state_id=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param origin_state_id: [Unsigned32] a monotonically increasing value. 
                                      If not provided will be initialized with the system timestamp 
        '''
        if origin_state_id is None:
            origin_state_id = int(time.time())
        else:
            origin_state_id = int(origin_state_id)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ORIGIN_STATE_ID, origin_state_id, vendor_id)
        self.origin_state_id = origin_state_id
    
class AuthApplicationIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Auth-Application-Id AVP message 
    '''
    
    def __init__(self, auth_app_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param auth_app_id: [Unsigned32] Authentication and Authorization of and application
                                Diameter Common Messages      0
                                NASREQ                        1 [NASREQ]
                                Mobile-IP                     2 [DIAMMIP]
                                Diameter Base Accounting      3
                                Relay                         0xffffffff
        '''
        auth_app_id = int(auth_app_id)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.AUTH_APPLICATION_ID, auth_app_id, vendor_id)
        self.auth_app_id = auth_app_id
    
class InbandSecurityIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Inband-Security-Id AVP message 
    '''
    
    NO_INBAND_SECURITY  = 0
    TLS                 = 1
    
    def __init__(self, inband_sec_id = NO_INBAND_SECURITY, vendor_id=0):
        '''
            Initialize the AVP message
            @param inband_sec_id: [Unsigned32] to choose between NO_INBAND_SECURITY and TLS.
                                  Can be expanded in the future.
        '''
        inband_sec_id = int(inband_sec_id)
        
        if inband_sec_id != self.NO_INBAND_SECURITY and inband_sec_id != self.TLS:
            raise AVPParametersException('Inband-Security AVP :: Incorrect inband_security_id [' + str(inband_sec_id) + ']')
        
        self.inband_sec_id = inband_sec_id
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.INBAND_SECURITY_ID, inband_sec_id, vendor_id)
    
class AcctApplicationIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Acct-Application-Id AVP message 
    '''
    
    def __init__(self, acct_app_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param acct_app_id: [Unsigned32] Accounting ID of and application
        '''
        acct_app_id = int(acct_app_id)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ACCT_APPLICATION_ID, acct_app_id, vendor_id)
        self.acct_app_id = acct_app_id
    
class VendorSpecificApplicationIDAVP(DiamAVP_Grouped):
    '''
        Class that defines a Vendor-Specific-Application-Id AVP message 
    '''
    
    def __init__(self, auth_app_id=None, acct_app_id=None, vendor_ids=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param vendor_specific_app_id: [Grouped] Accounting ID of and application
        '''
        if auth_app_id is None and acct_app_id is None:
            raise AVPParametersException('Vendor-Specific-Application-ID AVP :: Auth-Application-Id and Acct-Application-Id cannot be both None')
        
        self.auth_app_id = auth_app_id
        self.acct_app_id = acct_app_id
        self.vendor_ids = vendor_ids
        if not isinstance(self.vendor_ids, list):
            self.vendor_ids = [self.vendor_ids]
        self.vendor_id = vendor_id
        
        avps = []
        for vid in self.vendor_ids:
            a = VendorIDAVP(int(vid['value']))
            a.setFlags(vid['flags'])
            if 'vendor' in vid:
                a.setVendorID(vid['vendor'])
            avps.append(a)
        if self.auth_app_id is not None:
            a = AuthApplicationIDAVP(int(self.auth_app_id['value']))
            a.setFlags(self.auth_app_id['flags'])
            if 'vendor' in self.auth_app_id:
                a.setVendorID(self.auth_app_id['vendor'])
            avps.append(a)
        if self.acct_app_id is not None:
            a = AcctApplicationIDAVP(int(self.acct_app_id['value']))
            a.setFlags(self.acct_app_id['flags'])
            if 'vendor' in self.acct_app_id:
                a.setVendorID(self.acct_app_id['vendor'])
            avps.append(a)
        
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.VENDOR_SPECIFIC_APPLICATION_ID, avps, self.vendor_id)

class FirmwareRevisionAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Firmware-Revision AVP message 
    '''
    
    def __init__(self, firm_rev, vendor_id=0):
        '''
            Initialize the AVP message
            @param firm_rev: [Unsigned32] is the Firmware revision of the issuing device
        '''
        firm_rev = int(firm_rev)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.FIRMWARE_REVISION, firm_rev, vendor_id)
        self.firm_rev = firm_rev
  
class ResultCodeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Result-Code AVP message 
    '''
    
    def __init__(self, code, vendor_id=0):
        '''
            Initialize the AVP message
            @param code: [Unsigned32] is the result code in Answer messages
                         Diameter provides the following classes of errors, 
                         all identified by the thousands digit in the decimal notation:
                              -  1xxx (Informational)
                              -  2xxx (Success)
                              -  3xxx (Protocol Errors)
                              -  4xxx (Transient Failures)
                              -  5xxx (Permanent Failure)
        '''
        code = int(code)
        
        sCode = str(code)
                
        if code < 0:
            raise AVPParametersException('Result-Code AVP :: The result code cannot be negative')
        elif len(sCode) != 4:
            raise AVPParametersException('Result-Code AVP :: The result code MUST be of 4 digits')
        elif sCode[0] != '1' and sCode[0] != '2' and sCode[0] != '3' and sCode[0] != '4' and sCode[0] != '5':
            raise AVPParametersException('Result-Code AVP :: The result code MUST be of the form [1|2|3|4|5]xxx')
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.RESULT_CODE, code, vendor_id)
        self.code = code

class ExperimentalResultCodeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Experimental-Result-Code AVP message 
    '''
    
    def __init__(self, code, vendor_id=0):
        '''
            Initialize the AVP message
            @param code: [Unsigned32] is a vendor-assigned value representing the 
                                      result of processing the request.
        '''
        code = int(code)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.EXPERIMENTAL_RESULT_CODE, code, vendor_id)
        self.code = code

class ExperimentalResultAVP(DiamAVP_Grouped):
    '''
        Class that defines a Experimental-Result AVP message 
    '''
    
    def __init__(self, vendor_id, experimental_result_code):
        '''
            Initialize the AVP message
            @param vendor_id: the vendor id
            @param experimental_result_code: the result code
        '''
        
        self.vendor_id = vendor_id
        self.experimental_result_code = experimental_result_code
        
        avps = []
        if self.vendor_id != 0:
            a = VendorIDAVP(int(self.vendor_id['value']))
            a.setFlags(self.vendor_id['flags'])
            if 'vendor' in self.vendor_id:
                a.setVendorID(self.vendor_id['vendor'])
            avps.append(a)
            
        if self.experimental_result_code is not None:
            a = ExperimentalResultCodeAVP(self.experimental_result_code['value'])
            a.setFlags(self.experimental_result_code['flags'])
            if 'vendor' in self.experimental_result_code:
                a.setVendorID(self.experimental_result_code['vendor'])
            avps.append(a)
        
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.EXPERIMENTAL_RESULT, avps, self.vendor_id)

class ErrorMessageAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Error-Message AVP message 
    '''
    
    def __init__(self, err_message, vendor_id=0):
        '''
            Initialize the AVP message
            @param err_message: [UTF8String] is a human readable error message.
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.ERROR_MESSAGE, err_message, vendor_id)
        self.err_message = err_message

class FailedAVP(DiamAVP_Grouped):
    '''
        Class that defines a Failed-AVP AVP message 
    '''
    
    def __init__(self, avps, vendor_id=0):
        '''
            Initialize the AVP message
            @param avps: [Grouped] the AVPs
        '''
        self.avps = avps
        if not isinstance(self.avps, list):
            self.avps = [self.avps]
        
        DiamAVP.__init__(self, DiamAVPCodes.FAILED_AVP, avps, vendor_id)

class SessionIDAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Session-ID AVP message 
    '''
    
    def __init__(self, session_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param session_id: [UTF8String] is used to identify a specific session.
                               of the type:
                                   <DiameterIdentity>;<high 32 bits>;<low 32 bits>[;<optional value>]
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.SESSION_ID, session_id, vendor_id)
        self.session_id = session_id
        
class UserNameAVP(DiamAVP_UTF8String):
    '''
        Class that defines a User-Name AVP message 
    '''
    
    def __init__(self, user_name, vendor_id=0):
        '''
            Initialize the AVP message
            @param user_name: [UTF8String] is the user name
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.USER_NAME, user_name, vendor_id)
        self.user_name = user_name

class CancellationTypeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Cancellation-Type AVP message 
    '''
    
    MME_UPDATE_PROCEDURE        = 0
    SGSN_UPDATE_PROCEDURE       = 1
    SUBSCRIPTION_WITHDRAWAL     = 2
    UPDATE_PROCEDURE_IWF        = 3
    INITIAL_ATTACH_PROCEDURE    = 4
    
    def __init__(self, canc_type = MME_UPDATE_PROCEDURE, vendor_id=0):
        '''
            Initialize the AVP message
            @param canc_type: [Unsigned32] the type of cancellation. Accepted values:
                        * MME_UPDATE_PROCEDUR
                        * SGSN_UPDATE_PROCEDURE
                        * SUBSCRIPTION_WITHDRAWAL
                        * UPDATE_PROCEDURE_IWF
                        * INITIAL_ATTACH_PROCEDURE
        '''
        canc_type = int(canc_type)
        
        if canc_type != self.MME_UPDATE_PROCEDURE and \
           canc_type != self.SGSN_UPDATE_PROCEDURE and \
           canc_type != self.SUBSCRIPTION_WITHDRAWAL and \
           canc_type != self.UPDATE_PROCEDURE_IWF and \
           canc_type != self.INITIAL_ATTACH_PROCEDURE:
            raise AVPParametersException('Cancellation-Type AVP :: Incorrect Cancellation-Type [' + str(canc_type) + ']')
        
        self.canc_type = canc_type
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.CANCELLATION_TYPE, canc_type, vendor_id)

class FeatureListIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Feature-List-ID AVP message 
    '''
    
    def __init__(self, feature_list_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param feature_list_id: [Unsigned32] is the identity of a feature list
        '''
        feature_list_id = int(feature_list_id)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.FEATURE_LIST_ID, int(feature_list_id), vendor_id)
        self.feature_list_id = feature_list_id

class FeatureListAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Feature-List AVP message 
    '''
    
    def __init__(self, feature_list, vendor_id=0):
        '''
            Initialize the AVP message
            @param feature_list: [Unsigned32] is s a bit mask indicating the supported
                                 features of an application
        '''
        feature_list = int(feature_list)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.FEATURE_LIST, feature_list, vendor_id)
        self.feature_list = feature_list
        
class SupportedFeaturesAVP(DiamAVP_Grouped):
    '''
        Class that defines a Supported-Features AVP message 
    '''
    
    def __init__(self, vendor_id, feature_list_id, feature_list):
        '''
            Initialize the AVP message
            @param vendor_id: with the feature_list_id shall together identify which feature list is carried
            @param feature_list_id: with the vendor_id shall together identify which feature list is carried
            @param feature_list: a list of supported features of the origin host
        '''
        
        self.vendor_id = vendor_id
        self.feature_list_id = feature_list_id
        self.feature_list = feature_list
        
        avps = []
        
        if self.vendor_id is None:
            raise AVPParametersException('Supported-Features AVP :: The vendor_id is MANDATORY')
        a = VendorIDAVP(int(self.vendor_id['value']))
        a.setFlags(self.vendor_id['flags'])
        if 'vendor' in self.vendor_id:
            a.setVendorID(self.vendor_id['vendor'])
        avps.append(a)
        
        
        if self.feature_list_id is None:
            raise AVPParametersException('Supported-Features AVP :: The feature_list_id is MANDATORY')
        a = FeatureListIDAVP(self.feature_list_id['value'])
        a.setFlags(self.feature_list_id['flags'])
        if 'vendor' in self.feature_list_id:
            a.setVendorID(self.feature_list_id['vendor'])
        avps.append(a)
        
        if self.feature_list is None:
            raise AVPParametersException('Supported-Features AVP :: The feature_list is MANDATORY')
        a = FeatureListAVP(self.feature_list['value'])
        a.setFlags(self.feature_list['flags'])
        if 'vendor' in self.feature_list:
            a.setVendorID(self.feature_list['vendor'])
        avps.append(a)
        
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.SUPPORTED_FEATURES, avps, self.vendor_id['value'])

class CLRFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a CLR-Flags AVP message 
    '''
    
    def __init__(self, clr_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param clr_flags: [Unsigned32] two bits that acts as flags as follow
                              S6a/S6d-Indicator: 1, indicates that the CLR message is sent on the S6a interface
                                                 0, indicates that the CLR message is sent on the S6d interface
                              Reattach-Required: when set, indicates that the MME or SGSN shall request the 
                                                 UE to initiate an immediate re-attach procedure
        '''
        clr_flags = int(clr_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.CLR_FLAGS, clr_flags, vendor_id)
        self.clr_flags = clr_flags

class ProxyHostAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the Proxy-Host AVP message 
    '''
    
    def __init__(self, host, vendor_id=0):
        '''
            Initialize the AVP message
            @param host: [DiameterIdentity] the identity of the host
        '''
        DiamAVP.__init__(self, DiamAVPCodes.PROXY_HOST, host, vendor_id)
        self.host = host

class ProxyStateAVP(DiamAVP_OctetString):
    '''
        Class that defines a Proxy-State AVP message 
    '''
    
    def __init__(self, proxy_state, vendor_id=0):
        '''
            Initialize the AVP message
            @param proxy_state: [OctetString] is the state local information, and MUST be treated as opaque data
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.PROXY_STATE, proxy_state, vendor_id)
        self.proxy_state = proxy_state
        
class ProxyInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a Proxy-Info AVP message 
    '''
    
    def __init__(self, proxy_host, proxy_state, vendor_id=0):
        '''
            Initialize the AVP message
            @param proxy_host: the identity of the host that added the Proxy-Info AVP
            @param proxy_state: the state local information, and MUST be treated as opaque data
        '''
        
        self.proxy_host = proxy_host
        self.proxy_state = proxy_state
        self.vendor_id = vendor_id

        avps = []
        if self.proxy_host is None:
            raise AVPParametersException('Proxy-Info AVP :: The proxy_host is MANDATORY')
        a = ProxyHostAVP(self.proxy_host['value'])
        a.setFlags(self.proxy_host['flags'])
        if 'vendor' in self.proxy_host:
            a.setVendorID(self.proxy_host['vendor'])
        avps.append(a)
        
        if self.proxy_state is None:
            raise AVPParametersException('Proxy-Info AVP :: The proxy_state is MANDATORY')
        a = ProxyStateAVP(self.proxy_state['value'])
        a.setFlags(self.proxy_state['flags'])
        if 'vendor' in self.proxy_state:
            a.setVendorID(self.proxy_state['vendor'])
        avps.append(a)
        
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.PROXY_INFO, avps, self.vendor_id)

class RouteRecordAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the Route-Record AVP message 
    '''
    
    def __init__(self, route_record, vendor_id=0):
        '''
            Initialize the AVP message
            @param route_record: [DiameterIdentity] the identity added in this AVP MUST be the same as 
                                 the one received in the Origin-Host of the Capabilities Exchange message.
        '''
        DiamAVP.__init__(self, DiamAVPCodes.ROUTE_RECORD, route_record, vendor_id)
        self.route_record = route_record

class RATAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a RAT AVP message 
    '''
    
    WLAN                = 0
    VIRTUAL             = 1
    UTRAN               = 1000
    GERAN               = 1001
    GAN                 = 1002
    HSPA_EVOLUTION      = 1003
    EUTRAN              = 1004
    CDMA2000_1X         = 2000
    HRPD                = 2001
    UMB                 = 2002
    EHRPD               = 2003 
    
    def __init__(self, rat = WLAN, vendor_id=0):
        '''
            Initialize the AVP message
            @param rat: [Unsigned32] identify the radio access technology that is serving the UE. 
                        Accepted values:
                            * WLAN
                            * VIRTUAL
                            * UTRAN
                            * GERAN
                            * GAN
                            * HSPA_EVOLUTION
                            * EUTRAN
                            * CDMA2000_1X
                            * HRPD
                            * UMB
                            * EHRPD
        '''
        
        rat = int(rat)
        
        if rat != self.WLAN and \
           rat != self.VIRTUAL and \
           rat != self.UTRAN and \
           rat != self.GERAN and \
           rat != self.GAN and \
           rat != self.HSPA_EVOLUTION and \
           rat != self.EUTRAN and \
           rat != self.CDMA2000_1X and \
           rat != self.HRPD and \
           rat != self.UMB and \
           rat != self.EHRPD:
            raise AVPParametersException('RAT AVP :: Incorrect RAT value [' + str(rat) + ']')
        
        self.rat = rat
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.RAT, rat, vendor_id)

class ULRFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a ULR-Flags AVP message 
    '''
    
    def __init__(self, ulr_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param ulr_flags: [Unsigned32] bits that acts as flags as follow:
                            Bit    Name                                Value
                             0      Single-Registration-Indication      when set, indicates that the HSS shall send Cancel Location to the SGSN.
                             1      S6a/S6d-Indicator                   when set, indicates that the ULR message is sent on the S6a interface
                                                                        when cleared, indicates that the ULR message is sent on the S6d interface
                             2      Skip Subscriber Data                when set, indicates that the HSS may skip subscription data in ULA
                             3      GPRS-Subscription-Data-Indicator    when set, indicates that the HSS shall include in the ULA command the GPRS subscription data,
                             4      Node-Type-Indicator                 when set, indicates that the requesting node is a combined MME/SGSN.
                                                                        when cleared, indicates that the requesting node is a single MME or SGSN; in this case, if the S6a/S6d-Indicator is set
                             5      Initial-Attach-Indicator            when set, indicates that the HSS shall send Cancel Location to the MME or SGSN
                             6      PS-LCS-Not-Supported-By-UE          when set, indicates to the HSS that the UE does not support neither UE Based nor UE Assisted positioning methods for Packet Switched Location Services.
                             7      SMS-Only-Indication                 when set, indicates that the UE indicated "SMS only" when requesting a combined IMSI attach or combined RA/LU
        '''
        ulr_flags = int(ulr_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ULR_FLAGS, ulr_flags, vendor_id)
        self.ulr_flags = ulr_flags
        
class VisitedPLMNIDAVP(DiamAVP_Octet):
    '''
        Class that defines a Visited-PLMN-ID AVP message 
    '''
    
    def __init__(self, data, vendor_id=0):
        '''
            Initialize the AVP message
            @param data both MCC and MNC variables
        '''
       
        mnc = data[3:]
        mcc = data[:3]
            
        #Construct the visited-PLMN-ID bitmask
        hex_val = mcc[1]
        hex_val += mcc[0]
        if len(mnc) == 2 :
            hex_val += "f"
        else :
#             if mnc[0] == '0' :
#                 mnc_list = list(mnc)
#                 tmp = mnc_list[0]
#                 mnc_list[0] = mnc_list[1]
#                 mnc_list[1] = mnc_list[2]
#                 mnc_list[2] = tmp
#                 mnc = "".join(mnc_list)
            hex_val += mnc[2]
        hex_val += mcc[2]
        hex_val += mnc[1]
        hex_val += mnc[0]
                
        self.visited_plmn_id = hex_val
        DiamAVP_Octet.__init__(self, DiamAVPCodes.VISITED_PLMN_ID, self.visited_plmn_id, vendor_id)
        
class OCFeatureVectorAVP(DiamAVP_Unsigned64):
    '''
        Class that defines a OC-Feature-Vector AVP message 
    '''
    
    OLR_DEFAULT_ALGO    = 0x0000000000000001
        
    def __init__(self, oc_feature_vect=OLR_DEFAULT_ALGO, vendor_id=0):
        '''
            Initialize the AVP message
            @param oc_feature_vect: [Unsigned64] bits that specify the supported algorithms:
        '''
        oc_feature_vect = int(oc_feature_vect)
        
        DiamAVP_Unsigned64.__init__(self, DiamAVPCodes.OC_FEATURES_VECTOR, oc_feature_vect, vendor_id)
        self.oc_feature_vect = oc_feature_vect
        
class OCSupportedFeaturesAVP(DiamAVP_Grouped):
    '''
        Class that defines a OC-Supported-Features AVP message 
    '''
    
    def __init__(self, oc_feature_vector, vendor_id=0):
        '''
            Initialize the AVP message
            @param oc_feature_vector: a 64 bit flags field of announced capabilities of a DOIC node
        '''
        
        self.oc_feature_vector = oc_feature_vector
        self.vendor_id = vendor_id
        
        avps = []
        if self.oc_feature_vector is None:
            raise AVPParametersException('OC-Supported-Features AVP :: The proxy_host is MANDATORY')
        a = OCFeatureVectorAVP(self.oc_feature_vector['value'])
        a.setFlags(self.oc_feature_vector['flags'])
        if 'vendor' in self.oc_feature_vector:
            a.setVendorID(self.oc_feature_vector['vendor'])
        avps.append(a)
        
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.OC_SUPPORTED_FEATURES, avps, self.vendor_id)

class UESRVCCCapabilityAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a UE-SRVCC-Capability AVP message 
    '''
    
    UE_SRVCC_NOT_SUPPORTED  = 0
    UE_SRVCC_SUPPORTED      = 1
    
    def __init__(self, ue_srvcc_id = UE_SRVCC_NOT_SUPPORTED, vendor_id=0):
        '''
            Initialize the AVP message
            @param ue_srvcc_id: [Unsigned32] it shall indicate if the UE supports or does not support the SRVCC capability.
                                Accepted values:
                                    * UE_SRVCC_NOT_SUPPORTED
                                    * UE_SRVCC_SUPPORTED
        '''
        ue_srvcc_id = int(ue_srvcc_id)
        
        if ue_srvcc_id != self.UE_SRVCC_NOT_SUPPORTED and \
           ue_srvcc_id != self.UE_SRVCC_SUPPORTED:
            raise AVPParametersException('UE-SRVCC-Capability AVP :: Incorrect ue_srvcc_id value [' + str(ue_srvcc_id) + ']')
        
        self.ue_srvcc_id = ue_srvcc_id
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.UE_SRVCC_CAPABILITY, ue_srvcc_id, vendor_id)

class SGSNNumberAVP(DiamAVP_OctetString):
    '''
        Class that defines a SGSN-Number AVP message 
    '''
    
    def __init__(self, sgsn_number, vendor_id=0):
        '''
            Initialize the AVP message
            @param sgsn_number: [OctetString] it shall contain the ISDN number of the SGSN.
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.SGSN_NUMBER, sgsn_number, vendor_id)
        self.sgsn_number = sgsn_number

class HomogeneousSupportIMSVoiceOverPSSessionsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Homogeneous-Support-IMS-Voice-Over-PS-Session AVP message 
    '''
    
    NOT_SUPPORTED  = 0
    SUPPORTED      = 1
    
    def __init__(self, homogeneous_support_ims_voice_over_ps_session = NOT_SUPPORTED, vendor_id=0):
        '''
            Initialize the AVP message
            @param homogeneous_support_ims_voice_over_ps_session: [Unsigned32] defines if the IMS Voice over PS Session is supported
                                        Accepted values:
                                            * NOT_SUPPORTED
                                            * SUPPORTED
        '''
        homogeneous_support_ims_voice_over_ps_session = int(homogeneous_support_ims_voice_over_ps_session)
        
        if homogeneous_support_ims_voice_over_ps_session != self.NOT_SUPPORTED and \
           homogeneous_support_ims_voice_over_ps_session != self.SUPPORTED:
            raise AVPParametersException('Homogeneous-Support-Of-Ims-Voice-Over-Ps-Sessions AVP :: Incorrect homogeneous_support_ims_voice_over_ps_session value [' + str(homogeneous_support_ims_voice_over_ps_session) + ']')
        
        self.homogeneous_support_ims_voice_over_ps_session = homogeneous_support_ims_voice_over_ps_session
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.HOMOGENEOUS_SUPPORT_OF_IMS_VOICE_OVER_PS_SESSIONS, homogeneous_support_ims_voice_over_ps_session, vendor_id)

class GMLCAddressAVP(DiamAVP_Address):
    '''
        Class that defines the GMLC-Address AVP message 
    '''
    
    def __init__(self, ip, vendor_id=0):
        '''
            Initialize the AVP message
            @param ip: [Address] the IP address of the GMLC associated with the serving node
        '''
        DiamAVP_Address.__init__(self, DiamAVPCodes.GMLC_ADDRESS, ip, vendor_id)
        self.ip = ip

class ContextIentifierAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Context-Identifier AVP message 
    '''
    
    def __init__(self, context_id=0, vendor_id=0):
        '''
            Initialize the AVP message
            @param context-id: [Unsigned32] the identifier of the context
        '''
        self.context_id = int(context_id)
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.CONTEXT_IDENTIFIER, self.context_id, vendor_id)
    
class ServiceSelectionAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Service-Selection AVP message 
    '''
    
    def __init__(self, service, vendor_id=0):
        '''
            Initialize the AVP message
            @param service: [UTF8String] the name of the service or the external network with which the mobility service should be associated
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.SERVICE_SELECTION, service, vendor_id)
        self.service = service

class MIPHomeAgentAddressAVP(DiamAVP_Address):
    '''
        Class that defines the MIP-Home-Agent-Address AVP message 
    '''
    
    def __init__(self, ip, vendor_id=0):
        '''
            Initialize the AVP message
            @param ip: [Address] the IP address of the MIPv6 HA
        '''
        DiamAVP_Address.__init__(self, DiamAVPCodes.MIP_HOME_AGENT_ADDRESS, ip, vendor_id)
        self.ip = ip

class MIPHomeAgentHostAVP(DiamAVP_Grouped):
    '''
        Class that defines a MIP-Home-Agent-Host AVP message 
        
            MIP-Home-Agent-Host ::= < AVP Header: 348 >
                                  { Destination-Realm }
                                  { Destination-Host }
    '''
    
    def __init__(self, destination_realm, destination_host, vendor_id=0):
        '''
            Initialize the AVP message
            @param destination_realm: the realm of the MIP Agent Host
            @param destination_host: the host of the MIP Agent Host
        '''
        
        self.destination_realm = destination_realm
        self.destination_host = destination_host
        self.vendor_id = vendor_id
        
        avps = []        
        if self.destination_realm is None:
            raise AVPParametersException('MIP-Home-Agent-Host AVP :: The destination_realm is MANDATORY')
        a = DestinationRealmAVP(self.destination_realm['value'])
        a.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            a.setVendorID(self.destination_realm['vendor'])
        avps.append(a)
        
        if self.destination_host is None:
            raise AVPParametersException('MIP-Home-Agent-Host AVP :: The destination_host is MANDATORY')
        a = DestinationHostAVP(self.destination_host['value'])
        a.setFlags(self.destination_host['flags'])
        if 'vendor' in self.destination_host:
            a.setVendorID(self.destination_host['vendor'])
        avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.MIP_HOME_AGENT_HOST, avps, self.vendor_id)

class MIPHomeLinkPrefixAVP(DiamAVP_OctetString):
    '''
        Class that defines a MIP-Home-Link-Prefix AVP message 
    '''
    
    def __init__(self, home_link_prefix, vendor_id=0):
        '''
            Initialize the AVP message
            @param home_link_prefix: [OctetString] contains the Mobile IPv6 home network prefix information in a network byte order
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.MIP_HOME_LINK_PREFIX, home_link_prefix, vendor_id)
        self.home_link_prefix = home_link_prefix

class MIP6AgentInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a MIP6-Agent-Info AVP message 
        
            MIP6-Agent-Info ::= < AVP-Header: 486 >
                             *2[ MIP-Home-Agent-Address ]
                               [ MIP-Home-Agent-Host ]
                               [ MIP6-Home-Link-Prefix ]
    '''
    
    def __init__(self, home_agent_address=None, home_agent_host=None, home_link_prefix=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param home_agent_address: 
            @param home_agent_host: 
            @param home_link_prefix: 
        '''
        
        self.home_agent_address = home_agent_address
        if not isinstance(self.home_agent_address, list):
            self.home_agent_address = [self.home_agent_address]
        self.home_agent_host = home_agent_host
        self.home_link_prefix = home_link_prefix
        self.vendor_id = vendor_id
        
        avps = []
        if self.home_agent_address is not None and len(self.home_agent_address) <= 2:
            for haa in self.home_agent_address:
                if haa is not None:
                    a = MIPHomeAgentAddressAVP(haa['value'])
                    a.setFlags(haa['flags'])
                    if 'vendor' in haa:
                        a.setVendorID(haa['vendor'])
                    avps.append(a)
        
        if self.home_agent_host is not None:
            a = MIPHomeAgentHostAVP(self.home_agent_host['value'])
            a.setFlags(self.home_agent_host['flags'])
            if 'vendor' in self.home_agent_host:
                a.setVendorID(self.home_agent_host['vendor'])
            avps.append(a)
        
        if self.home_link_prefix is not None:
            a = MIPHomeLinkPrefixAVP(self.home_link_prefix['value'])
            a.setFlags(self.home_link_prefix['flags'])
            if 'vendor' in self.home_link_prefix:
                a.setVendorID(self.home_link_prefix['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.MIP6_AGENT_INFO, avps, self.vendor_id)

class VisitedNetworkIdentifierAVP(DiamAVP_OctetString):
    '''
        Class that defines a Visited-Network-Identifier AVP message 
    '''
    
    def __init__(self, visited_network_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param visited_network_id: [OctetString] contains an identifier that helps the home network to identify the visited network (e.g. the visited network domain name).
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.VISITED_NETWORK_IDENTIFIER, visited_network_id, vendor_id)
        self.visited_network_id = visited_network_id

class SpecificAPNInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a Specific-APN-Info AVP message 
        
            Specific-APN-Info ::= <AVP header: 1472 10415>
                                { Service-Selection }
                                { MIP6-Agent-Info }
                                [ Visited-Network-Identifier ]
    '''
    
    def __init__(self, service_selection, mip6_agent_info, visited_network_id=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param service_selection: 
            @param mip6_agent_info: 
            @param visited_network_id: 
        '''
        
        self.service_selection = service_selection
        self.mip6_agent_info = mip6_agent_info
        self.visited_network_id = visited_network_id
        self.vendor_id = vendor_id
        
        avps = []
        if self.service_selection is not None:
            a = ServiceSelectionAVP(self.service_selection['value'])
            a.setFlags(self.service_selection['flags'])
            if 'vendor' in self.service_selection:
                a.setVendorID(self.service_selection['vendor'])
            avps.append(a)
        
        if self.mip6_agent_info is not None:
            a = MIP6AgentInfoAVP(self.mip6_agent_info['value'])
            a.setFlags(self.mip6_agent_info['flags'])
            if 'vendor' in self.mip6_agent_info:
                a.setVendorID(self.mip6_agent_info['vendor'])
            avps.append(a)
        
        if self.visited_network_id is not None:
            a = VisitedNetworkIdentifierAVP(self.visited_network_id['value'])
            a.setFlags(self.visited_network_id['flags'])
            if 'vendor' in self.visited_network_id:
                a.setVendorID(self.visited_network_id['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.SPECIFIC_APN_INFO, avps, self.vendor_id)

class ActiveAPNAVP(DiamAVP_Grouped):
    '''
        Class that defines a Active-APN AVP message 
        
            Active-APN ::= <AVP header: 1612 10415>
                        { Context-Identifier }
                        [ Service-Selection ]
                        [ MIP6-Agent-Info ]
                        [ Visited-Network-Identifier ]
                        *[ Specific-APN-Info ]
    '''
    
    def __init__(self, context_id, service_selection=None, mip6_agent_info=None, visited_network_id=None, specific_apn_info=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param context_id:
            @param service_selection: 
            @param mip6_agent_info:
            @param visited_network_id:
            @param specific_apn_info:
        '''
        
        self.context_id = context_id
        self.service_selection = service_selection
        self.mip6_agent_info = mip6_agent_info
        self.visited_network_id = visited_network_id
        self.specific_apn_info = specific_apn_info
        if not isinstance(self.specific_apn_info, list):
            self.specific_apn_info = [self.specific_apn_info]
        self.vendor_id = vendor_id
        
        avps = []
        if self.context_id is None:
            raise AVPParametersException('Active-APN AVP :: The context_id is MANDATORY')
        a = ContextIentifierAVP(self.context_id['value'])
        a.setFlags(self.context_id['flags'])
        if 'vendor' in self.context_id:
            a.setVendorID(self.context_id['vendor'])
        avps.append(a)
        
        if self.service_selection is not None:
            a = ServiceSelectionAVP(self.service_selection['value'])
            a.setFlags(self.service_selection['flags'])
            if 'vendor' in self.service_selection:
                a.setVendorID(self.service_selection['vendor'])
            avps.append(a)
        
        if self.mip6_agent_info is not None:
            a = MIP6AgentInfoAVP(self.mip6_agent_info['value'])
            a.setFlags(self.mip6_agent_info['flags'])
            if 'vendor' in self.mip6_agent_info:
                a.setVendorID(self.mip6_agent_info['vendor'])
            avps.append(a)
        
        if self.visited_network_id is not None:
            a = VisitedNetworkIdentifierAVP(self.visited_network_id['value'])
            a.setFlags(self.visited_network_id['flags'])
            if 'vendor' in self.visited_network_id:
                a.setVendorID(self.visited_network_id['vendor'])
            avps.append(a)
        
        if self.specific_apn_info is not None:
            for sai in self.specific_apn_info:
                if sai is not None:
                    a = SpecificAPNInfoAVP(sai['value'])
                    a.setFlags(sai['flags'])
                    if 'vendor' in sai:
                        a.setVendorID(sai['vendor'])
                    avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.ACTIVE_APN, avps, self.vendor_id)

class EquivalentPLMNListAVP(DiamAVP_Grouped):
    '''
        Class that defines a Equivalent-PLMN-List AVP message 
        
            Equivalent-PLMN-List ::= <AVP header: 1637 10415>
                                1*{ Visited-PLMN-Id }
    '''
    
    def __init__(self, visited_plmn_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param visited_plmn_id:
        '''
        
        self.visited_plmn_id = visited_plmn_id
        if not isinstance(self.visited_plmn_id, list):
            self.visited_plmn_id = [self.visited_plmn_id]
        self.vendor_id = vendor_id
        
        avps = []
        if self.visited_plmn_id is None:
            raise AVPParametersException('Equivalent-PLMN-List AVP :: The visited_plmn_id is MANDATORY')
        for vpi in self.visited_plmn_id:
            a = VisitedPLMNIDAVP(vpi['value'])
            a.setFlags(vpi['flags'])
            if 'vendor' in vpi:
                a.setVendorID(vpi['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.EQUIVALENT_PLMN_LIST, avps, self.vendor_id)

class MMENumberForMTSMSAVP(DiamAVP_OctetString):
    '''
        Class that defines a MME-Number-For-MT-SMS AVP message 
    '''
    
    def __init__(self, mme_number, vendor_id=0):
        '''
            Initialize the AVP message
            @param mme_number: [OctetString] contain the ISDN number corresponding to the MME for MT SMS. 
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.MME_NUMBER_FOR_MT_SMS, mme_number, vendor_id)
        self.mme_number = mme_number

class SMSRegisterRequestAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a SMS-Register-Request AVP message 
    '''
    
    SMS_REGISTRATION_REQUIRED       = 0
    SMS_REGISTRATION_NOT_PREFERRED  = 1
    NO_PREFERENCE                   = 2
    
    def __init__(self, sms_register_request = SMS_REGISTRATION_REQUIRED, vendor_id=0):
        '''
            Initialize the AVP message
            @param sms_register_request: [Unsigned32] indicate whether the MME or the SGSN requires to be registered for SMS
                                         or if the MME or the SGSN prefers not to be registered for SMS or if the MME 
                                         or the SGSN has no preference
                                            Accepted values:
                                                * NOT_SUPPORTED
                                                * SUPPORTED
        '''
        sms_register_request = int(sms_register_request)
        
        if sms_register_request != self.SMS_REGISTRATION_REQUIRED and \
           sms_register_request != self.SMS_REGISTRATION_NOT_PREFERRED and \
           sms_register_request != self.NO_PREFERENCE:
            raise AVPParametersException('SMS-Register-Request AVP :: Incorrect sms_register_request value [' + str(sms_register_request) + ']')
        
        self.sms_register_request = sms_register_request
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SMS_REGISTER_REQUEST, sms_register_request, vendor_id)

class SGsMMEIdentityAVP(DiamAVP_UTF8String):
    '''
        Class that defines a SGs-MME-Identity AVP message 
    '''
    
    def __init__(self, sgs_mme_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param sgs_mme_id: [UTF8String] contain the MME identity used over the SGs interface
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.SGS_MME_IDENTITY, sgs_mme_id, vendor_id)
        self.sgs_mme_id = sgs_mme_id

class CoupledNodeDiameterIDAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the Coupled-Node-Diameter-ID AVP message 
    '''
    
    def __init__(self, coupled_node_diameter_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param coupled_node_diameter_id: [DiameterIdentity] contain the S6a or S6d Diameter identity of the coupled node
        '''
        DiamAVP.__init__(self, DiamAVPCodes.COUPLED_NODE_DIAMETER_ID, coupled_node_diameter_id, vendor_id)
        self.coupled_node_diameter_id = coupled_node_diameter_id

class ErrorDiagnosticAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Error-Diagnostic AVP message 
    '''
    
    GPRS_DATA_SUBSCRIBED        = 0
    NO_GPRS_DATA_SUBSCRIBED     = 1
    ODB_ALL_APN                 = 2
    ODB_HPLMN_APN               = 3
    ODB_VPLMN_APN               = 4
    
    def __init__(self, error_diagnostic = GPRS_DATA_SUBSCRIBED, vendor_id=0):
        '''
            Initialize the AVP message
            @param error_diagnostic: [Unsigned32] indicate whether the MME or the SGSN requires to be registered for SMS
                                         or if the MME or the SGSN prefers not to be registered for SMS or if the MME 
                                         or the SGSN has no preference
                                            Accepted values:
                                                * GPRS_DATA_SUBSCRIBED
                                                * NO_GPRS_DATA_SUBSCRIBED
                                                * ODB_ALL_APN
                                                * ODB_HPLMN_APN
                                                * ODB_VPLMN_APN
        '''
        error_diagnostic = int(error_diagnostic)
        
        if error_diagnostic != self.GPRS_DATA_SUBSCRIBED and \
           error_diagnostic != self.NO_GPRS_DATA_SUBSCRIBED and \
           error_diagnostic != self.ODB_ALL_APN and \
           error_diagnostic != self.ODB_HPLMN_APN and \
           error_diagnostic != self.ODB_VPLMN_APN:
            raise AVPParametersException('Error-Diagnostic AVP :: Incorrect error_diagnostic value [' + str(error_diagnostic) + ']')
        
        self.error_diagnostic = error_diagnostic
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ERROR_DIAGNOSTIC, error_diagnostic, vendor_id)

class OCSequenceNumberAVP(DiamAVP_Unsigned64):
    '''
        Class that defines a OC-Sequence-Number AVP message 
    '''
    
    def __init__(self, oc_seq_num, vendor_id=0):
        '''
            Initialize the AVP message
            @param oc_seq_num: [Unsigned64] incremental sequence_number
        '''
        oc_seq_num = int(oc_seq_num)
        
        DiamAVP_Unsigned64.__init__(self, DiamAVPCodes.OC_SEQUENCE_NUMBER, oc_seq_num, vendor_id)
        self.oc_seq_num = oc_seq_num
  
class OCValidityDurationAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a OC-Validity-Duration AVP message 
    '''
    
    def __init__(self, oc_validity_duration, vendor_id=0):
        '''
            Initialize the AVP message
            @param oc_validity_duration: [Unsigned32] indicates in seconds the validity time of the overload report
        '''
        oc_validity_duration = int(oc_validity_duration)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.OC_VALIDITY_DURATION, oc_validity_duration, vendor_id)
        self.oc_validity_duration = oc_validity_duration
      
class OCReportTypeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a OC-Report-Type AVP message 
    '''
    
    HOST_REPORT      = 0
    REALM_REPORT     = 1
    
    def __init__(self, oc_report_type = HOST_REPORT, vendor_id=0):
        '''
            Initialize the AVP message
            @param oc_report_type: [Unsigned32] describes what the overload report concerns
                                    Accepted values:
                                        * HOST_REPORT
                                        * REALM_REPORT
        '''
        oc_report_type = int(oc_report_type)
        
        if oc_report_type != self.HOST_REPORT and \
           oc_report_type != self.REALM_REPORT:
            raise AVPParametersException('OC-Report-Type AVP :: Incorrect oc_report_type value [' + str(oc_report_type) + ']')
        
        self.oc_report_type = oc_report_type
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.OC_REPORT_TYPE, oc_report_type, vendor_id)

class OCReductionPercentageAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a OC-Reduction-Percentage AVP message 
    '''
    
    def __init__(self, oc_reduction_percentage, vendor_id=0):
        '''
            Initialize the AVP message
            @param oc_reduction_percentage: [Unsigned32] describes the percentage of the traffic that the sender is requested to reduce, compared to what it otherwise would send.
        '''
        oc_reduction_percentage = int(oc_reduction_percentage)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.OC_REDUCTION_PERCENTAGE, oc_reduction_percentage, vendor_id)
        self.oc_reduction_percentage = oc_reduction_percentage
   
class OCOLRAVP(DiamAVP_Grouped):
    '''
        Class that defines a OC-OLR AVP message 
        
            OC-OLR ::= < AVP Header: TBD2 >
                     < OC-Sequence-Number >
                     < OC-Report-Type >
                     [ OC-Reduction-Percentage ]
                     [ OC-Validity-Duration ]
    '''
    
    def __init__(self, oc_sequence_number, oc_report_type, oc_reduction_percentage=None, oc_validity_duration=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param visited_plmn_id:
        '''
        
        self.oc_sequence_number = oc_sequence_number
        self.oc_report_type = oc_report_type
        self.oc_reduction_percentage = oc_reduction_percentage
        self.oc_validity_duration = oc_validity_duration
        self.vendor_id = vendor_id
        
        avps = []
        if self.oc_sequence_number is None:
            raise AVPParametersException('OC-OLR AVP :: The oc_sequence_number is MANDATORY')
        a = OCSequenceNumberAVP(self.oc_sequence_number['value'])
        a.setFlags(self.oc_sequence_number['flags'])
        if 'vendor' in self.oc_sequence_number:
            a.setVendorID(self.oc_sequence_number['vendor'])
        avps.append(a)
        
        if self.oc_report_type is None:
            raise AVPParametersException('OC-OLR AVP :: The oc_report_type is MANDATORY')
        a = OCReportTypeAVP(self.oc_report_type['value'])
        a.setFlags(self.oc_report_type['flags'])
        if 'vendor' in self.oc_report_type:
            a.setVendorID(self.oc_report_type['vendor'])
        avps.append(a)
        
        if self.oc_reduction_percentage is not None:
            a = OCReductionPercentageAVP(self.oc_reduction_percentage['value'])
            a.setFlags(self.oc_reduction_percentage['flags'])
            if 'vendor' in self.oc_reduction_percentage:
                a.setVendorID(self.oc_reduction_percentage['vendor'])
            avps.append(a)
        
        if self.oc_validity_duration is not None:
            a = OCValidityDurationAVP(self.oc_validity_duration['value'])
            a.setFlags(self.oc_validity_duration['flags'])
            if 'vendor' in self.oc_validity_duration:
                a.setVendorID(self.oc_validity_duration['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.OC_OLR, avps, self.vendor_id)

class ULAFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a ULA-Flags AVP message 
    '''
    
    def __init__(self, ula_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param ula_flags: [Unsigned32] it shall contain a bit mask.
        '''
        ula_flags = int(ula_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ULA_FLAGS, ula_flags, vendor_id)
        self.ula_flags = ula_flags
   
class ResetIDAVP(DiamAVP_OctetString):
    '''
        Class that defines a Reset-ID AVP message 
    '''
    
    def __init__(self, reset_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param reset_id: [OctetString] the value shall uniquely (within the HSS's realm) identify a resource in the HSS that may fail or has restarted. 
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.RESET_ID, reset_id, vendor_id)
        self.reset_id = reset_id

class AlertReasonAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Alert-Reason AVP message 
    '''
    
    UE_PRESENT              = 0
    UE_MEMORY_AVAILABLE     = 1
    
    def __init__(self, alert_reason = UE_PRESENT, vendor_id=0):
        '''
            Initialize the AVP message
            @param alert_reason: [Unsigned32] Accepted values:
                                                * UE_PRESENT
                                                * UE_MEMORY_AVAILABLE
        '''
        alert_reason = int(alert_reason)
        
        if alert_reason != self.UE_PRESENT and \
           alert_reason != self.UE_MEMORY_AVAILABLE:
            raise AVPParametersException('Alert-Reason AVP :: Incorrect alert_reason value [' + str(alert_reason) + ']')
        
        self.alert_reason = alert_reason
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ALERT_REASON, alert_reason, vendor_id)

class NORFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a NOR-Flags AVP message 
    '''
    
    def __init__(self, nor_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param nor_flags: [Unsigned32] it contains a bit mask.
        '''
        nor_flags = int(nor_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.NOR_FLAGS, nor_flags, vendor_id)
        self.nor_flags = nor_flags

class IMEIAVP(DiamAVP_UTF8String):
    '''
        Class that defines a IMEI AVP message 
    '''
    
    def __init__(self, imei, vendor_id=0):
        '''
            Initialize the AVP message
            @param imei: [UTF8String] the International Mobile Equipment Identity
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.IMEI, imei, vendor_id)
        self.imei = imei

class SoftwareVersionAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Software-Version AVP message 
    '''
    
    def __init__(self, software_version, vendor_id=0):
        '''
            Initialize the AVP message
            @param software_version: [UTF8String] contain the 2-digit Software Version Number (SVN) of the International Mobile Equipment Identity 
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.SOFTWARE_VERSION, software_version, vendor_id)
        self.software_version = software_version

class MEID3GPP2AVP(DiamAVP_OctetString):
    '''
        Class that defines a 3GPP2-MEI AVP message 
    '''
    
    def __init__(self, mei_3gpp2, vendor_id=0):
        '''
            Initialize the AVP message
            @param mei_3gpp2: [OctetString] he Mobile Equipment Identifier of the user's terminal
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.MEID_3GPP2, mei_3gpp2, vendor_id)
        self.mei_3gpp2 = mei_3gpp2

class TerminalInformationAVP(DiamAVP_Grouped):
    '''
        Class that defines a Terminal-Information AVP message 
        
            Terminal-Information ::= <AVP header: 1401 10415>
                                [ IMEI ]
                                [ 3GPP2-MEID ]
                                [ Software-Version ]
    '''
    
    def __init__(self, imei=None, meid_3gpp2=None, software_version=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param visited_plmn_id:
        '''
        
        self.imei = imei
        self.meid_3gpp2 = meid_3gpp2
        self.software_version = software_version
        self.vendor_id = vendor_id
        
        avps = []
        if self.imei is not None:
            a = IMEIAVP(self.imei['value'])
            a.setFlags(self.imei['flags'])
            if 'vendor' in self.imei:
                a.setVendorID(self.imei['vendor'])
            avps.append(a)
            
        if self.meid_3gpp2 is not None:
            a = MEID3GPP2AVP(self.meid_3gpp2['value'])
            a.setFlags(self.meid_3gpp2['flags'])
            if 'vendor' in self.meid_3gpp2:
                a.setVendorID(self.meid_3gpp2['vendor'])
            avps.append(a)
        
        if self.software_version is not None:
            a = SoftwareVersionAVP(self.software_version['value'])
            a.setFlags(self.software_version['flags'])
            if 'vendor' in self.software_version:
                a.setVendorID(self.software_version['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.TERMINAL_INFORMATION, avps, self.vendor_id)

class UserIDAVP(DiamAVP_UTF8String):
    '''
        Class that defines a User-ID AVP message 
    '''
    
    def __init__(self, user_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param user_id: [UTF8String] contains the leading digits of an IMSI formatted as a character string 
        '''
        self.user_id = user_id
        
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.USER_ID, user_id, vendor_id)
        
        

class PURFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a PUR-Flags AVP message 
    '''
    
    def __init__(self, pur_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param pur_flags: [Unsigned32] it contains a bit mask.
        '''
        pur_flags = int(pur_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PUR_FLAGS, pur_flags, vendor_id)
        self.pur_flags = pur_flags

class PUAFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a PUA-Flags AVP message 
    '''
    
    def __init__(self, pua_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param pur_flags: [Unsigned32] it contains a bit mask.
        '''
        pua_flags = int(pua_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PUA_FLAGS, pua_flags, vendor_id)
        self.pua_flags = pua_flags

class NumberRequestedVectorsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Number-Requested-Vectors AVP message 
    '''
    
    def __init__(self, num_req_vectors, vendor_id=0):
        '''
            Initialize the AVP message
            @param num_req_vectors: [Unsigned32] it contains the number of AVs the MME or SGSN is prepared to receive.
        '''
        num_req_vectors = int(num_req_vectors)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.NUMBER_OF_REQUESTED_VECTORS, num_req_vectors, vendor_id)
        self.num_req_vectors = num_req_vectors

class ImmediateResponsePreferredAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Immediate-Response-Preferred AVP message 
    '''
    
    def __init__(self, immediate_response_preferred, vendor_id=0):
        '''
            Initialize the AVP message
            @param immediate_response_preferred: [Unsigned32] indicates by its presence that immediate response is preferred, and by its absence that immediate response is not preferred. If present, the value of this AVP is not significant.
        '''
        immediate_response_preferred = int(immediate_response_preferred)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.IMMEDIATE_RESPONSE_PREFERRED, immediate_response_preferred, vendor_id)
        self.immediate_response_preferred = immediate_response_preferred

class ReSyncronizationInfoAVP(DiamAVP_OctetString):
    '''
        Class that defines a Re-Syncronization-Info AVP message 
    '''
    
    def __init__(self, re_sync_info, vendor_id=0):
        '''
            Initialize the AVP message
            @param re_sync_info: [OctetString] it contains the concatenation of RAND and AUTS.
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.RE_SYNCRONIZATION_INFO, re_sync_info, vendor_id)
        self.re_sync_info = re_sync_info

class RequestedEUTRANAuthenticationInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a Requested-EUTRAN-Authentication-Info AVP message 
        
            Requested-EUTRAN-Authentication-Info ::= <AVP header: 1408 10415>
                                [ Number-Of-Requested-Vectors ]
                                [ Immediate-Response-Preferred ]
                                [ Re-synchronization-Info ]
    '''
    
    def __init__(self, number_req_vectors=None, immmediate_response_preferred=None, re_sync_info=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param number_req_vectors:
            @param immmediate_response_preferred:
            @param re_sync_info:
        '''
        
        self.number_req_vectors = number_req_vectors
        self.immmediate_response_preferred = immmediate_response_preferred
        self.re_sync_info = re_sync_info
        self.vendor_id = vendor_id
        
        avps = []
        if self.number_req_vectors is not None:
            a = NumberRequestedVectorsAVP(self.number_req_vectors['value'])
            a.setFlags(self.number_req_vectors['flags'])
            if 'vendor' in self.number_req_vectors:
                a.setVendorID(self.number_req_vectors['vendor'])
            avps.append(a)
            
        if self.immmediate_response_preferred is not None:
            a = ImmediateResponsePreferredAVP(self.immmediate_response_preferred['value'])
            a.setFlags(self.immmediate_response_preferred['flags'])
            if 'vendor' in self.immmediate_response_preferred:
                a.setVendorID(self.immmediate_response_preferred['vendor'])
            avps.append(a)
        
        if self.re_sync_info is not None:
            a = ReSyncronizationInfoAVP(self.re_sync_info['value'])
            a.setFlags(self.re_sync_info['flags'])
            if 'vendor' in self.re_sync_info:
                a.setVendorID(self.re_sync_info['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.REQUESTED_EUTRAN_AUTHENTICATION_INFO, avps, self.vendor_id)

class RequestedUTRANGERANAuthenticationInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a Requested-UTRAN-GERAN-Authentication-Info AVP message 
        
            Requested-UTRAN-GERAN-Authentication-Info ::= <AVP header: 1409 10415>
                                [ Number-Of-Requested-Vectors]
                                [ Immediate-Response-Preferred ]
                                [ Re-synchronization-Info ]
    '''
    
    def __init__(self, number_req_vectors=None, immmediate_response_preferred=None, re_sync_info=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param number_req_vectors:
            @param immmediate_response_preferred:
            @param re_sync_info:
        '''
        
        self.number_req_vectors = number_req_vectors
        self.immmediate_response_preferred = immmediate_response_preferred
        self.re_sync_info = re_sync_info
        self.vendor_id = vendor_id
        
        avps = []
        if self.number_req_vectors is not None:
            a = NumberRequestedVectorsAVP(self.number_req_vectors['value'])
            a.setFlags(self.number_req_vectors['flags'])
            if 'vendor' in self.number_req_vectors:
                a.setVendorID(self.number_req_vectors['vendor'])
            avps.append(a)
            
        if self.immmediate_response_preferred is not None:
            a = ImmediateResponsePreferredAVP(self.immmediate_response_preferred['value'])
            a.setFlags(self.immmediate_response_preferred['flags'])
            if 'vendor' in self.immmediate_response_preferred:
                a.setVendorID(self.immmediate_response_preferred['vendor'])
            avps.append(a)
        
        if self.re_sync_info is not None:
            a = ReSyncronizationInfoAVP(self.re_sync_info['value'])
            a.setFlags(self.re_sync_info['flags'])
            if 'vendor' in self.re_sync_info:
                a.setVendorID(self.re_sync_info['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.REQUESTED_UTRAN_GERAN_AUTHENTICATION_INFO, avps, self.vendor_id)

class SubscriberStatusAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Subscriber-Status AVP message 
    '''
    
    SERVICE_GRANTED                 = 0
    OPERATOR_DETERMINED_BARRING     = 1
    
    def __init__(self, subscriber_status = SERVICE_GRANTED, vendor_id=0):
        '''
            Initialize the AVP message
            @param subscriber_status: [Unsigned32] Accepted values:
                                                * SERVICE_GRANTED
                                                * OPERATOR_DETERMINED_BARRING
        '''
        subscriber_status = int(subscriber_status)
        
        if subscriber_status != self.SERVICE_GRANTED and \
           subscriber_status != self.OPERATOR_DETERMINED_BARRING:
            raise AVPParametersException('Subscriber-Status AVP :: Incorrect subscriber_status value [' + str(subscriber_status) + ']')
        
        self.subscriber_status = subscriber_status
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SUBSCRIBER_STATUS, subscriber_status, vendor_id)

class AMSISDNAVP(DiamAVP_OctetString):
    '''
        Class that defines a A-MSISDN AVP message 
    '''
    
    def __init__(self, a_msisdn, vendor_id=0):
        '''
            Initialize the AVP message
            @param a_msisdn: [OctetString] it contains an A-MSISDN, in international number format encoded as a TBCD-string
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.A_MSISDN, a_msisdn, vendor_id)
        self.a_msisdn = a_msisdn

class STNSRAVP(DiamAVP_OctetString):
    '''
        Class that defines a STN-SR AVP message 
    '''
    
    def __init__(self, stn_sr, vendor_id=0):
        '''
            Initialize the AVP message
            @param stn_sr: [OctetString] it contains the Session Transfer Number for SRVCC.
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.STN_SR, stn_sr, vendor_id)
        self.stn_sr = stn_sr

class ICSIndicatorAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a ICS-Indicator AVP message 
    '''
    
    FALSE   = 0
    TRUE    = 1
    
    def __init__(self, ics_indicator = FALSE, vendor_id=0):
        '''
            Initialize the AVP message
            @param ics_indicator: [Unsigned32] Accepted values:
                                                * FALSE
                                                * TRUE
        '''
        ics_indicator = int(ics_indicator)
        
        if ics_indicator != self.FALSE and \
           ics_indicator != self.TRUE:
            raise AVPParametersException('ICS-Indicator AVP :: Incorrect ics_indicator value [' + str(ics_indicator) + ']')
        
        self.ics_indicator = ics_indicator
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ICS_INDICATOR, ics_indicator, vendor_id)

class NetworkAccessModeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Network-Access-Mode AVP message 
    '''
    
    PACKET_AND_CIRCUIT  = 0
    RESERVED            = 1
    ONLY_PACKET         = 2
    
    def __init__(self, network_access = PACKET_AND_CIRCUIT, vendor_id=0):
        '''
            Initialize the AVP message
            @param network_access: [Unsigned32] Accepted values:
                                                * PACKET_AND_CIRCUIT
                                                * RESERVED
                                                * ONLY_PACKET
        '''
        network_access = int(network_access)
        
        if network_access != self.PACKET_AND_CIRCUIT and \
           network_access != self.RESERVED and \
           network_access != self.ONLY_PACKET:
            raise AVPParametersException('Network-Access-Mode AVP :: Incorrect network_access value [' + str(network_access) + ']')
        
        self.network_access = network_access
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.NETWORK_ACCESS_MODE, network_access, vendor_id)

class OperatorDeterminedBarringAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Operator-Determined-Barring AVP message 
    '''
    
    def __init__(self, operator_determined_barring, vendor_id=0):
        '''
            Initialize the AVP message
            @param operator_determined_barring: [Unsigned32] it contains a bit mask indicating the services of a subscriber that are barred by the operator. 
        '''
        operator_determined_barring = int(operator_determined_barring)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.OPERATOR_DETERMINED_BARRING, operator_determined_barring, vendor_id)
        self.operator_determined_barring = operator_determined_barring

class HPLMNODBAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a HPLMN-ODB AVP message 
    '''
    
    def __init__(self, hplmn_odb, vendor_id=0):
        '''
            Initialize the AVP message
            @param hplmn_odb: [Unsigned32] it contains a bit mask indicating the HPLMN specific services of a subscriber that are barred by the operator. 
        '''
        hplmn_odb = int(hplmn_odb)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.HPLMN_ODB, hplmn_odb, vendor_id)
        self.hplmn_odb = hplmn_odb

class RegionalSubscriptionZoneCodeAVP(DiamAVP_OctetString):
    '''
        Class that defines a Regional-Subscription-Zone-Code AVP message 
    '''
    
    def __init__(self, reg_subscript_zone_code, vendor_id=0):
        '''
            Initialize the AVP message
            @param reg_subscript_zone_code: [OctetString] it contains a Zone Code (ZC).
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.REGIONAL_SUBSCRIPTION_ZONE_CODE, reg_subscript_zone_code, vendor_id)
        self.reg_subscript_zone_code = reg_subscript_zone_code

class AccessRestrictionDataAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Access-Restriction-Data AVP message 
    '''
    
    def __init__(self, access_restriction_data, vendor_id=0):
        '''
            Initialize the AVP message
            @param access_restriction_data: [Unsigned32] it contains a bit mask where each bit when set to 1 indicates a restriction. 
        '''
        access_restriction_data = int(access_restriction_data)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ACCESS_RESTRICTION_DATA, access_restriction_data, vendor_id)
        self.access_restriction_data = access_restriction_data

class APNOIReplacementAVP(DiamAVP_UTF8String):
    '''
        Class that defines a APN-OI-Replacement AVP message 
    '''
    
    def __init__(self, apn_oi_replacement, vendor_id=0):
        '''
            Initialize the AVP message
            @param apn_oi_replacement: [UTF8String] it indicate the domain name to replace the APN OI for the non-roaming case and the home routed roaming case when constructing the APN, and the APN-FQDN upon which to perform a DNS resolution. 
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.APN_OI_REPLACEMENT, apn_oi_replacement, vendor_id)
        self.apn_oi_replacement = apn_oi_replacement

class TeleserviceListAVP(DiamAVP_Grouped):
    '''
        Class that defines a Teleservice-List AVP message 
        
            Teleservice-List ::= <AVP header: 1486 10415>
                            1 * { TS-Code }
    '''
    
    def __init__(self, ts_code, vendor_id=0):
        '''
            Initialize the AVP message
            @param ts_code:
        '''
        
        self.ts_code = ts_code
        if not isinstance(self.ts_code, list):
            self.ts_code = [self.ts_code]
        self.vendor_id = vendor_id

        avps = []
        if self.ts_code is None:
            raise AVPParametersException('Teleservice-List AVP :: The ts_code is MANDATORY')
        for tsc in self.ts_code:
            a = TSCodeAVP(tsc['value'])
            a.setFlags(tsc['flags'])
            if 'vendor' in tsc:
                a.setVendorID(tsc['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.TELESERVICE_LIST, avps, self.vendor_id)

class SSStatusAVP(DiamAVP_OctetString):
    '''
        Class that defines a SS-Status AVP message 
    '''
    
    def __init__(self, ss_status, vendor_id=0):
        '''
            Initialize the AVP message
            @param ss_status: [OctetString] 
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.SS_STATUS, ss_status, vendor_id)
        self.ss_status = ss_status

class CallBarringInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a Call-Barring-Info AVP message 
        
            Call-Barring-Info ::= <AVP header: 1488 10415>
                                { SS-Code }
                                { SS-Status }
    '''
    
    def __init__(self, ss_code, ss_status, vendor_id=0):
        '''
            Initialize the AVP message
            @param ss_code:
            @param ss_status:
        '''
        
        self.ss_code = ss_code
        self.ss_status = ss_status
        self.vendor_id = vendor_id
        
        avps = []
        if self.ss_code is None:
            raise AVPParametersException('Call-Barring-Info AVP :: The ss_code is MANDATORY')
        a = SSCodeAVP(self.ss_code['value'])
        a.setFlags(self.ss_code['flags'])
        if 'vendor' in self.ss_code:
            a.setVendorID(self.ss_code['vendor'])
        avps.append(a)
        
        if self.ss_status is None:
            raise AVPParametersException('Call-Barring-Info AVP :: The ss_status is MANDATORY')
        a = SSStatusAVP(self.ss_status['value'])
        a.setFlags(self.ss_status['flags'])
        if 'vendor' in self.ss_status:
            a.setVendorID(self.ss_status['vendor'])
        avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.CALL_BARRING_INFO, avps, self.vendor_id)

class MaxRequestBandwidthULAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Max-Request-Bandwidth-UL AVP message 
    '''
    
    def __init__(self, max_req_bandwidth_ul, vendor_id=0):
        '''
            Initialize the AVP message
            @param max_req_bandwidth_ul: [Unsigned32]  it indicates the maximum requested sbandwidth in bits per second for an uplink IP flow. 
        '''
        max_req_bandwidth_ul = int(max_req_bandwidth_ul)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.MAX_REQUEST_BANDWIDTH_UL, max_req_bandwidth_ul, vendor_id)
        self.max_req_bandwidth_ul = max_req_bandwidth_ul

class MaxRequestBandwidthDLAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Max-Request-Bandwidth-DL AVP message 
    '''
    
    def __init__(self, max_req_bandwidth_dl, vendor_id=0):
        '''
            Initialize the AVP message
            @param max_req_bandwidth_dl: [Unsigned32] it indicates the maximum bandwidth in bits per second for a downlink IP flow.  
        '''
        max_req_bandwidth_dl = int(max_req_bandwidth_dl)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.MAX_REQUEST_BANDWIDTH_DL, max_req_bandwidth_dl, vendor_id)
        self.max_req_bandwidth_dl = max_req_bandwidth_dl

class AMBRAVP(DiamAVP_Grouped):
    '''
        Class that defines a AMBR AVP message 
        
            AMBR ::= <AVP header: 1435 10415>
                { Max-Requested-Bandwidth-UL }
                { Max-Requested-Bandwidth-DL }
    '''
    
    def __init__(self, max_req_bandwidth_ul, max_req_bandwidth_dl, vendor_id=0):
        '''
            Initialize the AVP message
            @param max_req_bandwidth_ul:
            @param max_req_bandwidth_dl:
        '''
        
        self.max_req_bandwidth_ul = max_req_bandwidth_ul
        self.max_req_bandwidth_dl = max_req_bandwidth_dl
        self.vendor_id = vendor_id
        
        if self.max_req_bandwidth_dl is not None and \
           int(self.max_req_bandwidth_dl['value']) == 0 and \
           self.max_req_bandwidth_ul is not None and \
           int(self.max_req_bandwidth_ul['value']) == 0:
            raise AVPParametersException('AMBR AVP :: Max-Requested-Bandwidth-UL and Max-Requested-Bandwidth-DL shall not both be set to "0".')
        
        avps = []
        if self.max_req_bandwidth_ul is None:
            raise AVPParametersException('AMBR AVP :: The max_req_bandwidth_ul is MANDATORY')
        a = MaxRequestBandwidthULAVP(self.max_req_bandwidth_ul['value'])
        a.setFlags(self.max_req_bandwidth_ul['flags'])
        if 'vendor' in self.max_req_bandwidth_ul:
            a.setVendorID(self.max_req_bandwidth_ul['vendor'])
        avps.append(a)
        
        if self.max_req_bandwidth_dl is None:
            raise AVPParametersException('AMBR AVP :: The max_req_bandwidth_dl is MANDATORY')
        a = MaxRequestBandwidthDLAVP(self.max_req_bandwidth_dl['value'])
        a.setFlags(self.max_req_bandwidth_dl['flags'])
        if 'vendor' in self.max_req_bandwidth_dl:
            a.setVendorID(self.max_req_bandwidth_dl['vendor'])
        avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.AMBR, avps, self.vendor_id)

class AllAPNConfigurationsIncludedIndicatorAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a All-APN-Configurations-Included-Indicator AVP message 
    '''
    
    All_APN_CONFIGURATIONS_INCLUDED                 = 0
    MODIFIED_ADDED_APN_CONFIGURATIONS_INCLUDED      = 1
    
    def __init__(self, all_apn_config_included_indicator = All_APN_CONFIGURATIONS_INCLUDED, vendor_id=0):
        '''
            Initialize the AVP message
            @param all_apn_config_included_indicator: [Unsigned32] Accepted values:
                                                        * All_APN_CONFIGURATIONS_INCLUDED
                                                        * MODIFIED_ADDED_APN_CONFIGURATIONS_INCLUDED
        '''
        all_apn_config_included_indicator = int(all_apn_config_included_indicator)
        
        if all_apn_config_included_indicator != self.All_APN_CONFIGURATIONS_INCLUDED and \
           all_apn_config_included_indicator != self.MODIFIED_ADDED_APN_CONFIGURATIONS_INCLUDED:
            raise AVPParametersException('All-APN-Configurations-Included-Indicator AVP :: Incorrect all_apn_config_included_indicator value [' + str(all_apn_config_included_indicator) + ']')
        
        self.all_apn_config_included_indicator = all_apn_config_included_indicator
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ALL_APN_CONFIGURATIONS_INCLUDED_INDICATOR, all_apn_config_included_indicator, vendor_id)

class APNConfigurationProfileAVP(DiamAVP_Grouped):
    '''
        Class that defines a APN-Configuration-Profile AVP message 
        
            APN-Configuration-Profile ::= <AVP header: 1429 10415>
                                        { Context-Identifier }
                                        { All-APN-Configurations-Included-Indicator }
                                        1*{APN-Configuration}
    '''
    
    def __init__(self, context_id, all_apn_config_included_indicator, apn_config, vendor_id=0):
        '''
            Initialize the AVP message
            @param context_id:
            @param all_apn_config_included_indicator:
            @param apn_config:
        '''
        
        self.context_id = context_id
        self.all_apn_config_included_indicator = all_apn_config_included_indicator
        self.apn_config = apn_config
        if self.apn_config is not None and not isinstance(self.apn_config, list):
            self.apn_config = [self.apn_config]
        self.vendor_id = vendor_id
        
        avps = []            
        if self.context_id is None:
            raise AVPParametersException('APN-Configuration-Profile AVP :: The context_id is MANDATORY')
        a = ContextIentifierAVP(self.context_id['value'])
        a.setFlags(self.context_id['flags'])
        if 'vendor' in self.context_id:
            a.setVendorID(self.context_id['vendor'])
        avps.append(a)
        
        if self.all_apn_config_included_indicator is None:
            raise AVPParametersException('APN-Configuration-Profile AVP :: The all_apn_config_included_indicator is MANDATORY')
        a = AllAPNConfigurationsIncludedIndicatorAVP(self.all_apn_config_included_indicator['value'])
        a.setFlags(self.all_apn_config_included_indicator['flags'])
        if 'vendor' in self.all_apn_config_included_indicator:
            a.setVendorID(self.all_apn_config_included_indicator['vendor'])
        avps.append(a)
        
        if self.apn_config is None:
            raise AVPParametersException('APN-Configuration-Profile AVP :: The APN-Configuration is MANDATORY')
        if self.apn_config == []:
            raise AVPParametersException('APN-Configuration-Profile AVP :: APN-Configuration CANNOT be empty.')
        logging.warning('APN-Configuration-Profile AVP :: APN-Configuration AVP NOT YET IMPLEMENTED')
        '''
        for ac in self.apn_config:
            a = APNConfigurationAVP(ac['value'])
            a.setFlags(ac['flags'])
            if 'vendor' in ac:
                a.setVendorID(ac['vendor'])
            avps.append(a)
        '''   
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.APN_CONFIGURATION_PROFILE, avps, self.vendor_id)

class RATFrequencySelectionPriorityIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a RAT-Frequency-Selection-Priority-Id AVP message 
    '''
    
    def __init__(self, rat_freq_prio, vendor_id=0):
        '''
            Initialize the AVP message
            @param rat_freq_prio: [Unsigned32] it contains the subscribed value of Subscriber Profile ID for RAT/Frequency Priority.  
        '''
        rat_freq_prio = int(rat_freq_prio)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.RAT_FREQUENCY_SELECTION_PRIORITY_ID, rat_freq_prio, vendor_id)
        self.rat_freq_prio = rat_freq_prio

class RoamingRestrictedDueToUnsupportedFeatureAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Roaming-Restricted-Due-To-Unsupported-Feature AVP message 
    '''
    
    ROAMING_RESTRICTED_DUE_TO_UNSUPPORTED_FEATURE   = 0
    
    def __init__(self, roaming_restricted = ROAMING_RESTRICTED_DUE_TO_UNSUPPORTED_FEATURE, vendor_id=0):
        '''
            Initialize the AVP message
            @param roaming_restricted: [Unsigned32] Accepted values:
                                            * ROAMING_RESTRICTED_DUE_TO_UNSUPPORTED_FEATURE
        '''
        roaming_restricted = int(roaming_restricted)
        
        if roaming_restricted != self.ROAMING_RESTRICTED_DUE_TO_UNSUPPORTED_FEATURE:
            raise AVPParametersException('Roaming-Restricted-Due-To-Unsupported-Feature AVP :: Incorrect roaming_restricted value [' + str(roaming_restricted) + ']')
        
        self.roaming_restricted = roaming_restricted
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ROAMING_RESTRICTED_DUE_TO_UNSUPPORTED_FEATURE, roaming_restricted, vendor_id)

class SubscribedPeriodicRAUTAUTimerAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Subscribed-Periodic-RAU-TAU-Timer AVP message 
    '''
    
    def __init__(self, subscrib_periodic_rau_tau_timer, vendor_id=0):
        '''
            Initialize the AVP message
            @param subscrib_periodic_rau_tau_timer: [Unsigned32] it contains the subscribed periodic RAU/TAU timer value in seconds.  
        '''
        subscrib_periodic_rau_tau_timer = int(subscrib_periodic_rau_tau_timer)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SUBSCRIBED_PERIODIC_RAU_TAU_TIMER, subscrib_periodic_rau_tau_timer, vendor_id)
        self.subscrib_periodic_rau_tau_timer = subscrib_periodic_rau_tau_timer

class MPSPriorityAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a MPS-Priority AVP message 
    '''
    
    def __init__(self, mps_priority, vendor_id=0):
        '''
            Initialize the AVP message
            @param mps_priority: [Unsigned32] it contains a bitmask.  
        '''
        mps_priority = int(mps_priority)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.MPS_PRIORITY, mps_priority, vendor_id)
        self.mps_priority = mps_priority

class VPLMNLIPAAllowedAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a VPLMN-LIPA-Allowed AVP message 
    '''
    
    LIPA_NOTALLOWED     = 0
    LIPA_ALLOWED        = 1
    
    def __init__(self, vplmn_lipa_allowed = LIPA_NOTALLOWED, vendor_id=0):
        '''
            Initialize the AVP message
            @param vplmn_lipa_allowed: [Unsigned32] Accepted values:
                                                        * LIPA_NOTALLOWED
                                                        * LIPA_ALLOWED
        '''
        vplmn_lipa_allowed = int(vplmn_lipa_allowed)
        
        if vplmn_lipa_allowed != self.LIPA_NOTALLOWED and \
           vplmn_lipa_allowed != self.LIPA_ALLOWED:
            raise AVPParametersException('VPLMN-LIPA-Allowed AVP :: Incorrect vplmn_lipa_allowed value [' + str(vplmn_lipa_allowed) + ']')
        
        self.vplmn_lipa_allowed = vplmn_lipa_allowed
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.VPLMN_LIPA_ALLOWED, vplmn_lipa_allowed, vendor_id)

class RelayNodeIndicatorAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Relay-Node-Indicator AVP message 
    '''
    
    NOT_RELAY_NODE      = 0
    RELAY_NODE          = 1
    
    def __init__(self, relay_node_indicator = NOT_RELAY_NODE, vendor_id=0):
        '''
            Initialize the AVP message
            @param relay_node_indicator: [Unsigned32] Accepted values:
                                                * NOT_RELAY_NODE
                                                * RELAY_NODE
        '''
        relay_node_indicator = int(relay_node_indicator)
        
        if relay_node_indicator != self.NOT_RELAY_NODE and \
           relay_node_indicator != self.RELAY_NODE:
            raise AVPParametersException('Relay-Node-Indicator AVP :: Incorrect relay_node_indicator value [' + str(relay_node_indicator) + ']')
        
        self.relay_node_indicator = relay_node_indicator
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.RELAY_NODE_INDICATOR, relay_node_indicator, vendor_id)

class MDTUserConsentAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a MDT-User-Consent AVP message 
    '''
    
    CONSENT_NOT_GIVEN      = 0
    CONSENT_GIVEN          = 1
    
    def __init__(self, mdt_user_consent = CONSENT_NOT_GIVEN, vendor_id=0):
        '''
            Initialize the AVP message
            @param mdt_user_consent: [Unsigned32] Accepted values:
                                                * CONSENT_NOT_GIVEN
                                                * CONSENT_GIVEN
        '''
        mdt_user_consent = int(mdt_user_consent)
        
        if mdt_user_consent != self.CONSENT_NOT_GIVEN and \
           mdt_user_consent != self.CONSENT_GIVEN:
            raise AVPParametersException('MDT-User-Consent AVP :: Incorrect mdt_user_consent value [' + str(mdt_user_consent) + ']')
        
        self.mdt_user_consent = mdt_user_consent
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.MDT_USER_CONSENT, mdt_user_consent, vendor_id)

class SubscribedVSRVCCAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Subscribed-VSRVCC AVP message 
    '''
    
    VSRVCC_SUBSCRIBED   = 0
    
    def __init__(self, subscribed_vsrvcc = VSRVCC_SUBSCRIBED, vendor_id=0):
        '''
            Initialize the AVP message
            @param subscribed_vsrvcc: [Unsigned32] Accepted values:
                                                * VSRVCC_SUBSCRIBED
        '''
        subscribed_vsrvcc = int(subscribed_vsrvcc)
        
        if subscribed_vsrvcc != self.VSRVCC_SUBSCRIBED:
            raise AVPParametersException('Subscribed-VSRVCC AVP :: Incorrect subscribed_vsrvcc value [' + str(subscribed_vsrvcc) + ']')
        
        self.subscribed_vsrvcc = subscribed_vsrvcc
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SUBSCRIBED_VSRVCC, subscribed_vsrvcc, vendor_id)

class ProSePermissionAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a ProSe-Permission AVP message 
    '''
    def __init__(self, prose_perm, vendor_id=0):
        '''
            Initialize the AVP message
            @param prose_perm: [Unsigned32] it contains a bit mask that indicates the permissions for ProSe subscribed by the user.
        '''
        prose_perm = int(prose_perm)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PROSE_PERMISSION, prose_perm, vendor_id)
        self.prose_perm = prose_perm

class ProseSubscriptionDataAVP(DiamAVP_Grouped):
    '''
        Class that defines a Prose-Subscription-Data AVP message 
        
            ProSe-Subscription-Data ::= <AVP header: xxx 10415>
                                    { ProSe-Permission }
    '''
    
    def __init__(self, prose_perm, vendor_id=0):
        '''
            Initialize the AVP message
            @param prose_perm:
        '''
        
        self.prose_perm = prose_perm
        
        avps = []            
        if self.prose_perm is None:
            raise AVPParametersException('ProSe-Subscription-Data AVP :: The prose_perm is MANDATORY')
        a = ProSePermissionAVP(self.prose_perm['value'])
        a.setFlags(self.prose_perm['flags'])
        if 'vendor' in self.prose_perm:
            a.setVendorID(self.prose_perm['vendor'])
        avps.append(a)

        DiamAVP_Grouped.__init__(self, DiamAVPCodes.PROSE_SUBSCRIPTION_DATA, avps, self.vendor_id)

class SubscriptionDataFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Subscription-Data-Flags AVP message 
    '''
    
    def __init__(self, subscript_data_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param subscript_data_flags: [Unsigned32] it contains a bitmask 
        '''
        subscript_data_flags = int(subscript_data_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SUBSCRIPTION_DATA_FLAGS, subscript_data_flags, vendor_id)
        self.subscript_data_flags = subscript_data_flags

class AdjacentAccessRestrictionDataAVP(DiamAVP_Grouped):
    '''
        Class that defines a Adjacent-Access-Restriction-Data AVP message 
        
            Adjacent-Access-Restriction-Data ::= <AVP header: 1673 10415>
                                                { Visited-PLMN-Id }
                                                { Access-Restriction-Data }
    '''
    
    def __init__(self, visited_plmn_id, access_restriction_data, vendor_id=0):
        '''
            Initialize the AVP message
            @param visited_plmn_id:
            @param access_restriction_data:
        '''
        
        self.visited_plmn_id = visited_plmn_id
        self.access_restriction_data = access_restriction_data
        
        avps = []
        if self.visited_plmn_id is None:
            raise AVPParametersException('Adjacent-Access-Restriction-Data AVP :: The visited_plmn_id is MANDATORY')
        a = VisitedPLMNIDAVP(self.visited_plmn_id['value'])
        a.setFlags(self.visited_plmn_id['flags'])
        if 'vendor' in self.visited_plmn_id:
            a.setVendorID(self.visited_plmn_id['vendor'])
        avps.append(a)
            
        if self.access_restriction_data is None:
            raise AVPParametersException('Adjacent-Access-Restriction-Data AVP :: The access_restriction_data is MANDATORY')
        a = AccessRestrictionDataAVP(self.access_restriction_data['value'])
        a.setFlags(self.access_restriction_data['flags'])
        if 'vendor' in self.access_restriction_data:
            a.setVendorID(self.access_restriction_data['vendor'])
        avps.append(a)

        DiamAVP_Grouped.__init__(self, DiamAVPCodes.ADJACENT_ACCESS_RESTRICTION_DATA, avps, self.vendor_id)

class DLBufferingSuggestedPacketCountAVP(DiamAVP_Integer32):
    '''
        Class that defines a DL-Buffering-Suggested-Packet-Count AVP message 
    '''
    
    NOT_REQUESTED                   = 0
    REQUESTED_WITHOUT_SUGGESTION    = -1
    
    def __init__(self, dl_buffering_suggested_packet_count, vendor_id=0):
        '''
            Initialize the AVP message
            @param dl_buffering_suggested_packet_count: [Integer32] it indicate whether extended buffering of downlink packets at the SGW, for High Latency Communication, is requested or not.
        '''
        dl_buffering_suggested_packet_count = int(dl_buffering_suggested_packet_count)
        
        self.dl_buffering_suggested_packet_count = dl_buffering_suggested_packet_count
        DiamAVP_Integer32.__init__(self, DiamAVPCodes.DL_BUFFERING_SUGGESTED_PACKET_COUNT, dl_buffering_suggested_packet_count, vendor_id)

class GroupServiceIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Group-Serivece-Id AVP message 
    '''
    
    def __init__(self, group_service_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param group_service_id: [Unsigned32] it contains a bitmask 
        '''
        group_service_id = int(group_service_id)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.GROUP_SERVICE_ID, group_service_id, vendor_id)
        self.group_service_id = group_service_id

class GroupPLMNIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Group-PLMN-Id AVP message 
    '''
    
    def __init__(self, group_plmn_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param group_plmn_id: [Unsigned32] it contains a bitmask 
        '''
        group_plmn_id = int(group_plmn_id)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.GROUP_PLMN_ID, group_plmn_id, vendor_id)
        self.group_plmn_id = group_plmn_id

class LocalGroupIDAVP(DiamAVP_OctetString):
    '''
        Class that defines a Local-Group-Id AVP message 
    '''
    
    def __init__(self, local_group_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param local_group_id: [OctetString] 
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.LOCAL_GROUP_ID, local_group_id, vendor_id)
        self.local_group_id = local_group_id

class IMSIGroupIDAVP(DiamAVP_Grouped):
    '''
        Class that defines a IMSI-Group AVP message 
        
            IMSI-Group-Id ::= <AVP header: 1675 10415>
                            { Group-Service-Id }
                            { Group-PLMN-Id }
                            { Local-Group-Id }
    '''
    
    def __init__(self, group_service_id, group_plmn_id, local_group_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param group_service_id:
            @param group_plmn_id:
            @param local_group_id:
        '''
        
        self.group_service_id = group_service_id
        self.group_plmn_id = group_plmn_id
        self.local_group_id = local_group_id
        
        avps = []
        if self.group_service_id is None:
            raise AVPParametersException('IMSI-Group-Id AVP :: The group_service_id is MANDATORY')
        a = GroupServiceIDAVP(self.group_service_id['value'])
        a.setFlags(self.group_service_id['flags'])
        if 'vendor' in self.group_service_id:
            a.setVendorID(self.group_service_id['vendor'])
        avps.append(a)
        
        if self.group_plmn_id is None:
            raise AVPParametersException('IMSI-Group-Id AVP :: The group_plmn_id is MANDATORY')
        a = GroupPLMNIDAVP(self.group_plmn_id['value'])
        a.setFlags(self.group_plmn_id['flags'])
        if 'vendor' in self.group_plmn_id:
            a.setVendorID(self.group_plmn_id['vendor'])
        avps.append(a)
            
        if self.local_group_id is None:
            raise AVPParametersException('IMSI-Group-Id AVP :: The local_group_id is MANDATORY')
        a = LocalGroupIDAVP(self.local_group_id['value'])
        a.setFlags(self.local_group_id['flags'])
        if 'vendor' in self.local_group_id:
            a.setVendorID(self.local_group_id['vendor'])
        avps.append(a)

        DiamAVP_Grouped.__init__(self, DiamAVPCodes.IMSI_GROUP_ID, avps, self.vendor_id)

''' FIXME: to manage. To implement...now on raw data '''
class SubscriptionDataAVP(DiamAVP_Grouped):
    '''
        Class that defines a Subscription-Data AVP message 
        
            Subscription-Data ::= <AVP header: 1400 10415>
                                [ Subscriber-Status ]
                                [ MSISDN ]
                                [ A-MSISDN ]
                                [ STN-SR ]
                                [ ICS-Indicator ]
                                [ Network-Access-Mode ]
                                [ Operator-Determined-Barring ]
                                [ HPLMN-ODB ]
                                *10[ Regional-Subscription-Zone-Code ]
                                [ Access-Restriction-Data ]
                                [ APN-OI-Replacement ]
                                [ LCS-Info ]
                                [ Teleservice-List ]
                                *[ Call-Barring-Info ]
                                [ 3GPP-Charging-Characteristics ]
                                [ AMBR ]
                                [ APN-Configuration-Profile ]
                                [ RAT-Frequency-Selection-Priority-ID ]
                                [ Trace-Data]
                                [ GPRS-Subscription-Data ]
                                *[ CSG-Subscription-Data ]
                                [ Roaming-Restricted-Due-To-Unsupported-Feature ]
                                [ Subscribed-Periodic-RAU-TAU-Timer ]
                                [ MPS-Priority ]
                                [ VPLMN-LIPA-Allowed ]
                                [ Relay-Node-Indicator ]
                                [ MDT-User-Consent ]
                                [ Subscribed-VSRVCC ]
                                [ ProSe-Subscription-Data ]
                                [ Subscription-Data-Flags ]
                                *[ Adjacent-Access-Restriction-Data ]
                                [ DL-Buffering-Suggested-Packet-Count ]
                                *[ IMSI-Group-Id ]
                                *[ AESE-Communication-Pattern ]
    '''
    
    def __init__(self,
                 subscriber_status=None,
                 msisdn=None,
                 a_msisdn=None,
                 stn_sr=None,
                 ics_indicator=None,
                 network_access_mode=None,
                 operator_determined_barring=None,
                 hplmn_odb=None,
                 regional_subscription_zone_code=None,
                 access_restriction_data=None,
                 apn_oi_replacement=None,
                 lcs_info=None,
                 teleservice_list=None,
                 call_barring_info=None,
                 charging_characteristics_3gpp=None,
                 ambr=None,
                 apn_configuration_profile=None,
                 rat_frequency_selection_priority_id=None,
                 trace_data=None,
                 gprs_subscription_data=None,
                 csg_subscription_data=None,
                 roaming_restricted_due_to_unsupported_feature=None,
                 subscribed_periodic_rau_tau_timer=None,
                 mps_priority=None,
                 vplmn_lipa_allowed=None,
                 relay_node_indicator=None,
                 mdt_user_consent=None,
                 subscribed_vsrvcc=None,
                 prose_subscription_data=None,
                 subscription_data_flags=None,
                 adjacent_access_restriction_data=None,
                 dl_buffering_suggested_packet_count=None,
                 imsi_group_id=None,
                 aese_communication_pattern=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
        '''
        
        self.subscriber_status = subscriber_status
        self.msisdn = msisdn
        self.a_msisdn = a_msisdn
        self.stn_sr = stn_sr
        self.ics_indicator = ics_indicator
        self.network_access_mode = network_access_mode
        self.operator_determined_barring = operator_determined_barring
        self.hplmn_odb = hplmn_odb
        self.regional_subscription_zone_code = regional_subscription_zone_code
        self.access_restriction_data = access_restriction_data
        self.apn_oi_replacement = apn_oi_replacement
        self.lcs_info = lcs_info
        self.teleservice_list = teleservice_list
        self.call_barring_info = call_barring_info
        self.charging_characteristics_3gpp = charging_characteristics_3gpp
        self.ambr = ambr
        self.apn_configuration_profile = apn_configuration_profile
        self.rat_frequency_selection_priority_id = rat_frequency_selection_priority_id
        self.trace_data = trace_data
        self.gprs_subscription_data = gprs_subscription_data
        self.csg_subscription_data = csg_subscription_data
        self.roaming_restricted_due_to_unsupported_feature = roaming_restricted_due_to_unsupported_feature
        self.subscribed_periodic_rau_tau_timer = subscribed_periodic_rau_tau_timer
        self.mps_priority = mps_priority
        self.vplmn_lipa_allowed = vplmn_lipa_allowed
        self.relay_node_indicator = relay_node_indicator
        self.mdt_user_consent = mdt_user_consent
        self.subscribed_vsrvcc = subscribed_vsrvcc
        self.prose_subscription_data = prose_subscription_data
        self.subscription_data_flags = subscription_data_flags
        self.adjacent_access_restriction_data = adjacent_access_restriction_data
        self.dl_buffering_suggested_packet_count = dl_buffering_suggested_packet_count
        self.imsi_group_id = imsi_group_id
        self.aese_communication_pattern = aese_communication_pattern
        self.vendor_id = vendor_id
        
        avps = []
        if self.subscriber_status is not None:
            a = SubscriberStatusAVP(self.subscriber_status['value'])
            a.setFlags(self.subscriber_status['flags'])
            if 'vendor' in self.subscriber_status:
                a.setVendorID(self.subscriber_status['vendor'])
            avps.append(a)
        
        if self.msisdn is not None:
            a = MSISDNAVP(self.msisdn['value'])
            a.setFlags(self.msisdn['flags'])
            if 'vendor' in self.msisdn:
                a.setVendorID(self.msisdn['vendor'])
            avps.append(a)
            
        if self.a_msisdn is not None:
            a = AMSISDNAVP(self.a_msisdn['value'])
            a.setFlags(self.a_msisdn['flags'])
            if 'vendor' in self.a_msisdn:
                a.setVendorID(self.a_msisdn['vendor'])
            avps.append(a)
        
        if self.stn_sr is not None:
            a = STNSRAVP(self.stn_sr['value'])
            a.setFlags(self.stn_sr['flags'])
            if 'vendor' in self.stn_sr:
                a.setVendorID(self.stn_sr['vendor'])
            avps.append(a)
        
        if self.ics_indicator is not None:
            a = ICSIndicatorAVP(self.ics_indicator['value'])
            a.setFlags(self.ics_indicator['flags'])
            if 'vendor' in self.ics_indicator:
                a.setVendorID(self.ics_indicator['vendor'])
            avps.append(a)
        
        if self.network_access_mode is not None:
            a = NetworkAccessModeAVP(self.network_access_mode['value'])
            a.setFlags(self.network_access_mode['flags'])
            if 'vendor' in self.network_access_mode:
                a.setVendorID(self.network_access_mode['vendor'])
            avps.append(a)
        
        if self.operator_determined_barring is not None:
            a = OperatorDeterminedBarringAVP(self.operator_determined_barring['value'])
            a.setFlags(self.operator_determined_barring['flags'])
            if 'vendor' in self.operator_determined_barring:
                a.setVendorID(self.operator_determined_barring['vendor'])
            avps.append(a)
        
        if self.hplmn_odb is not None:
            a = HPLMNODBAVP(self.hplmn_odb['value'])
            a.setFlags(self.hplmn_odb['flags'])
            if 'vendor' in self.hplmn_odb:
                a.setVendorID(self.hplmn_odb['vendor'])
            avps.append(a)
        
        if self.regional_subscription_zone_code is not None:
            a = RegionalSubscriptionZoneCodeAVP(self.regional_subscription_zone_code['value'])
            a.setFlags(self.regional_subscription_zone_code['flags'])
            if 'vendor' in self.regional_subscription_zone_code:
                a.setVendorID(self.regional_subscription_zone_code['vendor'])
            avps.append(a)
        
        if self.access_restriction_data is not None:
            a = AccessRestrictionDataAVP(self.access_restriction_data['value'])
            a.setFlags(self.access_restriction_data['flags'])
            if 'vendor' in self.access_restriction_data:
                a.setVendorID(self.access_restriction_data['vendor'])
            avps.append(a)
        
        if self.apn_oi_replacement is not None:
            a = APNOIReplacementAVP(self.apn_oi_replacement['value'])
            a.setFlags(self.apn_oi_replacement['flags'])
            if 'vendor' in self.apn_oi_replacement:
                a.setVendorID(self.apn_oi_replacement['vendor'])
            avps.append(a)
        
        if self.lcs_info is not None:
            logging.warning('Subscription-Data AVP :: LCS-Info AVP NOT YET IMPLEMENTED')
            '''
            a = LCSInfoAVP(self.lcs_info['value'])
            a.setFlags(self.lcs_info['flags'])
            if 'vendor' in self.lcs_info:
                a.setVendorID(self.lcs_info['vendor'])
            avps.append(a)
            '''
            
        if self.teleservice_list is not None:
            a = TeleserviceListAVP(self.teleservice_list['value'])
            a.setFlags(self.teleservice_list['flags'])
            if 'vendor' in self.teleservice_list:
                a.setVendorID(self.teleservice_list['vendor'])
            avps.append(a)
        
        if self.call_barring_info is not None:
            a = CallBarringInfoAVP(self.call_barring_info['value'])
            a.setFlags(self.call_barring_info['flags'])
            if 'vendor' in self.call_barring_info:
                a.setVendorID(self.call_barring_info['vendor'])
            avps.append(a)
        
        if self.charging_characteristics_3gpp is not None:
            logging.warning('Subscription-Data AVP :: 3GPP-Charging-Characteristics AVP NOT YET IMPLEMENTED')
            '''
            a = ChargingCharacteristics3GPPAVP(self.charging_characteristics_3gpp['value'])
            a.setFlags(self.charging_characteristics_3gpp['flags'])
            if 'vendor' in self.charging_characteristics_3gpp:
                a.setVendorID(self.charging_characteristics_3gpp['vendor'])
            avps.append(a)
            '''
        
        if self.ambr is not None:
            a = AMBRAVP(self.ambr['value'])
            a.setFlags(self.ambr['flags'])
            if 'vendor' in self.ambr:
                a.setVendorID(self.ambr['vendor'])
            avps.append(a)
        
        if self.apn_configuration_profile is not None:
            a = APNConfigurationProfileAVP(self.apn_configuration_profile['value'])
            a.setFlags(self.apn_configuration_profile['flags'])
            if 'vendor' in self.apn_configuration_profile:
                a.setVendorID(self.apn_configuration_profile['vendor'])
            avps.append(a)
        
        if self.rat_frequency_selection_priority_id is not None:
            a = RATFrequencySelectionPriorityIDAVP(self.rat_frequency_selection_priority_id['value'])
            a.setFlags(self.rat_frequency_selection_priority_id['flags'])
            if 'vendor' in self.rat_frequency_selection_priority_id:
                a.setVendorID(self.rat_frequency_selection_priority_id['vendor'])
            avps.append(a)
        
        if self.trace_data is not None:
            logging.warning('Subscription-Data AVP :: Trace-Data AVP NOT YET IMPLEMENTED')
            '''
            a = TraceDataAVP(self.trace_data['value'])
            a.setFlags(self.trace_data['flags'])
            if 'vendor' in self.trace_data:
                a.setVendorID(self.trace_data['vendor'])
            avps.append(a)
            '''
        
        if self.gprs_subscription_data is not None:
            logging.warning('Subscription-Data AVP :: GPRS-Subscription-Data AVP NOT YET IMPLEMENTED')
            '''
            a = GPRSSubscriptionDataAVP(self.gprs_subscription_data['value'])
            a.setFlags(self.gprs_subscription_data['flags'])
            if 'vendor' in self.gprs_subscription_data:
                a.setVendorID(self.gprs_subscription_data['vendor'])
            avps.append(a)
            '''
        
        if self.csg_subscription_data is not None:
            logging.warning('Subscription-Data AVP :: CSG-Subscription-Data AVP NOT YET IMPLEMENTED')
            '''
            a = CSGSubscriptionDataAVP(self.csg_subscription_data['value'])
            a.setFlags(self.csg_subscription_data['flags'])
            if 'vendor' in self.csg_subscription_data:
                a.setVendorID(self.csg_subscription_data['vendor'])
            avps.append(a)
            '''
        
        if self.roaming_restricted_due_to_unsupported_feature is not None:
            a = RoamingRestrictedDueToUnsupportedFeatureAVP(self.roaming_restricted_due_to_unsupported_feature['value'])
            a.setFlags(self.roaming_restricted_due_to_unsupported_feature['flags'])
            if 'vendor' in self.roaming_restricted_due_to_unsupported_feature:
                a.setVendorID(self.roaming_restricted_due_to_unsupported_feature['vendor'])
            avps.append(a)
        
        if self.subscribed_periodic_rau_tau_timer is not None:
            a = SubscribedPeriodicRAUTAUTimerAVP(self.subscribed_periodic_rau_tau_timer['value'])
            a.setFlags(self.subscribed_periodic_rau_tau_timer['flags'])
            if 'vendor' in self.subscribed_periodic_rau_tau_timer:
                a.setVendorID(self.subscribed_periodic_rau_tau_timer['vendor'])
            avps.append(a)
        
        if self.mps_priority is not None:
            a = MPSPriorityAVP(self.mps_priority['value'])
            a.setFlags(self.mps_priority['flags'])
            if 'vendor' in self.mps_priority:
                a.setVendorID(self.mps_priority['vendor'])
            avps.append(a)
        
        if self.vplmn_lipa_allowed is not None:
            a = VPLMNLIPAAllowedAVP(self.vplmn_lipa_allowed['value'])
            a.setFlags(self.vplmn_lipa_allowed['flags'])
            if 'vendor' in self.vplmn_lipa_allowed:
                a.setVendorID(self.vplmn_lipa_allowed['vendor'])
            avps.append(a)
        
        if self.relay_node_indicator is not None:
            a = RelayNodeIndicatorAVP(self.relay_node_indicator['value'])
            a.setFlags(self.relay_node_indicator['flags'])
            if 'vendor' in self.relay_node_indicator:
                a.setVendorID(self.relay_node_indicator['vendor'])
            avps.append(a)
        
        if self.mdt_user_consent is not None:
            a = MDTUserConsentAVP(self.mdt_user_consent['value'])
            a.setFlags(self.mdt_user_consent['flags'])
            if 'vendor' in self.mdt_user_consent:
                a.setVendorID(self.mdt_user_consent['vendor'])
            avps.append(a)
        
        if self.subscribed_vsrvcc is not None:
            a = SubscribedVSRVCCAVP(self.subscribed_vsrvcc['value'])
            a.setFlags(self.subscribed_vsrvcc['flags'])
            if 'vendor' in self.subscribed_vsrvcc:
                a.setVendorID(self.subscribed_vsrvcc['vendor'])
            avps.append(a)
        
        if self.prose_subscription_data is not None:
            a = ProseSubscriptionDataAVP(self.prose_subscription_data['value'])
            a.setFlags(self.prose_subscription_data['flags'])
            if 'vendor' in self.prose_subscription_data:
                a.setVendorID(self.prose_subscription_data['vendor'])
            avps.append(a)
        
        if self.subscription_data_flags is not None:
            a = SubscriptionDataFlagsAVP(self.subscription_data_flags['value'])
            a.setFlags(self.subscription_data_flags['flags'])
            if 'vendor' in self.subscription_data_flags:
                a.setVendorID(self.subscription_data_flags['vendor'])
            avps.append(a)
        
        if self.adjacent_access_restriction_data is not None:
            a = AdjacentAccessRestrictionDataAVP(self.adjacent_access_restriction_data['value'])
            a.setFlags(self.adjacent_access_restriction_data['flags'])
            if 'vendor' in self.adjacent_access_restriction_data:
                a.setVendorID(self.adjacent_access_restriction_data['vendor'])
            avps.append(a)
        
        if self.dl_buffering_suggested_packet_count is not None:
            a = DLBufferingSuggestedPacketCountAVP(self.dl_buffering_suggested_packet_count['value'])
            a.setFlags(self.dl_buffering_suggested_packet_count['flags'])
            if 'vendor' in self.dl_buffering_suggested_packet_count:
                a.setVendorID(self.dl_buffering_suggested_packet_count['vendor'])
            avps.append(a)
        
        if self.imsi_group_id is not None:
            a = IMSIGroupIDAVP(self.imsi_group_id['value'])
            a.setFlags(self.imsi_group_id['flags'])
            if 'vendor' in self.imsi_group_id:
                a.setVendorID(self.imsi_group_id['vendor'])
            avps.append(a)
        
        if self.aese_communication_pattern is not None:
            logging.warning('Subscription-Data AVP :: AESE-Communication-Pattern AVP NOT YET IMPLEMENTED')
            '''
            a = AESECommunicationPatternAVP(self.aese_communication_pattern['value'])
            a.setFlags(self.aese_communication_pattern['flags'])
            if 'vendor' in self.aese_communication_pattern:
                a.setVendorID(self.aese_communication_pattern['vendor'])
            avps.append(a)
            '''
        
        if self.vendor_id != 0:
            a = VendorIDAVP(self.vendor_id['value'])
            a.setFlags(self.vendor_id['flags'])
            if 'vendor' in self.vendor_id:
                a.setVendorID(self.vendor_id['vendor'])
            avps.append(a)

        DiamAVP_Grouped.__init__(self, DiamAVPCodes.SUBSCRIPTION_DATA, avps, self.vendor_id)

class IDRFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a IDR-Flags AVP message 
    '''
    
    def __init__(self, idr_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param idr_flags: [Unsigned32] it contains a bit mask.
        '''
        idr_flags = int(idr_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.IDR_FLAGS, idr_flags, vendor_id)
        self.idr_flags = idr_flags

class IMSVoiceOverPSSessionSupportedAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a IMS-Voice-Over-PS-Session-Supported AVP message 
    '''
    
    NOT_SUPPORTED   = 0
    SUPPORTED       = 1
    
    def __init__(self, ims_voice_session_supported = NOT_SUPPORTED, vendor_id=0):
        '''
            Initialize the AVP message
            @param ims_voice_session_supported: [Unsigned32] Accepted values:
                                                * NOT_SUPPORTED
                                                * SUPPORTED
        '''
        ims_voice_session_supported = int(ims_voice_session_supported)
        
        if ims_voice_session_supported != self.NOT_SUPPORTED and \
           ims_voice_session_supported != self.SUPPORTED:
            raise AVPParametersException('IMS-Voice-Over-PS-Session-Supported AVP :: Incorrect ims_voice_session_supported value [' + str(ims_voice_session_supported) + ']')
        
        self.ims_voice_session_supported = ims_voice_session_supported
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.IMS_VOICE_OVER_PS_SESSION_SUPPORTED, ims_voice_session_supported, vendor_id)

class LastUEActivityTimeAVP(DiamAVP_Time):
    '''
        Class that defines a Last-UE-Activity-Time AVP message 
    '''
    
    def __init__(self, last_ue_activity_time, vendor_id=0):
        '''
            Initialize the AVP message
            @param last_ue_activity_time: [Unsigned32] it contains the point of time of the last radio contact of the serving node (MME or SGSN) with the UE.
        '''
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LAST_UE_ACTIVITY_TIME, last_ue_activity_time, vendor_id)
        self.last_ue_activity_time = last_ue_activity_time

class IDAFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a IDA-Flags AVP message 
    '''
    
    def __init__(self, ida_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param ida_flags: [Unsigned32] it contains a bit mask.
        '''
        ida_flags = int(ida_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.IDA_FLAGS, ida_flags, vendor_id)
        self.ida_flags = ida_flags

class EPSUserStateAVP(DiamAVP_Grouped):
    '''
        Class that defines a EPS-User-State AVP message 
        
            Requested-EUTRAN-Authentication-Info ::= <AVP header: 1408 10415>
                                [ Number-Of-Requested-Vectors ]
                                [ Immediate-Response-Preferred ]
                                [ Re-synchronization-Info ]
    '''
    
    def __init__(self, number_req_vectors=None, immmediate_response_preferred=None, re_sync_info=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param number_req_vectors:
            @param immmediate_response_preferred:
            @param re_sync_info:
        '''
        
        self.number_req_vectors = number_req_vectors
        self.immmediate_response_preferred = immmediate_response_preferred
        self.re_sync_info = re_sync_info
        self.vendor_id = vendor_id
        
        avps = []
        if self.number_req_vectors is not None:
            a = NumberRequestedVectorsAVP(self.number_req_vectors['value'])
            a.setFlags(self.number_req_vectors['flags'])
            if 'vendor' in self.number_req_vectors:
                a.setVendorID(self.number_req_vectors['vendor'])
            avps.append(a)
            
        if self.immmediate_response_preferred is not None:
            a = ImmediateResponsePreferredAVP(self.immmediate_response_preferred['value'])
            a.setFlags(self.immmediate_response_preferred['flags'])
            if 'vendor' in self.immmediate_response_preferred:
                a.setVendorID(self.immmediate_response_preferred['vendor'])
            avps.append(a)
        
        if self.re_sync_info is not None:
            a = ReSyncronizationInfoAVP(self.re_sync_info['value'])
            a.setFlags(self.re_sync_info['flags'])
            if 'vendor' in self.re_sync_info:
                a.setVendorID(self.re_sync_info['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.EPS_USER_STATE, avps, self.vendor_id)

class TimeZoneAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Time-Zone AVP message 
    '''
    
    def __init__(self, time_zone, vendor_id=0):
        '''
            Initialize the AVP message
            @param time_zone: [UTF8String] contains the leading digits of an IMSI formatted as a character string 
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.TIME_ZONE, time_zone, vendor_id)
        self.time_zone = time_zone

class DaylightSavingTimeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Daylight-Saving-Time AVP message 
    '''
    
    NO_ADJUSTMENT               = 0
    PLUS_ONE_HOUR_ADJUSTMENT    = 1
    PLUS_TWO_HOURS_ADJUSTMENT   = 2
    
    def __init__(self, daylight_saving_time = NO_ADJUSTMENT, vendor_id=0):
        '''
            Initialize the AVP message
            @param daylight_saving_time: [Unsigned32] Accepted values:
                                                * NO_ADJUSTMENT
                                                * PLUS_ONE_HOUR_ADJUSTMENT
                                                * PLUS_TWO_HOURS_ADJUSTMENT
        '''
        daylight_saving_time = int(daylight_saving_time)
        
        if daylight_saving_time != self.NO_ADJUSTMENT and \
           daylight_saving_time != self.PLUS_ONE_HOUR_ADJUSTMENT and \
           daylight_saving_time != self.PLUS_TWO_HOURS_ADJUSTMENT:
            raise AVPParametersException('Daylight-Saving-Time AVP :: Incorrect daylight_saving_time value [' + str(daylight_saving_time) + ']')
        
        self.daylight_saving_time = daylight_saving_time
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.DAYLIGHT_SAVING_TIME, daylight_saving_time, vendor_id)

class LocalTimeZoneAVP(DiamAVP_Grouped):
    '''
        Class that defines a Local-Time-Zone AVP message 
        
            Local-Time-Zone ::= <AVP header: 1649 10415>
                            { Time-Zone }
                            { Daylight-Saving-Time }
    '''
    
    def __init__(self, time_zone, daylight_saving_time, vendor_id=0):
        '''
            Initialize the AVP message
            @param time_zone:
            @param daylight_saving_time:
        '''
        
        self.time_zone = time_zone
        self.daylight_saving_time = daylight_saving_time
        self.vendor_id = vendor_id
        
        avps = []
        if self.time_zone is None:
            raise AVPParametersException('Local-Time-Zone AVP :: The time_zone is MANDATORY')
        a = TimeZoneAVP(self.time_zone['value'])
        a.setFlags(self.time_zone['flags'])
        if 'vendor' in self.time_zone:
            a.setVendorID(self.time_zone['vendor'])
        avps.append(a)
        
        if self.daylight_saving_time is None:
            raise AVPParametersException('Local-Time-Zone AVP :: The daylight_saving_time is MANDATORY')
        a = DaylightSavingTimeAVP(self.daylight_saving_time['value'])
        a.setFlags(self.daylight_saving_time['flags'])
        if 'vendor' in self.daylight_saving_time:
            a.setVendorID(self.daylight_saving_time['vendor'])
        avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.LOCAL_TIME_ZONE, avps, self.vendor_id)

class DSRFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a DSR-Flags AVP message 
    '''
    
    def __init__(self, dsr_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param dsr_flags: [Unsigned32] it contains a bit mask.
        '''
        dsr_flags = int(dsr_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.DSR_FLAGS, dsr_flags, vendor_id)
        self.dsr_flags = dsr_flags

class TraceReferenceAVP(DiamAVP_OctetString):
    '''
        Class that defines a Trace-Reference AVP message 
    '''
    
    def __init__(self, trace_reference, vendor_id=0):
        '''
            Initialize the AVP message
            @param trace_reference: [OctetString] it contains the concatenation of MCC, MNC and Trace ID, where the Trace ID is a 3 byte Octet String
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.TRACE_REFERENCE, trace_reference, vendor_id)
        self.trace_reference = trace_reference

class TSCodeAVP(DiamAVP_Octet):
    '''
        Class that defines a TS-Code AVP message 
    '''
    
    def __init__(self, ts_code, vendor_id=0):
        '''
            Initialize the AVP message
            @param ts_code: [OctetString] it contains octets that are coded according to 3GPP TS 29.002.
        '''
        DiamAVP_Octet.__init__(self, DiamAVPCodes.TS_CODE, ts_code, vendor_id)
        self.ts_code = ts_code

class SSCodeAVP(DiamAVP_OctetString):
    '''
        Class that defines a SS-Code AVP message 
    '''
    
    def __init__(self, ss_code, vendor_id=0):
        '''
            Initialize the AVP message
            @param ss_code: [OctetString] it contains octets that are coded according to 3GPP TS 29.002.
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.SS_CODE, ss_code, vendor_id)
        self.ss_code = ss_code

class DSAFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a DSA-Flags AVP message 
    '''
    
    def __init__(self, dsa_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param dsa_flags: [Unsigned32] it contains a bit mask.
        '''
        dsa_flags = int(dsa_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.DSA_FLAGS, dsa_flags, vendor_id)
        self.dsa_flags = dsa_flags

class EquipmentStatusAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Equipment-Status AVP message 
    '''
    
    WHITELISTED     = 0
    BLACKLISTED     = 1
    GREYLISTED      = 2
    
    def __init__(self, equipment_status = WHITELISTED, vendor_id=0):
        '''
            Initialize the AVP message
            @param equipment_status: [Unsigned32] Accepted values:
                                                * WHITELISTED
                                                * BLACKLISTED
                                                * GREYLISTED
        '''
        equipment_status = int(equipment_status)
        
        if equipment_status != self.WHITELISTED and \
           equipment_status != self.BLACKLISTED and \
           equipment_status != self.GREYLISTED:
            raise AVPParametersException('Equipment-Status AVP :: Incorrect equipment_status value [' + str(equipment_status) + ']')
        
        self.equipment_status = equipment_status
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.EQUIPMENT_STATUS, equipment_status, vendor_id)

class APNConfigurationAVP(DiamAVP_Grouped):
    '''
        Class that defines a APN-Configuration AVP message 
        
            APN-Configuration ::= <AVP header: 1430 10415>
                                { Context-Identifier }
                                * 2 [ Served-Party-IP-Address ]
                                { PDN-Type }
                                { Service-Selection}
                                [ EPS-Subscribed-QoS-Profile ]
                                [ VPLMN-Dynamic-Address-Allowed ]
                                [MIP6-Agent-Info ]
                                [ Visited-Network-Identifier ]
                                [ PDN-GW-Allocation-Type ]
                                [ 3GPP-Charging-Characteristics ]
                                [ AMBR ]
                                *[ Specific-APN-Info ]
                                [ APN-OI-Replacement ]
                                [ SIPTO-Permission ]
                                [ LIPA-Permission ]
                                [ Restoration-Priority ]
                                [ SIPTO-Local-Network-Permission ]
                                [ WLAN-offloadability ]
    '''
    
    def __init__(self,
                 context_identifier,
                 pdn_type,
                 service_selection,
                 served_party_ip_address=None,
                 eps_subscribed_qos_profile=None,
                 vplmn_dynamic_address_allowed=None,
                 mip6_agent_info=None,
                 visited_network_identifier=None,
                 pdn_gw_allocation_type=None,
                 charging_characteristics_3gpp=None,
                 ambr=None,
                 specific_apn_info=None,
                 apn_oi_replacement=None,
                 sipto_permission=None,
                 lipa_permission=None,
                 restoration_priority=None,
                 sipto_local_network_permission=None,
                 wlan_offloadability=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
        '''
        
        self.context_identifier = context_identifier
        self.served_party_ip_address = served_party_ip_address
        if self.served_party_ip_address is not None and not isinstance(self.served_party_ip_address, list):
            self.served_party_ip_address = [self.served_party_ip_address]
        self.pdn_type = pdn_type
        self.service_selection = service_selection
        self.eps_subscribed_qos_profile = eps_subscribed_qos_profile
        self.vplmn_dynamic_address_allowed = vplmn_dynamic_address_allowed
        self.mip6_agent_info = mip6_agent_info
        self.visited_network_identifier = visited_network_identifier
        self.pdn_gw_allocation_type = pdn_gw_allocation_type
        self.charging_characteristics_3gpp = charging_characteristics_3gpp
        self.ambr = ambr
        self.specific_apn_info = specific_apn_info
        if self.specific_apn_info is not None and not isinstance(self.specific_apn_info, list):
            self.specific_apn_info = [self.specific_apn_info]
        self.apn_oi_replacement = apn_oi_replacement
        self.sipto_permission = sipto_permission
        self.lipa_permission = lipa_permission
        self.restoration_priority = restoration_priority
        self.sipto_local_network_permission = sipto_local_network_permission
        self.wlan_offloadability = wlan_offloadability
        self.vendor_id = vendor_id
        
        avps = []
        if self.context_identifier is None:
            raise AVPParametersException('APN-Configuration AVP :: The context_identifier is MANDATORY')
        a = ContextIentifierAVP(self.context_identifier['value'])
        a.setFlags(self.context_identifier['flags'])
        if 'vendor' in self.context_identifier:
            a.setVendorID(self.context_identifier['vendor'])
        avps.append(a)
        
        if self.pdn_type is None:
            raise AVPParametersException('APN-Configuration AVP :: The pdn_type is MANDATORY')
        a = PDNTypeAVP(self.pdn_type['value'])
        a.setFlags(self.pdn_type['flags'])
        if 'vendor' in self.pdn_type:
            a.setVendorID(self.pdn_type['vendor'])
        avps.append(a)
        
        if self.service_selection is None:
            raise AVPParametersException('APN-Configuration AVP :: The service_selection is MANDATORY')
        a = ServiceSelectionAVP(self.service_selection['value'])
        a.setFlags(self.service_selection['flags'])
        if 'vendor' in self.service_selection:
            a.setVendorID(self.service_selection['vendor'])
        avps.append(a)
        
        if self.eps_subscribed_qos_profile is not None:
            a = EPSSubscribedQoSProfileAVP(self.eps_subscribed_qos_profile['value'])
            a.setFlags(self.eps_subscribed_qos_profile['flags'])
            if 'vendor' in self.eps_subscribed_qos_profile:
                a.setVendorID(self.eps_subscribed_qos_profile['vendor'])
            avps.append(a)

        if self.vplmn_dynamic_address_allowed is not None:
            a = VPLMNDynamicAddressAllowedAVP(self.vplmn_dynamic_address_allowed['value'])
            a.setFlags(self.vplmn_dynamic_address_allowed['flags'])
            if 'vendor' in self.vplmn_dynamic_address_allowed:
                a.setVendorID(self.vplmn_dynamic_address_allowed['vendor'])
            avps.append(a)

        if self.mip6_agent_info is not None:
            a = MIP6AgentInfoAVP(self.mip6_agent_info['value'])
            a.setFlags(self.mip6_agent_info['flags'])
            if 'vendor' in self.mip6_agent_info:
                a.setVendorID(self.mip6_agent_info['vendor'])
            avps.append(a)

        if self.visited_network_identifier is not None:
            a = VisitedNetworkIdentifierAVP(self.visited_network_identifier['value'])
            a.setFlags(self.visited_network_identifier['flags'])
            if 'vendor' in self.visited_network_identifier:
                a.setVendorID(self.visited_network_identifier['vendor'])
            avps.append(a)

        if self.pdn_gw_allocation_type is not None:
            a = PDNGWAllocationTypeAVP(self.pdn_gw_allocation_type['value'])
            a.setFlags(self.pdn_gw_allocation_type['flags'])
            if 'vendor' in self.pdn_gw_allocation_type:
                a.setVendorID(self.pdn_gw_allocation_type['vendor'])
            avps.append(a)

        if self.charging_characteristics_3gpp is not None:
            logging.warning('APN-Configuration AVP :: 3GPP-Charging-Characteristics AVP NOT YET IMPLEMENTED')
            '''
            a = ChargingCharacteristics3GPPAVP(self.charging_characteristics_3gpp['value'])
            a.setFlags(self.charging_characteristics_3gpp['flags'])
            if 'vendor' in self.charging_characteristics_3gpp:
                a.setVendorID(self.charging_characteristics_3gpp['vendor'])
            avps.append(a)
            '''
        if self.ambr is not None:
            a = AMBRAVP(self.ambr['value'])
            a.setFlags(self.ambr['flags'])
            if 'vendor' in self.ambr:
                a.setVendorID(self.ambr['vendor'])
            avps.append(a)

        if self.apn_oi_replacement is not None:
            a = APNOIReplacementAVP(self.apn_oi_replacement['value'])
            a.setFlags(self.apn_oi_replacement['flags'])
            if 'vendor' in self.apn_oi_replacement:
                a.setVendorID(self.apn_oi_replacement['vendor'])
            avps.append(a)

        if self.sipto_permission is not None:
            a = SIPTOPermissionAVP(self.sipto_permission['value'])
            a.setFlags(self.sipto_permission['flags'])
            if 'vendor' in self.sipto_permission:
                a.setVendorID(self.sipto_permission['vendor'])
            avps.append(a)

        if self.lipa_permission is not None:
            a = LIPAPermissionAVP(self.lipa_permission['value'])
            a.setFlags(self.lipa_permission['flags'])
            if 'vendor' in self.lipa_permission:
                a.setVendorID(self.lipa_permission['vendor'])
            avps.append(a)

        if self.restoration_priority is not None:
            a = RestorationPriorityAVP(self.restoration_priority['value'])
            a.setFlags(self.restoration_priority['flags'])
            if 'vendor' in self.restoration_priority:
                a.setVendorID(self.restoration_priority['vendor'])
            avps.append(a)

        if self.sipto_local_network_permission is not None:
            a = SIPTOLocalNetworkPermissionAVP(self.sipto_local_network_permission['value'])
            a.setFlags(self.sipto_local_network_permission['flags'])
            if 'vendor' in self.sipto_local_network_permission:
                a.setVendorID(self.sipto_local_network_permission['vendor'])
            avps.append(a)

        if self.wlan_offloadability is not None:
            a = WlanOffloadabilityAVP(self.wlan_offloadability['value'])
            a.setFlags(self.wlan_offloadability['flags'])
            if 'vendor' in self.wlan_offloadability:
                a.setVendorID(self.wlan_offloadability['vendor'])
            avps.append(a)
        
        if self.served_party_ip_address is not None and len(self.served_party_ip_address)<=2:
            for el in self.served_party_ip_address:
                a = ServedPartyIPAddressAVP(el['value'])
                a.setFlags(el['flags'])
                if 'vendor' in el:
                    a.setVendorID(el['vendor'])
                avps.append(a)
        
        if self.specific_apn_info is not None:
            for el in self.specific_apn_info:
                a = SpecificAPNInfoAVP(el['value'])
                a.setFlags(el['flags'])
                if 'vendor' in el:
                    a.setVendorID(el['vendor'])
                avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.APN_CONFIGURATION, avps, self.vendor_id)

class PDNTypeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a PDN-Type AVP message 
    '''
    
    IP_V4           = 0
    IP_V6           = 1
    IP_V4_V6        = 2
    IP_V4_OR_V6     = 3
    
    def __init__(self, pdn_type = IP_V4, vendor_id=0):
        '''
            Initialize the AVP message
            @param pdn_type: [Unsigned32] Accepted values:
                                    * IP_V4
                                    * IP_V6
                                    * IP_V4_V6
                                    * IP_V4_OR_V6
        '''
        pdn_type = int(pdn_type)
        
        if pdn_type != self.IP_V4 and \
           pdn_type != self.IP_V6 and \
           pdn_type != self.IP_V4_V6 and \
           pdn_type != self.IP_V4_OR_V6:
            raise AVPParametersException('PDN-Type AVP :: Incorrect pdn_type value [' + str(pdn_type) + ']')
        
        self.pdn_type = pdn_type
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PDN_TYPE, pdn_type, vendor_id)

class PriorityLevelAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Priority-Level AVP message 
    '''
    
    def __init__(self, priority_level, vendor_id=0):
        '''
            Initialize the AVP message
            @param priority_level: [Unsigned32]  is used for deciding whether a bearer establishment or modification request can be accepted or needs to be rejected in case of resource limitations
        '''
        priority_level = int(priority_level)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PRIORITY_LEVEL, priority_level, vendor_id)
        self.priority_level = priority_level

class PreEmptionCapabilityAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Pre-Emption-Capability AVP message 
    '''
    
    PRE_EMPTION_CAPABILITY_ENABLED      = 0
    PRE_EMPTION_CAPABILITY_DISABLED     = 1
    
    def __init__(self, pre_emption_capability = PRE_EMPTION_CAPABILITY_ENABLED, vendor_id=0):
        '''
            Initialize the AVP message
            @param pre_emption_capability: [Unsigned32] Accepted values:
                                            * PRE_EMPTION_CAPABILITY_ENABLED
               
        priority_level = int(priority_level)
                                     * PRE_EMPTION_CAPABILITY_DISABLED
        '''
        pre_emption_capability = int(pre_emption_capability)
        
        if pre_emption_capability != self.PRE_EMPTION_CAPABILITY_ENABLED and \
           pre_emption_capability != self.PRE_EMPTION_CAPABILITY_DISABLED:
            raise AVPParametersException('Pre-Emption-Capability AVP :: Incorrect pre_emption_capability value [' + str(pre_emption_capability) + ']')
        
        self.pre_emption_capability = pre_emption_capability
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PRE_EMPTION_CAPABILITY, pre_emption_capability, vendor_id)

class PreEmptionVulnerabilityAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Pre-Emption-Vulnerability AVP message 
    '''
    
    PRE_EMPTION_VULNERABILITY_ENABLED      = 0
    PRE_EMPTION_VULNERABILITY_DISABLED     = 1
    
    def __init__(self, pre_emption_vulnerability = PRE_EMPTION_VULNERABILITY_ENABLED, vendor_id=0):
        '''
            Initialize the AVP message
            @param pre_emption_vulnerability: [Unsigned32] Accepted values:
                                            * PRE_EMPTION_VULNERABILITY_ENABLED
                                            * PRE_EMPTION_VULNERABILITY_DISABLED
        '''
        pre_emption_vulnerability = int(pre_emption_vulnerability)
        
        if pre_emption_vulnerability != self.PRE_EMPTION_VULNERABILITY_ENABLED and \
           pre_emption_vulnerability != self.PRE_EMPTION_VULNERABILITY_DISABLED:
            raise AVPParametersException('Pre-Emption-Vulnerability AVP :: Incorrect pre_emption_vulnerability value [' + str(pre_emption_vulnerability) + ']')
        
        self.pre_emption_vulnerability = pre_emption_vulnerability
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PRE_EMPTION_VULNERABILITY, pre_emption_vulnerability, vendor_id)

class QoSClassIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a QoS-Class-Identifier AVP message 
    '''
    QCI_1   = 1
    QCI_2   = 2
    QCI_3   = 3
    QCI_4   = 4
    QCI_5   = 5
    QCI_6   = 6
    QCI_7   = 7
    QCI_8   = 8
    QCI_9   = 9
    QCI_65  = 65
    QCI_66  = 66
    QCI_69  = 69
    QCI_70  = 70
    
    def __init__(self, qos_class_id = QCI_1, vendor_id=0):
        '''
            Initialize the AVP message
            @param qos_class_id: [Unsigned32] Accepted values:
                                    * QCI_1
                                    * QCI_2
                                    * QCI_3
                                    * QCI_4
                                    * QCI_5
                                    * QCI_6
                                    * QCI_7
                                    * QCI_8
                                    * QCI_9
                                    * QCI_65
                                    * QCI_66
                                    * QCI_69
                                    * QCI_70
        '''
        qos_class_id = int(qos_class_id)
        
        if qos_class_id != self.QCI_1 and \
           qos_class_id != self.QCI_2 and \
           qos_class_id != self.QCI_3 and \
           qos_class_id != self.QCI_4 and \
           qos_class_id != self.QCI_5 and \
           qos_class_id != self.QCI_6 and \
           qos_class_id != self.QCI_7 and \
           qos_class_id != self.QCI_8 and \
           qos_class_id != self.QCI_9 and \
           qos_class_id != self.QCI_65 and \
           qos_class_id != self.QCI_66 and \
           qos_class_id != self.QCI_69 and \
           qos_class_id != self.QCI_70:
            logging.warning('QoS-Class-Id :: Reserved qos_class_id value [' + str(qos_class_id) + ']')
        
        self.qos_class_id = qos_class_id
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.QOS_CLASS_IDENTIFIER, qos_class_id, vendor_id)

class AllocationRetentionPriorityAVP(DiamAVP_Grouped):
    '''
        Class that defines a Allocation-Retention-Priority AVP message 
        
            Allocation-Retention-Priority ::= <AVP header: 1034 10415>
                                            { Priority-Level }
                                            [ Pre-emption-Capability ]
                                            [ Pre-emption-Vulnerability ]
    '''
    
    def __init__(self, priority_level, pre_emption_capability=PreEmptionCapabilityAVP.PRE_EMPTION_CAPABILITY_DISABLED, pre_emption_vulnerability=PreEmptionVulnerabilityAVP.PRE_EMPTION_VULNERABILITY_ENABLED, vendor_id=0):
        '''
            Initialize the AVP message
            @param priority_level:
            @param pre_emption_capability:
            @param pre_emption_vulnerability:
        '''
        
        self.priority_level = priority_level
        self.pre_emption_capability = pre_emption_capability
        self.pre_emption_vulnerability = pre_emption_vulnerability
        self.vendor_id = vendor_id
        
        avps = []
        if self.priority_level is None:
            raise AVPParametersException('Allocation-Retention-Priority AVP :: The priority_level is MANDATORY')
        a = PriorityLevelAVP(self.priority_level['value'])
        a.setFlags(self.priority_level['flags'])
        if 'vendor' in self.priority_level:
            a.setVendorID(self.priority_level['vendor'])
        avps.append(a)
        
        if self.pre_emption_capability is not None:
            a = PreEmptionCapabilityAVP(self.pre_emption_capability['value'])
            a.setFlags(self.pre_emption_capability['flags'])
            if 'vendor' in self.pre_emption_capability:
                a.setVendorID(self.pre_emption_capability['vendor'])
            avps.append(a)
        
        if self.pre_emption_vulnerability is not None:
            a = PreEmptionVulnerabilityAVP(self.pre_emption_vulnerability['value'])
            a.setFlags(self.pre_emption_vulnerability['flags'])
            if 'vendor' in self.pre_emption_vulnerability:
                a.setVendorID(self.pre_emption_vulnerability['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.ALLOCATION_RETENTION_PRIORITY, avps, self.vendor_id)

class EPSSubscribedQoSProfileAVP(DiamAVP_Grouped):
    '''
        Class that defines a EPS-Subscribed-QoS-profile AVP message 
        
            EPS-Subscribed-QoS-Profile ::= <AVP header: 1431 10415>
                                        { QoS-Class-Identifier }
                                        { Allocation-Retention-Priority }
    '''
    
    def __init__(self, qos_class_id, allocation_retention_priority, vendor_id=0):
        '''
            Initialize the AVP message
            @param qos_class_id:
            @param allocation_retention_priority:
        '''
        
        self.qos_class_id = qos_class_id
        self.allocation_retention_priority = allocation_retention_priority
        self.vendor_id = vendor_id
        
        avps = []
        if self.qos_class_id is None:
            raise AVPParametersException('EPS-Subscribed-QoS-Profile AVP :: The qos_class_id is MANDATORY')
        a = QoSClassIDAVP(self.qos_class_id['value'])
        a.setFlags(self.qos_class_id['flags'])
        if 'vendor' in self.qos_class_id:
            a.setVendorID(self.qos_class_id['vendor'])
        avps.append(a)
        
        if self.allocation_retention_priority is None:
            raise AVPParametersException('EPS-Subscribed-QoS-Profile AVP :: The allocation_retention_priority is MANDATORY')
        a = AllocationRetentionPriorityAVP(self.allocation_retention_priority['value'])
        a.setFlags(self.allocation_retention_priority['flags'])
        if 'vendor' in self.allocation_retention_priority:
            a.setVendorID(self.allocation_retention_priority['vendor'])
        avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.ALLOCATION_RETENTION_PRIORITY, avps, self.vendor_id)

class VPLMNDynamicAddressAllowedAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a VPLMN-Dynamic-Address-Allowed AVP message 
    '''
    
    NOTALLOWED      = 0
    ALLOWED         = 1
    
    def __init__(self, vplmn_dynamic_address_allowed = NOTALLOWED, vendor_id=0):
        '''
            Initialize the AVP message
            @param vplmn_dynamic_address_allowed: [Unsigned32] Accepted values:
                                    * NOTALLOWED
                                    * ALLOWED
        '''
        vplmn_dynamic_address_allowed = int(vplmn_dynamic_address_allowed)
        
        if vplmn_dynamic_address_allowed != self.NOTALLOWED and \
           vplmn_dynamic_address_allowed != self.ALLOWED:
            raise AVPParametersException('VPLMN-Dynamic-Address-Allowed AVP :: Incorrect vplmn_dynamic_address_allowed value [' + str(vplmn_dynamic_address_allowed) + ']')
        
        self.vplmn_dynamic_address_allowed = vplmn_dynamic_address_allowed
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.VPLMN_DYNAMIC_ADDRESS_ALLOWED, vplmn_dynamic_address_allowed, vendor_id)

class PDNGWAllocationTypeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a PDN-GW-Allocation-Type AVP message 
    '''
    
    STATIC      = 0
    DYNAMIC     = 1
    
    def __init__(self, pdn_gw_allocation_type = STATIC, vendor_id=0):
        '''
            Initialize the AVP message
            @param pdn_gw_allocation_type: [Unsigned32] Accepted values:
                                    * STATIC
                                    * DYNAMIC
        '''
        pdn_gw_allocation_type = int(pdn_gw_allocation_type)
        
        if pdn_gw_allocation_type != self.STATIC and \
           pdn_gw_allocation_type != self.DYNAMIC:
            raise AVPParametersException('PDN-GW-Allocation-Type AVP :: Incorrect pdn_gw_allocation_type value [' + str(pdn_gw_allocation_type) + ']')
        
        self.pdn_gw_allocation_type = pdn_gw_allocation_type
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PDN_GW_ALLOCATION_TYPE, pdn_gw_allocation_type, vendor_id)

class SIPTOPermissionAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a SIPTO-Permission AVP message 
    '''
    
    SIPTO_ABOVE_RAN_ALLOWED         = 0
    SIPTO_ABOVE_RAN_NOTALLOWED      = 1
    
    def __init__(self, sipto_perm = SIPTO_ABOVE_RAN_ALLOWED, vendor_id=0):
        '''
            Initialize the AVP message
            @param sipto_perm: [Unsigned32] Accepted values:
                                    * SIPTO_ABOVE_RAN_ALLOWED
                                    * SIPTO_ABOVE_RAN_NOTALLOWED
        '''
        sipto_perm = int(sipto_perm)
        
        if sipto_perm != self.SIPTO_ABOVE_RAN_ALLOWED and \
           sipto_perm != self.SIPTO_ABOVE_RAN_NOTALLOWED:
            raise AVPParametersException('SIPTO-Permission AVP :: Incorrect sipto_perm value [' + str(sipto_perm) + ']')
        
        self.sipto_perm = sipto_perm
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SIPTO_PERMISSION, sipto_perm, vendor_id)

class LIPAPermissionAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LIPA-Permission AVP message 
    '''
    
    LIPA_PROHIBITED     = 0
    LIPA_ONLY           = 1
    LIPA_CONDITIONAL    = 2
    
    def __init__(self, lipa_perm = LIPA_PROHIBITED, vendor_id=0):
        '''
            Initialize the AVP message
            @param lipa_perm: [Unsigned32] Accepted values:
                                    * LIPA_PROHIBITED
                                    * LIPA_ONLY
                                    * LIPA_CONDITIONAL
        '''
        lipa_perm = int(lipa_perm)
        
        if lipa_perm != self.LIPA_PROHIBITED and \
           lipa_perm != self.LIPA_ONLY and \
           lipa_perm != self.LIPA_CONDITIONAL:
            raise AVPParametersException('LIPA-Permission AVP :: Incorrect lipa_perm value [' + str(lipa_perm) + ']')
        
        self.lipa_perm = lipa_perm
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LIPA_PERMISSION, lipa_perm, vendor_id)

class RestorationPriorityAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Restoration-Priority AVP message 
    '''
    
    def __init__(self, restoration_priority, vendor_id=0):
        '''
            Initialize the AVP message
            @param restoration_priority: [Unsigned32] it indicates the relative priority of a user's PDN connection among PDN connections to the same APN when restoring PDN connections affected by an SGW or PGW failure/restart
        '''
        restoration_priority = int(restoration_priority)
        
        if restoration_priority<0 or restoration_priority>16:
            raise AVPParametersException('Restoration-Priority AVP :: Only allowed values between 0 and 16')
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.RESTORATION_PRIORITY, restoration_priority, vendor_id)
        self.restoration_priority = restoration_priority

class SIPTOLocalNetworkPermissionAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a SIPTO-Local-Network-Permission AVP message 
    '''
    
    ALLOWED         = 0
    NOTALLOWED      = 1
    
    def __init__(self, sipto_local_network_perm = ALLOWED, vendor_id=0):
        '''
            Initialize the AVP message
            @param sipto_local_network_perm: [Unsigned32] Accepted values:
                                                * ALLOWED
                                                * NOTALLOWED
        '''
        sipto_local_network_perm = int(sipto_local_network_perm)
        
        if sipto_local_network_perm != self.ALLOWED and \
           sipto_local_network_perm != self.NOTALLOWED:
            raise AVPParametersException('SIPTO-Local-Network-Permission AVP :: Incorrect sipto_local_network_perm value [' + str(sipto_local_network_perm) + ']')
        
        self.sipto_local_network_perm = sipto_local_network_perm
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SIPTO_LOCAL_NETWORK_PERMISSION, sipto_local_network_perm, vendor_id)

class WlanOffloadabilityEUTRANAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Wlan-Offloadability-EUTRAN AVP message 
    '''
    
    def __init__(self, wlan_off_eutran, vendor_id=0):
        '''
            Initialize the AVP message
            @param wlan_off_eutran: [Unsigned32] it contains a bitmask.
        '''
        wlan_off_eutran = int(wlan_off_eutran)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.WLAN_OFFLOADABILITY_EUTRAN, wlan_off_eutran, vendor_id)
        self.wlan_off_eutran = wlan_off_eutran

class WlanOffloadabilityUTRANAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Wlan-Offloadability-UTRAN AVP message 
    '''
    
    def __init__(self, wlan_off_utran, vendor_id=0):
        '''
            Initialize the AVP message
            @param wlan_off_utran: [Unsigned32] it contains a bitmask.
        '''
        wlan_off_utran = int(wlan_off_utran)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.WLAN_OFFLOADABILITY_UTRAN, wlan_off_utran, vendor_id)
        self.wlan_off_utran = wlan_off_utran

class WlanOffloadabilityAVP(DiamAVP_Grouped):
    '''
        Class that defines a Wlan-Offloadability AVP message 
        
            WLAN-offloadability ::= <AVP header: 1667>
                                [ WLAN-offloadability-EUTRAN ]
                                [ WLAN-offloadability-UTRAN ]
    '''
    
    def __init__(self, wlan_off_eutran=None, wlan_off_utran=None, vendor_id=0):
        '''
            Initialize the AVP message
            @param wlan_off_eutran:
            @param wlan_off_utran:
        '''
        
        self.wlan_off_eutran = wlan_off_eutran
        self.wlan_off_utran = wlan_off_utran
        self.vendor_id = vendor_id
        
        avps = []
        if self.wlan_off_eutran is not None:
            a = WlanOffloadabilityEUTRANAVP(self.wlan_off_eutran['value'])
            a.setFlags(self.wlan_off_eutran['flags'])
            if 'vendor' in self.wlan_off_eutran:
                a.setVendorID(self.wlan_off_eutran['vendor'])
            avps.append(a)
        
        if self.wlan_off_utran is not None:
            a = WlanOffloadabilityUTRANAVP(self.wlan_off_utran['value'])
            a.setFlags(self.wlan_off_utran['flags'])
            if 'vendor' in self.wlan_off_utran:
                a.setVendorID(self.wlan_off_utran['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.WLAN_OFFLOADABILITY, avps, self.vendor_id)

class ServedPartyIPAddressAVP(DiamAVP_Address):
    '''
        Class that defines the Served-Party-IP-Address AVP message 
    '''
    
    def __init__(self, ip, vendor_id=0):
        '''
            Initialize the AVP message
            @param ip: [Address] the IP address of either the calling or called party, depending on whether the P-CSCF is in touch with the calling or the called party
        '''
        DiamAVP_Address.__init__(self, DiamAVPCodes.SERVED_PARTY_IP_ADDRESS, ip, vendor_id)
        self.ip = ip
    
class MSISDNAVP(DiamAVP_OctetString):
    '''
        Class that defines a MSISDN AVP message 
    '''
    
    def __init__(self, msisdn, vendor_id=0):
        '''
            Initialize the AVP message
            @param msisdn: [OctetString] it contains an MSISDN, in international number format as described in ITU-T Rec E.164 [8], encoded as a TBCD-string
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.MSISDN, msisdn, vendor_id)
        self.msisdn = msisdn


''' SLh AVPs '''
class LMSIAVP(DiamAVP_OctetString):
    '''
        Class that defines a LMSI (Local Mobile Station Identity) AVP message 
    '''
    
    def __init__(self, lmsi, vendor_id=0):
        '''
            Initialize the AVP message
            @param lmsi: [OctetString]  it shall contain the Local Mobile Station Identity (LMSI) 
                                        allocated by the VLR
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.LMSI, lmsi, vendor_id)
        self.lmsi = lmsi
        
class MMENameAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the MME-Name AVP message 
    '''
    
    def __init__(self, mme_name, vendor_id=0):
        '''
            Initialize the AVP message
            @param mme_name: [DiameterIdentity] the Diameter identity of the serving MME
        '''
        DiamAVP.__init__(self, DiamAVPCodes.MME_NAME, mme_name, vendor_id)
        self.mme_name = mme_name
        
class MSCNumberAVP(DiamAVP_OctetString):
    '''
        Class that defines a MSC-Number AVP message 
    '''
    
    def __init__(self, msc_number, vendor_id=0):
        '''
            Initialize the AVP message
            @param msc_number: [OctetString] it shall contain the ISDN number of the serving MSC or MSC server
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.MSC_NUMBER, msc_number, vendor_id)
        self.msc_number = msc_number

class LCSCapabilitiesSetsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LCS-Capabilities-Sets AVP message 
    '''
    
    def __init__(self, lcs_capabilities_sets, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_capabilities_sets: [Unsigned32] it contains a bitmask.
        '''
        lcs_capabilities_sets = int(lcs_capabilities_sets)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LCS_CAPANBILITIES_SETS, lcs_capabilities_sets, vendor_id)
        self.lcs_capabilities_sets = lcs_capabilities_sets

class ServingNodeAVP(DiamAVP_Grouped):
    '''
        Class that defines a Serving-Node AVP message 
        
            Serving-Node ::= <AVP header: 2401 10415>
                            [ SGSN-Number ]
                            [ SGSN-Name ]
                            [ SGSN-Realm ]
                            [ MME-Name ]
                            [ MME-Realm ]
                            [ MSC-Number ]
                            [ 3GPP-AAA-Server-Name ]
                            [ LCS-Capabilities-Sets ]
                            [ GMLC-Address ] 
    '''
    
    def __init__(self, 
                 sgsn_number=None,
                 sgsn_name=None,
                 sgsn_realm=None,
                 mme_name=None, 
                 mme_realm=None, 
                 msc_number=None, 
                 gpp3_aaa_server_name=None,
                 lcs_capabilities_sets=None,
                 gmlc_address=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param sgsn_number:
            @param sgsn_name:
            @param sgsn_realm:
            @param mme_name:
            @param mme_realm:
            @param msc_number:
            @param gpp3_aaa_server_name:
            @param lcs_capabilities_sets:
            @param gmlc_address:
        '''
        
        self.sgsn_number = sgsn_number
        self.sgsn_name = sgsn_name
        self.sgsn_realm = sgsn_realm
        self.mme_name = mme_name
        self.mme_realm = mme_realm
        self.msc_number = msc_number
        self.gpp3_aaa_server_name = gpp3_aaa_server_name
        self.lcs_capabilities_sets = lcs_capabilities_sets
        self.gmlc_address = gmlc_address
        self.vendor_id = vendor_id
        
        avps = []
        if self.sgsn_number is not None:
            a = SGSNNumberAVP(self.sgsn_number['value'])
            a.setFlags(self.sgsn_number['flags'])
            if 'vendor' in self.sgsn_number:
                a.setVendorID(self.sgsn_number['vendor'])
            avps.append(a)
            
        if self.sgsn_realm is not None:
            a = SGSNRealmAVP(self.sgsn_realm['value'])
            a.setFlags(self.sgsn_realm['flags'])
            if 'vendor' in self.sgsn_realm:
                a.setVendorID(self.sgsn_realm['vendor'])
            avps.append(a)
            
        if self.sgsn_number is not None:
            a = SGSNNumberAVP(self.sgsn_number['value'])
            a.setFlags(self.sgsn_number['flags'])
            if 'vendor' in self.sgsn_number:
                a.setVendorID(self.sgsn_number['vendor'])
            avps.append(a)
            
        if self.mme_name is not None:
            a = MMENameAVP(self.mme_name['value'])
            a.setFlags(self.mme_name['flags'])
            if 'vendor' in self.mme_name:
                a.setVendorID(self.mme_name['vendor'])
            avps.append(a)

        if self.mme_realm is not None:
            a = MMERealmAVP(self.mme_realm['value'])
            a.setFlags(self.mme_realm['flags'])
            if 'vendor' in self.mme_realm:
                a.setVendorID(self.mme_realm['vendor'])
            avps.append(a)
            
        if self.msc_number is not None:
            a = MSCNumberAVP(self.msc_number['value'])
            a.setFlags(self.msc_number['flags'])
            if 'vendor' in self.msc_number:
                a.setVendorID(self.msc_number['vendor'])
            avps.append(a)
        
        if self.gpp3_aaa_server_name is not None:
            a = AAAServerName3GPPAVP(self.gpp3_aaa_server_name['value'])
            a.setFlags(self.gpp3_aaa_server_name['flags'])
            if 'vendor' in self.gpp3_aaa_server_name:
                a.setVendorID(self.gpp3_aaa_server_name['vendor'])
            avps.append(a)
        
        if self.lcs_capabilities_sets is not None:
            a = LCSCapabilitiesSetsAVP(self.lcs_capabilities_sets['value'])
            a.setFlags(self.lcs_capabilities_sets['flags'])
            if 'vendor' in self.lcs_capabilities_sets:
                a.setVendorID(self.lcs_capabilities_sets['vendor'])
            avps.append(a)
        
        if self.gmlc_address is not None:
            a = GMLCAddressAVP(self.gmlc_address['value'])
            a.setFlags(self.gmlc_address['flags'])
            if 'vendor' in self.gmlc_address:
                a.setVendorID(self.gmlc_address['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.SERVING_NODE, avps, self.vendor_id)

class AdditionalServingNodeAVP(DiamAVP_Grouped):
    '''
        Class that defines a Additional-Serving-Node AVP message 
        
            Additional-Serving-Node ::= <AVP header: 2406 10415>
                                [ SGSN-Number ]
                                [ SGSN-Name ]
                                [ SGSN-Realm ]
                                [ MME-Name ]
                                [ MME-Realm ]
                                [ MSC-Number ]
                                [ 3GPP-AAA-Server-Name ]
                                [ LCS-Capabilities-Sets ]
                                [ GMLC-Address ] 
    '''
    
    def __init__(self, 
                 sgsn_number=None,
                 sgsn_name=None,
                 sgsn_realm=None,
                 mme_name=None, 
                 mme_realm=None, 
                 msc_number=None, 
                 gpp3_aaa_server_name=None,
                 lcs_capabilities_sets=None,
                 gmlc_address=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param sgsn_number:
            @param mme_name:
            @param sgsn_name: 
            @param sgsn_realm: 
            @param mme_realm:
            @param msc_number:
            @param gpp3_aaa_server_name:
            @param lcs_capabilities_sets:
            @param gmlc_address:
        '''
        
        self.sgsn_number = sgsn_number
        self.mme_name = mme_name
        self.sgsn_name = sgsn_name
        self.sgsn_realm = sgsn_realm 
        self.mme_realm = mme_realm 
        self.msc_number = msc_number
        self.gpp3_aaa_server_name = gpp3_aaa_server_name
        self.lcs_capabilities_sets = lcs_capabilities_sets
        self.gmlc_address = gmlc_address
        self.vendor_id = vendor_id
        
        avps = []
        if self.sgsn_number is not None:
            a = SGSNNumberAVP(self.sgsn_number['value'])
            a.setFlags(self.sgsn_number['flags'])
            if 'vendor' in self.sgsn_number:
                a.setVendorID(self.sgsn_number['vendor'])
            avps.append(a)
        
        if self.mme_name is not None:
            a = MMENameAVP(self.mme_name['value'])
            a.setFlags(self.mme_name['flags'])
            if 'vendor' in self.mme_name:
                a.setVendorID(self.mme_name['vendor'])
            avps.append(a)
        
        if self.sgsn_name is not None:
            a = SGSNNameAVP(self.sgsn_name['value'])
            a.setFlags(self.sgsn_name['flags'])
            if 'vendor' in self.sgsn_name:
                a.setVendorID(self.sgsn_name['vendor'])
            avps.append(a)
        
        if self.sgsn_realm is not None:
            a = SGSNRealmAVP(self.sgsn_realm['value'])
            a.setFlags(self.sgsn_realm['flags'])
            if 'vendor' in self.sgsn_realm:
                a.setVendorID(self.sgsn_realm['vendor'])
            avps.append(a)
        
        if self.mme_realm is not None:
            a = MMERealmAVP(self.mme_realm['value'])
            a.setFlags(self.mme_realm['flags'])
            if 'vendor' in self.mme_realm:
                a.setVendorID(self.mme_realm['vendor'])
            avps.append(a)
        
        if self.msc_number is not None:
            a = MSCNumberAVP(self.msc_number['value'])
            a.setFlags(self.msc_number['flags'])
            if 'vendor' in self.msc_number:
                a.setVendorID(self.msc_number['vendor'])
            avps.append(a)
        
        if self.gpp3_aaa_server_name is not None:
            a = AAAServerName3GPPAVP(self.gpp3_aaa_server_name['value'])
            a.setFlags(self.gpp3_aaa_server_name['flags'])
            if 'vendor' in self.gpp3_aaa_server_name:
                a.setVendorID(self.gpp3_aaa_server_name['vendor'])
            avps.append(a)
        
        if self.lcs_capabilities_sets is not None:
            a = LCSCapabilitiesSetsAVP(self.lcs_capabilities_sets['value'])
            a.setFlags(self.lcs_capabilities_sets['flags'])
            if 'vendor' in self.lcs_capabilities_sets:
                a.setVendorID(self.lcs_capabilities_sets['vendor'])
            avps.append(a)
        
        if self.gmlc_address is not None:
            a = GMLCAddressAVP(self.gmlc_address['value'])
            a.setFlags(self.gmlc_address['flags'])
            if 'vendor' in self.gmlc_address:
                a.setVendorID(self.gmlc_address['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.SERVING_NODE, avps, self.vendor_id)

class PPRAddressAVP(DiamAVP_Address):
    '''
        Class that defines the PPR-Address AVP message 
    '''
    
    def __init__(self, ppr_address, vendor_id=0):
        '''
            Initialize the AVP message
            @param ppr_address: [Address] the IPv4 or IPv6 address of the Privacy Profile Register
        '''
        DiamAVP_Address.__init__(self, DiamAVPCodes.PPR_ADDRESS, ppr_address, vendor_id)
        self.ppr_address = ppr_address
     
class GMLCNumberAVP(DiamAVP_OctetString):
    '''
        Class that defines a GMLC-Number AVP message 
    '''
    
    def __init__(self, gmlc_number, vendor_id=0):
        '''
            Initialize the AVP message
            @param gmlc_number: [OctetString] it shall contain the ISDN number of the GMLC
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.GMLC_NUBER, gmlc_number, vendor_id)
        self.gmlc_number = gmlc_number

class RIAFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a RIA-Flags AVP message 
    '''
    
    def __init__(self, ria_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param ria_flags: [Unsigned32] it contains a bit mask.
        '''
        ria_flags = int(ria_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.RIA_FLAGS, ria_flags, vendor_id)
        self.ria_flags = ria_flags

class MMERealmAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the MME-Realm AVP message 
    '''
    
    def __init__(self, mme_realm, vendor_id=0):
        '''
            Initialize the AVP message
            @param mme_name: [DiameterIdentity] the Diameter Realm Identity of the serving MME
        '''
        DiamAVP.__init__(self, DiamAVPCodes.MME_REALM, mme_realm, vendor_id)
        self.mme_realm = mme_realm

class SGSNNameAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the SGSN-Name AVP message 
    '''
    
    def __init__(self, sgsn_name, vendor_id=0):
        '''
            Initialize the AVP message
            @param sgsn_name: [DiameterIdentity] the Diameter identity of the serving SGSN
        '''
        DiamAVP.__init__(self, DiamAVPCodes.SGSN_NAME, sgsn_name, vendor_id)
        self.sgsn_name = sgsn_name

class SGSNRealmAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the SGSN-Realm AVP message 
    '''
    
    def __init__(self, sgsn_realm, vendor_id=0):
        '''
            Initialize the AVP message
            @param mme_name: [DiameterIdentity] the Diameter Realm Identity of the serving SGSN
        '''
        DiamAVP.__init__(self, DiamAVPCodes.SGSN_REALM, sgsn_realm, vendor_id)
        self.sgsn_realm = sgsn_realm

class AAAServerName3GPPAVP(DiamAVP_DiamIdent):
    '''
        Class that defines the 3GPP-AAA-Server-Name AVP message 
    '''
    
    def __init__(self, aaa_server_name, vendor_id=0):
        '''
            Initialize the AVP message
            @param mme_name: [DiameterIdentity] the Diameter address of the 3GPP AAA Server node
        '''
        DiamAVP.__init__(self, DiamAVPCodes.AAA_SERVER_NAME_3GPP, aaa_server_name, vendor_id)
        self.aaa_server_name = aaa_server_name


''' SLg AVPs '''
class SLgLocationTypeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a SLg-Location-Type AVP message 
    '''
    
    CURRENT_LOCATION                = 0
    CURRENT_OR_LAST_KNOWN_LOCATION  = 1
    INITIAL_LOCATION                = 2
    ACTIVATE_DEFERRED_LOCATION      = 3
    CANCEL_DEFERRED_LOCATION        = 4
    NOTIFICATION_VERIFICaTION_ONLY  = 5
    
    def __init__(self, slg_location_type = CURRENT_LOCATION, vendor_id=0):
        '''
            Initialize the AVP message
            @param slg_location_type: [Unsigned32] Accepted values:
                                                * CURRENT_LOCATION
                                                * CURRENT_OR_LAST_KNOWN_LOCATION
                                                * INITIAL_LOCATION
                                                * ACTIVATE_DEFERRED_LOCATION
                                                * CANCEL_DEFERRED_LOCATION
                                                * NOTIFICATION_VERIFICaTION_ONLY
        '''
        slg_location_type = int(slg_location_type)
        
        if slg_location_type != self.CURRENT_LOCATION and \
           slg_location_type != self.CURRENT_OR_LAST_KNOWN_LOCATION and \
           slg_location_type != self.INITIAL_LOCATION and \
           slg_location_type != self.ACTIVATE_DEFERRED_LOCATION and \
           slg_location_type != self.CANCEL_DEFERRED_LOCATION and \
           slg_location_type != self.NOTIFICATION_VERIFICaTION_ONLY:
            raise AVPParametersException('SLg-Location-Type AVP :: Incorrect slg_location_type value [' + str(slg_location_type) + ']')
        
        self.slg_location_type = slg_location_type
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SLG_LOCATION_TYPE, slg_location_type, vendor_id)

class LCSNameStringAVP(DiamAVP_UTF8String):
    '''
        Class that defines a LCS-Name-String AVP message 
    '''
    
    def __init__(self, lcs_name_string, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_name_string: [UTF8String] contains the LCS Client name 
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.LCS_NAME_STRING, lcs_name_string, vendor_id)
        self.lcs_name_string = lcs_name_string

class LCSFormatIndicatorAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LCS-Format-Indicator AVP message 
    '''
    
    LOGICAL_NAME    = 0
    EMAIL_ADDRESS   = 1
    MSISDN          = 2
    URL             = 3
    SIP_URL         = 4
    
    def __init__(self, lcs_format_indicator = LOGICAL_NAME, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_format_indicator: [Unsigned32] Accepted values:
                                                * LOGICAL_NAME
                                                * EMAIL_ADDRESS
                                                * MSISDN
                                                * URL
                                                * SIP_URL
        '''
        lcs_format_indicator = int(lcs_format_indicator)
        
        if lcs_format_indicator != self.LOGICAL_NAME and \
           lcs_format_indicator != self.EMAIL_ADDRESS and \
           lcs_format_indicator != self.MSISDN and \
           lcs_format_indicator != self.URL and \
           lcs_format_indicator != self.SIP_URL:
            raise AVPParametersException('LCS-Format-Indicator AVP :: Incorrect lcs_format_indicator value [' + str(lcs_format_indicator) + ']')
        
        self.lcs_format_indicator = lcs_format_indicator
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LCS_FORMAT_INDICATOR, lcs_format_indicator, vendor_id)

class LCSEPSClientNameAVP(DiamAVP_Grouped):
    '''
        Class that defines a LCS-EPS-Client-Name AVP message 
        
            LCS-EPS-Client-Name ::= <AVP header: 2501 10415>
                        [ LCS-Name-String ] 
                        [ LCS-Format-Indicator ]
    '''
    
    def __init__(self, 
                 lcs_name_string=None,
                 lcs_format_indicator=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_name_string:
            @param lcs_format_indicator:
        '''
        
        self.lcs_name_string = lcs_name_string
        self.lcs_format_indicator = lcs_format_indicator
        self.vendor_id = vendor_id
        
        avps = []
        if self.lcs_name_string is not None:
            a = LCSNameStringAVP(self.lcs_name_string['value'])
            a.setFlags(self.lcs_name_string['flags'])
            if 'vendor' in self.lcs_name_string:
                a.setVendorID(self.lcs_name_string['vendor'])
            avps.append(a)
            
        if self.lcs_format_indicator is not None:
            a = LCSFormatIndicatorAVP(self.lcs_format_indicator['value'])
            a.setFlags(self.lcs_format_indicator['flags'])
            if 'vendor' in self.lcs_format_indicator:
                a.setVendorID(self.lcs_format_indicator['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.LCS_EPS_CLIENT_NAME, avps, self.vendor_id)

class LCSRequestorIDStringAVP(DiamAVP_UTF8String):
    '''
        Class that defines a LCS-Requestor-ID-String AVP message 
    '''
    
    def __init__(self, lcs_name_string, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_name_string: [UTF8String] contains the identification of the Requestor and 
                                                 can be e.g. MSISDN or logical name
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.LCS_NAME_STRING, lcs_name_string, vendor_id)
        self.lcs_name_string = lcs_name_string

class LCSRequestorNameAVP(DiamAVP_Grouped):
    '''
        Class that defines a LCS-Requestor-Name AVP message 
        
            LCS-Requestor-Name ::= <AVP header: 2502 10415>
                        [ LCS-Requestor-Id-String ] 
                        [ LCS-Format-Indicator ]
    '''
    
    def __init__(self, 
                 lcs_req_id=None,
                 lcs_format_indicator=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_req_id:
            @param lcs_format_indicator:
        '''
        
        self.lcs_req_id = lcs_req_id
        self.lcs_format_indicator = lcs_format_indicator
        self.vendor_id = vendor_id
        
        avps = []
        if self.lcs_req_id is not None:
            a = LCSRequestorIDStringAVP(self.lcs_req_id['value'])
            a.setFlags(self.lcs_req_id['flags'])
            if 'vendor' in self.lcs_req_id:
                a.setVendorID(self.lcs_req_id['vendor'])
            avps.append(a)
            
        if self.lcs_format_indicator is not None:
            a = LCSFormatIndicatorAVP(self.lcs_format_indicator['value'])
            a.setFlags(self.lcs_format_indicator['flags'])
            if 'vendor' in self.lcs_format_indicator:
                a.setVendorID(self.lcs_format_indicator['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.LCS_REQUESTOR_NAME, avps, self.vendor_id)

class LCSPriorityAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LCS-Priority AVP message 
    '''
    
    def __init__(self, lcs_priority, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_priority: [Unsigned32] it indicates the priority of the location request. 
                                    The value 0 shall indicate the highest priority, 
                                    and the value 1 shall indicate normal priority.
                                    All other values shall be treated as 1 (normal priority)
        '''
        lcs_priority = int(lcs_priority)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LCS_PRIORITY, lcs_priority, vendor_id)
        self.lcs_priority = lcs_priority

class LCSQoSClassAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LCS-QoS-Class AVP message 
    '''
    
    ASSURED         = 0
    BEST_EFFORT     = 1
    
    def __init__(self, lcs_qos_class = ASSURED, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_qos_class: [Unsigned32] Accepted values:
                                                * ASSURED
                                                * BEST_EFFORT
        '''
        lcs_qos_class = int(lcs_qos_class)
        
        if lcs_qos_class != self.ASSURED and \
           lcs_qos_class != self.BEST_EFFORT:
            raise AVPParametersException('LCS-QoS-Class AVP :: Incorrect lcs_qos_class value [' + str(lcs_qos_class) + ']')
        
        self.lcs_qos_class = lcs_qos_class
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LCS_QOS_CLASS, lcs_qos_class, vendor_id)

class HorizontalAccuracyAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Horizontal-Accuracy AVP message 
    '''
    
    def __init__(self, horizontal_accuracy, vendor_id=0):
        '''
            Initialize the AVP message
            @param horizontal_accuracy: [Unsigned32] Bits 6-0 corresponds to Uncertainty Code
        '''
        horizontal_accuracy = int(horizontal_accuracy)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.HORIZONTAL_ACCURACY, horizontal_accuracy, vendor_id)
        self.horizontal_accuracy = horizontal_accuracy

class VerticalAccuracyAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Vertical-Accuracy AVP message 
    '''
    
    def __init__(self, vertical_accuracy, vendor_id=0):
        '''
            Initialize the AVP message
            @param vertical_accuracy: [Unsigned32] Bits 6-0 corresponds to Uncertainty Code
        '''
        vertical_accuracy = int(vertical_accuracy)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.VERTICAL_ACCURACY, vertical_accuracy, vendor_id)
        self.vertical_accuracy = vertical_accuracy

class VerticalRequestedAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Vertical-Requested AVP message 
    '''
    
    VERTICAL_COORDINATE_IS_NOT_REQUESTED    = 0
    VERTICAL_COORDINATE_IS_REQUESTED        = 1
    
    def __init__(self, vertical_requested = VERTICAL_COORDINATE_IS_NOT_REQUESTED, vendor_id=0):
        '''
            Initialize the AVP message
            @param vertical_requested: [Unsigned32] Accepted values:
                                                * VERTICAL_COORDINATE_IS_NOT_REQUESTED
                                                * VERTICAL_COORDINATE_IS_REQUESTED
        '''
        vertical_requested = int(vertical_requested)
        
        if vertical_requested != self.VERTICAL_COORDINATE_IS_NOT_REQUESTED and \
           vertical_requested != self.VERTICAL_COORDINATE_IS_REQUESTED:
            raise AVPParametersException('Vertical-Requested AVP :: Incorrect vertical_requested value [' + str(vertical_requested) + ']')
        
        self.vertical_requested = vertical_requested
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.VERTICAL_REQUESTED, vertical_requested, vendor_id)

class VelocityRequestedAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Velocity-Requested AVP message 
    '''
    
    VELOCITY_IS_NOT_REQUESTED    = 0
    VELOCITY_IS_REQUESTED        = 1
    
    def __init__(self, velocity_requested = VELOCITY_IS_NOT_REQUESTED, vendor_id=0):
        '''
            Initialize the AVP message
            @param velocity_requested: [Unsigned32] Accepted values:
                                                * VELOCITY_IS_NOT_REQUESTED
                                                * VELOCITY_IS_REQUESTED
        '''
        velocity_requested = int(velocity_requested)
        
        if velocity_requested != self.VELOCITY_IS_NOT_REQUESTED and \
           velocity_requested != self.VELOCITY_IS_REQUESTED:
            raise AVPParametersException('Velocity-Requested AVP :: Incorrect velocity_requested value [' + str(velocity_requested) + ']')
        
        self.velocity_requested = velocity_requested
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.VELOCITY_REQUESTED, velocity_requested, vendor_id)

class ResponseTimeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Response-Time AVP message 
    '''
    
    LOW_DELAY    = 0
    DELAY_TOLERANT        = 1
    
    def __init__(self, response_time = LOW_DELAY, vendor_id=0):
        '''
            Initialize the AVP message
            @param vertical_requested: [Unsigned32] Accepted values:
                                                * LOW_DELAY
                                                * DELAY_TOLERANT
        '''
        response_time = int(response_time)
        
        if response_time != self.LOW_DELAY and \
           response_time != self.DELAY_TOLERANT:
            raise AVPParametersException('Response-Time AVP :: Incorrect response_time value [' + str(response_time) + ']')
        
        self.response_time = response_time
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.RESPONSE_TIME, response_time, vendor_id)

class LCSQoSAVP(DiamAVP_Grouped):
    '''
        Class that defines a LCS-QoS AVP message 
        
            LCS-QoS ::= <AVP header: 2504 10415>
                    [ LCS-QoS-Class ] 
                    [ Horizontal-Accuracy ] 
                    [ Vertical-Accuracy ] 
                    [ Vertical-Requested ] 
                    [ Response-Time]
    '''
    
    def __init__(self, 
                 lcs_qos_class=None,
                 horizontal_accuracy=None,
                 vertical_accuracy=None,
                 vertical_requested=None,
                 response_time=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_qos_class:
            @param horizontal_accuracy:
            @param vertical_accuracy:
            @param vertical_requested:
            @param response_time:
        '''
        
        self.lcs_qos_class = lcs_qos_class
        self.horizontal_accuracy = horizontal_accuracy
        self.vertical_accuracy = vertical_accuracy
        self.vertical_requested = vertical_requested
        self.response_time = response_time
        self.vendor_id = vendor_id
        
        avps = []
        if self.lcs_qos_class is not None:
            a = LCSQoSClassAVP(self.lcs_qos_class['value'])
            a.setFlags(self.lcs_qos_class['flags'])
            if 'vendor' in self.lcs_qos_class:
                a.setVendorID(self.lcs_qos_class['vendor'])
            avps.append(a)
            
        if self.horizontal_accuracy is not None:
            a = HorizontalAccuracyAVP(self.horizontal_accuracy['value'])
            a.setFlags(self.horizontal_accuracy['flags'])
            if 'vendor' in self.horizontal_accuracy:
                a.setVendorID(self.horizontal_accuracy['vendor'])
            avps.append(a)
            
        if self.vertical_accuracy is not None:
            a = VerticalAccuracyAVP(self.vertical_accuracy['value'])
            a.setFlags(self.vertical_accuracy['flags'])
            if 'vendor' in self.vertical_accuracy:
                a.setVendorID(self.vertical_accuracy['vendor'])
            avps.append(a)
            
        if self.vertical_requested is not None:
            a = VerticalRequestedAVP(self.vertical_requested['value'])
            a.setFlags(self.vertical_requested['flags'])
            if 'vendor' in self.vertical_requested:
                a.setVendorID(self.vertical_requested['vendor'])
            avps.append(a)
            
        if self.response_time is not None:
            a = ResponseTimeAVP(self.response_time['value'])
            a.setFlags(self.response_time['flags'])
            if 'vendor' in self.response_time:
                a.setVendorID(self.response_time['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.LCS_QOS, avps, self.vendor_id)

class LCSSupportedGADShapesAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LCS-Supported-GAD-Shapes AVP message 
    '''
    
    def __init__(self, supported_gad_shapes, vendor_id=0):
        '''
            Initialize the AVP message
            @param supported_gad_shapes: [Unsigned32] it shall contain a bitmask
        '''
        supported_gad_shapes = int(supported_gad_shapes)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.SUPPORTED_GAD_SHAPES, supported_gad_shapes, vendor_id)
        self.supported_gad_shapes = supported_gad_shapes

class LCSCodewordAVP(DiamAVP_UTF8String):
    '''
        Class that defines a LCS-Codeword AVP message 
    '''
    
    def __init__(self, lcs_codeword, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_codeword: [UTF8String] indicates the potential codeword string 
                                        to send in a notification message to the UE 
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.LCS_CODEWORD, lcs_codeword, vendor_id)
        self.lcs_codeword = lcs_codeword

class LCSPrivacyCheckAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LCS-Privacy-Check AVP message 
    '''
    
    ALLOWED_WITHOUT_NOTIFICATION    = 0
    ALLOWED_WITH_NOTIFICATION       = 1
    ALLOWED_IF_NO_RESPONSE          = 2
    RESTRICTED_IF_NO_RESPONSE       = 3
    NOT_ALLOWED                     = 4
    
    def __init__(self, lcs_privacy_check = ALLOWED_WITHOUT_NOTIFICATION, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_privacy_check: [Unsigned32] Accepted values:
                                                * ALLOWED_WITHOUT_NOTIFICATION
                                                * ALLOWED_WITH_NOTIFICATION
                                                * ALLOWED_IF_NO_RESPONSE
                                                * RESTRICTED_IF_NO_RESPONSE
                                                * NOT_ALLOWED
        '''
        lcs_privacy_check = int(lcs_privacy_check)
        
        if lcs_privacy_check != self.ALLOWED_WITHOUT_NOTIFICATION and \
           lcs_privacy_check != self.ALLOWED_WITH_NOTIFICATION and \
           lcs_privacy_check != self.ALLOWED_IF_NO_RESPONSE and \
           lcs_privacy_check != self.RESTRICTED_IF_NO_RESPONSE and \
           lcs_privacy_check != self.NOT_ALLOWED:
            raise AVPParametersException('LCS-Privacy-Check AVP :: Incorrect lcs_privacy_check value [' + str(lcs_privacy_check) + ']')
        
        self.lcs_privacy_check = lcs_privacy_check
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LCS_PRIVACY_CHECK, lcs_privacy_check, vendor_id)

class AccuracyFulfilmentIndicatorAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Accuracy-Fulfilment-Indicator AVP message 
    '''
    
    REQUESTED_ACCURACY_FULFILLED        = 0
    REQUESTED_ACCURACY_NOT_FULFILLED    = 1
    
    def __init__(self, accuracy_fulfilment_indicator = REQUESTED_ACCURACY_FULFILLED, vendor_id=0):
        '''
            Initialize the AVP message
            @param accuracy_fulfilment_indicator: [Unsigned32] Accepted values:
                                                * REQUESTED_ACCURACY_FULFILLED
                                                * REQUESTED_ACCURACY_NOT_FULFILLED
        '''
        accuracy_fulfilment_indicator = int(accuracy_fulfilment_indicator)
        
        if accuracy_fulfilment_indicator != self.REQUESTED_ACCURACY_FULFILLED and \
           accuracy_fulfilment_indicator != self.REQUESTED_ACCURACY_NOT_FULFILLED:
            raise AVPParametersException('Accuracy-Fulfilment-Indicator AVP :: Incorrect accuracy_fulfilment_indicator value [' + str(accuracy_fulfilment_indicator) + ']')
        
        self.accuracy_fulfilment_indicator = accuracy_fulfilment_indicator
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.ACCURACY_FULFILMENT_INDICATOR, accuracy_fulfilment_indicator, vendor_id)

class PLRFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a PLR-Flags AVP message 
    '''
    
    def __init__(self, plr_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param plr_flags: [Unsigned32] it contains a bit mask.
        '''
        plr_flags = int(plr_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PLR_FLAGS, plr_flags, vendor_id)
        self.plr_flags = plr_flags

class DeferredLocationTypeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Deferred-Location-Type AVP message 
    '''
    
    def __init__(self, deferred_location_type, vendor_id=0):
        '''
            Initialize the AVP message
            @param deferred_location_type: [Unsigned32] it shall contain a bitmask
        '''
        deferred_location_type = int(deferred_location_type)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.DEFERRED_LOCATION_TYPE, deferred_location_type, vendor_id)
        self.deferred_location_type = deferred_location_type

class LCSServiceTypeIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LCS-Service-Type AVP message 
    '''
    
    def __init__(self, lcs_service_type, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_service_type: [Unsigned32] it defines the identifier associated to one of the Service Types 
                                            for which the LCS client is allowed to locate the particular UE
        '''
        lcs_service_type = int(lcs_service_type)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LCS_SERVICE_TYPE_ID, lcs_service_type, vendor_id)
        self.lcs_service_type = lcs_service_type

class LCSPrivacyCheckNonSessionAVP(DiamAVP_Grouped):
    '''
        Class that defines a LCS-Privacy-Check-Non-Session AVP message 
        
            LCS-Privacy-Check-Non-Session ::= <AVP header: 2521 10415>
                        { LCS-Privacy-Check }
    '''
    
    def __init__(self, 
                 lcs_privacy_check=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_privacy_check:
        '''
        
        self.lcs_privacy_check = lcs_privacy_check
        self.vendor_id = vendor_id
        
        avps = []
        if self.lcs_privacy_check is None:
            a = LCSPrivacyCheckAVP(LCSPrivacyCheckAVP.ALLOWED_WITHOUT_NOTIFICATION, vendor_id)
        else:
            a = LCSPrivacyCheckAVP(self.lcs_privacy_check['value'])
            a.setFlags(self.lcs_privacy_check['flags'])
            if 'vendor' in self.lcs_privacy_check:
                a.setVendorID(self.lcs_privacy_check['vendor'])
        avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.LCS_PRIVACY_CHECK_NON_SESSION, avps, self.vendor_id)

class LCSPrivacyCheckSessionAVP(DiamAVP_Grouped):
    '''
        Class that defines a LCS-Privacy-Check-Session AVP message 
        
            LCS-Privacy-Check-Session ::= <AVP header: 2522 10415>
                            { LCS-Privacy-Check }
    '''
    
    def __init__(self, 
                 lcs_privacy_check=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_privacy_check:
        '''
        
        self.lcs_privacy_check = lcs_privacy_check
        self.vendor_id = vendor_id
        
        avps = []
        if self.lcs_privacy_check is None:
            a = LCSPrivacyCheckAVP(LCSPrivacyCheckAVP.ALLOWED_WITHOUT_NOTIFICATION, vendor_id)
        else:
            a = LCSPrivacyCheckAVP(self.lcs_privacy_check['value'])
            a.setFlags(self.lcs_privacy_check['flags'])
            if 'vendor' in self.lcs_privacy_check:
                a.setVendorID(self.lcs_privacy_check['vendor'])
        avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.LCS_PRIVACY_CHECK_SESSION, avps, self.vendor_id)

class LCSClientTypeAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LCS-Client-Type AVP message 
    '''
    
    EMERGENCY_SERVICES          = 0
    VALUE_ADDED_SERVICES        = 1
    PLMN_OPERATOR_SERVICES      = 2
    LAWFUL_INTERCEPT_SERVICES   = 3
    
    def __init__(self, lcs_client_type = EMERGENCY_SERVICES, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_client_type: [Unsigned32] Accepted values:
                                        * EMERGENCY_SERVICES
                                        * VALUE_ADDED_SERVICES
                                        * PLMN_OPERATOR_SERVICES
                                        * LAWFUL_INTERCEPT_SERVICES
        '''
        lcs_client_type = int(lcs_client_type)
        
        if lcs_client_type != self.EMERGENCY_SERVICES and \
           lcs_client_type != self.VALUE_ADDED_SERVICES and \
           lcs_client_type != self.PLMN_OPERATOR_SERVICES and \
           lcs_client_type != self.LAWFUL_INTERCEPT_SERVICES:
            raise AVPParametersException('LCS-Client-Type AVP :: Incorrect lcs_client_type value [' + str(lcs_client_type) + ']')
        
        self.lcs_client_type = lcs_client_type
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LCS_CLIENT_TYPE, lcs_client_type, vendor_id)

class LocationEstimateAVP(DiamAVP_OctetString):
    '''
        Class that defines a Location-Estimate AVP message 
    '''
    
    def __init__(self, location_estimate, vendor_id=0):
        '''
            Initialize the AVP message
            @param location_estimate: [OctetString] it contains an estimate of the location of an MS in universal coordinates 
                                                and the accuracy of the estimate
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.LOCATION_ESTIMATE, location_estimate, vendor_id)
        self.location_estimate = location_estimate

class AgeOfLocationEstimateAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Age-Of-Location-Estimate AVP message 
    '''
    
    def __init__(self, age_of_location_estimate, vendor_id=0):
        '''
            Initialize the AVP message
            @param age_of_location_estimate: [Unsigned32] it indicates how long ago the location estimate was obtained in minutes
        '''
        age_of_location_estimate = int(age_of_location_estimate)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.AGE_OF_LOCATION_ESTIMATE, age_of_location_estimate, vendor_id)
        self.age_of_location_estimate = age_of_location_estimate

class VelocityEstimateAVP(DiamAVP_OctetString):
    '''
        Class that defines a Velocity-Estimate AVP message 
    '''
    
    def __init__(self, velocity_estimate, vendor_id=0):
        '''
            Initialize the AVP message
            @param velocity_estimate: [OctetString] it is composed of 4 or more octets with an internal structure
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.VELOCITY_ESTIMATE, velocity_estimate, vendor_id)
        self.velocity_estimate = velocity_estimate

class EUTRANPositioningDataAVP(DiamAVP_OctetString):
    '''
        Class that defines a Velocity-Estimate AVP message 
    '''
    
    def __init__(self, eutran_positioning_data, vendor_id=0):
        '''
            Initialize the AVP message
            @param eutran_positioning_data: [OctetString] it shall contain the encoded content of the "Positioning-Data" Information Element
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.EUTRAN_POSITIONING_DATA, eutran_positioning_data, vendor_id)
        self.eutran_positioning_data = eutran_positioning_data

class ECGIAVP(DiamAVP_OctetString):
    '''
        Class that defines a ECGI AVP message 
    '''
    
    def __init__(self, ecgi, vendor_id=0):
        '''
            Initialize the AVP message
            @param ecgi: [OctetString] it indicates the E-UTRAN Cell Global Identifier
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.ECGI, ecgi, vendor_id)
        self.ecgi = ecgi

class GERANPositioningDataAVP(DiamAVP_OctetString):
    '''
        Class that defines a GERAN-Positioning-Data AVP message 
    '''
    
    def __init__(self, geran_positioning_data, vendor_id=0):
        '''
            Initialize the AVP message
            @param geran_positioning_data: [OctetString] it shall contain the encoded content of the "Positioning Data"
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.GERAN_POSITIONING_DATA, geran_positioning_data, vendor_id)
        self.geran_positioning_data = geran_positioning_data

class GERANGANSSPositioningDataAVP(DiamAVP_OctetString):
    '''
        Class that defines a GERAN-GANSS-Positioning-Data AVP message 
    '''
    
    def __init__(self, geran_ganss_positioning_data, vendor_id=0):
        '''
            Initialize the AVP message
            @param geran_ganss_positioning_data: [OctetString] it shall contain the encoded content of the "GANSS Positioning Data"
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.GERAN_GANSS_POSITIONING_DATA, geran_ganss_positioning_data, vendor_id)
        self.geran_ganss_positioning_data = geran_ganss_positioning_data

class GERANPositioningInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a GERAN-Positioning-Info AVP message 
        
            GERAN-Positioning-Info ::= <AVP header: 2524 10415>
                        [ GERAN-Positioning-Data ]
                        [ GERAN-GANSS-Positioning-Data ]
    '''
    
    def __init__(self, 
                 geran_positioning_data=None,
                 geran_ganss_positioning_data=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param geran_positioning_data:
            @param geran_ganss_positioning_data:
        '''
        
        self.geran_positioning_data = geran_positioning_data
        self.geran_ganss_positioning_data = geran_ganss_positioning_data
        self.vendor_id = vendor_id
        
        avps = []
        if self.geran_positioning_data is not None:
            a = GERANPositioningDataAVP(self.geran_positioning_data['value'])
            a.setFlags(self.geran_positioning_data['flags'])
            if 'vendor' in self.geran_positioning_data:
                a.setVendorID(self.geran_positioning_data['vendor'])
            avps.append(a)
            
        if self.geran_ganss_positioning_data is not None:
            a = GERANGANSSPositioningDataAVP(self.geran_ganss_positioning_data['value'])
            a.setFlags(self.geran_ganss_positioning_data['flags'])
            if 'vendor' in self.geran_ganss_positioning_data:
                a.setVendorID(self.geran_ganss_positioning_data['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.GERAN_POSITIONING_INFO, avps, self.vendor_id)

class UTRANPositioningDataAVP(DiamAVP_OctetString):
    '''
        Class that defines a UTRAN-Positioning-Data AVP message 
    '''
    
    def __init__(self, utran_positioning_data, vendor_id=0):
        '''
            Initialize the AVP message
            @param utran_positioning_data: [OctetString] it shall contain the encoded content of the "Positioning Data"
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.UTRAN_POSITIONING_DATA, utran_positioning_data, vendor_id)
        self.utran_positioning_data = utran_positioning_data

class UTRANGANSSPositioningDataAVP(DiamAVP_OctetString):
    '''
        Class that defines a UTRAN-GANSS-Positioning-Data AVP message 
    '''
    
    def __init__(self, utran_ganss_positioning_data, vendor_id=0):
        '''
            Initialize the AVP message
            @param utran_ganss_positioning_data: [OctetString] it shall contain the encoded content of the "GANSS Positioning Data"
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.UTRAN_GANSS_POSITIONING_DATA, utran_ganss_positioning_data, vendor_id)
        self.utran_ganss_positioning_data = utran_ganss_positioning_data

class UTRANAdditionalPositioningDataAVP(DiamAVP_OctetString):
    '''
        Class that defines a UTRAN-Additional-Positioning-Data AVP message 
    '''
    
    def __init__(self, utran_additional_positioning_data, vendor_id=0):
        '''
            Initialize the AVP message
            @param utran_additional_positioning_data: [OctetString] it  contains the "UTRAN Additional Positioning Data"
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.UTRAN_ADDITIONAL_POSITIONING_DATA, utran_additional_positioning_data, vendor_id)
        self.utran_additional_positioning_data = utran_additional_positioning_data

class UTRANPositioningInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a UTRAN-Positioning-Info AVP message 
        
            UTRAN-Positioning-Info ::= <AVP header: 2527 10415>
                        [ UTRAN-Positioning-Data ]
                        [ UTRAN-GANSS-Positioning-Data ]
                        [ UTRAN-Additional-Positioning-Data ]
    '''
    
    def __init__(self, 
                 utran_positioning_data=None,
                 utran_ganss_positioning_data=None,
                 utran_additional_positioning_data=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param utran_positioning_data:
            @param utran_ganss_positioning_data:
            @param utran_additional_positioning_data:
        '''
        
        self.utran_positioning_data = utran_positioning_data
        self.utran_ganss_positioning_data = utran_ganss_positioning_data
        self.utran_additional_positioning_data = utran_additional_positioning_data
        self.vendor_id = vendor_id
        
        avps = []
        if self.utran_positioning_data is not None:
            a =UTRANPositioningDataAVP(self.utran_positioning_data['value'])
            a.setFlags(self.utran_positioning_data['flags'])
            if 'vendor' in self.utran_positioning_data:
                a.setVendorID(self.utran_positioning_data['vendor'])
            avps.append(a)
            
        if self.utran_ganss_positioning_data is not None:
            a = UTRANGANSSPositioningDataAVP(self.utran_ganss_positioning_data['value'])
            a.setFlags(self.utran_ganss_positioning_data['flags'])
            if 'vendor' in self.utran_ganss_positioning_data:
                a.setVendorID(self.utran_ganss_positioning_data['vendor'])
            avps.append(a)
            
        if self.utran_additional_positioning_data is not None:
            a = UTRANAdditionalPositioningDataAVP(self.utran_additional_positioning_data['value'])
            a.setFlags(self.utran_additional_positioning_data['flags'])
            if 'vendor' in self.utran_additional_positioning_data:
                a.setVendorID(self.utran_additional_positioning_data['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.UTRAN_POSITIONING_INFO, avps, self.vendor_id)

class PLAFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a PLA-Flags AVP message 
    '''
    
    def __init__(self, pla_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param pla_flags: [Unsigned32] it contains a bit mask.
        '''
        pla_flags = int(pla_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PLA_FLAGS, pla_flags, vendor_id)
        self.pla_flags = pla_flags

class LRRFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LRR-Flags AVP message 
    '''
    
    def __init__(self, lrr_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param lrr_flags: [Unsigned32] it contains a bit mask.
        '''
        lrr_flags = int(lrr_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LRR_FLAGS, lrr_flags, vendor_id)
        self.lrr_flags = lrr_flags

class CellPortionIDAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Cell-Portion-ID AVP message 
    '''
    
    def __init__(self, cell_portion_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param cell_portion_id: [Unsigned32] it indicates the current Cell Portion location of the target UE as provided by the E-SMLC
        '''
        cell_portion_id = int(cell_portion_id)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.CELL_PORTION_ID, cell_portion_id, vendor_id)
        self.cell_portion_id = cell_portion_id

class ESMLCCellInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a ESMLC-Cell-Info AVP message 
        
            ESMLC-Cell-Info ::= <AVP header: 2552 10415>
                        [ ECGI ]
                        [ Cell-Portion-ID ]
    '''
    
    def __init__(self, 
                 ecgi=None,
                 cell_portion_id=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param ecgi:
            @param cell_portion_id:
        '''
        
        self.ecgi = ecgi
        self.cell_portion_id = cell_portion_id
        self.vendor_id = vendor_id
        
        avps = []
        if self.ecgi is not None:
            a =ECGIAVP(self.ecgi['value'])
            a.setFlags(self.ecgi['flags'])
            if 'vendor' in self.ecgi:
                a.setVendorID(self.ecgi['vendor'])
            avps.append(a)
            
        if self.cell_portion_id is not None:
            a = CellPortionIDAVP(self.cell_portion_id['value'])
            a.setFlags(self.cell_portion_id['flags'])
            if 'vendor' in self.cell_portion_id:
                a.setVendorID(self.cell_portion_id['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.ESMLC_CELL_INFO, avps, self.vendor_id)

class CivicAddressAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Civic-Address AVP message 
    '''
    
    def __init__(self, civic_address, vendor_id=0):
        '''
            Initialize the AVP message
            @param civic_address: [UTF8String] it contains the XML document carried in the "Civic Address" Information Element 
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.CIVIC_ADDRESS, civic_address, vendor_id)
        self.civic_address = civic_address

class BarometricPressureAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Barometric-Pressure AVP message 
    '''
    
    def __init__(self, barometric_pressure, vendor_id=0):
        '''
            Initialize the AVP message
            @param barometric_pressure: [Unsigned32] it contains the "Barometric Pressure" Information Element
        '''
        barometric_pressure = int(barometric_pressure)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.BAROMETRIC_PRESSURE, barometric_pressure, vendor_id)
        self.barometric_pressure = barometric_pressure

class CellGlobalIdentityAVP(DiamAVP_OctetString):
    '''
        Class that defines a Cell-Global-Identity AVP message 
    '''
    
    def __init__(self, cell_global_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param cell_global_id: [OctetString] it shall contain the Cell Global Identification of the user 
                                         which identifies the cell the user equipment is registered
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.CELL_GLOBAL_IDENTITY, cell_global_id, vendor_id)
        self.cell_global_id = cell_global_id

class ServiceAreaIdentityAVP(DiamAVP_OctetString):
    '''
        Class that defines a Service-Area-Identity AVP message 
    '''
    
    def __init__(self, service_area_id, vendor_id=0):
        '''
            Initialize the AVP message
            @param service_area_id: [OctetString] it shall contain the Service Area Identifier of the user where the user is located
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.SERVICE_AREA_IDENTITY, service_area_id, vendor_id)
        self.service_area_id = service_area_id

class LocationEventAVP(DiamAVP_Integer32):
    '''
        Class that defines the Location-Event AVP message
    '''

    EMERGENCY_CALL_ORIGINATION      = 0
    EMERGENCY_CALL_RELEASE          = 1
    MO_LR                           = 2
    EMERGENCY_CALL_HANDOVER         = 3
    DEFERRED_MT_LR_RESPONSE         = 4
    DEFERRED_MO_LR_TTTP_INITIATION  = 5
    DELAYED_LOCATION_REPORTING      = 6

    def __init__(self, location_event, vendor_id=0):
        '''
            Initialize the AVP message
            @param location_event: [Enumerated] 
        '''
        
        location_event = int(location_event)
        if location_event != self.EMERGENCY_CALL_ORIGINATION and \
           location_event != self.EMERGENCY_CALL_RELEASE and \
           location_event != self.MO_LR and \
           location_event != self.EMERGENCY_CALL_HANDOVER and \
           location_event != self.DEFERRED_MT_LR_RESPONSE and \
           location_event != self.DEFERRED_MO_LR_TTTP_INITIATION and \
           location_event != self.DELAYED_LOCATION_REPORTING:
            raise AVPParametersException('Location-Event AVP :: Incorrect location_event [' + str(location_event) + ']')

        self.location_event = location_event
        DiamAVP_Integer32.__init__(self, DiamAVPCodes.LOCATION_EVENT, location_event, vendor_id)

class PseudonymIndicatorAVP(DiamAVP_Integer32):
    '''
        Class that defines the Pseudonym-Indicator AVP message
    '''

    PSEUDONYM_NOT_REQUESTED     = 0
    PSEUDONYM_REQUESTED         = 1

    def __init__(self, pseudonym_indicator, vendor_id=0):
        '''
            Initialize the AVP message
            @param pseudonym_indicator: [Enumerated] it defines if a pseudonym is requested
        '''
        
        pseudonym_indicator = int(pseudonym_indicator)
        if pseudonym_indicator != self.PSEUDONYM_NOT_REQUESTED and \
            pseudonym_indicator != self.PSEUDONYM_REQUESTED:
            raise AVPParametersException('Pseudonym-Indicator AVP :: Incorrect pseudonym_indicator [' + str(pseudonym_indicator) + ']')

        self.pseudonym_indicator = pseudonym_indicator
        DiamAVP_Integer32.__init__(self, DiamAVPCodes.PSEUDONYM_INDICATOR, pseudonym_indicator, vendor_id)

class DeferredMTLRDataAVP(DiamAVP_Grouped):
    '''
        Class that defines a Deferred-MT-LR-Data AVP message 
        
            Deferred-MT-LR-Data ::= <AVP header: 2547 10415>
                        { Deferred-Location-Type }
                        [ Termination-Cause ]
                        [ Serving-Node ]
    '''
    
    def __init__(self, 
                 deferred_location_type=None,
                 termination_cause=None,
                 serving_node=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param deferred_location_type:
            @param termination_cause:
            @param serving_node:
        '''
        
        self.deferred_location_type = deferred_location_type
        self.termination_cause = termination_cause
        self.serving_node = serving_node
        self.vendor_id = vendor_id
        
        avps = []
        if self.deferred_location_type is not None:
            a = DeferredLocationTypeAVP(self.deferred_location_type['value'])
            a.setFlags(self.deferred_location_type['flags'])
            if 'vendor' in self.deferred_location_type:
                a.setVendorID(self.deferred_location_type['vendor'])
            avps.append(a)
        
        if self.termination_cause is not None:
            a = TerminationCauseAVP(self.termination_cause['value'])
            a.setFlags(self.termination_cause['flags'])
            if 'vendor' in self.termination_cause:
                a.setVendorID(self.termination_cause['vendor'])
            avps.append(a)
            
        if self.serving_node is not None:
            a = ServingNodeAVP(self.serving_node['value'])
            a.setFlags(self.serving_node['flags'])
            if 'vendor' in self.serving_node:
                a.setVendorID(self.serving_node['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.DEFERRED_MT_LR_DATA, avps, self.vendor_id)

class TerminationCauseAVP(DiamAVP_Unsigned32):
    '''
        Class that defines the Termination-Cause AVP message
    '''

    NORMAL                                      = 0
    ERROR_UNDEFINED                             = 1
    INTERNAL_TIMEOUT                            = 2
    CONGESTION                                  = 3
    MT_LR_RESTART                               = 4
    PRIVACY_VIOLATION                           = 5
    SHAPE_OF_LOCATION_ESTIMATE_NOT_SUPPORTED    = 6
    SUBSCRIBER_TERMINATION                      = 7
    UE_TERMINATION                              = 8
    NETWORK_TERMINATION                         = 9

    def __init__(self, termination_cause, vendor_id=0):
        '''
            Initialize the AVP message
            @param termination_cause: [Enumerated] 
        '''
        
        termination_cause = int(termination_cause)
        if termination_cause != self.NORMAL and \
           termination_cause != self.ERROR_UNDEFINED and \
           termination_cause != self.INTERNAL_TIMEOUT and \
           termination_cause != self.CONGESTION and \
           termination_cause != self.MT_LR_RESTART and \
           termination_cause != self.PRIVACY_VIOLATION and \
           termination_cause != self.SHAPE_OF_LOCATION_ESTIMATE_NOT_SUPPORTED and \
           termination_cause != self.SUBSCRIBER_TERMINATION and \
           termination_cause != self.UE_TERMINATION and \
           termination_cause != self.NETWORK_TERMINATION:
            raise AVPParametersException('Termination-Cause AVP :: Incorrect termination_cause [' + str(termination_cause) + ']')

        self.termination_cause = termination_cause
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.TERMINATION_CAUSE, termination_cause, vendor_id)

class xRTTRCID1AVP(DiamAVP_OctetString):
    '''
        Class that defines a 1xRTT-RCID AVP message 
    '''
    
    def __init__(self, xrtt_rcid, vendor_id=0):
        '''
            Initialize the AVP message
            @param xrtt_rcid: [OctetString] it indicates the 1xRTT Reference Cell Id
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.XRTT_RCID_1, xrtt_rcid, vendor_id)
        self.xrtt_rcid = xrtt_rcid

class LCSReferenceNumberAVP(DiamAVP_OctetString):
    '''
        Class that defines a LCS-Reference-Number AVP message 
    '''
    
    def __init__(self, lcs_reference_number, vendor_id=0):
        '''
            Initialize the AVP message
            @param lcs_reference_number: [OctetString] it shall contain the reference number identifying the deferred location request.
        '''
        DiamAVP_OctetString.__init__(self, DiamAVPCodes.LCS_REFERENCE_NUMBER, lcs_reference_number, vendor_id)
        self.lcs_reference_number = lcs_reference_number

class ReportingAmountAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Reporting-Amount AVP message 
    '''
    
    def __init__(self, reporting_amount, vendor_id=0):
        '''
            Initialize the AVP message
            @param reporting_amount: [Unsigned32] it contains reporting frequency
        '''
        reporting_amount = int(reporting_amount)
        
        if reporting_amount < 1 or reporting_amount > 8639999:
            raise AVPParametersException('Reporting-Amount AVP :: The reporting_amount must be between 1 and 8639999') 
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.REPORTING_AMOUNT, reporting_amount, vendor_id)
        self.reporting_amount = reporting_amount

class ReportingIntervalAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Reporting-Interval AVP message 
    '''
    
    def __init__(self, reporting_interval, vendor_id=0):
        '''
            Initialize the AVP message
            @param reporting_interval: [Unsigned32] it contains reporting interval in seconds
        '''
        reporting_interval = int(reporting_interval)
        
        if reporting_interval < 1 or reporting_interval > 8639999:
            raise AVPParametersException('Reporting-Interval AVP :: The reporting_interval must be between 1 and 8639999') 
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.REPORTING_INTERVAL, reporting_interval, vendor_id)
        self.reporting_interval = reporting_interval

class PeriodicLDRInformationAVP(DiamAVP_Grouped):
    '''
        Class that defines a Periodic-LDR-Info AVP message 
        
            Periodic-LDR-Info ::= <AVP header: 2540 10415>
                    { Reporting-Amount }
                    { Reporting-Interval }
    '''
    
    def __init__(self, 
                 reporting_amount=None,
                 reporting_interval=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param reporting_amount:
            @param reporting_interval:
        '''
        
        self.reporting_amount = reporting_amount
        self.reporting_interval = reporting_interval
        self.vendor_id = vendor_id
        
        avps = []
        if self.reporting_amount is None:
            raise AVPParametersException('Periodic-LDR-Info AVP :: The reporting_amount is MANDATORY')
        a = ReportingAmountAVP(self.reporting_amount['value'])
        a.setFlags(self.reporting_amount['flags'])
        if 'vendor' in self.reporting_amount:
            a.setVendorID(self.reporting_amount['vendor'])
        avps.append(a)
        
        if self.reporting_interval is None:
            raise AVPParametersException('Periodic-LDR-Info AVP :: The reporting_interval is MANDATORY')
        a = ReportingIntervalAVP(self.reporting_interval['value'])
        a.setFlags(self.reporting_interval['flags'])
        if 'vendor' in self.reporting_interval:
            a.setVendorID(self.reporting_interval['vendor'])
        avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.PERIODIC_LDR_INFORMATION, avps, self.vendor_id)

class LRAFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a LRA-Flags AVP message 
    '''
    
    def __init__(self, lra_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param lra_flags: [Unsigned32] it contains reporting interval in seconds
        '''
        lra_flags = int(lra_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.LRA_FLAGS, lra_flags, vendor_id)
        self.lra_flags = lra_flags

class ReportingPLMNListAVP(DiamAVP_Grouped):
    '''
        Class that defines a DReporting-PLMN-List AVP message 
        
            Reporting-PLMN-List ::= <AVP header: 2543 10415>
                        1*20{ PLMN-ID-List }
                        [ Prioritized-List-Indicator ]
    '''
    
    def __init__(self, 
                 plmn_id_list=None,
                 prioritized_list_indicator=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param plmn_id_list:
            @param reporting_interval:
        '''
        
        self.plmn_id_list = plmn_id_list
        self.prioritized_list_indicator = prioritized_list_indicator
        self.vendor_id = vendor_id
        
        avps = []
        if self.plmn_id_list is None:
            raise AVPParametersException('Reporting-PLMN-List AVP :: The plmn_id_list is MANDATORY')
        a = PLMNIDListAVP(self.plmn_id_list['value'])
        a.setFlags(self.plmn_id_list['flags'])
        if 'vendor' in self.plmn_id_list:
            a.setVendorID(self.plmn_id_list['vendor'])
        avps.append(a)
        
        if self.prioritized_list_indicator is None:
            raise AVPParametersException('Reporting-PLMN-List AVP :: The prioritized_list_indicator is MANDATORY')
        a = PrioritizedListIndicatorAVP(self.prioritized_list_indicator['value'])
        a.setFlags(self.prioritized_list_indicator['flags'])
        if 'vendor' in self.prioritized_list_indicator:
            a.setVendorID(self.prioritized_list_indicator['vendor'])
        avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.PERIODIC_LDR_INFORMATION, avps, self.vendor_id)

class PrioritizedListIndicatorAVP(DiamAVP_Unsigned32):
    '''
        Class that defines the Prioritized-List-Indicator AVP message
    '''

    NOT_SUPPORTED       = 0
    SUPPORTED           = 1

    def __init__(self, prioritized_list_indicator, vendor_id=0):
        '''
            Initialize the AVP message
            @param prioritized_list_indicator: [Enumerated] 
        '''
        
        prioritized_list_indicator = int(prioritized_list_indicator)
        if prioritized_list_indicator != self.NOT_SUPPORTED and \
           prioritized_list_indicator != self.SUPPORTED:
            raise AVPParametersException('Prioritized-List-Indicator AVP :: Incorrect prioritized_list_indicator [' + str(prioritized_list_indicator) + ']')

        self.prioritized_list_indicator = prioritized_list_indicator
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PRIORITIZED_LIST_INDICATOR, prioritized_list_indicator, vendor_id)

class PeriodicLocationSupportIndicatorAVP(DiamAVP_Unsigned32):
    '''
        Class that defines the Periodic-Location-Support-Indicator AVP message
    '''

    NOT_SUPPORTED       = 0
    SUPPORTED           = 1

    def __init__(self, periodic_location_support_indicator, vendor_id=0):
        '''
            Initialize the AVP message
            @param periodic_location_support_indicator: [Enumerated] 
        '''
        
        periodic_location_support_indicator = int(periodic_location_support_indicator)
        if periodic_location_support_indicator != self.NOT_SUPPORTED and \
           periodic_location_support_indicator != self.SUPPORTED:
            raise AVPParametersException('Periodic-Location-Support-Indicator AVP :: Incorrect periodic_location_support_indicator [' + str(periodic_location_support_indicator) + ']')

        self.periodic_location_support_indicator = periodic_location_support_indicator
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.PERIODIC_LOCATION_SUPPORT_INDICATOR, periodic_location_support_indicator, vendor_id)

class PLMNIDListAVP(DiamAVP_Grouped):
    '''
        Class that defines a PLMN-ID-List AVP message 
        
            PLMN-ID-List ::= <AVP header: 2544 10415>
                    { Visited-PLMN-Id }
                    [ Periodic-Location-Support-Indicator ]
    '''
    
    def __init__(self, 
                 visited_plmn_id=None,
                 periodic_location_support_indicator=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param visited_plmn_id:
            @param periodic_location_support_indicator:
        '''
        
        self.visited_plmn_id = visited_plmn_id
        self.periodic_location_support_indicator = periodic_location_support_indicator
        self.vendor_id = vendor_id
        
        avps = []
        if self.visited_plmn_id is None:
            raise AVPParametersException('PLMN-ID-List :: The visited_plmn_id is MANDATORY')
        a = VisitedPLMNIDAVP(self.visited_plmn_id['value'])
        a.setFlags(self.visited_plmn_id['flags'])
        if 'vendor' in self.visited_plmn_id:
            a.setVendorID(self.visited_plmn_id['vendor'])
        avps.append(a)
        
        if self.periodic_location_support_indicator is not None:
            a = PeriodicLocationSupportIndicatorAVP(self.periodic_location_support_indicator['value'])
            a.setFlags(self.periodic_location_support_indicator['flags'])
            if 'vendor' in self.periodic_location_support_indicator:
                a.setVendorID(self.periodic_location_support_indicator['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.PLMN_ID_LIST, avps, self.vendor_id)

class UARFlagsAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a UAR-Flags AVP message 
    '''
    
    def __init__(self, uar_flags, vendor_id=0):
        '''
            Initialize the AVP message
            @param uar_flags: [Unsigned32] it shall contain a bit mask.
        '''
        uar_flags = int(uar_flags)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.UAR_FLAGS, uar_flags, vendor_id)
        self.uar_flags = uar_flags

class PublicIdentityAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Public-Identity AVP message 
    '''
    
    def __init__(self, public_identity, vendor_id=0):
        '''
            Initialize the AVP message
            @param public_identity: [UTF8String] 
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.PUBLIC_IDENTITY, public_identity, vendor_id)
        self.public_identity = public_identity

class UserAuthorizationTypeAVP(DiamAVP_Integer32):
    '''
        Class that defines the User-Authorization-Type AVP message 
    '''
    
    REGISTRATION                    = 0
    DE_REGISTRATION                 = 1
    REGISTRATION_AND_CAPABILITIES   = 2
    
    def __init__(self, user_authorization_type = REGISTRATION, vendor_id=0):
        '''
            Initialize the AVP message
            @param user_authorization_type: [Enumerated] to choose between REGISTRATION, DE_REGISTRATION and REGISTRATION_AND_CAPABILITIES
        '''
        user_authorization_type = int(user_authorization_type)
        if user_authorization_type != self.REGISTRATION and \
           user_authorization_type != self.DE_REGISTRATION and \
           user_authorization_type != self.REGISTRATION_AND_CAPABILITIES:
            raise AVPParametersException('User-Authorization-Type AVP :: Incorrect user_authorization_type [' + str(user_authorization_type) + ']')
        
        self.user_authorization_type = user_authorization_type
        DiamAVP_Integer32.__init__(self, DiamAVPCodes.USER_AUTHORIZATION_TYPE, self.user_authorization_type, vendor_id)

class ServerNameAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Server-Name AVP message 
    '''
    
    def __init__(self, server_name, vendor_id=0):
        '''
            Initialize the AVP message
            @param server_name: [UTF8String] This AVP contains a SIP-URL used to identify a SIP server (e.g. S-CSCF name).
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.SERVER_NAME, server_name, vendor_id)
        self.server_name = server_name

class MandatoryCapabilityAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a Mandatory-Capability AVP message 
    '''
    
    def __init__(self, mandatory_capability, vendor_id=0):
        '''
            Initialize the AVP message
            @param mandatory_capability: [Unsigned32] it represent a single determined mandatory capability or 
                                                      a set of capabilities of an S-CSCF.
        '''
        mandatory_capability = int(mandatory_capability)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.MANDATORY_CAPABILITY, mandatory_capability, vendor_id)
        self.mandatory_capability = mandatory_capability

class OptionalCapabilityAVP(DiamAVP_Unsigned32):
    '''
        Class that defines a UAR-Flags AVP message 
    '''
    
    def __init__(self, optional_capability, vendor_id=0):
        '''
            Initialize the AVP message
            @param optional_capability: [Unsigned32] it represent a single determined optional capability or 
                                                     a set of capabilities of an S-CSCF
        '''
        optional_capability = int(optional_capability)
        
        DiamAVP_Unsigned32.__init__(self, DiamAVPCodes.OPTIONAL_CAPABILITY, optional_capability, vendor_id)
        self.optional_capability = optional_capability

class ServerCapabilitiesAVP(DiamAVP_Grouped):
    '''
        Class that defines a Server-Capabilities AVP message 
        
            Server-Capabilities ::= <AVP header: 603 10415>
                        *[Mandatory-Capability]
                        *[Optional-Capability]
                        *[Server-Name]
    '''
    
    def __init__(self, 
                 mandatory_capability=None,
                 optional_capability=None,
                 server_name=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param mandatory_capability:
            @param optional_capability:
            @param server_name:
        '''
        
        self.mandatory_capability = mandatory_capability
        self.optional_capability = optional_capability
        self.server_name = server_name
        self.vendor_id = vendor_id
        
        avps = []
        if self.mandatory_capability is not None:
            a = VisitedPLMNIDAVP(self.mandatory_capability['value'])
            a.setFlags(self.mandatory_capability['flags'])
            if 'vendor' in self.mandatory_capability:
                a.setVendorID(self.mandatory_capability['vendor'])
            avps.append(a)
        
        if self.optional_capability is not None:
            a = PeriodicLocationSupportIndicatorAVP(self.optional_capability['value'])
            a.setFlags(self.optional_capability['flags'])
            if 'vendor' in self.optional_capability:
                a.setVendorID(self.optional_capability['vendor'])
            avps.append(a)

        if self.server_name is not None:
            a = ServerNameAVP(self.server_name['value'])
            a.setFlags(self.server_name['flags'])
            if 'vendor' in self.server_name:
                a.setVendorID(self.server_name['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.SERVER_CAPABILITY, avps, self.vendor_id)

class ServerAssignmentTypeAVP(DiamAVP_Integer32):
    '''
        Class that defines the Server-Assignment-Type AVP message 
    '''
    
    NO_ASSIGNMENT                               = 0
    REGISTRATION                                = 1
    RE_REGISTRATION                             = 2
    UNREGISTERED_USER                           = 3
    TIMEOUT_DEREGISTRATION                      = 4
    USER_DEREGISTRATION                         = 5
    TIMEOUT_DEREGISTRATION_STORE_SERVER_NAME    = 6
    USER_DEREGISTRATION_STORE_SERVER_NAME       = 7
    ADMINISTRATIVE_DEREGISTRATION               = 8
    AUTHENTICATION_FAILURE                      = 9
    AUTHENTICATION_TIMEOUT                      = 10
    DEREGISTRATION_TOO_MUCH_DATA                = 11
    AAA_USER_DATA_REQUEST                        = 12
    PGW_UPDATE                                  = 13
    RESTORATION                                 = 14
    
    def __init__(self, server_assignment_type = NO_ASSIGNMENT, vendor_id=0):
        '''
            Initialize the AVP message
            @param server_assignment_type: [Enumerated] some values
        '''
        server_assignment_type = int(server_assignment_type)
        if server_assignment_type != self.NO_ASSIGNMENT and \
           server_assignment_type != self.REGISTRATION and \
           server_assignment_type != self.RE_REGISTRATION and \
           server_assignment_type != self.UNREGISTERED_USER and \
           server_assignment_type != self.TIMEOUT_DEREGISTRATION and \
           server_assignment_type != self.USER_DEREGISTRATION and \
           server_assignment_type != self.TIMEOUT_DEREGISTRATION_STORE_SERVER_NAME and \
           server_assignment_type != self.USER_DEREGISTRATION_STORE_SERVER_NAME and \
           server_assignment_type != self.ADMINISTRATIVE_DEREGISTRATION and \
           server_assignment_type != self.AUTHENTICATION_FAILURE and \
           server_assignment_type != self.AUTHENTICATION_TIMEOUT and \
           server_assignment_type != self.DEREGISTRATION_TOO_MUCH_DATA and \
           server_assignment_type != self.AAA_USER_DATA_REQUEST and \
           server_assignment_type != self.PGW_UPDATE and \
           server_assignment_type != self.RESTORATION:
            raise AVPParametersException('Server-Assignment-Type AVP :: Incorrect server_assignment_type [' + str(server_assignment_type) + ']')
        
        self.server_assignment_type = server_assignment_type
        DiamAVP_Integer32.__init__(self, DiamAVPCodes.SERVER_ASSIGNMENT_TYPE, self.server_assignment_type, vendor_id)

class UserDataAlreadyAvailableAVP(DiamAVP_Integer32):
    '''
        Class that defines the User-Data-Already-Available AVP message 
    '''
    
    USER_DATA_NOT_AVAILABLE                    = 0
    USER_DATA_ALREADY_AVAILABLE                = 1
    
    def __init__(self, user_data_already_available = USER_DATA_NOT_AVAILABLE, vendor_id=0):
        '''
            Initialize the AVP message
            @param user_data_already_available: [Enumerated] to choose between USER_DATA_NOT_AVAILABLE and USER_DATA_ALREADY_AVAILABLE
        '''
        user_data_already_available = int(user_data_already_available)
        if user_data_already_available != self.USER_DATA_NOT_AVAILABLE and \
           user_data_already_available != self.USER_DATA_ALREADY_AVAILABLE:
            raise AVPParametersException('User-Data-Already-Available AVP :: Incorrect user_data_already_available [' + str(user_data_already_available) + ']')
        
        self.user_data_already_available = user_data_already_available
        DiamAVP_Integer32.__init__(self, DiamAVPCodes.USER_DATA_ALREADY_AVAILABLE, self.user_data_already_available, vendor_id)

class DRMPAVP(DiamAVP_Integer32):
    '''
        Class that defines the DRMP AVP message 
    '''
    
    PRIORITY_0  = 0
    PRIORITY_1  = 1
    PRIORITY_2  = 2
    PRIORITY_3  = 3
    PRIORITY_4  = 4
    PRIORITY_5  = 5
    PRIORITY_6  = 6
    PRIORITY_7  = 7
    PRIORITY_8  = 8
    PRIORITY_9  = 9
    PRIORITY_10 = 10
    PRIORITY_11 = 11
    PRIORITY_12 = 12
    PRIORITY_13 = 13
    PRIORITY_14 = 14
    
    def __init__(self, drmp = PRIORITY_0, vendor_id=0):
        '''
            Initialize the AVP message
            @param drmp: [Enumerated] to choose between PRIORITY_0 and PRIORITY_14
        '''
        drmp = int(drmp)
        if drmp != self.PRIORITY_0 and \
           drmp != self.PRIORITY_1 and \
           drmp != self.PRIORITY_2 and \
           drmp != self.PRIORITY_3 and \
           drmp != self.PRIORITY_4 and \
           drmp != self.PRIORITY_5 and \
           drmp != self.PRIORITY_6 and \
           drmp != self.PRIORITY_7 and \
           drmp != self.PRIORITY_8 and \
           drmp != self.PRIORITY_9 and \
           drmp != self.PRIORITY_10 and \
           drmp != self.PRIORITY_11 and \
           drmp != self.PRIORITY_12 and \
           drmp != self.PRIORITY_13 and \
           drmp != self.PRIORITY_14:
            raise AVPParametersException('User-Data-Already-Available AVP :: Incorrect drmp [' + str(drmp) + ']')
        
        self.drmp = drmp
        DiamAVP_Integer32.__init__(self, DiamAVPCodes.DRMP, self.drmp, vendor_id)

class WildcardedPublicIdentityAVP(DiamAVP_UTF8String):
    '''
        Class that defines a Wildcarded-Public-Identity AVP message 
    '''
    
    def __init__(self, wildcarded_public_identity, vendor_id=0):
        '''
            Initialize the AVP message
            @param wildcarded_public_identity: [UTF8String] This AVP contains a Wildcarded PSI or Wildcarded Public User Identity stored in the HSS.
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.WILDCARDED_PUBLIC_IDENTITY, wildcarded_public_identity, vendor_id)
        self.wildcarded_public_identity = wildcarded_public_identity

class SCSCFRestorationInfoAVP(DiamAVP_Grouped):
    '''
        Class that defines a SCSCF-Restoration-Info AVP message 
        
           SCSCF-Restoration-Info ::= < AVP Header: 639, 10415>
                        { User-Name }
                        1*{ Restoration-Info }
                        [ SIP-Authentication-Scheme ]
    '''
    
    def __init__(self, 
                 user_name=None,
                 restoration_info=None,
                 sip_authentication_scheme=None,
                 vendor_id=0):
        '''
            Initialize the AVP message
            @param user_name:
            @param restoration_info:
            @param sip_authentication_scheme:
        '''
        
        self.user_name = user_name
        self.restoration_info = restoration_info
        self.sip_authentication_scheme = sip_authentication_scheme
        self.vendor_id = vendor_id
        
        avps = []
        if self.user_name is None:
            raise AVPParametersException('SCSCF-Restoration-Info :: The user_name is MANDATORY')
        a = UserNameAVP(self.user_name['value'])
        a.setFlags(self.user_name['flags'])
        if 'vendor' in self.user_name:
            a.setVendorID(self.user_name['vendor'])
        avps.append(a)
        
        if self.restoration_info is None:
            raise AVPParametersException('SCSCF-Restoration-Info :: The restoration_info is MANDATORY')
        a = SCSCFRestorationInfoAVP(self.restoration_info['value'])
        a.setFlags(self.restoration_info['flags'])
        if 'vendor' in self.restoration_info:
            a.setVendorID(self.restoration_info['vendor'])
        avps.append(a)

        if self.sip_authentication_scheme is not None:
            a = SIPAuthenticationSchemeAVP(self.sip_authentication_scheme['value'])
            a.setFlags(self.sip_authentication_scheme['flags'])
            if 'vendor' in self.sip_authentication_scheme:
                a.setVendorID(self.sip_authentication_scheme['vendor'])
            avps.append(a)
            
        DiamAVP_Grouped.__init__(self, DiamAVPCodes.SCSCF_RESTORATION_INFO, avps, self.vendor_id)

class SIPAuthenticationSchemeAVP(DiamAVP_UTF8String):
    '''
        Class that defines a SIP-Authentication-Scheme AVP message 
    '''
    
    def __init__(self, sip_authentication_scheme, vendor_id=0):
        '''
            Initialize the AVP message
            @param sip_authentication_scheme: [UTF8String] This AVP contains a Wildcarded PSI or Wildcarded Public User Identity stored in the HSS.
        '''
        DiamAVP_UTF8String.__init__(self, DiamAVPCodes.SIP_AUTHENTICATION_SCHEME, sip_authentication_scheme, vendor_id)
        self.sip_authentication_scheme = sip_authentication_scheme












''' ---------------------------------------------------------------------------------------- '''
''' 
    ~~~ MISSING AVPs  ::  UNIMPLEMENTED ~~~
        LCSInfoAVP
        ChargingCharacteristics3GPPAVP            NOOOOOO
        TraceDataAVP
        GPRSSubscriptionDataAVP
        CSGSubscriptionDataAVP
        AESECommunicationPatternAVP
        EPSLocationInformationAVP
        SubscriptionDataAVP                    MISSING SOME AVP
        AuthenticationInfoAVP
'''
''' ---------------------------------------------------------------------------------------- '''


