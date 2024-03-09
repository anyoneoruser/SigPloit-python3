from .base_interface import BaseInterface
from ..utilities import checkAvpValue, getAvpData
from ..diameter.diamCommandCodes import DiamCommandCodes
from ..diameter.diamApplicationIDs import DiamApplicationIDs
from .common_messages_classes import DiamCapabilitiesExchangeAnswer,\
        DiamCapabilitiesExchangeRequest, DiamDeviceWatchdogRequest,\
        DiamDeviceWatchdogAnswer
from ..commons import logWarn


##
## @brief      Generates the most common Diameter's messages
##
class CommonInterface(BaseInterface):
        def __init__(self):
                super(CommonInterface, self).__init__()
                self.appid = DiamApplicationIDs.DIAMETER_COMMON_MESSAGES
                self.TAG_NAME = "CommonInterface"
 
        ##
        ## @brief      Generates each message based on the command code
        ##
        ## @param      self        refers to the class itself
        ## @param      cmd_code    the AVP command code
        ## @param      is_request  indicates if it's a request
        ## @param      is_answer   indicates if it's an answer
        ##
        ## @return     the generated diameter message
        ##
        def __generateMessage(self, cmd_code, is_request, is_answer):
                self.orig_host = self.conf['origin_host']
                if self.orig_host is not None:
                        self.orig_host = {'value': self.orig_host,
                                                            'flags': ['M'],
                                                            'name': 'origin-host'}
                else:
                        checkAvpValue(self.conf['avps'], 'origin-host')
                        self.orig_host = getAvpData(self.conf['avps'], 'origin-host')
                        
                self.orig_realm = self.conf['origin_realm']
                if self.orig_realm is not None:
                        self.orig_realm = {'value': self.orig_realm,
                                                            'flags': ['M'],
                                                            'name': 'origin-realm'}
                else:
                        checkAvpValue(self.conf['avps'], 'origin-realm')
                        self.orig_realm = getAvpData(self.conf['avps'], 'origin-realm')
                                
                if cmd_code == DiamCommandCodes.CAPABILITIES_EXCHANGE:
                        return self.__generateCapabilitiesExchangeMessages(is_request, is_answer)
                
                if cmd_code == DiamCommandCodes.DEVICE_WATCHDOG :
                        return self.__generateDeviceWatchdogMessages(is_request, is_answer)
                
                logWarn("Unsupported command code %d" %(cmd_code), self.TAG_NAME)
                return None
        
        ##
        ## @brief      Generates Capabilities Exchange messages, both request and answer
        ##
        ## @param      self        refers to the class itself
        ## @param      is_request  indicates if it's a request
        ## @param      is_answer   indicates if it's an answer
        ##
        ## @return     a dict with the request and answer messages if required
        ##                     {
        ##                       'request': <CER>,
        ##                       'answer': <CEA>
        ##                     }
        ##
        def __generateCapabilitiesExchangeMessages(self, is_request, is_answer):
                checkAvpValue(self.conf['avps'], 'host-ip-address')
                checkAvpValue(self.conf['avps'], 'vendor-id')
                checkAvpValue(self.conf['avps'], 'product-name')
                
                msg_list = {}  
                                
                if is_request:
                        msg_list["request"] = DiamCapabilitiesExchangeRequest(
                            self.appid, self.orig_host,
                            self.orig_realm,
                            getAvpData(self.conf['avps'], 'host-ip-address'),
                            getAvpData(self.conf['avps'], 'vendor-id'),
                            getAvpData(self.conf['avps'], 'product-name')
                            )
                        
                if is_answer:
                        checkAvpValue(self.conf['avps'], 'result-code')
                        
                        msg_list["answer"] = DiamCapabilitiesExchangeAnswer(
                            self.appid, getAvpData(self.conf['avps'], 
                                        'result-code'),
                            self.orig_host, self.orig_realm,
                            getAvpData(self.conf['avps'], 'host-ip-address'),
                            getAvpData(self.conf['avps'], 'vendor-id'),
                            getAvpData(self.conf['avps'],'product-name')
                            )
                                                    
                        msg_list["answer"].set_error_message(getAvpData(
                            self.conf['avps'], 'error-message'))
                        msg_list["answer"].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
                        
                for msg in msg_list.values():
                        msg.set_origin_state_id(getAvpData(self.conf['avps'], 'origin-state-id'))
                        msg.set_supported_vendor_id(getAvpData(self.conf['avps'], 'supported-vendor-id'))
                        msg.set_auth_app_id(getAvpData(self.conf['avps'], 'auth-application-id'))
                        msg.set_inband_security_id(getAvpData(self.conf['avps'], 'inband-security-id'))
                        msg.set_acct_app_id(getAvpData(self.conf['avps'], 'acct-application-id'))
                        msg.set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
                        msg.set_firmware(getAvpData(self.conf['avps'], 'firmware'))
                        
                return msg_list

        ##
        ## @brief      Generates Device Watchdog messages, both request and answer
        ##
        ## @param      self        refers to the class itself
        ## @param      is_request  indicates if it's a request
        ## @param      is_answer   indicates if it's an answer
        ##
        ## @return     a dict with the request and answer messages if required
        ##                     {
        ##                       'request': <DWR>,
        ##                       'answer': <DWA>
        ##                     }
        ##
        def __generateDeviceWatchdogMessages(self, is_request, is_answer):
                msg_list = {}           

                if is_request:
                        msg_list["request"] = DiamDeviceWatchdogRequest(
                                                                        self.appid,
                                                                        self.orig_host,
                                                                        self.orig_realm,
                                                                       )
                        
                if is_answer:
                        checkAvpValue(self.conf['avps'], 'result-code')
                                                        
                        msg_list["answer"] = DiamDeviceWatchdogAnswer(
                                                                     self.appid,
                                                                     getAvpData(self.conf['avps'], 'result-code'),
                                                                     self.orig_host,
                                                                     self.orig_realm,
                                                                    )
                                                    
                        msg_list["answer"].set_error_message(getAvpData(self.conf['avps'], 'error-message'))
                        msg_list["answer"].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
                        
                for msg in msg_list.values():
                        msg.set_origin_state_id(getAvpData(self.conf['avps'], 'origin-state-id'))
                        
                return msg_list
        
        ##
        ## @brief      Generates all the messages for the Common Interface
        ##
        ## @param      self  refers to the class itself
        ##
        ## @return     a list of dict that represent all the messages of the interface
        ##                     [
        ##                         {'<APV-code>': <AVP-object>},
        ##                         {'<AVP-code>': 
        ##                             {
        ##                             'answer': <AVP-object>,
        ##                             'request': <AVP-object>
        ##                             }
        ##                         },
        ##                         ...
        ##                     ]
        ##
        def generateMessages(self):
                msgs_list = {}
                
                for e in self.conf['base_message_list']:
                        m = self.__generateMessage(e['cmd_code'], e['has_request'], e['has_answer'])
                        if len(m) > 0:
                                if e['cmd_code'] not in msgs_list:
                                        msgs_list[e['cmd_code']] = m
                                else:
                                        if 'answer' in m:
                                                msgs_list[e['cmd_code']]['answer'] = m['answer']
                                        if 'request' in m:
                                                msgs_list[e['cmd_code']]['request'] = m['request']
                
                return msgs_list
        
