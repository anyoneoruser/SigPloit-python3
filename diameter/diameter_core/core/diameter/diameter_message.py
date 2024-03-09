#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import struct

'''
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Version     |                                             |
|0 0 0 0 0 0 0 1|              Message Length                 |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Flags     |                                             |
|R P E T x x x x|              Command-Code                   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Application-ID                         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Hop-by-hop Identifier                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      End-to-End Identifier                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   AVPs ...
+-+-+-+-+-+-+-+-+-+-+-+-+-
'''


##
## @brief      Support class that defines a RFC-based Diameter header (RFC 3588)
##
class DiamHDR(object):
    def __init__(self, cmd_code, app_id):
        self.version = 0x01                 # (8bit/1byte)
        self.message_length = -1            # (24bit/3byte) header 
        self.is_request = False             # (1bit)
        self.is_proxiable = False           # (1bit) 
        self.is_error = False               # (1bit)
        self.is_retrasmitted = False        # (1bit)
        self.cmd_code = cmd_code            # (24bit/3byte) from DiamCommandCodes
        self.app_id = app_id                # (32bit/4byte) some from DiamApplicationIDs (authentication application, an accounting application, or a vendor-specific application)
        self.hophop_id = 0x34d1cff8         # (32bit/4byte) unsigned 32-bit integer field (in network byte order)
        self.endend_id = 0x0011779f         # (32bit/4byte) unsigned 32-bit integer field (in network byte order)
        
    ''' GETTERS & SETTERS '''
    
    def setRequestFlag(self, val):
        self.is_request = val
        
    def setProxiableFlag(self, val):
        self.is_proxiable = val
        
    def setErrorFlag(self, val):
        self.is_error = val
        
    def setRetrasmissionFlag(self, val):
        self.is_retrasmitted = val
        
    def setCommandCode(self, val):
        self.cmd_code = val
        
    def setApplicationID(self, val):
        self.app_id = val
        
    def setHopHopID(self, val):
        self.hophop_id = val
    
    def setEndEndID(self, val):
        self.endend_id = val
        
    def isRequest(self):
        return self.is_request
        
    def isProxiable(self):
        return self.is_proxiable
        
    def isError(self):
        return self.is_error
        
    def isRetrasmission(self):
        return self.is_retrasmitted
    
    def getCommandCode(self):
        return self.cmd_code
    
    def getApplicationID(self):
        return self.app_id
    
    def getHopHopID(self):
        return self.hophop_id
    
    def getEndEndID(self):
        return self.endend_id
    
    def getVersion(self):
        return self.version        

    def getLength(self):
        return 20
    
    def getPackedVersion(self):
        return struct.pack("!B", self.version)
    
    def getPackedMessageLength(self):
        hex_len = "{0:08b}".format(self.getMessageLength())
        return struct.pack('>I', int(hex_len,2))[-3:]
    
    def getPackedFlags(self):
        hex_flags = 0x00
        hex_flags += 0x80 if self.is_request else 0x00
        hex_flags += 0x40 if self.is_proxiable else 0x00
        hex_flags += 0x20 if self.is_error else 0x00
        hex_flags += 0x10 if self.is_retrasmitted else 0x00
        
        return struct.pack("!B", hex_flags)
    
    def getPackedCommandCode(self):
        hex_cmd_code = "{0:08b}".format(self.cmd_code)
        return struct.pack('!I', int(hex_cmd_code,2))[-3:] 
    
    def getAppHopEnd(self):
        return struct.pack("!LLL", self.app_id, self.hophop_id, self.endend_id)
    
    def __copy__(self):
        return self
    
    def __deepcopy__(self):
        copied = DiamHDR(self.getCommandCode(), self.getApplicationID())
        copied.setEndEndID(self.endend_id)
        copied.setHopHopID(self.hophop_id)
        copied.setRequestFlag(self.is_request)
        copied.setProxiableFlag(self.is_proxiable)
        copied.setErrorFlag(self.is_error)
        copied.setRetrasmissionFlag(self.is_retrasmitted)
        return copied

##
## @brief      Class that defines a RFC-based Diameter message (RFC 3588)
##
class DiamMessage(object):

    def __init__(self, cmd_code, app_id):
        self.hdr = DiamHDR(cmd_code, app_id)
        self.avps = []
    
    def deepcopy(self):
        copied = DiamMessage(self.getCommandCode(), self.getApplicationID())
        copied.setEndEndID(self.getEndEndID())
        copied.setHopHopID(self.getHopHopID())
        copied.setRequestFlag(self.isRequest())
        copied.setProxiableFlag(self.isProxiable())
        copied.setErrorFlag(self.isError())
        copied.setRetrasmissionFlag(self.isRetrasmission())
        for avp in self.avps:
            copied.addAVP(avp)
        return copied   
    ''' GETTERS & SETTERS '''
    
    def setRequestFlag(self, val):
        self.hdr.setRequestFlag(val)
        
    def setProxiableFlag(self, val):
        self.hdr.setProxiableFlag(val)
        
    def setErrorFlag(self, val):
        self.hdr.setErrorFlag(val)
        
    def setRetrasmissionFlag(self, val):
        self.hdr.setRetrasmissionFlag(val)
        
    def setCommandCode(self, val):
        self.hdr.setCommandCode(val)
        
    def setApplicationID(self, val):
        self.hdr.setApplicationID(val)
        
    def setHopHopID(self, val):
        self.hdr.setHopHopID(val)
    
    def setEndEndID(self, val):
        self.hdr.setEndEndID(val)
        
    def isRequest(self):
        return self.hdr.isRequest()
        
    def isProxiable(self):
        return self.hdr.isProxiable()
        
    def isError(self):
        return self.hdr.isError()
        
    def isRetrasmission(self):
        return self.hdr.isRetrasmission()
    
    def getCommandCode(self):
        return self.hdr.getCommandCode()
    
    def getApplicationID(self):
        return self.hdr.getApplicationID()
    
    def getHopHopID(self):
        return self.hdr.getHopHopID()
    
    def getEndEndID(self):
        return self.hdr.getEndEndID()
    
    def getMessageLength(self):
        return self.__calculateLength()
    
    def getVersion(self):
        return self.hdr.getVersion()
    

    
    ''' FUNCTIONS '''
    
    ##
    ## @brief      Gets all the message's AVPs.
    ##
    ## @param      self  refers to the class itself
    ##
    ## @return     a list of AVPs.
    ##
    def getAVPs(self):
        return self.avps
    
    ##
    ## @brief      Gets the first AVP in the message with the specified command code
    ##
    ## @param      self      refers to the class itself
    ## @param      cmd_code  The command code of the AVP
    ##
    ## @return     the requested AVP if present, None otherwise.
    ##
    def getAVPbyCode(self, cmd_code):
        for a in self.avps:
            if a.getAVPCode() == cmd_code:
                return a
        
        return None
    
    ##
    ## @brief      Removes the first AVP in the message with the specified command code
    ##
    ## @param      self      refers to the class itself
    ## @param      cmd_code  The command code of the AVP
    ##
    ## @return     the removed AVP if present, None otherwise
    ##
    def removeAVPbyCode(self, cmd_code):
        for a in self.avps:
            if a.getAVPCode() == cmd_code:
                self.avps.remove(a)
                return a
        
        return None
    

    ##
    ## @brief      Replaces the first AVP in the message with the specified command code
    ##
    ## @param      self     refers to the class itself
    ## @param      new_avp  The newest AVP to replace with
    ##
    ## @return     the old APV if present, None otherwise
    ##
    def replaceAVP(self, new_avp):
        for n, a in enumerate(self.avps):
            if a.getAVPCode() == new_avp.getAVPCode():
                self.avps[n] = new_avp
                return a
    
    ##
    ## @brief      Adds an AVP to the message.
    ##
    ## @param      self  refers to the class itself
    ## @param      avp   The AVP to be added
    ##
    def addAVP(self, avp):
        self.avps.append(avp)
    
    def generateMessage(self) :
        pass
    ##
    ## @brief      Generates the byte-encoded string representing the message
    ##
    ## @param      self  refers to the class itself
    ##
    ## @return     the byte-encoded message string
    ##
    def generateByteMessage(self):
        bAVPs = ''
        #self.avps = []
        #print "\nbAVPs type:", type(bAVPs)
        self.generateMessage()
        bVer = self.hdr.getPackedVersion()
        bLen = self.__getPackedMessageLength()
        bFlags = self.hdr.getPackedFlags()
        bCmdCode = self.hdr.getPackedCommandCode()
        bAppHopEnd = self.hdr.getAppHopEnd()
                
        for avp in self.avps:
            b = avp.generateAVPMessage()
            bAVPs += b
            
        out = bVer + bLen + bFlags + bCmdCode + bAppHopEnd + bAVPs
        
        return out
    
    ##
    ## @brief      Generates the printable version of the byte-encoded message
    ##
    ## @param      self  refers to the class itself
    ##
    ## @return     a printable version of the byte-encoded message
    ##
    def generateStringfiedMessage(self):
        byte_msg = self.generateByteMessage()
        return "".join("{:02x}".format(ord(c)) for c in byte_msg)
    
    ##
    ## @brief      Gets a string prefix suitable for building a __str__ result
    ##
    ## @param      self  refers to the class itself
    ##
    ## @return     the command code of the message with the following suffix if applicable:
    ##              ".r": if is a request message (R Flag)
    ##              ".p": if is a proxiable message (P Flag)
    ##              ".e": if is an error message (E Flag)
    ##              ".t": if is a retrasmission message (T Flag)
    ##
    def str_prefix__(self):
        
        s = str(self.getCommandCode())
        if self.isRequest():
            s+= ".r"
        if self.isProxiable():
            s+= ".p"
        if self.isError():
            s+= ".e"
        if self.isRetrasmission():
            s+= ".t"
        return s
    
    ##
    ## @brief      Returns a string representation of the message
    ##
    ## @param      self  refers to the class itself
    ##
    ## @return     string representation of the message
    ##
    def __str__(self):
        return self.str_prefix__()
    
    ''' SUPPORTS '''
    
    ##
    ## @brief      Gets the message length in the correct form to be stored in the message header
    ##
    ## @param      self  refers to the class itself
    ##
    ## @return     The packed message length.
    ##
    def __getPackedMessageLength(self):
        hex_len = "{0:08b}".format(self.__calculateLength())
        return struct.pack('>I', int(hex_len,2))[-3:]

    ##
    ## @brief      Calculates the length of the whole message (header + AVPs)
    ##
    ## @param      self  refers to the class itself
    ##
    ## @return     the number of octects of the message
    ##
    def __calculateLength(self):
        # is the number of OCTETS in the message header + payload (AVP length + Padding length)
        l = self.hdr.getLength()
               
        for avp in self.avps:
            l += avp.getAVPLength()
            l += avp.getPaddingLength()
        
        return l
