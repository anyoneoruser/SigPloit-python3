from .base_interface import BaseInterface
from ..utilities import checkAvpValue, getAvpData, generateSessionIDAVP
from ..diameter.diamCommandCodes import DiamCommandCodes
from .s6a_messages_classes import DiamCancelLocationRequest,\
    DiamMEIdentityCheckAnswer, DiamCancelLocationAnswer,\
    DiamUpdateLocationRequest, DiamUpdateLocationAnswer,\
    DiamAuthenticationInformationRequest, DiamAuthenticationInformationAnswer,\
    DiamInsertSubscriberDataRequest, DiamInsertSubscriberDataAnswer,\
    DiamDeleteSubscriberDataRequest, DiamDeleteSubscriberDataAnswer,\
    DiamPurgeUERequest, DiamPurgeUEAnswer, DiamResetAnswer, DiamResetRequest,\
    DiamNotifyRequest, DiamNotifyAnswer, DiamMEIdentityCheckRequest
from ..diameter.diamApplicationIDs import DiamApplicationIDs
from ..diameter.diamAVPExceptions import MissingMandatoryAVPException
from ..commons import logWarn

##
## @brief      Generates 3GPP's s6a Diameter's messages
## 
## @author: Ilario Dal Grande, Rosalia d'Alessandro
##    

### TODO: 
### 1. Code redesign/optimization (issue #3)
### 2. multiple d-h/d-r support (issue #1, #2)

class S6a3gppInterface(BaseInterface):
    def __init__(self):
        super(S6a3gppInterface, self).__init__()
        self.appid = DiamApplicationIDs.DI_3GPP_S6A
        
    def __generateMessage(self, cmd_code, is_request, is_answer):
        try:
            checkAvpValue(self.conf['avps'], 'origin-host')
            self.orig_host = getAvpData(self.conf['avps'], 'origin-host')
        except Exception:
            self.orig_host = self.conf['origin_host']
            if self.orig_host is None:
                raise MissingMandatoryAVPException('Origin-Host AVP is mandatory')
            self.orig_host = {'value': self.orig_host,
                              'flags': ['M'],
                              'name': 'origin-host'}

        try:
            checkAvpValue(self.conf['avps'], 'origin-realm')
            self.orig_realm = getAvpData(self.conf['avps'], 'origin-realm')
        except Exception:
            self.orig_realm = self.conf['origin_realm']
            if self.orig_realm is None:
                raise MissingMandatoryAVPException('Origin-Realm AVP is mandatory')
            self.orig_realm = {'value': self.orig_realm,
                              'flags': ['M'],
                              'name': 'origin-realm'}
            
        self.dest_host = self.conf['destination_host']
        if self.dest_host is not None:
            self.dest_host = {'value': self.dest_host,
                              'flags': [],
                              'name': 'destination-host'}
            
        self.dest_realm = self.conf['destination_realm']
        if self.dest_realm is not None:
            self.dest_realm = {'value': self.dest_realm,
                              'flags': ['M'],
                              'name': 'destination-realm'}
            
        checkAvpValue(self.conf['avps'], 'auth-session-state')

        try:
            checkAvpValue(self.conf['avps'], 'session-id')
            self.sid_seed = getAvpData(self.conf['avps'], 
                                    'session-id')['value']
        except Exception:
            self.sid_seed = self.orig_host['value']
                
        if cmd_code == DiamCommandCodes.CANCEL_LOCATION_3GPP:
            return self.__generateCancelLocationMessages(is_request, is_answer)
        elif cmd_code == DiamCommandCodes.UPDATE_LOCATION_3GPP:
            return self.__generateUpdateLocationMessages(is_request, is_answer)
        elif cmd_code == DiamCommandCodes.AUTHENTICATION_INFORMATION_3GPP:
            return self.__generateAuthenticationInformationMessages(is_request, is_answer)
        elif cmd_code == DiamCommandCodes.INSERT_SUBSCRIBER_DATA_3GPP:
            return self.__generateInsertSubscriberDataMessages(is_request, is_answer)
        elif cmd_code == DiamCommandCodes.DELETE_SUBSCRIBER_DATA_3GPP:
            return self.__generateDeleteSubscriberDataMessages(is_request, is_answer)
        elif cmd_code == DiamCommandCodes.PURGE_UE_3GPP:
            return self.__generatePurgeUEMessages(is_request, is_answer)
        elif cmd_code == DiamCommandCodes.RESET_3GPP:
            return self.__generateResetMessages(is_request, is_answer)
        elif cmd_code == DiamCommandCodes.NOTIFY_3GPP:
            return self.__generateNotifyMessages(is_request, is_answer)
        elif cmd_code == DiamCommandCodes.ME_IDENTITY_CHECK_3GPP:
            return self.__generateMEIdentityCheckMessages(is_request, is_answer)
        
        logWarn("Unsupported command code %d" % (cmd_code), self.TAG_NAME)
        return None
        
    def __generateCancelLocationMessages(self, is_request, is_answer):
        msg_list = {}
        
        if is_request:
            if self.dest_host is None:
                checkAvpValue(self.conf['avps'], 'destination-host')
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
                
            checkAvpValue(self.conf['avps'], 'user-name')
            checkAvpValue(self.conf['avps'], 'cancellation-type')

        try:
            checkAvpValue(self.conf['avps'], 'session-id')
            sid_seed = getAvpData(self.conf['avps'], 'session-id')
            print(sid_seed)
        except Exception:
            print("session id not found")


            
            msg_list['request'] = DiamCancelLocationRequest(
                                self.appid,
                                generateSessionIDAVP(self.orig_host['value']),
                                self.orig_host,
                                self.orig_realm,
                                self.dest_host,
                                self.dest_realm, 
                                getAvpData(self.conf['avps'], 'auth-session-state'),
                                getAvpData(self.conf['avps'], 'user-name'),
                                getAvpData(self.conf['avps'], 'cancellation-type')
                               )

            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 
                                'supported-features'))
            msg_list['request'].set_clr_flags(getAvpData(self.conf['avps'], 
                                'clr-flags'))
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 
                                'vendor-specific-application-id'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 
                                'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 
                                'route-record'))
            
        if is_answer:
            msg_list['answer'] = DiamCancelLocationAnswer(
                                self.appid, 
                                generateSessionIDAVP(self.orig_host['value']),
                                self.orig_host,
                                self.orig_realm,
                                getAvpData(self.conf['avps'], 'auth-session-state')
                               )
            
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result-code'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
                
        return msg_list
        
    def __generateUpdateLocationMessages(self, is_request, is_answer):
        msg_list = {}
        
        if is_request:
            if self.dest_host is None:
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
                
            checkAvpValue(self.conf['avps'], 'user-name')
            checkAvpValue(self.conf['avps'], 'rat-type')
            checkAvpValue(self.conf['avps'], 'ulr-flags')
            
            checkAvpValue(self.conf['avps'], 'visited-plmn-id')

            msg_list['request'] = DiamUpdateLocationRequest(
                                self.appid, 
                                generateSessionIDAVP(self.orig_host['value']),
                                self.orig_host,
                                self.orig_realm,
                                self.dest_realm, 
                                getAvpData(self.conf['avps'], 'auth-session-state'),
                                getAvpData(self.conf['avps'], 'user-name'),
                                getAvpData(self.conf['avps'], 'rat-type'),
                                getAvpData(self.conf['avps'], 'ulr-flags'),
                                getAvpData(self.conf['avps'], 'visited-plmn-id')
                               )

            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_destination_host(self.dest_host)
            msg_list['request'].set_oc_supported_features(getAvpData(self.conf['avps'], 'oc-supported-features'))
            msg_list['request'].set_ue_srvcc_capability(getAvpData(self.conf['avps'], 'ue-srvcc-capability'))
            msg_list['request'].set_sgsn_number(getAvpData(self.conf['avps'], 'sgsn-number'))
            msg_list['request'].set_homogeneous_support_ims_voice_over_ps_sessions(getAvpData(self.conf['avps'], 'homogeneous-support-ims-voice-over-ps-sessions'))
            msg_list['request'].set_gmlc_address(getAvpData(self.conf['avps'], 'gmlc-address'))
            msg_list['request'].set_active_apn(getAvpData(self.conf['avps'], 'active-apn'))
            msg_list['request'].set_equivalent_plmn_list(getAvpData(self.conf['avps'], 'equivalent-plmn-list'))
            msg_list['request'].set_mme_number_for_mt_sms(getAvpData(self.conf['avps'], 'mme-number-for-mt-sms'))
            msg_list['request'].set_sms_register_request(getAvpData(self.conf['avps'], 'sms-register-request'))
            msg_list['request'].set_sgs_mme_identity(getAvpData(self.conf['avps'], 'sgs-mme-identity'))
            msg_list['request'].set_coupled_node_diameter_id(getAvpData(self.conf['avps'], 'coupled-node-diameter-id'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
                
        if is_answer:
            msg_list['answer'] = DiamUpdateLocationAnswer(
                            self.appid, 
                            generateSessionIDAVP(self.orig_host['value']),
                            getAvpData(self.conf['avps'], 'auth-session-state'),
                            self.orig_host,
                            self.orig_realm,
                           )
            
            msg_list['answer'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result-code'))
            msg_list['answer'].set_error_diagnostic(getAvpData(self.conf['avps'], 'error-diagnostic'))
            msg_list['answer'].set_oc_supported_features(getAvpData(self.conf['avps'], 'oc-supported-features'))
            msg_list['answer'].set_oc_olr(getAvpData(self.conf['avps'], 'oc-olr'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_ula_flags(getAvpData(self.conf['avps'], 'ula-flags'))
            msg_list['answer'].set_subscription_data(getAvpData(self.conf['avps'], 'subscription-data'))
            msg_list['answer'].set_reset_id(getAvpData(self.conf['avps'], 'reset-id'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
    
        return msg_list
    
    def __generateAuthenticationInformationMessages(self, is_request, is_answer):
        msg_list = {}
                                
        if is_request:
            if self.dest_host is None:
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
                
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
            
            checkAvpValue(self.conf['avps'], 'user-name')
            checkAvpValue(self.conf['avps'], 'visited-plmn-id')
            
                
            msg_list['request'] = DiamAuthenticationInformationRequest(
                                self.appid,
                                generateSessionIDAVP(self.sid_seed),
                                getAvpData(self.conf['avps'], 'auth-session-state'),
                                self.orig_host,
                                self.orig_realm,
                                self.dest_realm,
                                getAvpData(self.conf['avps'], 'user-name'),
                                getAvpData(self.conf['avps'], 'visited-plmn-id')
                               )
            
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_destination_host(self.dest_host)
            msg_list['request'].set_oc_supported_features(getAvpData(self.conf['avps'], 'oc-supported-features'))
            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['request'].set_requested_eutran_authentication_info(getAvpData(self.conf['avps'], 'requested-eutran-authentication-info'))
            msg_list['request'].set_requested_utran_geran_authentication_info(getAvpData(self.conf['avps'], 'requested-utran-geran-authentication-info'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
            
        if is_answer:
            msg_list['answer'] = DiamAuthenticationInformationAnswer(
                                self.appid,
                                generateSessionIDAVP(self.sid_seed),
                                getAvpData(self.conf['avps'], 'auth-session-state'),
                                self.orig_host,
                                self.orig_realm
                               )
        
            msg_list['answer'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result-code'))
            msg_list['answer'].set_error_diagnostic(getAvpData(self.conf['avps'], 'error-diagnostic'))
            msg_list['answer'].set_oc_supported_features(getAvpData(self.conf['avps'], 'oc-supported-features'))
            msg_list['answer'].set_oc_olr(getAvpData(self.conf['avps'], 'oc-olr'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_authentication_info(getAvpData(self.conf['avps'], 'authentication-info'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
            
        return msg_list
    
    def __generateInsertSubscriberDataMessages(self, is_request, is_answer):
        msg_list = {}
        
        if is_request:
            if self.dest_host is None:
                checkAvpValue(self.conf['avps'], 'destination-host')
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
                
            checkAvpValue(self.conf['avps'], 'user-name')
            checkAvpValue(self.conf['avps'], 'subscription-data')
            
            msg_list['request'] = DiamInsertSubscriberDataRequest(
                                self.appid, 
                                generateSessionIDAVP(self.orig_host['value']),
                                getAvpData(self.conf['avps'], 'auth-session-state'),
                                self.orig_host,
                                self.orig_realm,
                                self.dest_host,
                                self.dest_realm,
                                getAvpData(self.conf['avps'], 'user-name'),
                                getAvpData(self.conf['avps'], 'subscription-data'),
                               )
            
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['request'].set_idr_flags(getAvpData(self.conf['avps'], 'idr-flags'))
            msg_list['request'].set_reset_id(getAvpData(self.conf['avps'], 'reset-id'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
            
        if is_answer:
            msg_list['answer'] = DiamInsertSubscriberDataAnswer(
                                 self.appid,
                                 generateSessionIDAVP(self.orig_host['value']),
                                 getAvpData(self.conf['avps'], 'auth-session-state'),
                                 self.orig_host,
                                 self.orig_realm
                                )
                                                 
            msg_list['answer'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result-code'))
            msg_list['answer'].set_ims_voice_over_ps_sessions_supported(getAvpData(self.conf['avps'], 'ims-voice-over-ps-sessions-supported'))
            msg_list['answer'].set_last_ue_activity_time(getAvpData(self.conf['avps'], 'last-ue-activity-time'))
            msg_list['answer'].set_rat_type(getAvpData(self.conf['avps'], 'rat-type'))
            msg_list['answer'].set_ida_flags(getAvpData(self.conf['avps'], 'ida-flags'))
            msg_list['answer'].set_eps_user_state(getAvpData(self.conf['avps'], 'eps-user-state'))
            msg_list['answer'].set_eps_location_information(getAvpData(self.conf['avps'], 'eps-location-information'))
            msg_list['answer'].set_local_time_zone(getAvpData(self.conf['avps'], 'local-time-zone'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))                                     
     
        return msg_list
    
    def __generateDeleteSubscriberDataMessages(self, is_request, is_answer):
        msg_list = {}
        
        if is_request:
            if self.dest_host is None:
                checkAvpValue(self.conf['avps'], 'destination-host')
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
                
            checkAvpValue(self.conf['avps'], 'user-name')
            checkAvpValue(self.conf['avps'], 'dsr-flags')
            
            msg_list['request'] = DiamDeleteSubscriberDataRequest(
                                  self.appid, 
                                  generateSessionIDAVP(self.orig_host['value']),
                                  getAvpData(self.conf['avps'], 'auth-session-state'),
                                  self.orig_host,
                                  self.orig_realm,
                                  self.dest_host,
                                  self.dest_realm,
                                  getAvpData(self.conf['avps'], 'user-name'),
                                  getAvpData(self.conf['avps'], 'dsr-flags')
                                 )
                                                  
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['request'].set_context_identifier(getAvpData(self.conf['avps'], 'context-identifier'))
            msg_list['request'].set_trace_reference(getAvpData(self.conf['avps'], 'trace-reference'))
            msg_list['request'].set_ts_code(getAvpData(self.conf['avps'], 'ts-code'))
            msg_list['request'].set_ss_code(getAvpData(self.conf['avps'], 'ss-code'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
                
        if is_answer:
            msg_list['answer'] = DiamDeleteSubscriberDataAnswer(
                                 self.appid, 
                                 generateSessionIDAVP(self.orig_host['value']),
                                 getAvpData(self.conf['avps'], 'auth-session-state'),
                                 self.orig_host,
                                 self.orig_realm
                                )
                                                 
            msg_list['answer'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result-code'))
            msg_list['answer'].set_dsa_flags(getAvpData(self.conf['avps'], 'dsa-flags'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))  
    
        return msg_list
    
    def __generatePurgeUEMessages(self, is_request, is_answer):
        msg_list = {}
        
        if is_request:
            if self.dest_host is None:
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
                
            checkAvpValue(self.conf['avps'], 'user-name')
            
            msg_list['request'] = DiamPurgeUERequest(
                                  self.appid, 
                                  generateSessionIDAVP(self.orig_host['value']),
                                  getAvpData(self.conf['avps'], 'auth-session-state'),
                                  self.orig_host,
                                  self.orig_realm,
                                  self.dest_realm,
                                  getAvpData(self.conf['avps'], 'user-name')
                                 )
                                                  
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
            msg_list['request'].set_destination_host(self.dest_host)
            msg_list['request'].set_oc_supported_features(getAvpData(self.conf['avps'], 'oc-supported-features'))
            msg_list['request'].set_pur_flags(getAvpData(self.conf['avps'], 'pur-flags'))
            msg_list['request'].set_eps_location_information(getAvpData(self.conf['avps'], 'eps-location-information'))
            
        if is_answer:
            msg_list['answer'] = DiamPurgeUEAnswer(
                                 self.appid, 
                                 generateSessionIDAVP(self.orig_host['value']),
                                 getAvpData(self.conf['avps'], 'auth-session-state'),
                                 self.orig_host,
                                 self.orig_realm
                                )
                                                 
            msg_list['answer'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result-code'))
            msg_list['answer'].set_pua_flags(getAvpData(self.conf['avps'], 'pua-flags'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))  
            msg_list['answer'].set_oc_supported_features(getAvpData(self.conf['avps'], 'oc-supported-features'))
            msg_list['answer'].set_oc_olr(getAvpData(self.conf['avps'], 'oc-olr'))
    
        return msg_list
    
    def __generateResetMessages(self, is_request, is_answer):
        msg_list = {}
        
        if is_request:
            if self.dest_host is None:
                checkAvpValue(self.conf['avps'], 'destination-host')
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
            
            msg_list['request'] = DiamResetRequest(
                                self.appid, 
                                generateSessionIDAVP(self.orig_host['value']),
                                getAvpData(self.conf['avps'], 'auth-session-state'),
                                self.orig_host,
                                self.orig_realm,
                                self.dest_host,
                                self.dest_realm
                               )
                                                 
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['request'].set_user_id(getAvpData(self.conf['avps'], 'user-id'))
            msg_list['request'].set_reset_id(getAvpData(self.conf['avps'], 'reset-id'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))      

        if is_answer:
            msg_list['answer'] = DiamResetAnswer(
                                  self.appid, 
                                  generateSessionIDAVP(self.orig_host['value']),
                                  getAvpData(self.conf['avps'], 'auth-session-state'),
                                  self.orig_host,
                                  self.orig_realm
                                )
                                                 
            msg_list['answer'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result-code'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
            
        return msg_list
    
    def __generateNotifyMessages(self, is_request, is_answer):
        msg_list = {}
        
        if is_request:
            if self.dest_host is None:
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
                
            checkAvpValue(self.conf['avps'], 'user-name')
            
            msg_list['request'] = DiamNotifyRequest(
                                 self.appid, 
                                 generateSessionIDAVP(self.orig_host['value']),
                                 getAvpData(self.conf['avps'], 'auth-session-state'),
                                 self.orig_host,
                                 self.orig_realm,
                                 self.dest_realm,
                                 getAvpData(self.conf['avps'], 'user-name')
                                )
                                                 
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['request'].set_destination_host(self.dest_host)
            msg_list['request'].set_terminal_information(getAvpData(self.conf['avps'], 'terminal-information'))
            msg_list['request'].set_mip6_agent_info(getAvpData(self.conf['avps'], 'mip6-agent-info'))
            msg_list['request'].set_visited_network_identifier(getAvpData(self.conf['avps'], 'visited-network-identifier'))
            msg_list['request'].set_context_identifier(getAvpData(self.conf['avps'], 'context-identifier'))
            msg_list['request'].set_service_selection(getAvpData(self.conf['avps'], 'service-selection'))
            msg_list['request'].set_alert_reason(getAvpData(self.conf['avps'], 'alert-reason'))
            msg_list['request'].set_ue_srvcc_capability(getAvpData(self.conf['avps'], 'ue-srvcc-capability'))
            msg_list['request'].set_nor_flags(getAvpData(self.conf['avps'], 'nor-flags'))
            msg_list['request'].set_homogeneous_support_ims_voice_over_ps_sessions(getAvpData(self.conf['avps'], 'homogeneous-support-ims-voice-over-ps-sessions'))
            msg_list['request'].set_oc_supported_features(getAvpData(self.conf['avps'], 'oc-supported-features'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
                
        if is_answer:
            msg_list['answer'] = DiamNotifyAnswer(
                                self.appid, 
                                generateSessionIDAVP(self.orig_host['value']),
                                getAvpData(self.conf['avps'], 'auth-session-state'),
                                self.orig_host,
                                self.orig_realm
                               )
                                                 
            msg_list['answer'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result-code'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp')) 
            msg_list['answer'].set_oc_supported_features(getAvpData(self.conf['avps'], 'oc-supported-features'))
            msg_list['answer'].set_oc_olr(getAvpData(self.conf['avps'], 'oc-olr'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record')) 
                
        return msg_list
    
    def __generateMEIdentityCheckMessages(self, is_request, is_answer):
        msg_list = {}
        
        if is_request:
            if self.dest_host is None:
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
                
            checkAvpValue(self.conf['avps'], 'terminal-information')
            
            msg_list['request'] = DiamMEIdentityCheckRequest(
                                  self.appid, 
                                  generateSessionIDAVP(self.orig_host['value']),
                                  getAvpData(self.conf['avps'], 'auth-session-state'),
                                  self.orig_host,
                                  self.orig_realm,
                                  self.dest_realm,
                                  getAvpData(self.conf['avps'], 'terminal-information')
                                 ) 
                                                 
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_user_name(getAvpData(self.conf['avps'], 'user-name'))
            msg_list['request'].set_destination_host(self.dest_host)
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
            
        if is_answer:
            msg_list['answer'] = DiamMEIdentityCheckAnswer(
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
            msg_list['answer'].set_equipment_status(getAvpData(self.conf['avps'], 'equipment-status'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record')) 
            
        return msg_list
    
    def generateMessages(self):
        msgs_list = []
        
        for e in self.conf['3gpp_messages_list']:
            m = self.__generateMessage(e['cmd_code'], e['has_request'], e['has_answer'])
            if len(m) > 0:
                for val in m.values():
                    msgs_list.append(val)
        
        return msgs_list
    