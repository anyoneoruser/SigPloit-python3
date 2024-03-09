from .base_interface import BaseInterface
from ..utilities import checkAvpValue, getAvpData, generateSessionIDAVP
from ..diameter.diamCommandCodes import DiamCommandCodes
from ..diameter.diamApplicationIDs import DiamApplicationIDs
from ..commons import logWarn
from .slg_messages_classes import DiamProvideLocationRequest, DiamProvideLocationAnswer,\
    DiamLocationReportRequest, DiamLocationReportAnswer
    
##
## @brief      Generates 3GPP's SLg Diameter's messages
## 
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##
class SLg3GPPInterface(BaseInterface):
    def __init__(self, conf):
        super(SLg3GPPInterface, self).__init__(conf)
        self.appid = DiamApplicationIDs.DI_3GPP_LCS_SLG
        
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
                
        if cmd_code == DiamCommandCodes.PROVIDE_LOCATION:
            return self.__generateProvideLocationMessages(is_request, is_answer)
        elif cmd_code == DiamCommandCodes.LOCATION_REPORT:
            return self.__generateLocationReportMessages(is_request, is_answer)
        
        logWarn("Unsupported command code %d" % (cmd_code), self.TAG_NAME)
        return None
     
    def __generateProvideLocationMessages(self, is_request, is_answer):
        msg_list = {}  
        
        if is_request:
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
            if self.dest_host is None:
                checkAvpValue(self.conf['avps'], 'destination-host')
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
                
            checkAvpValue(self.conf['avps'], 'slg-location-type')    
            checkAvpValue(self.conf['avps'], 'lcs-eps-client-name')    
            checkAvpValue(self.conf['avps'], 'lcs-client-type')
            
            msg_list['request'] = DiamProvideLocationRequest(
                                         self.appid, 
                                         generateSessionIDAVP(self.orig_host['value']),
                                         getAvpData(self.conf['avps'], 'auth-session-state'),
                                         self.orig_host,
                                         self.orig_realm,
                                         self.dest_host,
                                         self.dest_realm,
                                         getAvpData(self.conf['avps'], 'slg-location-type'),
                                         getAvpData(self.conf['avps'], 'lcs-eps-client-name'),
                                         getAvpData(self.conf['avps'], 'lcs-client-type')
                                        ) 
            
            msg_list['request'].set_vendor_specific_app_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['request'].set_user_name(getAvpData(self.conf['avps'], 'user-name'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))
            msg_list['request'].set_msisdn(getAvpData(self.conf['avps'], 'msisdn'))
            msg_list['request'].set_msisdn(getAvpData(self.conf['avps'], 'imei'))
            msg_list['request'].set_lcs_requestor_name(getAvpData(self.conf['avps'], 'lcs-requestor-name'))
            msg_list['request'].set_lcs_priority(getAvpData(self.conf['avps'], 'lcs-priority'))
            msg_list['request'].set_lcs_qos(getAvpData(self.conf['avps'], 'lcs-qos'))
            msg_list['request'].set_velocity_requested(getAvpData(self.conf['avps'], 'velocity-requested'))
            msg_list['request'].set_lcs_supported_gad_shapes(getAvpData(self.conf['avps'], 'lcs-supported-gad-shapes'))
            msg_list['request'].set_lcs_service_type_id(getAvpData(self.conf['avps'], 'lcs-service-type-id'))
            msg_list['request'].set_lcs_codeword(getAvpData(self.conf['avps'], 'lcs-codeword'))
            msg_list['request'].set_lcs_privacy_check_non_session(getAvpData(self.conf['avps'], 'lcs-privacy-check-non-session'))
            msg_list['request'].set_lcs_privacy_check_session(getAvpData(self.conf['avps'], 'lcs-privacy-check-session'))
            msg_list['request'].set_service_selection(getAvpData(self.conf['avps'], 'service-selection'))
            msg_list['request'].set_deferred_location_type(getAvpData(self.conf['avps'], 'deferred-location-type'))
            msg_list['request'].set_plr_flags(getAvpData(self.conf['avps'], 'plr-flags'))
            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))                                            
        
        if is_answer:
            msg_list['answer'] = DiamProvideLocationAnswer(
                                        self.appid, 
                                        generateSessionIDAVP(self.orig_host['value']),
                                        getAvpData(self.conf['avps'], 'auth-session-state'),
                                        self.orig_host,
                                        self.orig_realm
                                       )
                                                 
            msg_list['answer'].set_vendor_specific_application_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result'))
            msg_list['answer'].set_location_estimate(getAvpData(self.conf['avps'], 'location-estimate'))
            msg_list['answer'].set_accuracy_fulfilment_indicator(getAvpData(self.conf['avps'], 'accuracy-fulfilment-indicator'))
            msg_list['answer'].set_age_of_location_estimate(getAvpData(self.conf['avps'], 'age-of-location-estimate'))
            msg_list['answer'].set_velocity_estimate(getAvpData(self.conf['avps'], 'velocity-estimate'))
            msg_list['answer'].set_eutran_positioning_data(getAvpData(self.conf['avps'], 'eutran-positioning-data'))
            msg_list['answer'].set_ecgi(getAvpData(self.conf['avps'], 'ecgi'))
            msg_list['answer'].set_geran_positioning_info(getAvpData(self.conf['avps'], 'geran-positioning-info'))
            msg_list['answer'].set_cell_global_identity(getAvpData(self.conf['avps'], 'cell-global-identity'))
            msg_list['answer'].set_utran_positioning_info(getAvpData(self.conf['avps'], 'utran-positioning-info'))
            msg_list['answer'].set_service_area_identity(getAvpData(self.conf['avps'], 'service-area-identity'))
            msg_list['answer'].set_serving_node(getAvpData(self.conf['avps'], 'serving-node'))
            msg_list['answer'].set_pla_flags(getAvpData(self.conf['avps'], 'pla-flags'))
            msg_list['answer'].set_esmlc_cell_info(getAvpData(self.conf['avps'], 'esmlc-cell-info'))
            msg_list['answer'].set_civic_address(getAvpData(self.conf['avps'], 'civic-address'))
            msg_list['answer'].set_barometric_pressure(getAvpData(self.conf['avps'], 'barometric-pressure'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))   
                
        return msg_list
     
    def __generateLocationReportMessages(self, is_request, is_answer):
        msg_list = {}  
        
        if is_request:
            if self.dest_realm is None:
                checkAvpValue(self.conf['avps'], 'destination-realm')
                self.dest_realm = getAvpData(self.conf['avps'], 'destination-realm')
            if self.dest_host is None:
                checkAvpValue(self.conf['avps'], 'destination-host')
                self.dest_host = getAvpData(self.conf['avps'], 'destination-host')
                
            checkAvpValue(self.conf['avps'], 'location-event')
            
            msg_list['request'] = DiamLocationReportRequest(
                                         self.appid, 
                                         generateSessionIDAVP(self.orig_host['value']),
                                         getAvpData(self.conf['avps'], 'auth-session-state'),
                                         self.orig_host,
                                         self.orig_realm,
                                         self.dest_host,
                                         self.dest_realm,
                                         getAvpData(self.conf['avps'], 'location-event')
                                        ) 
            
            msg_list['request'].set_vendor_specific_application_id(getAvpData(self.conf['avps'],'vendor-specific-application-id'))
            msg_list['request'].set_lcs_eps_client_name(getAvpData(self.conf['avps'],'lcs-eps-client-name'))
            msg_list['request'].set_user_name(getAvpData(self.conf['avps'],'user-name'))
            msg_list['request'].set_msisdn(getAvpData(self.conf['avps'],'msisdn'))
            msg_list['request'].set_imei(getAvpData(self.conf['avps'],'imei'))
            msg_list['request'].set_location_estimate(getAvpData(self.conf['avps'],'location-estimate'))
            msg_list['request'].set_accuracy_fulfilment_indicator(getAvpData(self.conf['avps'],'accuracy-fulfilment-indicator'))
            msg_list['request'].set_age_of_location_estimate(getAvpData(self.conf['avps'],'age-of-location-estimate'))
            msg_list['request'].set_velocity_estimate(getAvpData(self.conf['avps'],'velocity-estimate'))
            msg_list['request'].set_eutran_positioning_data(getAvpData(self.conf['avps'],'eutran-positioning-data'))
            msg_list['request'].set_ecgi(getAvpData(self.conf['avps'],'ecgi'))
            msg_list['request'].set_geran_positioning_info(getAvpData(self.conf['avps'],'geran-positioning-info'))
            msg_list['request'].set_cell_global_identity(getAvpData(self.conf['avps'],'cell-global-identity'))
            msg_list['request'].set_utran_positioning_info(getAvpData(self.conf['avps'],'utran-positioning-info'))
            msg_list['request'].set_service_area_identity(getAvpData(self.conf['avps'],'service-area-identity'))
            msg_list['request'].set_lcs_service_type_id(getAvpData(self.conf['avps'],'lcs-service-type-id'))
            msg_list['request'].set_pseudonym_indicator(getAvpData(self.conf['avps'],'pseudonym-indicator'))
            msg_list['request'].set_lcs_qos_class(getAvpData(self.conf['avps'],'lcs-qos-class'))
            msg_list['request'].set_serving_node(getAvpData(self.conf['avps'],'serving-node'))
            msg_list['request'].set_lrr_flags(getAvpData(self.conf['avps'],'lrr-flags'))
            msg_list['request'].set_lcs_reference_number(getAvpData(self.conf['avps'],'lcs-reference-number'))
            msg_list['request'].set_deferred_mt_lr_data(getAvpData(self.conf['avps'],'deferred-mt-lr-data'))
            msg_list['request'].set_gmlc_address(getAvpData(self.conf['avps'],'gmlc-address'))
            msg_list['request'].set_reporting_amount(getAvpData(self.conf['avps'],'reporting-amount'))
            msg_list['request'].set_periodic_ldr_information(getAvpData(self.conf['avps'],'periodic-ldr-information'))
            msg_list['request'].set_esmlc_cell_info(getAvpData(self.conf['avps'],'esmlc-cell-info'))
            msg_list['request'].set_xrtt_rcid_1(getAvpData(self.conf['avps'],'xrtt-rcid-1'))
            msg_list['request'].set_civic_address(getAvpData(self.conf['avps'],'civic-address'))
            msg_list['request'].set_barometric_pressure(getAvpData(self.conf['avps'],'barometric-pressure'))
            msg_list['request'].set_supported_features(getAvpData(self.conf['avps'],'supported-features'))
            msg_list['request'].set_proxy_info(getAvpData(self.conf['avps'],'proxy-info'))
            msg_list['request'].set_route_record(getAvpData(self.conf['avps'],'route-record'))                                            
        
        if is_answer:
            msg_list['answer'] = DiamLocationReportAnswer(
                                        self.appid, 
                                        generateSessionIDAVP(self.orig_host['value']),
                                        getAvpData(self.conf['avps'], 'auth-session-state'),
                                        self.orig_host,
                                        self.orig_realm
                                       )
                                                 
            msg_list['answer'].set_vendor_specific_application_id(getAvpData(self.conf['avps'], 'vendor-specific-application-id'))
            msg_list['answer'].set_result_code(getAvpData(self.conf['avps'], 'result-code'))
            msg_list['answer'].set_experimental_result(getAvpData(self.conf['avps'], 'experimental-result'))
            msg_list['answer'].set_gmlc_address(getAvpData(self.conf['avps'], 'gmlc-address'))
            msg_list['answer'].set_lra_flags(getAvpData(self.conf['avps'], 'lra-flags'))
            msg_list['answer'].set_reporting_plmn_list(getAvpData(self.conf['avps'], 'reporting-plmn-list'))
            msg_list['answer'].set_lcs_reference_number(getAvpData(self.conf['avps'], 'lcs-reference-number'))
            msg_list['answer'].set_supported_features(getAvpData(self.conf['avps'], 'supported-features'))
            msg_list['answer'].set_failed_avp(getAvpData(self.conf['avps'], 'failed-avp'))
            msg_list['answer'].set_proxy_info(getAvpData(self.conf['avps'], 'proxy-info'))
            msg_list['answer'].set_route_record(getAvpData(self.conf['avps'], 'route-record'))  
                
        return msg_list

    def generateMessages(self):
        msgs_list = []
        
        for e in self.conf['3gpp_messages_list']:
            m = self.__generateMessage(e['cmd_code'], e['has_request'], e['has_answer'])
            if len(m) > 0 :
                for val in m.values():
                    msgs_list.append(val)
        
        return msgs_list
    