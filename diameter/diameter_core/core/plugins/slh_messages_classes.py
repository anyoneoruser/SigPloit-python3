from ..diameter.diameter_message import DiamMessage
from ..diameter.diam_avp_data import *
from ..diameter.diamCommandCodes import DiamCommandCodes

##
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##

''' >>> SLh INTERFACE <<< '''

''' 3GPP: LCS ROUTING INFO '''
##
## @brief      Class that defines a DIAMETER Message 
##
##         < LCS-Routing-Info-Request> ::= < Diameter Header: 8388622, REQ, PXY, 16777291 >
##                            < Session-Id >
##                            [ Vendor-Specific-Application-Id ]
##                            { Auth-Session-State }
##                            { Origin-Host }
##                            { Origin-Realm }
##                            [ Destination-Host ]
##                            { Destination-Realm }
##                            [ User-Name ]
##                            [ MSISDN ]
##                            [ GMLC-Number ]
##                            *[ Supported-Features ]
##                            *[ Proxy-Info ]
##                            *[ Route-Record ] 
##
class DiamLCSRoutingInfoRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 destination_realm,
                 vendor_specific_app_id=None,
                 destination_host=None,
                 user_name=None,
                 msisdn=None,
                 gmlc_number=None,
                 supported_features=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.LCS_ROUTING_INFO, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.destination_realm = destination_realm
        self.vendor_specific_app_id = vendor_specific_app_id
        self.destination_host = destination_host
        self.user_name = user_name
        self.msisdn = msisdn,
        self.gmlc_number = gmlc_number,
        self.supported_features = supported_features,
        self.proxy_info = proxy_info
        self.route_record = route_record
        
        self.setRequestFlag(True)
        self.setProxiableFlag(True)

    def get_session_id(self):
        return self.session_id

    def get_origin_host(self):
        return self.origin_host

    def get_origin_realm(self):
        return self.origin_realm

    def get_destination_realm(self):
        return self.destination_realm

    def get_auth_session_state(self):
        return self.auth_session_state

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_destination_host(self):
        return self.destination_host

    def get_user_name(self):
        return self.user_name
        
    def get_msisdn(self):
        return self.msisdn
        
    def get_gmlc_number(self):
        return self.gmlc_number
        
    def get_supported_features(self):
        return self.supported_features

    def get_proxy_info(self):
        return self.proxy_info

    def get_route_record(self):
        return self.route_record

    def set_session_id(self, value):
        self.session_id = value

    def set_origin_host(self, value):
        self.origin_host = value

    def set_origin_realm(self, value):
        self.origin_realm = value

    def set_destination_realm(self, value):
        self.destination_realm = value

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_destination_host(self, value):
        self.destination_host = value

    def set_user_name(self, value):
        self.user_name = value
        
    def set_msisdn(self, value):
        self.msisdn = value
        
    def set_gmlc_number(self, value):
        self.gmlc_number = value
        
    def set_supported_features(self, value):
        self.supported_features = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        if self.session_id is None:
            raise MissingMandatoryAVPException('ECR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('ECR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('ECR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)

        if self.destination_realm is None:
            raise MissingMandatoryAVPException('ECR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('ECR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.vendor_specific_app_id is not None:
            if not isinstance(self.vendor_specific_app_id, list):
                self.vendor_specific_app_id = [self.vendor_specific_app_id]
                
            for vsid in self.vendor_specific_app_id:
                if vsid is not None:
                    if 'type' in vsid and vsid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.VENDOR_SPECIFIC_APPLICATION_ID, vsid['value'])
                    else:
                        topass = {'auth_app_id':None,
                                  'acct_app_id':None,
                                  'vendor_id':0}
                        
                        for vavp in vsid['avps']:
                            if vavp['name'] == 'auth-application-id':
                                topass['auth_app_id'] = vavp
                            if vavp['name'] == 'acct-application-id':
                                topass['acct_app_id'] = vavp
                            if vavp['name'] == 'vendor-id':
                                topass['vendor_id'] = vavp
                            
                        avp = VendorSpecificApplicationIDAVP(topass['auth_app_id'], topass['acct_app_id'], topass['vendor_id'])
                        avp.setFlags(vsid['flags'])
                    self.addAVP(avp)
        
        if self.destination_host is not None:
            if 'type' in self.destination_host and self.destination_host['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.DESTINATION_HOST, self.destination_host['value'])
            else:
                avp = DestinationHostAVP(self.destination_host['value'])
                avp.setFlags(self.destination_host['flags'])
                if 'vendor' in self.destination_host:
                    avp.setVendorID(self.destination_host['vendor'])
            self.addAVP(avp)
        
        if self.user_name is not None:
            if 'type' in self.user_name and self.user_name['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.USER_NAME, self.user_name['value'])
            else:
                avp = UserNameAVP(self.user_name['value'])
                avp.setFlags(self.user_name['flags'])
                if 'vendor' in self.user_name:
                    avp.setVendorID(self.user_name['vendor'])
            self.addAVP(avp)
        
        if self.msisdn is not None:
            if 'type' in self.msisdn and self.msisdn['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.MSISDN, self.msisdn['value'])
            else:
                avp = MSISDNAVP(self.msisdn['value'])
                avp.setFlags(self.msisdn['flags'])
                if 'vendor' in self.msisdn:
                    avp.setVendorID(self.msisdn['vendor'])
            self.addAVP(avp)
        
        if self.gmlc_number is not None:
            if 'type' in self.get_gmlc_number and self.get_gmlc_number['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.GMLC_NUMBER, self.get_gmlc_number['value'])
            else:
                avp = GMLCNumberAVP(self.get_gmlc_number['value'])
                avp.setFlags(self.get_gmlc_number['flags'])
                if 'vendor' in self.get_gmlc_number:
                    avp.setVendorID(self.get_gmlc_number['vendor'])
            self.addAVP(avp)
        
        if self.supported_features is not None:
            if not isinstance(self.supported_features, list):
                self.supported_features = [self.supported_features]
                
            for sf in self.supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.SUPPORTED_FEATURES, sf['value'])
                    else:
                        topass = {'feature_list_id':None,
                                  'feature_list':None,
                                  'vendor_id':0}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'feature-list-id':
                                topass['feature_list_id'] = savp
                            if savp['name'] == 'feature-list':
                                topass['feature_list'] = savp
                            if savp['name'] == 'vendor-id':
                                topass['vendor_id'] = savp
                                
                        avp = SupportedFeaturesAVP(topass['vendor_id'], topass['feature_list_id'], topass['feature_list'])
                        avp.setFlags(sf['flags'])
                    self.addAVP(avp)
                 
        if self.proxy_info is not None:
            if not isinstance(self.proxy_info, list):
                self.proxy_info = [self.proxy_info]
                
            for pi in self.proxy_info:
                if pi is not None:
                    if 'type' in pi and pi['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.PROXY_INFO, pi['value'])
                    else:
                        topass = {'proxy_host':None,
                                  'proxy_state':None,
                                  'vendor_id':0}
                        
                        for pavp in pi['avps']:
                            if pavp['name'] == 'proxy-host':
                                topass['proxy_host'] = pavp
                            if pavp['name'] == 'proxy-state':
                                topass['proxy_state'] = pavp
                            if pavp['name'] == 'vendor-id':
                                topass['vendor_id'] = pavp
                            
                        avp = ProxyInfoAVP(topass['proxy_host'], topass['proxy_state'], topass['vendor_id'])
                        avp.setFlags(pi['flags'])
                    self.addAVP(avp)
            
        if self.route_record is not None:
            if not isinstance(self.route_record, list):
                self.route_record = [self.route_record]
                
            for rr in self.route_record:
                if rr is not None:
                    if 'type' in rr and rr['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, rr['value'])
                    else:
                        avp = RouteRecordAVP(rr['value'])
                        avp.setFlags(rr['flags'])
                        if 'vendor_id' in rr:
                            avp.setVendorID(rr['vendor'])
                    self.addAVP(avp)

##
## @brief      Class that defines a DIAMETER Message 
##
##         < LCS-Routing-Info-Answer> ::= < Diameter Header: 8388622, PXY, 16777291 >
##                                < Session-Id >
##                                [ Vendor-Specific-Application-Id ]
##                                [ Result-Code ] 
##                                [ Experimental-Result ]
##                                { Auth-Session-State }
##                                { Origin-Host }
##                                { Origin-Realm }
##                                *[ Supported-Features ]
##                                [ User-Name ]
##                                [ MSISDN ]
##                                [ LMSI ]
##                                [ Serving-Node ]
##                                *[ Additional-Serving-Node ]
##                                [ GMLC-Address ]
##                                [ PPR-Address ]
##                                [ RIA-Flags ]
##                                *[ Failed-AVP ]
##                                *[ Proxy-Info ]
##                                *[ Route-Record ] 
##
class DiamLCSRoutingInfoAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 vendor_specific_app_id=None,
                 result_code=None,
                 experimental_result=None,
                 supported_features=None,
                 user_name=None,
                 msisdn=None,
                 lmsi=None,
                 serving_node=None,
                 additional_serving_node=None,
                 gmlc_address=None,
                 ppr_address=None,
                 ria_flags=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.ME_IDENTITY_CHECK_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.auth_session_state = auth_session_state
        self.vendor_specific_app_id = vendor_specific_app_id
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.supported_features = supported_features
        self.user_name = user_name
        self.msisdn = msisdn
        self.lmsi = lmsi
        self.serving_node = serving_node
        self.additional_serving_node = additional_serving_node
        self.gmlc_address = gmlc_address
        self.ppr_address = ppr_address
        self.ria_flags = ria_flags
        self.failed_avp = failed_avp
        self.proxy_info = proxy_info
        self.route_record = route_record
        
        self.setProxiableFlag(True)

    def get_session_id(self):
        return self.session_id

    def get_origin_host(self):
        return self.origin_host

    def get_origin_realm(self):
        return self.origin_realm

    def get_auth_session_state(self):
        return self.auth_session_state

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_result_code(self):
        return self.result_code

    def get_experimental_result(self):
        return self.experimental_result

    def get_supported_features(self):
        return self.supported_features
    
    def get_user_name(self):
        return self.user_name
    
    def get_msisdn(self):
        return self.msisdn
    
    def get_lmsi(self):
        return self.lmsi
    
    def get_serving_node(self):
        return self.serving_node
    
    def get_additional_serving_node(self):
        return self.additional_serving_node
    
    def get_gmlc_address(self):
        return self.gmlc_address
    
    def get_ppr_address(self):
        return self.ppr_address
    
    def get_ria_flags(self):
        return self.ria_flags

    def get_failed_avp(self):
        return self.failed_avp

    def get_proxy_info(self):
        return self.proxy_info

    def get_route_record(self):
        return self.route_record

    def set_session_id(self, value):
        self.session_id = value

    def set_origin_host(self, value):
        self.origin_host = value

    def set_origin_realm(self, value):
        self.origin_realm = value

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_result_code(self, value):
        self.result_code = value

    def set_experimental_result(self, value):
        self.experimental_result = value

    def set_supported_features(self, value):
        self.supported_features = value
    
    def set_user_name(self, value):
        self.user_name = value
    
    def set_msisdn(self, value):
        self.msisdn = value
    
    def set_lmsi(self, value):
        self.lmsi = value
    
    def set_serving_node(self, value):
        self.serving_node = value
    
    def set_additional_serving_node(self, value):
        self.additional_serving_node = value
    
    def set_gmlc_address(self, value):
        self.gmlc_address = value
    
    def set_ppr_address(self, value):
        self.ppr_address = value
    
    def set_ria_flags(self, value):
        self.ria_flags = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        if self.session_id is None:
            raise MissingMandatoryAVPException('ECA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('ECA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('ECA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)

        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('ECA: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.vendor_specific_app_id is not None:
            if not isinstance(self.vendor_specific_app_id, list):
                self.vendor_specific_app_id = [self.vendor_specific_app_id]
                
            for vsid in self.vendor_specific_app_id:
                if vsid is not None:
                    if 'type' in vsid and vsid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.VENDOR_SPECIFIC_APPLICATION_ID, vsid['value'])
                    else:
                        topass = {'auth_app_id':None,
                                  'acct_app_id':None,
                                  'vendor_id':0}
                        
                        for vavp in vsid['avps']:
                            if vavp['name'] == 'auth-application-id':
                                topass['auth_app_id'] = vavp
                            if vavp['name'] == 'acct-application-id':
                                topass['acct_app_id'] = vavp
                            if vavp['name'] == 'vendor-id':
                                topass['vendor_id'] = vavp
                            
                        avp = VendorSpecificApplicationIDAVP(topass['auth_app_id'], topass['acct_app_id'], topass['vendor_id'])
                        avp.setFlags(vsid['flags'])
                    self.addAVP(avp)
        
        if self.result_code is not None:
            if 'type' in self.result_code and self.result_code['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.RESULT_CODE, self.result_code['value'])
            else:
                avp = ResultCodeAVP(self.result_code['value'])
                avp.setFlags(self.result_code['flags'])
                if 'vendor' in self.result_code:
                    avp.setVendorID(self.result_code['vendor'])
            self.addAVP(avp)
            
        if self.experimental_result is not None:
            if 'type' in self.experimental_result and self.experimental_result['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.EXPERIMENTAL_RESULT, self.experimental_result['value'])
            else:
                avp = ExperimentalResultAVP(self.experimental_result['value'])
                avp.setFlags(self.experimental_result['flags'])
                if 'vendor' in self.experimental_result:
                    avp.setVendorID(self.experimental_result['vendor'])
            self.addAVP(avp)
        
        if self.user_name is None:
            raise MissingMandatoryAVPException('CLR: The User-Name AVP is MANDATORY')
        avp = UserNameAVP(self.user_name['value'])
        avp.setFlags(self.user_name['flags'])
        if 'vendor' in self.user_name:
            avp.setVendorID(self.user_name['vendor'])
        self.addAVP(avp)
                
        if self.supported_features is not None:
            if not isinstance(self.supported_features, list):
                self.supported_features = [self.supported_features]
                
            for sf in self.supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.SUPPORTED_FEATURES, sf['value'])
                    else:
                        topass = {'feature_list_id':None,
                                  'feature_list':None,
                                  'vendor_id':0}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'feature-list-id':
                                topass['feature_list_id'] = savp
                            if savp['name'] == 'feature-list':
                                topass['feature_list'] = savp
                            if savp['name'] == 'vendor-id':
                                topass['vendor_id'] = savp
                                
                        avp = SupportedFeaturesAVP(topass['vendor_id'], topass['feature_list_id'], topass['feature_list'])
                        avp.setFlags(sf['flags'])
                    self.addAVP(avp)
        
        if self.msisdn is not None:
            if 'type' in self.msisdn and self.msisdn['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.MSISDN, self.msisdn['value'])
            else:
                avp = MSISDNAVP(self.msisdn['value'])
                avp.setFlags(self.msisdn['flags'])
                if 'vendor' in self.msisdn:
                    avp.setVendorID(self.msisdn['vendor'])
            self.addAVP(avp)
        
        if self.lmsi is not None:
            if 'type' in self.lmsi and self.lmsi['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LMSI, self.lmsi['value'])
            else:
                avp = LMSIAVP(self.lmsi['value'])
                avp.setFlags(self.lmsi['flags'])
                if 'vendor' in self.lmsi:
                    avp.setVendorID(self.lmsi['vendor'])
            self.addAVP(avp)

        if self.serving_node is not None:
            if not isinstance(self.serving_node, list):
                self.serving_node = [self.serving_node]

            for el in self.serving_node:
                if el is not None:
                    if 'type' in el and el['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.SERVING_NODE, el['value'])
                    else:
                        topass = {'sgsn_number':None,
                                  'sgsn_name':None,
                                  'sgsn_realm':None,
                                  'mme_name':None,
                                  'mme_realm':None,
                                  'msc_number':None,
                                  'gpp3_aaa_server_name':None,
                                  'lcs_capabilities_sets':None,
                                  'gmlc_address':None,
                                  'vendor_id':0}

                        for vavp in el['avps']:
                            if vavp['name'] == 'sgsn_number':
                                topass['sgsn_number'] = vavp
                            if vavp['name'] == 'sgsn_name':
                                topass['sgsn_name'] = vavp
                            if vavp['name'] == 'sgsn_realm':
                                topass['sgsn_realm'] = vavp
                            if vavp['name'] == 'mme_name':
                                topass['mme_name'] = vavp
                            if vavp['name'] == 'mme_realm':
                                topass['mme_realm'] = vavp
                            if vavp['name'] == 'msc_number':
                                topass['msc_number'] = vavp
                            if vavp['name'] == 'gpp3_aaa_server_name':
                                topass['gpp3_aaa_server_name'] = vavp
                            if vavp['name'] == 'lcs_capabilities_sets':
                                topass['lcs_capabilities_sets'] = vavp
                            if vavp['name'] == 'gmlc_address':
                                topass['gmlc_address'] = vavp
                            if vavp['name'] == 'vendor-id':
                                topass['vendor_id'] = vavp

                        avp = ServingNodeAVP(topass['sgsn_number'], topass['sgsn_name'], topass['sgsn_realm'], topass['mme_name'], topass['mme_realm'], topass['msc_number'], topass['gpp3_aaa_server_name'], topass['lcs_capabilities_sets'], topass['gmlc_address'], topass['vendor_id'])
                        avp.setFlags(el['flags'])
                    self.addAVP(avp)

        if self.additional_serving_node is not None:
            if not isinstance(self.additional_serving_node, list):
                self.additional_serving_node = [self.additional_serving_node]

            for el in self.additional_serving_node:
                if el is not None:
                    if 'type' in el and el['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.ADDITIONAL_SERVING_NODE, el['value'])
                    else:
                        topass = {'sgsn_number':None,
                                  'sgsn_name':None,
                                  'sgsn_realm':None,
                                  'mme_name':None,
                                  'mme_realm':None,
                                  'msc_number':None,
                                  'gpp3_aaa_server_name':None,
                                  'lcs_capabilities_sets':None,
                                  'gmlc_address':None,
                                  'vendor_id':0}

                        for vavp in el['avps']:
                            if vavp['name'] == 'sgsn_number':
                                topass['sgsn_number'] = vavp
                            if vavp['name'] == 'sgsn_name':
                                topass['sgsn_name'] = vavp
                            if vavp['name'] == 'sgsn_realm':
                                topass['sgsn_realm'] = vavp
                            if vavp['name'] == 'mme_name':
                                topass['mme_name'] = vavp
                            if vavp['name'] == 'mme_realm':
                                topass['mme_realm'] = vavp
                            if vavp['name'] == 'msc_number':
                                topass['msc_number'] = vavp
                            if vavp['name'] == 'gpp3_aaa_server_name':
                                topass['gpp3_aaa_server_name'] = vavp
                            if vavp['name'] == 'lcs_capabilities_sets':
                                topass['lcs_capabilities_sets'] = vavp
                            if vavp['name'] == 'gmlc_address':
                                topass['gmlc_address'] = vavp
                            if vavp['name'] == 'vendor-id':
                                topass['vendor_id'] = vavp

                        avp = AdditionalServingNodeAVP(topass['sgsn_number'], topass['sgsn_name'], topass['sgsn_realm'], topass['mme_name'], topass['mme_realm'], topass['msc_number'], topass['gpp3_aaa_server_name'], topass['lcs_capabilities_sets'], topass['gmlc_address'], topass['vendor_id'])
                        avp.setFlags(el['flags'])
                    self.addAVP(avp)
        
        if self.gmlc_address is not None:
            if 'type' in self.gmlc_address and self.gmlc_address['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.GMLC_ADDRESS, self.gmlc_address['value'])
            else:
                avp = GMLCAddressAVP(self.gmlc_address['value'])
                avp.setFlags(self.gmlc_address['flags'])
                if 'vendor' in self.gmlc_address:
                    avp.setVendorID(self.gmlc_address['vendor'])
            self.addAVP(avp)
        
        if self.ppr_address is not None:
            if 'type' in self.ppr_address and self.ppr_address['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.PPR_ADDRESS, self.ppr_address['value'])
            else:
                avp = PPRAddressAVP(self.ppr_address['value'])
                avp.setFlags(self.ppr_address['flags'])
                if 'vendor' in self.ppr_address:
                    avp.setVendorID(self.ppr_address['vendor'])
            self.addAVP(avp)
            
        if self.ria_flags is not None:
            if 'type' in self.ria_flags and self.ria_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.RIA_FLAGS, self.ria_flags['value'])
            else:
                avp = RIAFlagsAVP(self.ria_flags['value'])
                avp.setFlags(self.ria_flags['flags'])
                if 'vendor' in self.ria_flags:
                    avp.setVendorID(self.ria_flags['vendor'])
            self.addAVP(avp)

        if self.failed_avp is not None:
            if not isinstance(self.failed_avp, list):
                self.failed_avp = [self.failed_avp]
                
            for fa in self.failed_avp:
                if fa is not None:
                    if 'type' in fa and fa['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.FAILED_AVP, fa['value'])
                    else:
                        avp = FailedAVP(fa['value'])
                        avp.setFlags(fa['flags'])
                        if 'vendor_id' in fa:
                            avp.setVendorID(fa['vendor'])
                    self.addAVP(avp)
                 
        if self.proxy_info is not None:
            if not isinstance(self.proxy_info, list):
                self.proxy_info = [self.proxy_info]
                
            for pi in self.proxy_info:
                if pi is not None:
                    if 'type' in pi and pi['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.PROXY_INFO, pi['value'])
                    else:
                        topass = {'proxy_host':None,
                                  'proxy_state':None,
                                  'vendor_id':0}
                        
                        for pavp in pi['avps']:
                            if pavp['name'] == 'proxy-host':
                                topass['proxy_host'] = pavp
                            if pavp['name'] == 'proxy-state':
                                topass['proxy_state'] = pavp
                            if pavp['name'] == 'vendor-id':
                                topass['vendor_id'] = pavp
                            
                        avp = ProxyInfoAVP(topass['proxy_host'], topass['proxy_state'], topass['vendor_id'])
                        avp.setFlags(pi['flags'])
                    self.addAVP(avp)
            
        if self.route_record is not None:
            if not isinstance(self.route_record, list):
                self.route_record = [self.route_record]
                
            for rr in self.route_record:
                if rr is not None:
                    if 'type' in rr and rr['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, rr['value'])
                    else:
                        avp = RouteRecordAVP(rr['value'])
                        avp.setFlags(rr['flags'])
                        if 'vendor_id' in rr:
                            avp.setVendorID(rr['vendor'])
                    self.addAVP(avp)
''' /3GPP: LCS ROUTING INFO '''
