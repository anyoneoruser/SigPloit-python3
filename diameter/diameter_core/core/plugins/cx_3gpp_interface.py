from .base_interface import BaseInterface
from ..utilities import checkAvpValue, getAvpData, generateSessionIDAVP
from ..diameter.diamCommandCodes import DiamCommandCodes
from ..diameter.diamApplicationIDs import DiamApplicationIDs
from .slh_messages_classes import DiamLCSRoutingInfoAnswer,\
    DiamLCSRoutingInfoRequest
from ..commons import logWarn
    
##
## @brief      Generates 3GPP's Cx Diameter's messages
## 
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##
class Cx3GPPInterface(BaseInterface):
    def __init__(self, conf):
        super(Cx3GPPInterface, self).__init__(conf)
        self.appid = DiamApplicationIDs.DI_3GPP_CX
        
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
            
        self.dest_host = self.conf['destination_host']
        if self.dest_host is not None:
            self.dest_host = {'value': self.dest_host,
                              'flags': [],
                              'name': 'destination-host'}
            
        self.dest_realm = self.conf['destination_realm']
        if self.dest_realm is not None:
            self.dest_realm = {'value': self.dest_realm,
                              'flags': [],
                              'name': 'destination-realm'}
            
        checkAvpValue(self.conf['avps'], 'auth-session-state')
                
        if cmd_code == DiamCommandCodes.LCS_ROUTING_INFO:
            return self.__generateLCSRoutingInfoMessages(is_request, is_answer)
        
        logWarn("Unsupported command code %d" % (cmd_code), self.TAG_NAME)
        return None
     
    def __generateLCSRoutingInfoMessages(self, is_request, is_answer):
        msg_list = {}  
        
        if is_request:
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
            
            msg_list['request'] = DiamLCSRoutingInfoRequest(
                                         self.appid, 
                                         generateSessionIDAVP(self.orig_host['value']),
                                         getAvpData(self.conf['avps'], 'auth-session-state'),
                                         self.orig_host,
                                         self.orig_realm,
                                         self.dest_realm
                                        ) 
                                                 
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_user_name(getAvpData(self.conf['avps'], 'user-name'))
            msg_list['request'].set_destination_host(self.dest_host)
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
            msg_list['request'].set_msisdn(getAvpData(self.conf['avps'], 'msisdn'))   
            msg_list['request'].set_gmlc_number(getAvpData(self.conf['avps'], 'gmlc-number'))           
            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))                                            
        
        if is_answer:
            msg_list['answer'] = DiamLCSRoutingInfoAnswer(
                                        self.appid, 
                                        generateSessionIDAVP(self.orig_host['value']),
                                        getAvpData(self.conf['avps'], 'auth-session-state'),
                                        self.orig_host,
                                        self.orig_realm
                                       )
                                                 
            msg_list['answer'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result-code'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp')) 
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))  
            msg_list['answer'].set_user_name(getAvpData(self.conf['avps'], 'user-name'))
            msg_list['answer'].set_lmsi(getAvpData(self.conf['avps'], 'lmsi'))
            msg_list['answer'].set_serving_node(getAvpData(self.conf['avps'], 'serving-node'))
            msg_list['answer'].set_additional_serving_node(getAvpData(self.conf['avps'], 'additional-serving-node'))
            msg_list['answer'].set_msisdn(getAvpData(self.conf['avps'], 'msisdn'))   
            msg_list['answer'].set_gmlc_address(getAvpData(self.conf['avps'], 'gmlc-address'))   
            msg_list['answer'].set_ppr_address(getAvpData(self.conf['avps'], 'ppr-address'))
            msg_list['answer'].set_ria_flags(getAvpData(self.conf['avps'], 'ria-flags'))   
                
        return msg_list
    
    def generateMessages(self):
        msgs_list = []
        
        for e in self.conf['3gpp_messages_list']:
            m = self.__generateMessage(e['cmd_code'], e['has_request'], e['has_answer'])
            if len(m) > 0:
                for val in m.values():
                    msgs_list.append(val)
        
        return msgs_list
    