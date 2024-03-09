import threading
from sctp import sctpsocket_tcp
import socket
import struct
from .commons import byteToHex, logErr, logOk, logWarn, logNormal
from core.diameter.diamAVPCodes import DiamAVPCodes
from core.diameter.diamCommandCodes import DiamCommandCodes
import time
from .sender_listener import SenderListener
import errno
from .watchdog_listener import WatchdogListener
from _socket import timeout
import signal

##
## @brief      Class that execute all the actions for the server mode
## 
## @author: Ilario Dal Grande 
##
class ServerListener(threading.Thread):
    def __init__(self, server_address, messages, cea, dwa, accepted_ips=None,
                 isSCTP = True, isVerbose = False, msgs_freq=1, wait_time=20):
        threading.Thread.__init__(self)
        
        self.TAG_NAME = 'SERVER_LISTENER'
        
        if isSCTP:
            self.sock = sctpsocket_tcp(socket.AF_INET)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.sock.bind(server_address)
        self.sock.listen(1)
        
        self.server_address = server_address
        
        self.is_verbose = isVerbose
        self.messages = messages
        self.cea = cea
        self.dwa = dwa
        self.accepted_ips = accepted_ips
        if self.accepted_ips is not None and not isinstance(self.accepted_ips, list):
            self.accepted_ips = [self.accepted_ips]
        
        self.msgs_freq = msgs_freq
        self.wait_time = wait_time
        
        self.lsntWatch = None
        self.lsntSender = None
        
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
        
        if self.is_verbose: 
            logNormal("listening for a connection on %s:%s" % self.server_address, self.TAG_NAME)
            
        opened_conn = None
        while self.is_running and not self.cer_cea_complete:
            try: 
                if opened_conn is  None :
                    if self.is_verbose: 
                        logNormal("waiting for a connection", self.TAG_NAME)
                        
                    opened_conn, client_address = self.sock.accept()
                
                    if self.accepted_ips is not None and self.accepted_ips!=[] and \
                            client_address[0] not in self.accepted_ips:
                        logWarn("Ignoring client address (%s:%s)" % (self.TAG_NAME, client_address), self.TAG_NAME)
                        opened_conn = None
                        continue
            
                start_time = time.time()
                
                opened_conn.settimeout(5)
                
                if self.is_verbose: 
                    logOk("connection from %s:%s" % (client_address), self.TAG_NAME)
                
                data = opened_conn.recv(4096)
                if data or data != "":
                    if self.is_verbose: 
                        logNormal("consistent data received, unpacking & analyzing data...", self.TAG_NAME, False)
                        
                    (b1, b2, app_id, hophop, endend) = struct.unpack("!LLLLL", data[:20])
                    length = b1 & 0x00ffffff
                    version = int(b1>>24) 
                    cmd_code = int(b2 & 0x00ffffff)
                    flags = int(b2 >> 24)
                    
                    ''' get all AVPS '''
                    start_byte = 20
                    total_bytes = length-start_byte
                    avps = []
                    while start_byte < total_bytes:
                        (avp_code, avp_flags, avp_len, vendor_id, pad_len) = self.__getRawAVPData(data[start_byte:start_byte+12])
                        avp = {
                               'code': avp_code,
                               'flags': avp_flags,
                               'length': avp_len,
                               'vendor_id': vendor_id,
                               'pad_len': pad_len
                              }
                
                        avp['raw_data'] = data[start_byte:start_byte+avp_len+pad_len]
                        if vendor_id is not None:
                            avp['raw_data'] = data[start_byte:start_byte+avp_len+pad_len]
                
                        avps.append(avp)

                        start_byte += avp_len + pad_len
                    
                    vid = None
                    for a in avps:
                        if a['code'] == DiamAVPCodes.VENDOR_ID:
                            vid = self.__extractVendorID(a)
                    
                    if self.is_verbose: 
                        logOk("DONE!")

                        logNormal("  DIAMETER version: %s" % (version), self.TAG_NAME)
                        logNormal("  packet length: %s" % (length), self.TAG_NAME)
                        logNormal("  packet flags: %s" % (bin(flags)), self.TAG_NAME)
                        logNormal("  packet command code: %s" % (cmd_code), self.TAG_NAME)
                        logNormal("  packet application id: %s" % (app_id), self.TAG_NAME)
                        logNormal("  packet hop-by-hop id: %s" % (hex(hophop)), self.TAG_NAME)
                        logNormal("  packet end-by-end id: %s" % (hex(endend)), self.TAG_NAME)
                        if vid is not None: 
                            logNormal("  packet-avp vendor_id: %s" % (vid), self.TAG_NAME)
                        
                    if cmd_code == DiamCommandCodes.CAPABILITIES_EXCHANGE and (flags & 0x80)==0x80:
                        if self.is_verbose:
                            logNormal("valid DIAMETER CER message...prepare and send ", self.TAG_NAME, False)
                            logOk("CEA")
                            
                            logNormal("constructing CEA message...", self.TAG_NAME, False)
                        if self.cea is not None:
                            self.cea.setApplicationID(app_id)
                            self.cea.setHopHopID(hophop)
                            self.cea.setEndEndID(endend)
                            
                            if self.is_verbose: 
                                logOk("DONE!")
                                
                                logNormal("sending CEA message...", self.TAG_NAME, False)
                            sent_bytes = opened_conn.send(self.cea.generateByteMessage())
                            if sent_bytes is not None and sent_bytes>0:
                                if self.is_verbose:
                                    logOk("DONE!", None, False)
                                    logNormal(" (byte sent %d)" % (sent_bytes))
                                self.cer_cea_complete = True
                            else:
                                if self.is_verbose: 
                                    logErr("NO!")
                        else:
                            if self.is_verbose: 
                                logErr("ERROR! Unset CEA message")
                            break
            
            except timeout as e:
                logWarn("TIMEOUT_ERROR (%s): %s" % (self.TAG_NAM, e), None, False)
                logNormal(e)
                pass
            except Exception as e:
                if e.errno == errno.ECONNREFUSED:
                    logErr("CONNECTION_REFUSED (%s): %s" % (self.TAG_NAM, e), None, False)
                if e.errno == errno.EBADFD:
                    logErr("BAD_FILE_DESCRIPTOR_ERROR (%s): %s" % (self.TAG_NAM, e), None, False)
                elif e.errno == errno.EPIPE:
                    logErr("BROKEN_PIPE_ERROR (%s): %s" % (self.TAG_NAM, e), None, False)
                elif e.errno == errno.ECONNRESET:
                    logErr("CONNECTION_RESET_ERROR (%s): %s" % (self.TAG_NAM, e), None, False)
                else:
                    logErr("UNKNOWN_ERROR (%s): %s" % (self.TAG_NAM, e), None, False)
                    pass
                
                break
            
        
        if self.cer_cea_complete:
            ''' START WATCHDOG LISTENER '''
            self.lsntWatch = WatchdogListener(opened_conn, self.dwa, self.is_verbose)
            self.lsntWatch.daemon = True
            self.lsntWatch.start()
            
            ''' START SENDER CLIENT '''
            self.lsntSender= SenderListener(opened_conn, self.messages, start_time, self.is_verbose,  
                                            self.msgs_freq, self.wait_time)            
            self.lsntSender.daemon = True
            self.lsntSender.start()
            self.lsntSender.join()
            time.sleep(15)
            
            
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
        
    ##
    ## @brief      Extracts the raw data of the AVP.
    ##
    ## @param      self   refers to the class itself
    ## @param      hdata  the header bytes
    ##
    ## @return     a tuple with (apv_code, flags, length, vendor_id, padding_length)
    ##
    def __getRawAVPData(self, hdata):
        (avp_code, b2) = struct.unpack("!LL", hdata[:8])
        length = b2 & 0x00ffffff
        flags = int(b2 >> 24)
        
        pad_len = 4 - (length % 4)
        if pad_len == 4:
            pad_len = 0
        
        vendor_id = None
        if (flags == 0x80):
            vendor_id = struct.unpack("!L", hdata[8:])[0]
        
        return (avp_code, flags, length, vendor_id, pad_len)

    ##
    ## @brief      Retrieve the Vendor-ID from the AVP
    ##
    ## @param      self  refers to the class itself
    ## @param      avp   the AVP
    ##
    ## @return     an int representing the Vendor-ID
    ##
    def __extractVendorID(self, avp):
        payload_start = 8
        if avp['vendor_id'] is not None:
            payload_start += 4
        payload_start += avp['pad_len']
        
        hdata = avp['raw_data'][payload_start:]
        
        return int(byteToHex(hdata), 16)
