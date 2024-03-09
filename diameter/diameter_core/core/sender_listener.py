import threading
import socket
import time
from .commons import logNormal, logOk, logErr, logWarn
from _socket import timeout
import errno
import signal

##
## @brief      Class that actually sends all the Diameter messages
## 
## @author: Ilario Dal Grande 
##
class SenderListener(threading.Thread):
    def __init__(self, connection, messages, start_time=None, isVerbose = False, 
                 msg_freq=1, wait_time=20):
        threading.Thread.__init__(self)
        
        self.TAG_NAME = 'SENDER_LISTENER'
        
        if messages is None or len(messages) == 0 :
            raise Exception("%s :: no messages" % (self.TAG_NAME))             
        
        if connection is None :
            raise Exception("%s :: no connection available" % (self.TAG_NAME))
        
        self.connection = connection
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.is_verbose = isVerbose
        
        if not isinstance(messages, list):
            self.messages = [messages]
        else:
            self.messages = messages

        self.start_time = start_time
        self.msg_freq = msg_freq
        self.wait_time = wait_time
        
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
            print("\n--: Acting as SENDER :--")
            
            logNormal("Waiting %d seconds to correctly establish the connection..." % (self.wait_time), self.TAG_NAME, False)
        time.sleep(self.wait_time)
        if self.is_verbose: 
            logOk("DONE!")
            
            logNormal("keep working on the opened connection", self.TAG_NAME)
                
        if self.is_running and self.connection is not None:
            ''' Prepare the messages to send '''
            if self.is_verbose: 
                logNormal("preparing NORMAL messages...", self.TAG_NAME, False)
            mdatas = []
            if self.messages is not None and len(self.messages) > 0:
                for m in self.messages:
                    mdatas.append(m.generateByteMessage())
            if self.is_verbose: 
                logOk("DONE!")
                
            try:
                ''' SENDS MESSAGES '''
                if mdatas != []:
                    curr_count = 1
                    tot_count = len(mdatas)
                    for data in mdatas:
                        if self.is_verbose:
                            logNormal("sending message (#%d of %d)..." % (curr_count, tot_count), self.TAG_NAME, False)
                        sent_bytes = self.connection.send(data)
                        if sent_bytes is not None and sent_bytes>0:
                            if self.is_verbose: 
                                logOk("DONE!", None, False)
                                logNormal(" (byte sent %d)" % (sent_bytes))
                        else:
                            if self.is_verbose: 
                                logErr("NO!")
                        curr_count += 1
                        
                        time.sleep(self.msg_freq)
                else:
                    if self.is_verbose: 
                        logWarn("\nNo MESSAGE to send\n")
                  
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
                
                if self.start_time is not None:
                    stop_time = time.time()
                    hours, rem = divmod(stop_time - self.start_time, 3600)
                    minutes, seconds = divmod(rem, 60)
                    print('\n')
                    logNormal("Elapsed time: {:0>2}:{:0>2}:{:05.4f}".format(int(hours),int(minutes),seconds), self.TAG_NAME)
                
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
