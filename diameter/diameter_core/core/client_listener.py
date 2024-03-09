import threading
from sctp import sctpsocket_tcp
import socket
from .commons import logNormal, logErr, logOk
import errno
import time
from core.diameter.diamCommandCodes import DiamCommandCodes
import struct
from .sender_listener import SenderListener
from _socket import timeout
from .watchdog_listener import WatchdogListener
import signal

##
## @brief      Class that execute all the actions for the client mode
## 
## @author: Ilario Dal Grande
##
class ClientListener(threading.Thread):
    def __init__(self, server_address, messages, cer, dwa, isSCTP = True, 
                 isVerbose = False, msgs_freq=1, wait_time=20):
        threading.Thread.__init__(self)

        self.TAG_NAME = 'CLIENT_LISTENER'
        
        if isSCTP:
            self.sock = sctpsocket_tcp(socket.AF_INET)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.server_address = server_address
        
        self.is_verbose = isVerbose
        
        self.messages = messages       
        self.cer = cer
        self.dwa = dwa
        self.msgs_freq = msgs_freq
        self.wait_time = wait_time
        
        self.lsntWatch = None
        self.lsntSender= None
        
        signal.signal(signal.SIGQUIT, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)
        
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
        self.cer_cea_complete = False
        self.is_running = True
        
        if self.is_verbose: logNormal('connecting to %s:%s' % self.server_address, self.TAG_NAME)
        try:
            self.sock.connect(self.server_address)
        
            start_time = time.time()
            
            if self.cer is None or self.cer.getCommandCode() != DiamCommandCodes.CAPABILITIES_EXCHANGE:
                logErr("ERROR!", None, False)
                logNormal("First message MUST be of type CapabilitiesExchangeRequest (257)")
                self.stop()
                return
            
            if self.is_verbose: 
                logNormal("sending CER...", self.TAG_NAME, False)
            
            sent_bytes = self.sock.send(self.cer.generateByteMessage())
            if sent_bytes is not None and sent_bytes>0:
                if self.is_verbose: 
                    logOk("DONE!", None, False)
                    logNormal(" (byte sent %d)"%(sent_bytes), None)
            else:
                if self.is_verbose: logErr("NO!")
                            
            if self.is_verbose: 
                logNormal("waiting for answer message from %s:%d" % self.server_address, self.TAG_NAME, False)
            error_count = 5
            
            while not self.cer_cea_complete and error_count>0:
                answ_data = self.sock.recv(4096)
                
                if answ_data or answ_data != "":
                    try:
                        if self.is_verbose: 
                            logOk("OK!")
                            logNormal("consistent data received, unpacking & analyzing data...", self.TAG_NAME, False)
                        (_, b2) = struct.unpack("!LL", answ_data[:8])
                        cmd_code = int(b2 & 0x00ffffff)
                        flags = int(b2 >> 24)
                        
                        if self.is_verbose:
                            logOk("DONE!")
                            
                            logNormal("  packet flags: %s" % (bin(flags)), self.TAG_NAME)
                            logNormal("  packet command code: %s" % (cmd_code), self.TAG_NAME)
                        
                            logNormal("checking if is CEA message...", self.TAG_NAME, False)
                        if cmd_code==DiamCommandCodes.CAPABILITIES_EXCHANGE:
                            if (flags & 0x80)!=0x80:
                                self.cer_cea_complete = True
                                if self.is_verbose:
                                    logOk('OK!')                            
                            else:
                                if self.is_verbose:
                                    logErr("ERROR during Capabilities Exchange! Received a CER instead of a CEA!", self.TAG_NAME)
                                    continue
                        else: 
                            error_count -= 1    
                        
                    except Exception as e:
                        logErr("Exception: ", self.TAG_NAME, False)
                        logNormal(e)
                        error_count -= 1
                        pass
        
        except timeout as e:
            logErr("TIMEOUT_ERROR: %s" % (e), None, False)
            logNormal(e)
            pass
        except Exception as e:
            if e.errno == errno.ECONNREFUSED:
                logErr("CONNECTION_REFUSED: %s" % (e), None, False)
            if e.errno == errno.EBADFD:
                logErr("BAD_FILE_DESCRIPTOR_ERROR: %s" % (e), None, False)
            elif e.errno == errno.EPIPE:
                logErr("BROKEN_PIPE_ERROR: %s" % (e), None, False)
            elif e.errno == errno.ECONNRESET:
                logErr("CONNECTION_RESET_ERROR: %s" % (e), None, False)
            else:
                logErr("UNKNOWN_ERROR: %s" % (e), None, False)
                pass
            
        if self.cer_cea_complete:
            ''' START WATCHDOG LISTENER '''
            self.lsntWatch = WatchdogListener(self.sock, self.dwa, self.is_verbose)
            self.lsntWatch.daemon = True
            self.lsntWatch.start()
            
            ''' START MESSAGE SENDER CLIENT '''
            self.lsntSender = SenderListener(self.sock, self.messages, start_time, self.is_verbose,  
                                             self.msgs_freq, self.wait_time)
            self.lsntSender.daemon = True
            self.lsntSender.start()
            self.lsntSender.join()
            time.sleep(5)
            
        self.stop()
    
    ##
    ## @brief      Stops the execution of the thread
    ##
    ## @param      self  refers to the class itself
    ##
    def stop(self):
        if self.lsntWatch is not None:
            self.lsntWatch.stop()
        
        if self.lsntSender is not None:
            self.lsntSender.stop()
        
        self.sock.close()
        self.is_running = False
        
        if self.is_verbose:
            logOk("stopped", self.TAG_NAME)
