import threading
import socket
from .commons import logNormal, logErr, logOk, logWarn
import errno
from core.diameter.diamCommandCodes import DiamCommandCodes
import struct
from _socket import timeout


##
## @brief      Class that listen and respond to all Diameter's Watchdog messages
## 
## @author: Ilario Dal Grande 
##
class WatchdogListener(threading.Thread):
    def __init__(self, connection, dwa, isVerbose=False):
        threading.Thread.__init__(self)
        
        self.TAG_NAME = 'WATCHDOG_LISTENER'
        
        self.connection = connection
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.is_verbose = isVerbose
        self.dwa = dwa
                  
    ##
    ## @brief      Determines if the thread is running
    ##
    ## @param      self  refers to the class itself
    ##
    ## @return     True if running, False otherwise.
    ##    
    def isRunning(self):
        return self.is_running

    ##
    ## @brief      Starts the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def run(self):
        self.is_running = True
        
        if self.is_verbose: 
            print("\n\n--: WATCHDOG MANAGER :--")
            
            logNormal("keep working on the opened connection")
        
        while self.connection is not None and self.is_running:
            try:
                data = self.connection.recv(4096)
            
                if data or data != "":
                    if self.is_verbose: 
                        logNormal("consistent data received, unpacking & analyzing data...", self.TAG_NAME, False)
                        
                    (b1, b2, app_id, hophop, endend) = struct.unpack("!LLLLL", data[:20])
                    length = b1 & 0x00ffffff
                    version = int(b1>>24) 
                    cmd_code = int(b2 & 0x00ffffff)
                    flags = int(b2 >> 24)
                    
                    if self.is_verbose: 
                        logOk("DONE!\n")

                        logNormal("  DIAMETER version: %s" % (version), self.TAG_NAME)
                        logNormal("  packet length: %s" % (length), self.TAG_NAME)
                        logNormal("  packet flags: %s" % (bin(flags)), self.TAG_NAME)
                        logNormal("  packet command code: %s" % (cmd_code), self.TAG_NAME)
                        logNormal("  packet application id: %s" % (app_id), self.TAG_NAME)
                        logNormal("  packet hop-by-hop id: %s" % (hex(hophop)), self.TAG_NAME)
                        logNormal("  packet end-by-end id: %s" % (hex(endend)), self.TAG_NAME)
                    
                    if cmd_code == DiamCommandCodes.DEVICE_WATCHDOG:
                        if self.is_verbose:
                            logNormal("valid DIAMETER WHATCHDOG message...prepare and send", self.TAG_NAME, False)
                            logOk("DWA")
                        
                        if self.is_verbose: 
                            logNormal("constructing DWA message...", self.TAG_NAME, False)
                        if self.dwa is not None:
                            self.dwa.setApplicationID(app_id)
                            self.dwa.setHopHopID(hophop)
                            self.dwa.setEndEndID(endend)
                            if self.is_verbose: 
                                logOk("DONE!")
                        
                                logNormal("sending DWA message...", self.TAG_NAME, False)
                            sent_bytes = self.connection.send(self.dwa.generateByteMessage())
                            if sent_bytes is not None and sent_bytes>0:
                                if self.is_verbose:
                                    logOk("DONE!", False) 
                                    logNormal(" (byte sent %d)" % (sent_bytes))
                            else:
                                if self.is_verbose: 
                                    logErr("NO!")
                        else:
                            if self.is_verbose: 
                                logErr("ERROR! Unset DWA message")
            
            except timeout as e:
                logWarn("TIMEOUT_ERROR (%s): %s" % (self.TAG_NAME, e), None, False)
                logNormal(e)
                pass
            except Exception as e:
                if e.errno == errno.ECONNREFUSED:
                    logErr("CONNECTION_REFUSED (%s): %s" % (self.TAG_NAME, e), None, False)
                if e.errno == errno.EBADFD:
                    logErr("BAD_FILE_DESCRIPTOR_ERROR (%s): %s" % (self.TAG_NAME, e), None, False)
                elif e.errno == errno.EPIPE:
                    logErr("BROKEN_PIPE_ERROR (%s): %s" % (self.TAG_NAME, e), None, False)
                elif e.errno == errno.ECONNRESET:
                    logErr("CONNECTION_RESET_ERROR (%s): %s" % (self.TAG_NAME, e), None, False)
                else:
                    logErr("UNKNOWN_ERROR (%s): %s" % (self.TAG_NAME, e), None, False)
                    pass
                
                break
    
    ##
    ## @brief      Stops the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def stop(self):
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.is_verbose: 
            logOk("stopped", self.TAG_NAME)
