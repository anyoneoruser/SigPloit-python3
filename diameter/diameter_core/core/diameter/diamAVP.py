#!/usr/bin/env  python
# -*- coding: utf-8 -*-
'''
Created on 07 ott 2015

@author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
'''

import struct
import binascii
from core.commons import logErr

'''
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      AVP Code                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Flags     |                                             |
|V M P x x x x x|                AVP Length                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|              Vendor-ID (if vendor-specific AVP)             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   AVP Data ... (variable length)
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
'''
   
##
## @brief      Support class that defines a RFC-based Diameter AVP (RFC 3588)
##         
class DiamAVP(object):

    avp_flag_vendor        = 0x80
    avp_flag_mandatory     = 0x40
    avp_flag_private       = 0x20
    
    def __init__(self, avp_code, data, vendor_id = 0):
        self.avp_code = avp_code    # (32) from DiamAVPCodes
        self.flags = 0x00

        if vendor_id is not None and vendor_id != 0:
            self.is_vendor = True   # (1)
            self.vendor_id = vendor_id # (32)
            self.flags += 0x80 if self.is_vendor else 0x00
            if isinstance(self.vendor_id, dict) and 'value' in self.vendor_id:
                self.vendor_id = int(self.vendor_id['value'])
            if not isinstance(self.vendor_id, int):
                self.vendor_id = int(self.vendor_id)            
        else:
            self.is_vendor = False  # (1)
            self.vendor_id = 0      # (32)
            
        self.is_mandatory = False   # (1)
        self.is_protected = False   # (1)
        self.avp_length = -1        # (24)
        self.data = data            # (8*n)
            
        self.flags += 0x40 if self.is_mandatory else 0x00
        self.flags += 0x20 if self.is_protected else 0x00
    
    def deepcopy(self):
        copied = DiamAVP(self.avp_code, self.data, self.vendor_id)
        copied.setFlagsBits(self.flags)
        return copied
    
    ''' GETTERS & SETTERS '''
        
    def setAVPCode(self, val):
        self.avp_code = val
        
    def setVendorFlag(self, val):
        self.is_vendor = val
        
        self.flags = 0x00
        self.flags += 0x80 if self.is_vendor else 0x00
        self.flags += 0x40 if self.is_mandatory else 0x00
        self.flags += 0x20 if self.is_protected else 0x00
        
    def setMandatoryFlag(self, val):
        self.is_mandatory = val
        
        self.flags = 0x00
        self.flags += 0x80 if self.is_vendor else 0x00
        self.flags += 0x40 if self.is_mandatory else 0x00
        self.flags += 0x20 if self.is_protected else 0x00
        
    def setProtectedFlag(self, val):
        self.is_protected = val
        
        self.flags = 0x00
        self.flags += 0x80 if self.is_vendor else 0x00
        self.flags += 0x40 if self.is_mandatory else 0x00
        self.flags += 0x20 if self.is_protected else 0x00
        
    def setFlags(self, flags):
        self.is_vendor = 'V' in flags
        self.is_mandatory = 'M' in flags
        self.is_protected = 'P' in flags
        
        self.flags = 0x00
        self.flags += 0x80 if self.is_vendor else 0x00
        self.flags += 0x40 if self.is_mandatory else 0x00
        self.flags += 0x20 if self.is_protected else 0x00
    
    def setFlagsBits(self, flags):
        self.flags = flags
        self.is_vendor = True if (flags & 0x80) else False
        self.is_mandatory = True if (flags & 0x40) else False
        self.is_protected = True if (flags & 0x20) else False
    
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
        self.avp_length = self.__calculateLength()
        return self.avp_length
    
    def getPaddingLength(self):
        padLen = 4 - (len(self.data) % 4)
        if padLen != 4:
            return padLen
        return 0
    
    def getData(self):
        return self.data
    
    def getVendorID(self):
        return self.vendor_id
    
    def getAvp(self):
        return self.generateAVPMessage()
    
    def getPackedData(self):
        bData = self.__getPackedData()
        bPadding = self.__getPadding(len(self.data))
        
        if bPadding is None:
            return bData
        return bData + bPadding
    
    def getPackedHeader(self):
        bCode = struct.pack("!L", self.avp_code)
        bFlags = self.__getPackedFlags()
        bLength = self.__getPackedLength()
        
        out = bCode + bFlags + bLength
        
        if self.vendor_id != 0:
            bVendorID = struct.pack("!L", self.vendor_id)
            out += bVendorID
        
        return out
    
    ''' FUNCTIONS '''
        
    def generateAVPMessage(self):
        bCode = struct.pack("!L", self.avp_code)
        bFlags = self.__getPackedFlags()
        bLength = self.__getPackedLength()
        bData = self.__getPackedData()
        bPadding = self.__getPadding(len(self.data))
        out = ''
        if self.vendor_id != 0:
            bVendorID = struct.pack("!L", self.vendor_id)
            out = bCode + bFlags + bLength + bVendorID + bData
        else:
            out = bCode + bFlags + bLength + bData
        
        if bPadding is not None:
            out += bPadding
        
        return out
    
    @staticmethod
    def decodeSize(unpacker, bytes):
        start = unpacker.get_position()
        if bytes<8:
            return 0
        unpacker.set_position(start+4)
        flags_and_length = unpacker.unpack_uint()
        unpacker.set_position(start)
        flags_ = (flags_and_length>>24)
        length = (flags_and_length&0x00FFFFFF)
        padded_length = ((length+3)&~3)
        if (flags_&DiamAVP.avp_flag_vendor)!=0:
            if length<12:
                return 0  #garbage
        else:
            if length<8:
                return 0  #garbage
        return padded_length
    
    def decode(self, unpacker, bytes):
        if bytes<8:
            return False
        i = 0
        self.avp_code = unpacker.unpack_uint()
        i += 4
        flags_and_length = unpacker.unpack_uint()
        i += 4
        self.flags = (flags_and_length>>24)
        length = flags_and_length&0x00FFFFFF
        padded_length = ((length+3)&~3)
        if bytes!=padded_length:
            return False
        length -= 8
        if (self.flags&DiamAVP.avp_flag_vendor)!=0:
            if length<4:
                return False
            self.vendor_id = unpacker.unpack_uint()
            i += 4
            length -= 4
        else:
            self.vendor_id = 0
        self.data = unpacker.unpack_fopaque(length)
        
        return True
    
    def encodeSize(self):
        sz = 4 + 4
        if self.vendor_id!=0:
            sz += 4
        sz += (len(self.data)+3)&~3
        return sz;
    
    def encode(self,packer):
        sz = 4 + 4
        if self.vendor_id!=0:
            sz += 4
        sz += len(self.data)
        
        f = self.flags
        if self.vendor_id!=0:
            f |= DiamAVP.avp_flag_vendor
        else:
            f &= ~DiamAVP.avp_flag_vendor
        
        i=0
        packer.pack_uint(self.avp_code)
        i += 4
        packer.pack_uint(sz | (f<<24))
        i += 4
        if self.vendor_id!=0:
            packer.pack_uint(self.vendor_id)
            i += 4
        padded_len = (len(self.data)+3)&~3
        packer.pack_fopaque(padded_len,self.data)
        i += padded_len
        
        return i
    
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
        return self.str_prefix__() + "\t0x" + binascii.b2a_hex(self.data)

    
    
    ''' SUPPORTS '''
        
    def __getPackedFlags(self):
        return struct.pack("!B", self.flags)
    
    def __getPackedLength(self):
        bit_len = "{0:08b}".format(self.__calculateLength())
        return struct.pack('!I', int(bit_len,2))[-3:]
    
    def __getPackedData(self):
        l=len(self.data)
        try :
            return struct.pack(('!%ds'%l), str(self.data))
        except Exception:
            logErr(self.data)
            print(type(self.data))
            return self.data
    
    def __getPadding(self, dataLen):
        padLen = 4 - (dataLen % 4)
        if padLen != 4:
            return struct.pack(('!%ds'%padLen), '')
        return None
    
    def __calculateLength(self):
        # calculate the number of octets in the message
        l = 4 + 1 + 3
        l += 4 if self.is_vendor else 0
        l += len(self.data)
        
        return l
    
    