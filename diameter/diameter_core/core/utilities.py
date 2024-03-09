#!/usr/bin/env python

import os
from os import listdir
from os.path import isfile, join

from core.diameter.diamCommandCodes import DiamCommandCodes
from configobj import ConfigObj, ConfigObjError
from core.diameter.diamAVPExceptions import MissingMandatoryAVPException
from core.diameter.diamAVPCodes import DiamAVPCodes
from core.diameter.diamAVP import DiamAVP
from .commons import *
from plugins.common_messages_classes import DiamGenericMessage

##
## @author: Ilario Dal Grande
##

DEFAULT_MSGS = [
                DiamCommandCodes.CAPABILITIES_EXCHANGE,
                DiamCommandCodes.DEVICE_WATCHDOG,
                DiamCommandCodes.CANCEL_LOCATION_3GPP,
                DiamCommandCodes.UPDATE_LOCATION_3GPP,
                DiamCommandCodes.AUTHENTICATION_INFORMATION_3GPP,
                DiamCommandCodes.INSERT_SUBSCRIBER_DATA_3GPP,
                DiamCommandCodes.DELETE_SUBSCRIBER_DATA_3GPP,
                DiamCommandCodes.PURGE_UE_3GPP,
                DiamCommandCodes.RESET_3GPP,
                DiamCommandCodes.NOTIFY_3GPP,
                DiamCommandCodes.ME_IDENTITY_CHECK_3GPP
               ]

##
## @brief      Lists all the config files in the passed path
##
## @param      path  the path to check in
##
def configList(path):
    if not os.path.isdir(path) or not os.path.exists(path):
        printRed("No such directory '%s'"%path)
        return
        
    onlyfiles = []
    for f in listdir(path):
        if isfile(join(path, f)):
            _, file_extension = os.path.splitext(f)
            if file_extension == '.cnf':
                onlyfiles.append(f)
    
    if onlyfiles==[]:
        printYellow("NO .cnf files in directory")
        return
    
    print("List of config (.cnf) files:")
    for f in onlyfiles:
        print("  * ", f)

##
## @brief      Validates the config for the passed AVP
##
## @param      key       parent key
## @param      avp       the avp to validate
## @param      avp_type  the type of the avp
##
## @return     True if the config file is correct, the error message otherwise
##
def validateConfigAVP(key, avp, avp_type=None):
    error_msgs = []
    
    if avp_type is not None:
        if not 'type' in avp:
            error_msgs.append('"type" key is missing in %s'%(key))
        if avp_type == 'grouped':
            if avp['type'] != 'grouped':
                error_msgs.append('"type" MUST "grouped" for key %s'%(key))
            if not 'flags' in avp:
                error_msgs.append('"flags" key is missing in %s'%(key))
        elif avp_type == 'multiple':
            if avp['type'] != 'multiple':
                error_msgs.append('"type" MUST "grouped" for key %s'%(key))
    else:
        if not 'value' in avp:
            error_msgs.append('"value" key is missing in %s'%(key))
        if not 'flags' in avp:
            error_msgs.append('"flags" key is missing in %s'%(key))
    
    if error_msgs==[]:
        return True
    else:
        return error_msgs

##
## @brief      Recursively unpack all the passed AVPs
##
## @param      lst              the list of AVPs to check
## @param      parent_avp_name  the name of the parent AVP
## @param      avp_type         the type of the parent AVP
## 
## @throw      ConfigObjError if some required data is missing 
##
## @return     the unpacked AVPs if all is correct, None otherwise
##
def unpackAVPs(lst, parent_avp_name=None, avp_type=None):
    if lst is None or lst==[]:
        return None
    
    avps = []
    for key, val in lst.items():
        avp = None
        avp_name = slugfy(key)
        
        if 'type' in val:
            t = val['type']
            valid_errs = validateConfigAVP(key, val, t)
            if valid_errs != True:
                s_err = "ERRORS FOUND IN CONFIG FILE:\n"
                for s in valid_errs:
                    s_err += "  * " + s + "\n"
                raise ConfigObjError(s_err)
                
            if t == 'grouped':
                nval = val.copy()
                nval.pop('type', None)
                nval.pop('name', None)
                nval.pop('flags', None)
                nval.pop('vendor', None)
                avp = {'name': (parent_avp_name if parent_avp_name is not None else avp_name), 
                       'avps':[], 
                       'flags': val['flags']}
                if 'vendor' in val:
                    avp['vendor'] = val['vendor']
                avp['avps'] = unpackAVPs(nval, avp_name, t)
                avps.append(avp)
            elif t == 'multiple':
                nval = val.copy()
                nval.pop('type', None)
                nval.pop('name', None)
                avps.extend(unpackAVPs(nval, avp_name, t))
            elif t == 'raw':
                avp = val
                if parent_avp_name is not None and avp_type=='multiple':
                    avp['name'] = parent_avp_name
                else:
                    avp['name'] = avp_name
                    
                if avp is not None:
                    avps.append(avp)
        else:
            valid_errs = validateConfigAVP(key, val)
            if valid_errs != True:
                s_err = "ERRORS FOUND IN CONFIG FILE:\n"
                for s in valid_errs:
                    s_err += "  * " + s + "\n"
                raise ConfigObjError(s_err)
                
            avp = val
            if parent_avp_name is not None and avp_type=='multiple':
                avp['name'] = parent_avp_name
            else:
                avp['name'] = avp_name
                
            if avp is not None:
                avps.append(avp)
    
    return avps

##
## @brief      Split the command-code and reitrieve its informations
##
## @param      el    the command-code element to work on
##
## @return     a dict representing the command description:
##              {
##                'cmd_code': <apv-code>,
##                'has_request': True/False,
##                'has_answer': True/False
##              }
##
def splitCommandCode(el):
    ret_el = {
              'cmd_code': None,
              'has_request': True,
              'has_answer': True
             }
    
    v=el.split('.')
    ret_el['cmd_code'] = int(v[0])
    if len(v)>1:
        flags = v[1]
        ret_el['has_request'] = 'r' in flags
        ret_el['has_answer'] = 'a' in flags
        
    return ret_el

##
## @brief      Unpack and structure the passed messages
##
## @param      lst   the list of messages to work on
##
## @return     a list of dict representing the messages
##
def unpackMessageList(lst):
    msg_list = []
    
    for el in lst:
        msg_list.append(splitCommandCode(el))
        
    return msg_list

##
## @brief      Parsify the passed config file
##
## @param      conf_path  the path to the config file
## 
## @throw      ConfigObjError if some required data is missing
##
## @return     the configuration object based on the passed file
##
def parseConfigs(conf_path):
    confobj = ConfigObj(conf_path)
    
    configs = {'interface': None,
               'base_message_list': [],
               '3gpp_messages_list': [],
               'fuzzy_messages_list': None,
               'raw_config_file': None,
               'origin_host': None,
               'origin_realm': None,
               'destination_host': None,
               'destination_realm': None,
               'avps': []}
    
    if 'GENERIC' not in confobj.sections:
        raise ConfigObjError('Section GENERIC is required')
    
    if 'interface' not in confobj['GENERIC']:
        raise ConfigObjError('Value "GENERIC.interface" is required')
    configs['interface'] = confobj['GENERIC']['interface']
    
    if 'base_message_list' not in confobj['GENERIC']:
        raise ConfigObjError('Value "GENERIC.base_message_list" is required')
    configs['base_message_list'] = unpackMessageList(confobj['GENERIC']['base_message_list'])
    
    if '3gpp_messages_list' not in confobj['GENERIC']:
        raise ConfigObjError('Value "GENERIC.3gpp_messages_list" is required')
    configs['3gpp_messages_list'] = unpackMessageList(confobj['GENERIC']['3gpp_messages_list'])
    
    if configs['base_message_list'] is None or configs['base_message_list']=="" or configs['base_message_list'] == []:
        configs['base_message_list'] = DEFAULT_MSGS
    
    if not isinstance(configs['base_message_list'], list):
        configs['base_message_list'] = [configs['base_message_list']]
    
    if 'origin_host' not in confobj['GENERIC']:
        raise ConfigObjError('Value "GENERIC.origin_host" is required')
    configs['origin_host'] = confobj['GENERIC']['origin_host']
    
    if 'origin_realm' not in confobj['GENERIC']:
        raise ConfigObjError('Value "GENERIC.origin_realm" is required')
    configs['origin_realm'] = confobj['GENERIC']['origin_realm']
    
    if 'destination_host' in confobj['GENERIC']:
        configs['destination_host'] = confobj['GENERIC']['destination_host']
    else:
        print('Value GENERIC.destination_host is missed')
    
    if 'destination_realm' not in confobj['GENERIC']:
        raise ConfigObjError('Value "GENERIC.destination_realm" is required')
    configs['destination_realm'] = confobj['GENERIC']['destination_realm']
    
        
    if 'raw_config_file' in confobj['GENERIC']:
        configs['raw_config_file'] = confobj['GENERIC']['raw_config_file']
      
    if 'AVPS' not in confobj.sections:
        raise ConfigObjError('Section AVPS is required')
    configs['avps'] = unpackAVPs(confobj['AVPS'])
        
    return configs

##
## @brief      Check if the passed value is present in the AVP list
##
## @param      avps   the list of AVPs to check
## @param      value  the value to check
## @param      key    the key of the dictionary to check in (default 'name')
##
## @throw      MissingMandatoryAVPException if the value is not present in the AVPs
##
def checkAvpValue(avps, value, key='name'):
    if not any(d[key] == value for d in avps):
        raise MissingMandatoryAVPException(('%s AVP is MANDATORY')%(value))

##
## @brief      Get the data of the passed AVP
##
## @param      avps        the list of AVPs to get
## @param      value_name  name of the AVP to retrieve
## @param      key         the key of the dictionary to check in (default 'name')
##
## @return     the avp data
##
def getAvpData(avps, value, key='name'):    
    idx = [index for (index, d) in enumerate(avps) if d[key] == value]
    ret = []
    
    if idx==[]:
        return None
        
    for i in idx:
        ret.append(avps[i])
    
    if len(ret) == 1:
        ret = ret[0]
    
    return ret  
 
def getFuzzyAvpCodes(avps):
    ret = []    
    for (index, d) in enumerate(avps):
        if 'fuzzy' in d and int(d['fuzzy']) == 1 :
            ret.append(DiamAVPCodes.name2code(avps[index]['name']))   
    return ret 
##
## @brief      Parsify the passed config file for RAW messages
##
## @param      raw_path  the path to the raw config file
##
## @return     a list of raw messages
##
def parseRawConfigs(raw_path):
    msgs = []
    
    with open(raw_path) as f:
        for l in f:
            if not l.startswith('#'):
                el = l.replace(' ','')
                el = el.replace('\n','')
                el = el.replace('\r','')
                if el!='':
                    m = DiamGenericMessage(el)
                    msgs.append(m)
        
    return msgs

##
## @brief      Parsify the passed config file for FUZZY messages
##
## @param      conf_path  the path to the fuzzy config file
##
## @return     the configuration object for the FUZZY
##
def parseFuzzyConfigs(conf_path):
    confobj = ConfigObj(conf_path)
    
    configs = {'list': None,
               'customizations': []}
        
    if 'test_list' not in confobj:
        raise ConfigObjError('The key "test_list" is required')
    configs['list'] = confobj['test_list']
    
    if 'CUSTOMIZATIONS' in confobj.sections:
        customs = {}
        
        for kp,vp in confobj['CUSTOMIZATIONS'].items():
            for k,v in vp.items():
                if 'custom' not in v:
                    raise ConfigObjError('The key "custom" is required for each custom field [err in %s]'%k)
                if v['custom'] != "" and v['custom'] != []:
                    
                    if kp not in customs:
                        customs[kp] = {}
                        customs[kp][k] = v['custom']
                    else:
                        if k not in customs[kp]:
                            customs[kp] = {k: v['custom']}
                        else:
                            customs[kp][k].append(v['custom'])
        configs['customizations'] = customs
    
    return configs

##
## @brief      Alter the passed string replacing the special tags with the passed info
##
## @param      text                 the text to work on
## @param      destination_host_ip  the IP for the DESTINATION_HOST
## @param      origin_host_ip       the IP for the ORIGIN_HOST
##
## @return     the new text with the replaced special tags
##
def replaceSpecialTag(text, destination_host_ip, origin_host_ip):
    if '%%DESTINATION_HOST%%' in text:
        return text.replace('%%DESTINATION_HOST%%', destination_host_ip)
    elif '%%ORIGIN_HOST%%' in text:
        return text.replace('%%ORIGIN_HOST%%', origin_host_ip)
    
    return text

##
## @brief      Generates the fuzzy messages from the passed correct messages and the config structure
##
## @param      configs   the config strutcture where to retrieve custom fuzzy strings
## @param      msgs_map  the correct messages
## @param      dest_ip   the IP of the destination host
## @param      orig_ip   the IP of the origin host
##
## @return     a list of fuzzy messages
##
def generateFuzzyMessages(configs, msgs_map, dest_ip, orig_ip):
    msgs = []
    customs = configs['customizations']
        
    for f in configs['list']:
        el = splitCommandCode(f)
        cmd_code = el['cmd_code']
        isRequest = el['is_request']
        isAnswer = el['is_answer']
        
        if cmd_code == DiamCommandCodes.UPDATE_LOCATION_3GPP:
            # get or create the base message
            base_msg = None
            if DiamCommandCodes.UPDATE_LOCATION_3GPP not in msgs_map:
                printYellow("Fuzzy Messages: NO UPDATE_LOCATION CONFIG FILE PROVIDED")
                continue
            
            # list of all AVPs to test
            toTest = {
                      str(DiamAVPCodes.ORIGIN_HOST): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              str(dest_ip),
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(20),
                              generateRandomHexByte(20)
                             ],
                      str(DiamAVPCodes.ORIGIN_REALM): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(8),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.USER_NAME): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                      str(DiamAVPCodes.ULR_FLAGS): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'klasmddbdkkhksk',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(6),
                              generateRandomHexByte(6)
                             ],
                     }
            
            # add custom AVPs to test
            if (isRequest or (not isRequest and not isAnswer)) and 'ULR' in customs:
                for k, v in customs['ULR'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
            if (isAnswer or (not isRequest and not isAnswer)) and 'ULA' in customs:
                for k, v in customs['ULA'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
                
            # create all the fuzzy messages
            for k,v in toTest.items():
                # generate fuzzy AVP
                avps = generateFuzzyAVPs(k, v)
                
                for a in avps:
                    base_msg = msgs_map[DiamCommandCodes.UPDATE_LOCATION_3GPP]['msg']
                    base_msg.removeAVPbyCode(int(k))
                    base_msg.addAVP(a)
                    msgs.append(base_msg)
                
                
        elif cmd_code == DiamCommandCodes.CANCEL_LOCATION_3GPP:
            # get or create the base message
            base_msg = None
            if DiamCommandCodes.CANCEL_LOCATION_3GPP in msgs_map:
                base_msg = msgs_map[DiamCommandCodes.CANCEL_LOCATION_3GPP]['msg']
            else:
                printYellow("Fuzzy Messages: NO CANCEL_LOCATION CONFIG FILE PROVIDED")
                continue
                
            # list of all AVPs to test
            toTest = {
                      str(DiamAVPCodes.ORIGIN_HOST): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              str(dest_ip),   # special tag that refers to the IP of the server
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(20),
                              generateRandomHexByte(20)
                             ],
                      str(DiamAVPCodes.ORIGIN_REALM): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(8),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.USER_NAME): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                      str(DiamAVPCodes.CLR_FLAGS): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'klasmddbdkkhksk',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(6),
                              generateRandomHexByte(6)
                             ],
                     }
            
            # add custom AVPs to test
            if (isRequest or (not isRequest and not isAnswer)) and 'CLR' in customs:
                for k, v in customs['CLR'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
            if (isAnswer or (not isRequest and not isAnswer)) and 'CLA' in customs:
                for k, v in customs['CLA'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
                
            # create all the fuzzy messages
            for k,v in toTest.items():
                # generate fuzzy AVP
                avps = generateFuzzyAVPs(k, v)
                                
                for a in avps:
                    base_msg = msgs_map[DiamCommandCodes.CANCEL_LOCATION_3GPP]['msg']
                    base_msg.removeAVPbyCode(int(k))
                    base_msg.addAVP(a)
                    msgs.append(base_msg)
            
            
        elif cmd_code == DiamCommandCodes.AUTHENTICATION_INFORMATION_3GPP:
            # get or create the base message
            base_msg = None
            if DiamCommandCodes.AUTHENTICATION_INFORMATION_3GPP in msgs_map:
                base_msg = msgs_map[DiamCommandCodes.AUTHENTICATION_INFORMATION_3GPP]['msg']
            else:
                printYellow("Fuzzy Messages: NO AUTHENTICATION_INFORMATION CONFIG FILE PROVIDED")
                continue
                
            # list of all AVPs to test
            toTest = {
                      str(DiamAVPCodes.ORIGIN_HOST): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              str(dest_ip),   # special tag that refers to the IP of the server
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(20),
                              generateRandomHexByte(20)
                             ],
                      str(DiamAVPCodes.ORIGIN_REALM): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(8),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.USER_NAME): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                      str(DiamAVPCodes.ROUTE_RECORD): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'dwepxccjncpqkp',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                     }
            
            # add custom AVPs to test
            if (isRequest or (not isRequest and not isAnswer)) and 'AIR' in customs:
                for k, v in customs['AIR'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
            if (isAnswer or (not isRequest and not isAnswer)) and 'AIA' in customs:
                for k, v in customs['AIA'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
                
            # create all the fuzzy messages
            for k,v in toTest.items():
                # generate fuzzy AVP
                avps = generateFuzzyAVPs(k, v)
                                
                for a in avps:
                    base_msg = msgs_map[DiamCommandCodes.AUTHENTICATION_INFORMATION_3GPP]['msg']
                    base_msg.removeAVPbyCode(int(k))
                    base_msg.addAVP(a)
                    msgs.append(base_msg)
                
                
        elif cmd_code == DiamCommandCodes.INSERT_SUBSCRIBER_DATA_3GPP:
            # get or create the base message
            base_msg = None
            if DiamCommandCodes.INSERT_SUBSCRIBER_DATA_3GPP in msgs_map:
                base_msg = msgs_map[DiamCommandCodes.INSERT_SUBSCRIBER_DATA_3GPP]['msg']
            else:
                printYellow("Fuzzy Messages: NO INSERT_SUBSCRIBER_DATA CONFIG FILE PROVIDED")
                continue
                
            # list of all AVPs to test
            toTest = {
                      str(DiamAVPCodes.ORIGIN_HOST): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              str(dest_ip),   # special tag that refers to the IP of the server
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(20),
                              generateRandomHexByte(20)
                             ],
                      str(DiamAVPCodes.ORIGIN_REALM): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(8),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.USER_NAME): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                      str(DiamAVPCodes.IDR_FLAGS): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'dwepxccjncpqkp',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(4),
                              generateRandomHexByte(6)
                             ],
                     }
            
            # add custom AVPs to test
            if (isRequest or (not isRequest and not isAnswer)) and 'IDR' in customs:
                for k, v in customs['IDR'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
            if (isAnswer or (not isRequest and not isAnswer)) and 'IDA' in customs:
                for k, v in customs['IDA'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
                
            # create all the fuzzy messages
            for k,v in toTest.items():
                # generate fuzzy AVP
                avps = generateFuzzyAVPs(k, v)
                                
                for a in avps:
                    base_msg = msgs_map[DiamCommandCodes.INSERT_SUBSCRIBER_DATA_3GPP]['msg']
                    base_msg.removeAVPbyCode(int(k))
                    base_msg.addAVP(a)
                    msgs.append(base_msg)
                
                
        elif cmd_code == DiamCommandCodes.DELETE_SUBSCRIBER_DATA_3GPP:
            # get or create the base message
            base_msg = None
            if DiamCommandCodes.DELETE_SUBSCRIBER_DATA_3GPP in msgs_map:
                base_msg = msgs_map[DiamCommandCodes.DELETE_SUBSCRIBER_DATA_3GPP]['msg']
            else:
                printYellow("Fuzzy Messages: NO DELETE_SUBSCRIBER_DATA CONFIG FILE PROVIDED")
                continue
                
            # list of all AVPs to test
            toTest = {
                      str(DiamAVPCodes.ORIGIN_HOST): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              str(dest_ip),   # special tag that refers to the IP of the server
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(20),
                              generateRandomHexByte(20)
                             ],
                      str(DiamAVPCodes.ORIGIN_REALM): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(8),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.USER_NAME): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                      str(DiamAVPCodes.DSA_FLAGS): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'dwepxccjncpqkp',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(6),
                              generateRandomHexByte(6)
                             ],
                      str(DiamAVPCodes.DSR_FLAGS): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'dwepxccjncpqkp',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(7),
                              generateRandomHexByte(8)
                             ],
                     }
            
            # add custom AVPs to test
            if (isRequest or (not isRequest and not isAnswer)) and 'DSR' in customs:
                for k, v in customs['DSR'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
            if (isAnswer or (not isRequest and not isAnswer)) and 'DSA' in customs:
                for k, v in customs['DSA'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
                
            # create all the fuzzy messages
            for k,v in toTest.items():
                # generate fuzzy AVP
                avps = generateFuzzyAVPs(k, v)
                                
                for a in avps:
                    base_msg = msgs_map[DiamCommandCodes.DELETE_SUBSCRIBER_DATA_3GPP]['msg']
                    base_msg.removeAVPbyCode(int(k))
                    base_msg.addAVP(a)
                    msgs.append(base_msg)
                
                
        elif cmd_code == DiamCommandCodes.PURGE_UE_3GPP:
            # get or create the base message
            base_msg = None
            if DiamCommandCodes.PURGE_UE_3GPP in msgs_map:
                base_msg = msgs_map[DiamCommandCodes.PURGE_UE_3GPP]['msg']
            else:
                printYellow("Fuzzy Messages: NO PURGE_UE CONFIG FILE PROVIDED")
                continue
                
            # list of all AVPs to test
            toTest = {
                      str(DiamAVPCodes.ORIGIN_HOST): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              str(dest_ip),   # special tag that refers to the IP of the server
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(20),
                              generateRandomHexByte(20)
                             ],
                      str(DiamAVPCodes.ORIGIN_REALM): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(8),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.USER_NAME): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                     }
            
            # add custom AVPs to test
            if (isRequest or (not isRequest and not isAnswer)) and 'DSR' in customs:
                for k, v in customs['DSR'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
            if (isAnswer or (not isRequest and not isAnswer)) and 'DSA' in customs:
                for k, v in customs['DSA'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
                
            # create all the fuzzy messages
            for k,v in toTest.items():
                # generate fuzzy AVP
                avps = generateFuzzyAVPs(k, v)
                                
                for a in avps:
                    base_msg = msgs_map[DiamCommandCodes.PURGE_UE_3GPP]['msg']
                    base_msg.removeAVPbyCode(int(k))
                    base_msg.addAVP(a)
                    msgs.append(base_msg)
                
                
        elif cmd_code == DiamCommandCodes.RESET_3GPP:
            # get or create the base message
            base_msg = None
            if DiamCommandCodes.RESET_3GPP in msgs_map:
                base_msg = msgs_map[DiamCommandCodes.RESET_3GPP]['msg']
            else:
                printYellow("Fuzzy Messages: NO RESET CONFIG FILE PROVIDED")
                continue
                
            # list of all AVPs to test
            toTest = {
                      str(DiamAVPCodes.ORIGIN_HOST): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              str(dest_ip),   # special tag that refers to the IP of the server
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(20),
                              generateRandomHexByte(20)
                             ],
                      str(DiamAVPCodes.ORIGIN_REALM): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(8),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.USER_NAME): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                      str(DiamAVPCodes.ROUTE_RECORD): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'dwepxccjncpqkp',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(12),
                              generateRandomHexByte(7)
                             ],
                      str(DiamAVPCodes.SERVICE_SELECTION): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'dwepxccjncpqkp',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(7),
                              generateRandomHexByte(8)
                             ],
                     }
            
            # add custom AVPs to test
            if (isRequest or (not isRequest and not isAnswer)) and 'RSR' in customs:
                for k, v in customs['RSR'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
            if (isAnswer or (not isRequest and not isAnswer)) and 'RSA' in customs:
                for k, v in customs['RSA'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
                
            # create all the fuzzy messages
            for k,v in toTest.items():
                # generate fuzzy AVP
                avps = generateFuzzyAVPs(k, v)
                                
                for a in avps:
                    base_msg = msgs_map[DiamCommandCodes.RESET_3GPP]['msg']
                    base_msg.removeAVPbyCode(int(k))
                    base_msg.addAVP(a)
                    msgs.append(base_msg)
                
                
        elif cmd_code == DiamCommandCodes.NOTIFY_3GPP:
            # get or create the base message
            base_msg = None
            if DiamCommandCodes.NOTIFY_3GPP in msgs_map:
                base_msg = msgs_map[DiamCommandCodes.NOTIFY_3GPP]['msg']
            else:
                printYellow("Fuzzy Messages: NO NOTIFY CONFIG FILE PROVIDED")
                continue
                
            # list of all AVPs to test
            toTest = {
                      str(DiamAVPCodes.ORIGIN_HOST): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              str(dest_ip),   # special tag that refers to the IP of the server
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(20),
                              generateRandomHexByte(20)
                             ],
                      str(DiamAVPCodes.ORIGIN_REALM): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(8),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.USER_NAME): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                      str(DiamAVPCodes.NOR_FLAGS): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'dwepxccjncpqkp',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(7),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.ROUTE_RECORD): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'dwepxccjncpqkp',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(7),
                              generateRandomHexByte(8)
                             ],
                     }
            
            # add custom AVPs to test
            if (isRequest or (not isRequest and not isAnswer)) and 'NOR' in customs:
                for k, v in customs['NOR'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
            if (isAnswer or (not isRequest and not isAnswer)) and 'NOA' in customs:
                for k, v in customs['NOA'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
                
            # create all the fuzzy messages
            for k,v in toTest.items():
                # generate fuzzy AVP
                avps = generateFuzzyAVPs(k, v)
                                
                for a in avps:
                    base_msg = msgs_map[DiamCommandCodes.NOTIFY_3GPP]['msg']
                    base_msg.removeAVPbyCode(int(k))
                    base_msg.addAVP(a)
                    msgs.append(base_msg)
                
                
        elif cmd_code == DiamCommandCodes.ME_IDENTITY_CHECK_3GPP:
            # get or create the base message
            base_msg = None
            if DiamCommandCodes.ME_IDENTITY_CHECK_3GPP in msgs_map:
                base_msg = msgs_map[DiamCommandCodes.ME_IDENTITY_CHECK_3GPP]['msg']
            else:
                printYellow("Fuzzy Messages: NO ME_IDENTITY_CHECK CONFIG FILE PROVIDED")
                continue
                
            # list of all AVPs to test
            toTest = {
                      str(DiamAVPCodes.ORIGIN_HOST): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              str(dest_ip),   # special tag that refers to the IP of the server
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(20),
                              generateRandomHexByte(20)
                             ],
                      str(DiamAVPCodes.ORIGIN_REALM): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(8),
                              generateRandomHexByte(8)
                             ],
                      str(DiamAVPCodes.USER_NAME): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(15),
                              generateRandomHexByte(15)
                             ],
                      str(DiamAVPCodes.ROUTE_RECORD): [
                              '123456789', 
                              '!"$%/&%()=@#',
                              '<b>Hello</b>&nbsp;<i>World!</i>',
                              'dwepxccjncpqkp',
                              generateRandomMsg('A-Za-z0-9'),
                              generateRandomMsg(),
                              generateRandomHexString(7),
                              generateRandomHexByte(8)
                             ],
                     }
            
            # add custom AVPs to test
            if (isRequest or (not isRequest and not isAnswer)) and 'ECR' in customs:
                for k, v in customs['ECR'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
            if (isAnswer or (not isRequest and not isAnswer)) and 'ECA' in customs:
                for k, v in customs['ECA'].items():
                    v = replaceSpecialTag(v, dest_ip, orig_ip)
                    
                    a = str(DiamAVPCodes.name2code(k))
                    
                    if a not in toTest:
                        toTest[a] = v
                    else:
                        toTest[a].extend(v)
                
            # create all the fuzzy messages
            for k,v in toTest.items():
                # generate fuzzy AVP
                avps = generateFuzzyAVPs(k, v)
                                
                for a in avps:
                    base_msg = msgs_map[DiamCommandCodes.ME_IDENTITY_CHECK_3GPP]['msg']
                    base_msg.removeAVPbyCode(int(k))
                    base_msg.addAVP(a)
                    msgs.append(base_msg)
            
    return msgs

##
## @brief      Generates a generic AVP with the passed FUZZY value
##
## @param      avp_code  the code of the AVP to generate
## @param      customs   the list of custom values to generate
##
## @return     a list of fuzzied AVPs
##
def generateFuzzyAVPs(avp_code, customs):
    avps = []
    avp_code = int(avp_code)

    for c in customs:
        avp = DiamAVP(avp_code, c, None)
        avp.setMandatoryFlag(True)
        avps.append(avp)
    
    return avps    

##
## @brief      Generates a random SessionID AVP
##
## @param      host  the required host value
##
## @return     a dict representing the Session-ID-AVP
##              {
##                'name': 'session-id',
##                'value': <generated-session-id-value>,
##                'flags': ['M']
##              }
##
def generateSessionIDAVP(host):
    return {'name': 'session-id',
            'value': generateSessionID(host),
            'flags': ['M']}

##
## @brief      Generates a random SessionID value
##
## @param      host  the required host value
##
## @return     a string representing the SessionID value
##
def generateSessionID(host):
    return "%s;%s;%s" % (host,
                         ''.join([random.choice('0123456789') for _ in range(9)]),
                         ''.join([random.choice('0123456789') for _ in range(9)]))    

        