from ..diameter.diameter_message import DiamMessage
from ..diameter.diam_avp_data import *
from ..diameter.diamCommandCodes import DiamCommandCodes

##
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##

''' >>> SLg INTERFACE <<< '''

''' 3GPP: PROVIDE LOCATION '''
##
## @brief      Class that defines a DIAMETER Message 
##  
##        < Provide-Location-Request> ::= < Diameter Header: 8388620, REQ, PXY, 16777255 >
##                                < Session-Id >
##                                [ Vendor-Specific-Application-Id ]
##                                { Auth-Session-State }
##                                { Origin-Host }
##                                { Origin-Realm }
##                                {Destination-Host }
##                                { Destination-Realm }
##                                { SLg-Location-Type }
##                                [ User-Name ]
##                                [ MSISDN]
##                                [ IMEI ]
##                                { LCS-EPS-Client-Name }
##                                { LCS-Client-Type }
##                                [ LCS-Requestor-Name ]
##                                [ LCS-Priority ]
##                                [ LCS-QoS ]
##                                [ Velocity-Requested ]
##                                [LCS-Supported-GAD-Shapes ]
##                                [ LCS-Service-Type-ID ]
##                                [ LCS-Codeword ]
##                                [ LCS-Privacy-Check-Non-Session ]
##                                [ LCS-Privacy-Check-Session ]
##                                [Service-Selection ]
##                                [ Deferred-Location-Type ]
##                                [ PLR-Flags ]
##                                *[ Supported-Features ]
##                                *[ Proxy-Info ]
##                                *[ Route-Record ]
##
class DiamProvideLocationRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 destination_host,
                 destination_realm,
                 slg_location_type,
                 lcs_eps_client_name,
                 lcs_client_type,
                 vendor_specific_application_id=None,
                 user_name=None,
                 msisdn=None,
                 imei=None,
                 lcs_requestor_name=None,
                 lcs_priority=None,
                 lcs_qos=None,
                 velocity_requested=None,
                 lcs_supported_gad_shapes=None,
                 lcs_service_type_id=None,
                 lcs_codeword=None,
                 lcs_privacy_check_non_session=None,
                 lcs_privacy_check_session=None,
                 service_selection=None,
                 deferred_location_type=None,
                 plr_flags=None,
                 supported_features=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.PROVIDE_LOCATION, app_id)

        self.session_id = session_id
        self.auth_session_state = auth_session_state
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_host = destination_host
        self.destination_realm = destination_realm
        self.slg_location_type = slg_location_type
        self.lcs_eps_client_name = lcs_eps_client_name
        self.lcs_client_type = lcs_client_type
        self.vendor_specific_application_id = vendor_specific_application_id
        self.user_name = user_name
        self.msisdn = msisdn
        self.imei = imei
        self.lcs_requestor_name = lcs_requestor_name
        self.lcs_priority = lcs_priority
        self.lcs_qos = lcs_qos
        self.velocity_requested = velocity_requested
        self.lcs_supported_gad_shapes = lcs_supported_gad_shapes
        self.lcs_service_type_id = lcs_service_type_id
        self.lcs_codeword = lcs_codeword
        self.lcs_privacy_check_non_session = lcs_privacy_check_non_session
        self.lcs_privacy_check_session = lcs_privacy_check_session
        self.service_selection = service_selection
        self.deferred_location_type = deferred_location_type
        self.plr_flags = plr_flags
        self.supported_features = supported_features
        self.proxy_info = proxy_info
        self.route_record = route_record
        
        self.setRequestFlag(True)
        self.setProxiableFlag(True)

    def get_auth_session_state(self):
        return self.auth_session_state
    
    def get_origin_host(self):
        return self.origin_host
    
    def get_origin_realm(self):
        return self.origin_realm
    
    def get_destination_host(self):
        return self.destination_host
    
    def get_destination_realm(self):
        return self.destination_realm
    
    def get_slg_location_type(self):
        return self.slg_location_type
    
    def get_lcs_eps_client_name(self):
        return self.lcs_eps_client_name
    
    def get_lcs_client_type(self):
        return self.lcs_client_type
    
    def get_vendor_specific_application_id(self):
        return self.vendor_specific_application_id
    
    def get_user_name(self):
        return self.user_name
    
    def get_msisdn(self):
        return self.msisdn
    
    def get_imei(self):
        return self.imei
    
    def get_lcs_requestor_name(self):
        return self.lcs_requestor_name
    
    def get_lcs_priority(self):
        return self.lcs_priority
    
    def get_lcs_qos(self):
        return self.lcs_qos
    
    def get_velocity_requested(self):
        return self.velocity_requested
    
    def get_lcs_supported_gad_shapes(self):
        return self.lcs_supported_gad_shapes
    
    def get_lcs_service_type_id(self):
        return self.lcs_service_type_id
    
    def get_lcs_codeword(self):
        return self.lcs_codeword
    
    def get_lcs_privacy_check_non_session(self):
        return self.lcs_privacy_check_non_session
    
    def get_lcs_privacy_check_session(self):
        return self.lcs_privacy_check_session
    
    def get_service_selection(self):
        return self.service_selection
    
    def get_deferred_location_type(self):
        return self.deferred_location_type
    
    def get_plr_flags(self):
        return self.plr_flags
    
    def get_supported_features(self):
        return self.supported_features
    
    def get_proxy_info(self):
        return self.proxy_info
    
    def get_route_record(self):
        return self.route_record
    
    def set_auth_session_state(self, value):
        self.auth_session_state = value
    
    def set_origin_host(self, value):
        self.origin_host = value
    
    def set_origin_realm(self, value):
        self.origin_realm = value
    
    def set_destination_host(self, value):
        self.destination_host = value
    
    def set_destination_realm(self, value):
        self.destination_realm = value
    
    def set_slg_location_type(self, value):
        self.slg_location_type = value
    
    def set_lcs_eps_client_name(self, value):
        self.lcs_eps_client_name = value
    
    def set_lcs_client_type(self, value):
        self.lcs_client_type = value
    
    def set_vendor_specific_application_id(self, value):
        self.vendor_specific_application_id = value
    
    def set_user_name(self, value):
        self.user_name = value
    
    def set_msisdn(self, value):
        self.msisdn = value
    
    def set_imei(self, value):
        self.imei = value
    
    def set_lcs_requestor_name(self, value):
        self.lcs_requestor_name = value
    
    def set_lcs_priority(self, value):
        self.lcs_priority = value
    
    def set_lcs_qos(self, value):
        self.lcs_qos = value
    
    def set_velocity_requested(self, value):
        self.velocity_requested = value
    
    def set_lcs_supported_gad_shapes(self, value):
        self.lcs_supported_gad_shapes = value
    
    def set_lcs_service_type_id(self, value):
        self.lcs_service_type_id = value
    
    def set_lcs_codeword(self, value):
        self.lcs_codeword = value
    
    def set_lcs_privacy_check_non_session(self, value):
        self.lcs_privacy_check_non_session = value
    
    def set_lcs_privacy_check_session(self, value):
        self.lcs_privacy_check_session = value
    
    def set_service_selection(self, value):
        self.service_selection = value
    
    def set_deferred_location_type(self, value):
        self.deferred_location_type = value
    
    def set_plr_flags(self, value):
        self.plr_flags = value
    
    def set_supported_features(self, value):
        self.supported_features = value
    
    def set_proxy_info(self, value):
        self.proxy_info = value
    
    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        if self.session_id is None:
            raise MissingMandatoryAVPException('PLR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('PLR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(self.auth_session_state['value'])
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('PLR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('PLR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.destination_host is None:
            raise MissingMandatoryAVPException('PLR: The Destination-Host AVP is MANDATORY')
        avp = DestinationHostAVP(self.destination_host['value'])
        avp.setFlags(self.destination_host['flags'])
        if 'vendor' in self.destination_host:
            avp.setVendorID(self.destination_host['vendor'])
        self.addAVP(avp)

        if self.destination_realm is None:
            raise MissingMandatoryAVPException('PLR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)
        
        if self.slg_location_type is None:
            raise MissingMandatoryAVPException('PLR: The SLg-Location-Type AVP is MANDATORY')
        avp = SLgLocationTypeAVP(int(self.slg_location_type['value']))
        avp.setFlags(self.slg_location_type['flags'])
        if 'vendor' in self.slg_location_type:
            avp.setVendorID(self.slg_location_type['vendor'])
        self.addAVP(avp)
        
        if self.lcs_eps_client_name is None:
            raise MissingMandatoryAVPException('PLR: The LCS-EPS-Client-Name AVP is MANDATORY')
        if not isinstance(self.lcs_eps_client_name, list):
            self.lcs_eps_client_name = [self.lcs_eps_client_name]

        for el in self.lcs_eps_client_name:
            if el is not None:
                if 'type' in el and el['type']=='raw':
                    avp = GenericAVP(DiamAVPCodes.LCS_EPS_CLIENT_NAME, el['value'])
                else:
                    topass = {'lcs_name_string':None,
                              'lcs_format_indicator':None,
                              'vendor_id':0}

                    for vavp in el['avps']:
                        if vavp['name'] == 'lcs-name-string':
                            topass['lcs_name_string'] = vavp
                        if vavp['name'] == 'lcs-format-indicator':
                            topass['lcs_format_indicator'] = vavp
                        if vavp['name'] == 'vendor-id':
                            topass['vendor_id'] = vavp

                    avp = LCSEPSClientNameAVP(topass['lcs_name_string'], topass['lcs_format_indicator'], topass['vendor_id'])
                    avp.setFlags(el['flags'])
                self.addAVP(avp)
        
        if self.lcs_client_type is None:
            raise MissingMandatoryAVPException('PLR: The LCS-Client-Type AVP is MANDATORY')
        avp = LCSClientTypeAVP(int(self.lcs_client_type['value']))
        avp.setFlags(self.lcs_client_type['flags'])
        if 'vendor' in self.lcs_client_type:
            avp.setVendorID(self.lcs_client_type['vendor'])
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
        
        if self.imei is not None:
            if 'type' in self.imei and self.imei['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.IMEI, self.imei['value'])
            else:
                avp = IMEIAVP(self.imei['value'])
                avp.setFlags(self.imei['flags'])
                if 'vendor' in self.imei:
                    avp.setVendorID(self.imei['vendor'])
            self.addAVP(avp)
        
        if self.lcs_requestor_name is not None:
            if not isinstance(self.lcs_requestor_name, list):
                self.lcs_requestor_name = [self.lcs_requestor_name]
                
            for vsid in self.lcs_requestor_name:
                if vsid is not None:
                    if 'type' in vsid and vsid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.LCS_REQUESTOR_NAME, vsid['value'])
                    else:
                        topass = {'auth_app_id':None,
                                  'acct_app_id':None,
                                  'vendor_id':0}
                        
                        for vavp in vsid['avps']:
                            if vavp['name'] == 'lcs-requestor-id':
                                topass['lcs_req_id'] = vavp
                            if vavp['name'] == 'lcs-format-indicator':
                                topass['lcs_format_indicator'] = vavp
                            if vavp['name'] == 'vendor-id':
                                topass['vendor_id'] = vavp
                            
                        avp = LCSRequestorNameAVP(topass['lcs_req_id'], topass['lcs_format_indicator'], topass['vendor_id'])
                        avp.setFlags(vsid['flags'])
                    self.addAVP(avp)
        
        if self.lcs_priority is not None:
            if 'type' in self.lcs_priority and self.lcs_priority['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_PRIORITY, self.lcs_priority['value'])
            else:
                avp = LCSPriorityAVP(self.lcs_priority['value'])
                avp.setFlags(self.lcs_priority['flags'])
                if 'vendor' in self.lcs_priority:
                    avp.setVendorID(self.lcs_priority['vendor'])
            self.addAVP(avp)
        
        if self.lcs_qos is not None:
            if not isinstance(self.lcs_qos, list):
                self.lcs_qos = [self.lcs_qos]
                
            for qos in self.lcs_qos:
                if vsid is not None:
                    if 'type' in qos and qos['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.LCS_QOS, qos['value'])
                    else:
                        topass = {'lcs_qos_class':None,
                                  'horizontal_accuracy':None,
                                  'vertical_accuracy':None,
                                  'vertical_requested':None,
                                  'response_time':None,
                                  'vendor_id':0}
                        
                        for vavp in qos['avps']:
                            if vavp['name'] == 'lcs-qos-class':
                                topass['lcs_qos_class'] = vavp
                            if vavp['name'] == 'horizontal-accuracy':
                                topass['horizontal_accuracy'] = vavp
                            if vavp['name'] == 'vertical-accuracy':
                                topass['vertical_accuracy'] = vavp
                            if vavp['name'] == 'vertical-requested':
                                topass['vertical_requested'] = vavp
                            if vavp['name'] == 'response-time':
                                topass['response_time'] = vavp
                            if vavp['name'] == 'vendor-id':
                                topass['vendor_id'] = vavp
                            
                        avp = LCSQoSAVP(topass['lcs_qos_class'], topass['horizontal_accuracy'], topass['vertical_accuracy'], topass['vertical_requested'], topass['response_time'], topass['vendor_id'])
                        avp.setFlags(qos['flags'])
                    self.addAVP(avp)
        
        if self.velocity_requested is not None:
            if 'type' in self.velocity_requested and self.velocity_requested['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.VELOCITY_REQUESTED, self.velocity_requested['value'])
            else:
                avp = VelocityRequestedAVP(self.velocity_requested['value'])
                avp.setFlags(self.velocity_requested['flags'])
                if 'vendor' in self.velocity_requested:
                    avp.setVendorID(self.velocity_requested['vendor'])
            self.addAVP(avp)
        
        if self.lcs_supported_gad_shapes is not None: 
            if 'type' in self.lcs_supported_gad_shapes and self.lcs_supported_gad_shapes['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_SUPPORTED_GAD_SHAPES, self.lcs_supported_gad_shapes['value'])
            else:
                avp = LCSSupportedGADShapesAVP(self.lcs_supported_gad_shapes['value'])
                avp.setFlags(self.lcs_supported_gad_shapes['flags'])
                if 'vendor' in self.lcs_supported_gad_shapes:
                    avp.setVendorID(self.lcs_supported_gad_shapes['vendor'])
            self.addAVP(avp)
        
        if self.lcs_service_type_id is not None:
            if 'type' in self.lcs_service_type_id and self.lcs_service_type_id['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_SERVICE_TYPE, self.lcs_service_type_id['value'])
            else:
                avp = LCSServiceTypeIDAVP(self.lcs_service_type_id['value'])
                avp.setFlags(self.lcs_service_type_id['flags'])
                if 'vendor' in self.lcs_service_type_id:
                    avp.setVendorID(self.lcs_service_type_id['vendor'])
            self.addAVP(avp)
        
        if self.lcs_codeword is not None:
            if 'type' in self.lcs_codeword and self.lcs_codeword['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_CODEWORD, self.lcs_codeword['value'])
            else:
                avp = LCSCodewordAVP(self.lcs_codeword['value'])
                avp.setFlags(self.lcs_codeword['flags'])
                if 'vendor' in self.lcs_codeword:
                    avp.setVendorID(self.lcs_codeword['vendor'])
            self.addAVP(avp)
        
        if self.lcs_privacy_check_non_session is not None:
            if 'type' in self.lcs_privacy_check_non_session and self.lcs_privacy_check_non_session['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_PRIVACY_CHECK_NON_SESSION, self.lcs_privacy_check_non_session['value'])
            else:
                avp = LCSPrivacyCheckNonSessionAVP(self.lcs_privacy_check_non_session['value'])
                avp.setFlags(self.lcs_privacy_check_non_session['flags'])
                if 'vendor' in self.lcs_privacy_check_non_session:
                    avp.setVendorID(self.lcs_privacy_check_non_session['vendor'])
            self.addAVP(avp)
        
        if self.lcs_privacy_check_session is not None:
            if 'type' in self.lcs_privacy_check_session and self.lcs_privacy_check_session['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_PRIVACY_CHECK_SESSION, self.lcs_privacy_check_session['value'])
            else:
                avp = LCSPrivacyCheckSessionAVP(self.lcs_privacy_check_session['value'])
                avp.setFlags(self.lcs_privacy_check_session['flags'])
                if 'vendor' in self.lcs_privacy_check_session:
                    avp.setVendorID(self.lcs_privacy_check_session['vendor'])
            self.addAVP(avp)
        
        if self.service_selection is not None:
            if 'type' in self.service_selection and self.service_selection['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.SERVICE_SELECTION, self.service_selection['value'])
            else:
                avp = ServiceSelectionAVP(self.service_selection['value'])
                avp.setFlags(self.service_selection['flags'])
                if 'vendor' in self.service_selection:
                    avp.setVendorID(self.service_selection['vendor'])
            self.addAVP(avp)

        if self.deferred_location_type is not None:
            if 'type' in self.deferred_location_type and self.deferred_location_type['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.DEFERRED_LOCATION_TYPE, self.deferred_location_type['value'])
            else:
                avp = DeferredLocationTypeAVP(self.deferred_location_type['value'])
                avp.setFlags(self.deferred_location_type['flags'])
                if 'vendor' in self.deferred_location_type:
                    avp.setVendorID(self.deferred_location_type['vendor'])
            self.addAVP(avp)
        
        if self.plr_flags is not None:
            if 'type' in self.plr_flags and self.plr_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.PLR_FLAGS, self.plr_flags['value'])
            else:
                avp = PLRFlagsAVP(self.plr_flags['value'])
                avp.setFlags(self.plr_flags['flags'])
                if 'vendor' in self.plr_flags:
                    avp.setVendorID(self.plr_flags['vendor'])
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
##        < Provide-Location-Answer > ::= < Diameter Header: 8388620, PXY, 16777255 >
##                                < Session-Id >
##                                [ Vendor-Specific-Application-Id ]
##                                [ Result-Code ]
##                                [ Experimental-Result ]
##                                { Auth-Session-State }
##                                { Origin-Host }
##                                { Origin-Realm }
##                                [ Location-Estimate ]
##                                [ Accuracy-Fulfilment-Indicator ]
##                                [ Age-Of-Location-Estimate]
##                                [ Velocity-Estimate ]
##                                [ EUTRAN-Positioning-Data]
##                                [ ECGI ]
##                                [ GERAN-Positioning-Info ]
##                                [ Cell-Global-Identity ]
##                                [ UTRAN-Positioning-Info ]
##                                [ Service-Area-Identity ]
##                                [ Serving-Node ]
##                                [ PLA-Flags ]
##                                [ ESMLC-Cell-Info ]
##                                [ Civic-Address ]
##                                [ Barometric-Pressure ]
##                                *[ Supported-Features ]
##                                *[ Failed-AVP ]
##                                *[ Proxy-Info ]
##                                *[ Route-Record ]
##
class DiamProvideLocationAnswer(DiamMessage):    
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 vendor_specific_application_id=None,
                 result_code=None,
                 experimental_result=None,
                 location_estimate=None,
                 accuracy_fulfilment_indicator=None,
                 age_of_location_estimate=None,
                 velocity_estimate=None,
                 eutran_positioning_data=None,
                 ecgi=None,
                 geran_positioning_info=None,
                 cell_global_identity=None,
                 utran_positioning_info=None,
                 service_area_identity=None,
                 serving_node=None,
                 pla_flags=None,
                 esmlc_cell_info=None,
                 civic_address=None,
                 barometric_pressure=None,
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.PROVIDE_LOCATION, app_id)

        self.session_id = session_id
        self.auth_session_state = auth_session_state
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.vendor_specific_application_id = vendor_specific_application_id
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.location_estimate = location_estimate
        self.accuracy_fulfilment_indicator = accuracy_fulfilment_indicator
        self.age_of_location_estimate = age_of_location_estimate
        self.velocity_estimate = velocity_estimate
        self.eutran_positioning_data = eutran_positioning_data
        self.ecgi = ecgi
        self.geran_positioning_info = geran_positioning_info
        self.cell_global_identity = cell_global_identity
        self.utran_positioning_info = utran_positioning_info
        self.service_area_identity = service_area_identity
        self.serving_node = serving_node
        self.pla_flags = pla_flags
        self.esmlc_cell_info = esmlc_cell_info
        self.civic_address = civic_address
        self.barometric_pressure = barometric_pressure
        self.supported_features = supported_features
        self.failed_avp = failed_avp
        self.proxy_info = proxy_info
        self.route_record = route_record

        self.setProxiableFlag(True)

    def get_vendor_specific_application_id(self):
        return self.vendor_specific_application_id
    
    def get_result_code(self):
        return self.result_code
    
    def get_experimental_result(self):
        return self.experimental_result
    
    def get_location_estimate(self):
        return self.location_estimate
    
    def get_accuracy_fulfilment_indicator(self):
        return self.accuracy_fulfilment_indicator
    
    def get_age_of_location_estimate(self):
        return self.age_of_location_estimate
    
    def get_velocity_estimate(self):
        return self.velocity_estimate
    
    def get_eutran_positioning_data(self):
        return self.eutran_positioning_data
    
    def get_ecgi(self):
        return self.ecgi
    
    def get_geran_positioning_info(self):
        return self.geran_positioning_info
    
    def get_cell_global_identity(self):
        return self.cell_global_identity
    
    def get_utran_positioning_info(self):
        return self.utran_positioning_info
    
    def get_service_area_identity(self):
        return self.service_area_identity
    
    def get_serving_node(self):
        return self.serving_node
    
    def get_pla_flags(self):
        return self.pla_flags
    
    def get_esmlc_cell_info(self):
        return self.esmlc_cell_info
    
    def get_civic_address(self):
        return self.civic_address
    
    def get_barometric_pressure(self):
        return self.barometric_pressure
    
    def get_supported_features(self):
        return self.supported_features
    
    def get_failed_avp(self):
        return self.failed_avp
    
    def get_proxy_info(self):
        return self.proxy_info
    
    def get_route_record(self):
        return self.route_record

    def set_vendor_specific_application_id(self, value):
        self.vendor_specific_application_id = value
    
    def set_result_code(self, value):
        self.result_code = value
    
    def set_experimental_result(self, value):
        self.experimental_result = value
    
    def set_location_estimate(self, value):
        self.location_estimate = value
    
    def set_accuracy_fulfilment_indicator(self, value):
        self.accuracy_fulfilment_indicator = value
    
    def set_age_of_location_estimate(self, value):
        self.age_of_location_estimate = value
    
    def set_velocity_estimate(self, value):
        self.velocity_estimate = value
    
    def set_eutran_positioning_data(self, value):
        self.eutran_positioning_data = value
    
    def set_ecgi(self, value):
        self.ecgi = value
    
    def set_geran_positioning_info(self, value):
        self.geran_positioning_info = value
    
    def set_cell_global_identity(self, value):
        self.cell_global_identity = value
    
    def set_utran_positioning_info(self, value):
        self.utran_positioning_info = value
    
    def set_service_area_identity(self, value):
        self.service_area_identity = value
    
    def set_serving_node(self, value):
        self.serving_node = value
    
    def set_pla_flags(self, value):
        self.pla_flags = value
    
    def set_esmlc_cell_info(self, value):
        self.esmlc_cell_info = value
    
    def set_civic_address(self, value):
        self.civic_address = value
    
    def set_barometric_pressure(self, value):
        self.barometric_pressure = value
    
    def set_supported_features(self, value):
        self.supported_features = value
    
    def set_failed_avp(self, value):
        self.failed_avp = value
    
    def set_proxy_info(self, value):
        self.proxy_info = value
    
    def set_route_record(self, value):
        self.route_record = value

    def generateMessage(self):
        if self.session_id is None:
            raise MissingMandatoryAVPException('PLA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('PLA: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(self.auth_session_state['value'])
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('PLA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('PLA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
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
        
        if self.location_estimate is not None:
            if 'type' in self.location_estimate and self.location_estimate['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LOCATION_ESTIMATE, self.location_estimate['value'])
            else:
                avp = LocationEstimateAVP(self.location_estimate['value'])
                avp.setFlags(self.location_estimate['flags'])
                if 'vendor' in self.location_estimate:
                    avp.setVendorID(self.location_estimate['vendor'])
            self.addAVP(avp)
        
        if self.accuracy_fulfilment_indicator is not None:
            if 'type' in self.accuracy_fulfilment_indicator and self.accuracy_fulfilment_indicator['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ACCURACY_FULFILMENT_INDICATOR, self.accuracy_fulfilment_indicator['value'])
            else:
                avp = AccuracyFulfilmentIndicatorAVP(self.accuracy_fulfilment_indicator['value'])
                avp.setFlags(self.accuracy_fulfilment_indicator['flags'])
                if 'vendor' in self.accuracy_fulfilment_indicator:
                    avp.setVendorID(self.accuracy_fulfilment_indicator['vendor'])
            self.addAVP(avp)

        if self.age_of_location_estimate is not None:
            if 'type' in self.age_of_location_estimate and self.age_of_location_estimate['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.AGE_OF_LOCATION_ESTIMATE, self.age_of_location_estimate['value'])
            else:
                avp = AgeOfLocationEstimateAVP(self.age_of_location_estimate['value'])
                avp.setFlags(self.age_of_location_estimate['flags'])
                if 'vendor' in self.age_of_location_estimate:
                    avp.setVendorID(self.age_of_location_estimate['vendor'])
            self.addAVP(avp)
        
        if self.velocity_estimate is not None:
            if 'type' in self.velocity_estimate and self.velocity_estimate['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.VELOCITY_ESTIMATE, self.velocity_estimate['value'])
            else:
                avp = VelocityEstimateAVP(self.velocity_estimate['value'])
                avp.setFlags(self.velocity_estimate['flags'])
                if 'vendor' in self.velocity_estimate:
                    avp.setVendorID(self.velocity_estimate['vendor'])
            self.addAVP(avp)
        
        if self.eutran_positioning_data is not None:
            if 'type' in self.eutran_positioning_data and self.eutran_positioning_data['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.EUTRAN_POSITIONING_DATA, self.eutran_positioning_data['value'])
            else:
                avp = EUTRANPositioningDataAVP(self.eutran_positioning_data['value'])
                avp.setFlags(self.eutran_positioning_data['flags'])
                if 'vendor' in self.eutran_positioning_data:
                    avp.setVendorID(self.eutran_positioning_data['vendor'])
            self.addAVP(avp)

        if self.ecgi is not None:
            if 'type' in self.ecgi and self.ecgi['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ECGI, self.ecgi['value'])
            else:
                avp = ECGIAVP(self.ecgi['value'])
                avp.setFlags(self.ecgi['flags'])
                if 'vendor' in self.ecgi:
                    avp.setVendorID(self.ecgi['vendor'])
            self.addAVP(avp)
        
        if self.geran_positioning_info is not None:
            if 'type' in self.geran_positioning_info and self.geran_positioning_info['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.GERAN_POSITIONING_INFO, self.geran_positioning_info['value'])
            else:
                avp = GERANPositioningInfoAVP(self.geran_positioning_info['value'])
                avp.setFlags(self.geran_positioning_info['flags'])
                if 'vendor' in self.geran_positioning_info:
                    avp.setVendorID(self.geran_positioning_info['vendor'])
            self.addAVP(avp)
        
        if self.cell_global_identity is not None:
            if 'type' in self.cell_global_identity and self.cell_global_identity['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.CELL_GLOBAL_IDENTITY, self.cell_global_identity['value'])
            else:
                avp = CellGlobalIdentityAVP(self.cell_global_identity['value'])
                avp.setFlags(self.cell_global_identity['flags'])
                if 'vendor' in self.cell_global_identity:
                    avp.setVendorID(self.cell_global_identity['vendor'])
            self.addAVP(avp)

        if self.utran_positioning_info is not None:
            if 'type' in self.utran_positioning_info and self.utran_positioning_info['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.UTRAN_POSITIONING_INFO, self.utran_positioning_info['value'])
            else:
                avp = UTRANPositioningInfoAVP(self.utran_positioning_info['value'])
                avp.setFlags(self.utran_positioning_info['flags'])
                if 'vendor' in self.utran_positioning_info:
                    avp.setVendorID(self.utran_positioning_info['vendor'])
            self.addAVP(avp)
        
        if self.service_area_identity is not None:
            if 'type' in self.service_area_identity and self.service_area_identity['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.SERVICE_AREA_IDENTITY, self.service_area_identity['value'])
            else:
                avp = ServiceAreaIdentityAVP(self.service_area_identity['value'])
                avp.setFlags(self.service_area_identity['flags'])
                if 'vendor' in self.service_area_identity:
                    avp.setVendorID(self.service_area_identity['vendor'])
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
        
        if self.pla_flags is not None:
            if 'type' in self.pla_flags and self.pla_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.PLA_FLAGS, self.pla_flags['value'])
            else:
                avp = PLAFlagsAVP(self.pla_flags['value'])
                avp.setFlags(self.pla_flags['flags'])
                if 'vendor' in self.pla_flags:
                    avp.setVendorID(self.pla_flags['vendor'])
            self.addAVP(avp)

        if self.esmlc_cell_info is not None:
            if 'type' in self.esmlc_cell_info and self.esmlc_cell_info['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ESMLC_CELL_INFO, self.esmlc_cell_info['value'])
            else:
                avp = ESMLCCellInfoAVP(self.esmlc_cell_info['value'])
                avp.setFlags(self.esmlc_cell_info['flags'])
                if 'vendor' in self.esmlc_cell_info:
                    avp.setVendorID(self.esmlc_cell_info['vendor'])
            self.addAVP(avp)
        
        if self.civic_address is not None:
            if 'type' in self.civic_address and self.civic_address['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.CIVIC_ADDRESS, self.civic_address['value'])
            else:
                avp = CivicAddressAVP(self.civic_address['value'])
                avp.setFlags(self.civic_address['flags'])
                if 'vendor' in self.civic_address:
                    avp.setVendorID(self.civic_address['vendor'])
            self.addAVP(avp)
        
        if self.barometric_pressure is not None:
            if 'type' in self.barometric_pressure and self.barometric_pressure['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.BAROMETRIC_PRESSURE, self.barometric_pressure['value'])
            else:
                avp = BarometricPressureAVP(self.barometric_pressure['value'])
                avp.setFlags(self.barometric_pressure['flags'])
                if 'vendor' in self.barometric_pressure:
                    avp.setVendorID(self.barometric_pressure['vendor'])
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
''' /3GPP: PROVIDE LOCATION '''

''' 3GPP: OCATION REPORT '''
##
## @brief      Class that defines a DIAMETER Message
##
##        < Location-Report-Request> ::= < Diameter Header: 8388621, REQ, PXY, 16777255 >
##                < Session-Id >
##                [ Vendor-Specific-Application-Id ]
##                { Auth-Session-State }
##                { Origin-Host }
##                { Origin-Realm }
##                { Destination-Host }
##                { Destination-Realm }
##                { Location-Event }
##                [ LCS-EPS-Client-Name ]
##                [ User-Name ]
##                [ MSISDN]
##                [ IMEI ]
##                [ Location-Estimate ]
##                [ Accuracy-Fulfilment-Indicator ]
##                [ Age-Of-Location-Estimate ]
##                [ Velocity-Estimate ]
##                [ EUTRAN-Positioning-Data ]
##                [ ECGI]
##                [ GERAN-Positioning-Info ]
##                [ Cell-Global-Identity ]
##                [ UTRAN-Positioning-Info ]
##                [ Service-Area-Identity ]
##                [ LCS-Service-Type-ID ]
##                [ Pseudonym-Indicator ]
##                [ LCS-QoS-Class ]
##                [ Serving-Node ]
##                [ LRR-Flags ]
##                [ LCS-Reference-Number ]
##                [ Deferred-MT-LR-Data]
##                [ GMLC-Address ]
##                [ Reporting-Amount ]
##                [ Periodic-LDR-Information ]
##                [ ESMLC-Cell-Info ]
##                [ 1xRTT-RCID ]
##                [ Civic-Address ]
##                [ Barometric-Pressure ]
##                *[ Supported-Features ]
##                *[ Proxy-Info ]
##                *[ Route-Record ]
##
class DiamLocationReportRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id, 
                 auth_session_state, 
                 origin_host, 
                 origin_realm, 
                 destination_host, 
                 destination_realm, 
                 location_event, 
                 vendor_specific_application_id=None, 
                 lcs_eps_client_name=None, 
                 user_name=None, 
                 msisdn=None, 
                 imei=None, 
                 location_estimate=None, 
                 accuracy_fulfilment_indicator=None, 
                 age_of_location_estimate=None, 
                 velocity_estimate=None, 
                 eutran_positioning_data=None, 
                 ecgi=None, 
                 geran_positioning_info=None, 
                 cell_global_identity=None, 
                 utran_positioning_info=None, 
                 service_area_identity=None, 
                 lcs_service_type_id=None, 
                 pseudonym_indicator=None, 
                 lcs_qos_class=None, 
                 serving_node=None, 
                 lrr_flags=None, 
                 lcs_reference_number=None, 
                 deferred_mt_lr_data=None, 
                 gmlc_address=None, 
                 reporting_amount=None, 
                 periodic_ldr_information=None, 
                 esmlc_cell_info=None, 
                 xrtt_rcid_1=None, 
                 civic_address=None, 
                 barometric_pressure=None, 
                 supported_features=None, 
                 proxy_info=None, 
                 route_record=None):

        DiamMessage.__init__(self, DiamCommandCodes.LOCATION_REPORT, app_id)
        
        self.session_id = session_id
        self.vendor_specific_application_id = vendor_specific_application_id
        self.auth_session_state = auth_session_state
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_host = destination_host
        self.destination_realm = destination_realm
        self.location_event = location_event
        self.lcs_eps_client_name = lcs_eps_client_name
        self.user_name = user_name
        self.msisdn = msisdn
        self.imei = imei
        self.location_estimate = location_estimate
        self.accuracy_fulfilment_indicator = accuracy_fulfilment_indicator
        self.age_of_location_estimate = age_of_location_estimate
        self.velocity_estimate = velocity_estimate
        self.eutran_positioning_data = eutran_positioning_data
        self.ecgi = ecgi
        self.geran_positioning_info = geran_positioning_info
        self.cell_global_identity = cell_global_identity
        self.utran_positioning_info = utran_positioning_info
        self.service_area_identity = service_area_identity
        self.lcs_service_type_id = lcs_service_type_id
        self.pseudonym_indicator = pseudonym_indicator
        self.lcs_qos_class = lcs_qos_class
        self.serving_node = serving_node
        self.lrr_flags = lrr_flags
        self.lcs_reference_number = lcs_reference_number
        self.deferred_mt_lr_data = deferred_mt_lr_data
        self.gmlc_address = gmlc_address
        self.reporting_amount = reporting_amount
        self.periodic_ldr_information = periodic_ldr_information
        self.esmlc_cell_info = esmlc_cell_info
        self.xrtt_rcid_1 = xrtt_rcid_1
        self.civic_address = civic_address
        self.barometric_pressure = barometric_pressure
        self.supported_features = supported_features
        self.proxy_info = proxy_info
        self.route_record = route_record
        
        self.setRequestFlag(True)
        self.setProxiableFlag(True)

    def get_session_id(self):
        return self.session_id

    def get_vendor_specific_application_id(self):
        return self.vendor_specific_application_id

    def get_auth_session_state(self):
        return self.auth_session_state

    def get_origin_host(self):
        return self.origin_host

    def get_origin_realm(self):
        return self.origin_realm

    def get_destination_host(self):
        return self.destination_host

    def get_destination_realm(self):
        return self.destination_realm

    def get_location_event(self):
        return self.location_event

    def get_lcs_eps_client_name(self):
        return self.lcs_eps_client_name

    def get_user_name(self):
        return self.user_name

    def get_msisdn(self):
        return self.msisdn

    def get_imei(self):
        return self.imei

    def get_location_estimate(self):
        return self.location_estimate

    def get_accuracy_fulfilment_indicator(self):
        return self.accuracy_fulfilment_indicator

    def get_age_of_location_estimate(self):
        return self.age_of_location_estimate

    def get_velocity_estimate(self):
        return self.velocity_estimate

    def get_eutran_positioning_data(self):
        return self.eutran_positioning_data

    def get_ecgi(self):
        return self.ecgi

    def get_geran_positioning_info(self):
        return self.geran_positioning_info

    def get_cell_global_identity(self):
        return self.cell_global_identity

    def get_utran_positioning_info(self):
        return self.utran_positioning_info

    def get_service_area_identity(self):
        return self.service_area_identity

    def get_lcs_service_type_id(self):
        return self.lcs_service_type_id

    def get_pseudonym_indicator(self):
        return self.pseudonym_indicator

    def get_lcs_qos_class(self):
        return self.lcs_qos_class

    def get_serving_node(self):
        return self.serving_node

    def get_lrr_flags(self):
        return self.lrr_flags

    def get_lcs_reference_number(self):
        return self.lcs_reference_number

    def get_deferred_mt_lr_data(self):
        return self.deferred_mt_lr_data

    def get_gmlc_address(self):
        return self.gmlc_address

    def get_reporting_amount(self):
        return self.reporting_amount

    def get_periodic_ldr_information(self):
        return self.periodic_ldr_information

    def get_esmlc_cell_info(self):
        return self.esmlc_cell_info

    def get_xrtt_rcid_1(self):
        return self.xrtt_rcid_1

    def get_civic_address(self):
        return self.civic_address

    def get_barometric_pressure(self):
        return self.barometric_pressure

    def get_supported_features(self):
        return self.supported_features

    def get_proxy_info(self):
        return self.proxy_info

    def get_route_record(self):
        return self.route_record

    def set_session_id(self, value):
        self.session_id = value

    def set_vendor_specific_application_id(self, value):
        self.vendor_specific_application_id = value

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_origin_host(self, value):
        self.origin_host = value

    def set_origin_realm(self, value):
        self.origin_realm = value

    def set_destination_host(self, value):
        self.destination_host = value

    def set_destination_realm(self, value):
        self.destination_realm = value

    def set_location_event(self, value):
        self.location_event = value

    def set_lcs_eps_client_name(self, value):
        self.lcs_eps_client_name = value

    def set_user_name(self, value):
        self.user_name = value

    def set_msisdn(self, value):
        self.msisdn = value

    def set_imei(self, value):
        self.imei = value

    def set_location_estimate(self, value):
        self.location_estimate = value

    def set_accuracy_fulfilment_indicator(self, value):
        self.accuracy_fulfilment_indicator = value

    def set_age_of_location_estimate(self, value):
        self.age_of_location_estimate = value

    def set_velocity_estimate(self, value):
        self.velocity_estimate = value

    def set_eutran_positioning_data(self, value):
        self.eutran_positioning_data = value

    def set_ecgi(self, value):
        self.ecgi = value

    def set_geran_positioning_info(self, value):
        self.geran_positioning_info = value

    def set_cell_global_identity(self, value):
        self.cell_global_identity = value

    def set_utran_positioning_info(self, value):
        self.utran_positioning_info = value

    def set_service_area_identity(self, value):
        self.service_area_identity = value

    def set_lcs_service_type_id(self, value):
        self.lcs_service_type_id = value

    def set_pseudonym_indicator(self, value):
        self.pseudonym_indicator = value

    def set_lcs_qos_class(self, value):
        self.lcs_qos_class = value

    def set_serving_node(self, value):
        self.serving_node = value

    def set_lrr_flags(self, value):
        self.lrr_flags = value

    def set_lcs_reference_number(self, value):
        self.lcs_reference_number = value

    def set_deferred_mt_lr_data(self, value):
        self.deferred_mt_lr_data = value

    def set_gmlc_address(self, value):
        self.gmlc_address = value

    def set_reporting_amount(self, value):
        self.reporting_amount = value

    def set_periodic_ldr_information(self, value):
        self.periodic_ldr_information = value

    def set_esmlc_cell_info(self, value):
        self.esmlc_cell_info = value

    def set_xrtt_rcid_1(self, value):
        self.xrtt_rcid_1 = value

    def set_civic_address(self, value):
        self.civic_address = value

    def set_barometric_pressure(self, value):
        self.barometric_pressure = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value

    def generateMessage(self):
        if self.session_id is None:
            raise MissingMandatoryAVPException('LRR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)

        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('LRR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(self.auth_session_state['value'])
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)

        if self.origin_host is None:
            raise MissingMandatoryAVPException('LRR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)

        if self.origin_realm is None:
            raise MissingMandatoryAVPException('LRR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)

        if self.destination_host is None:
            raise MissingMandatoryAVPException('LRR: The Destination-Host AVP is MANDATORY')
        avp = DestinationHostAVP(self.destination_host['value'])
        avp.setFlags(self.destination_host['flags'])
        if 'vendor' in self.destination_host:
            avp.setVendorID(self.destination_host['vendor'])
        self.addAVP(avp)

        if self.destination_realm is None:
            raise MissingMandatoryAVPException('LRR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)

        if self.location_event is None:
            raise MissingMandatoryAVPException('LRR: The Location-Event AVP is MANDATORY')
        avp = LocationEventAVP(self.location_event['value'])
        avp.setFlags(self.location_event['flags'])
        if 'vendor' in self.location_event:
            avp.setVendorID(self.location_event['vendor'])
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

        if self.lcs_eps_client_name is not None:
            if not isinstance(self.lcs_eps_client_name, list):
                self.lcs_eps_client_name = [self.lcs_eps_client_name]

            for el in self.lcs_eps_client_name:
                if el is not None:
                    if 'type' in el and el['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.LCS_EPS_CLIENT_NAME, el['value'])
                    else:
                        topass = {'lcs_name_string':None,
                                  'lcs_format_indicator':None,
                                  'vendor_id':0}

                        for vavp in el['avps']:
                            if vavp['name'] == 'lcs-name-string':
                                topass['lcs_name_string'] = vavp
                            if vavp['name'] == 'lcs-format-indicator':
                                topass['lcs_format_indicator'] = vavp
                            if vavp['name'] == 'vendor-id':
                                topass['vendor_id'] = vavp

                        avp = LCSEPSClientNameAVP(topass['lcs_name_string'], topass['lcs_format_indicator'], topass['vendor_id'])
                        avp.setFlags(el['flags'])
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

        if self.imei is not None:
            if 'type' in self.imei and self.imei['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.IMEI, self.imei['value'])
            else:
                avp = IMEIAVP(self.imei['value'])
                avp.setFlags(self.imei['flags'])
                if 'vendor' in self.imei:
                    avp.setVendorID(self.imei['vendor'])
            self.addAVP(avp)

        if self.location_estimate is not None:
            if 'type' in self.location_estimate and self.location_estimate['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LOCATION_ESTIMATE, self.location_estimate['value'])
            else:
                avp = LocationEstimateAVP(self.location_estimate['value'])
                avp.setFlags(self.location_estimate['flags'])
                if 'vendor' in self.location_estimate:
                    avp.setVendorID(self.location_estimate['vendor'])
            self.addAVP(avp)

        if self.accuracy_fulfilment_indicator is not None:
            if 'type' in self.accuracy_fulfilment_indicator and self.accuracy_fulfilment_indicator['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ACCURACY_FULFILMENT_INDICATOR, self.accuracy_fulfilment_indicator['value'])
            else:
                avp = AccuracyFulfilmentIndicatorAVP(self.accuracy_fulfilment_indicator['value'])
                avp.setFlags(self.accuracy_fulfilment_indicator['flags'])
                if 'vendor' in self.accuracy_fulfilment_indicator:
                    avp.setVendorID(self.accuracy_fulfilment_indicator['vendor'])
            self.addAVP(avp)

        if self.age_of_location_estimate is not None:
            if 'type' in self.age_of_location_estimate and self.age_of_location_estimate['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.AGE_OF_LOCATION_ESTIMATE, self.age_of_location_estimate['value'])
            else:
                avp = AgeOfLocationEstimateAVP(self.age_of_location_estimate['value'])
                avp.setFlags(self.age_of_location_estimate['flags'])
                if 'vendor' in self.age_of_location_estimate:
                    avp.setVendorID(self.age_of_location_estimate['vendor'])
            self.addAVP(avp)

        if self.velocity_estimate is not None:
            if 'type' in self.velocity_estimate and self.velocity_estimate['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.VELOCITY_ESTIMATE, self.velocity_estimate['value'])
            else:
                avp = VelocityEstimateAVP(self.velocity_estimate['value'])
                avp.setFlags(self.velocity_estimate['flags'])
                if 'vendor' in self.velocity_estimate:
                    avp.setVendorID(self.velocity_estimate['vendor'])
            self.addAVP(avp)

        if self.eutran_positioning_data is not None:
            if 'type' in self.eutran_positioning_data and self.eutran_positioning_data['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.EUTRAN_POSITIONING_DATA, self.eutran_positioning_data['value'])
            else:
                avp = EUTRANPositioningDataAVP(self.eutran_positioning_data['value'])
                avp.setFlags(self.eutran_positioning_data['flags'])
                if 'vendor' in self.eutran_positioning_data:
                    avp.setVendorID(self.eutran_positioning_data['vendor'])
            self.addAVP(avp)

        if self.ecgi is not None:
            if 'type' in self.ecgi and self.ecgi['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ECGI, self.ecgi['value'])
            else:
                avp = ECGIAVP(self.ecgi['value'])
                avp.setFlags(self.ecgi['flags'])
                if 'vendor' in self.ecgi:
                    avp.setVendorID(self.ecgi['vendor'])
            self.addAVP(avp)

        if self.geran_positioning_info is not None:
            if 'type' in self.geran_positioning_info and self.geran_positioning_info['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.GERAN_POSITIONING_INFO, self.geran_positioning_info['value'])
            else:
                avp = GERANPositioningInfoAVP(self.geran_positioning_info['value'])
                avp.setFlags(self.geran_positioning_info['flags'])
                if 'vendor' in self.geran_positioning_info:
                    avp.setVendorID(self.geran_positioning_info['vendor'])
            self.addAVP(avp)

        if self.cell_global_identity is not None:
            if 'type' in self.cell_global_identity and self.cell_global_identity['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.CELL_GLOBAL_IDENTITY, self.cell_global_identity['value'])
            else:
                avp = CellGlobalIdentityAVP(self.cell_global_identity['value'])
                avp.setFlags(self.cell_global_identity['flags'])
                if 'vendor' in self.cell_global_identity:
                    avp.setVendorID(self.cell_global_identity['vendor'])
            self.addAVP(avp)

        if self.utran_positioning_info is not None:
            if 'type' in self.utran_positioning_info and self.utran_positioning_info['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.UTRAN_POSITIONING_INFO, self.utran_positioning_info['value'])
            else:
                avp = UTRANPositioningInfoAVP(self.utran_positioning_info['value'])
                avp.setFlags(self.utran_positioning_info['flags'])
                if 'vendor' in self.utran_positioning_info:
                    avp.setVendorID(self.utran_positioning_info['vendor'])
            self.addAVP(avp)

        if self.service_area_identity is not None:
            if 'type' in self.service_area_identity and self.service_area_identity['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.SERVICE_AREA_IDENTITY, self.service_area_identity['value'])
            else:
                avp = ServiceAreaIdentityAVP(self.service_area_identity['value'])
                avp.setFlags(self.service_area_identity['flags'])
                if 'vendor' in self.service_area_identity:
                    avp.setVendorID(self.service_area_identity['vendor'])
            self.addAVP(avp)

        if self.lcs_service_type_id is not None:
            if 'type' in self.lcs_service_type_id and self.lcs_service_type_id['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_SERVICE_TYPE_ID, self.lcs_service_type_id['value'])
            else:
                avp = LCSServiceTypeIDAVP(self.lcs_service_type_id['value'])
                avp.setFlags(self.lcs_service_type_id['flags'])
                if 'vendor' in self.lcs_service_type_id:
                    avp.setVendorID(self.lcs_service_type_id['vendor'])
            self.addAVP(avp)

        if self.pseudonym_indicator is not None:
            if 'type' in self.pseudonym_indicator and self.pseudonym_indicator['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.PSEUDONYM_INDICATOR, self.pseudonym_indicator['value'])
            else:
                avp = PseudonymIndicatorAVP(self.pseudonym_indicator['value'])
                avp.setFlags(self.pseudonym_indicator['flags'])
                if 'vendor' in self.pseudonym_indicator:
                    avp.setVendorID(self.pseudonym_indicator['vendor'])
            self.addAVP(avp)

        if self.lcs_qos_class is not None:
            if 'type' in self.lcs_qos_class and self.lcs_qos_class['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_QOS_CLASS, self.lcs_qos_class['value'])
            else:
                avp = LCSQoSClassAVP(self.lcs_qos_class['value'])
                avp.setFlags(self.lcs_qos_class['flags'])
                if 'vendor' in self.lcs_qos_class:
                    avp.setVendorID(self.lcs_qos_class['vendor'])
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

        if self.lrr_flags is not None:
            if 'type' in self.lrr_flags and self.lrr_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LRR_FLAGS, self.lrr_flags['value'])
            else:
                avp = LRRFlagsAVP(self.lrr_flags['value'])
                avp.setFlags(self.lrr_flags['flags'])
                if 'vendor' in self.lrr_flags:
                    avp.setVendorID(self.lrr_flags['vendor'])
            self.addAVP(avp)

        if self.lcs_reference_number is not None:
            if 'type' in self.lcs_reference_number and self.lcs_reference_number['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_REFERENCE_NUMBER, self.lcs_reference_number['value'])
            else:
                avp = LCSReferenceNumberAVP(self.lcs_reference_number['value'])
                avp.setFlags(self.lcs_reference_number['flags'])
                if 'vendor' in self.lcs_reference_number:
                    avp.setVendorID(self.lcs_reference_number['vendor'])
            self.addAVP(avp)

        if self.deferred_mt_lr_data is not None:
            if 'type' in self.deferred_mt_lr_data and self.deferred_mt_lr_data['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.DEFERRED_MT_LR_DATA, self.deferred_mt_lr_data['value'])
            else:
                avp = DeferredMTLRDataAVP(self.deferred_mt_lr_data['value'])
                avp.setFlags(self.deferred_mt_lr_data['flags'])
                if 'vendor' in self.deferred_mt_lr_data:
                    avp.setVendorID(self.deferred_mt_lr_data['vendor'])
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

        if self.reporting_amount is not None:
            if 'type' in self.reporting_amount and self.reporting_amount['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.REPORTING_AMOUNT, self.reporting_amount['value'])
            else:
                avp = ReportingAmountAVP(self.reporting_amount['value'])
                avp.setFlags(self.reporting_amount['flags'])
                if 'vendor' in self.reporting_amount:
                    avp.setVendorID(self.reporting_amount['vendor'])
            self.addAVP(avp)

        if self.periodic_ldr_information is not None:
            if 'type' in self.periodic_ldr_information and self.periodic_ldr_information['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.PERIODIC_LDR_INFORMATION, self.periodic_ldr_information['value'])
            else:
                avp = PeriodicLDRInformationAVP(self.periodic_ldr_information['value'])
                avp.setFlags(self.periodic_ldr_information['flags'])
                if 'vendor' in self.periodic_ldr_information:
                    avp.setVendorID(self.periodic_ldr_information['vendor'])
            self.addAVP(avp)

        if self.esmlc_cell_info is not None:
            if 'type' in self.esmlc_cell_info and self.esmlc_cell_info['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ESMLC_CELL_INFO, self.esmlc_cell_info['value'])
            else:
                avp = ESMLCCellInfoAVP(self.esmlc_cell_info['value'])
                avp.setFlags(self.esmlc_cell_info['flags'])
                if 'vendor' in self.esmlc_cell_info:
                    avp.setVendorID(self.esmlc_cell_info['vendor'])
            self.addAVP(avp)

        if self.xrtt_rcid_1 is not None:
            if 'type' in self.xrtt_rcid_1 and self.xrtt_rcid_1['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.XRTT_RCID_1, self.xrtt_rcid_1['value'])
            else:
                avp = xRTTRCID1AVP(self.xrtt_rcid_1['value'])
                avp.setFlags(self.xrtt_rcid_1['flags'])
                if 'vendor' in self.xrtt_rcid_1:
                    avp.setVendorID(self.xrtt_rcid_1['vendor'])
            self.addAVP(avp)

        if self.civic_address is not None:
            if 'type' in self.civic_address and self.civic_address['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.CIVIC_ADDRESS, self.civic_address['value'])
            else:
                avp = CivicAddressAVP(self.civic_address['value'])
                avp.setFlags(self.civic_address['flags'])
                if 'vendor' in self.civic_address:
                    avp.setVendorID(self.civic_address['vendor'])
            self.addAVP(avp)

        if self.barometric_pressure is not None:
            if 'type' in self.barometric_pressure and self.barometric_pressure['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.BAROMETRIC_PRESSURE, self.barometric_pressure['value'])
            else:
                avp = BarometricPressureAVP(self.barometric_pressure['value'])
                avp.setFlags(self.barometric_pressure['flags'])
                if 'vendor' in self.barometric_pressure:
                    avp.setVendorID(self.barometric_pressure['vendor'])
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
            if 'type' in self.route_record and self.route_record['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, self.route_record['value'])
            else:
                avp = RouteRecordAVP(self.route_record['value'])
                avp.setFlags(self.route_record['flags'])
                if 'vendor' in self.route_record:
                    avp.setVendorID(self.route_record['vendor'])
            self.addAVP(avp)

##
## @brief      Class that defines a DIAMETER Message
##
##        < Location-Report-Answer > ::= < Diameter Header: 8388621, PXY, 16777255>
##                < Session-Id >
##                [ Vendor-Specific-Application-Id ]
##                [ Result-Code ]
##                [ Experimental-Result ]
##                { Auth-Session-State }
##                { Origin-Host }
##                { Origin-Realm }
##                [ GMLC-Address ]
##                [ LRA-Flags ]
##                [ Reporting-PLMN-List ]
##                [ LCS-Reference-Number ]
##                *[ Supported-Features ]
##                *[ Failed-AVP ]
##                *[ Proxy-Info ]
##                *[ Route-Record ]
##
class DiamLocationReportAnswer(DiamMessage):
    def __init__(self, 
             app_id, 
             session_id, 
             auth_session_state, 
             origin_host, 
             origin_realm, 
             vendor_specific_application_id=None, 
             result_code=None, 
             experimental_result=None, 
             gmlc_address=None, 
             lra_flags=None, 
             reporting_plmn_list=None, 
             lcs_reference_number=None, 
             supported_features=None, 
             failed_avp=None, 
             proxy_info=None, 
             route_record=None):

        DiamMessage.__init__(self, DiamCommandCodes.LOCATION_REPORT, app_id)
        
        self.session_id = session_id
        self.vendor_specific_application_id = vendor_specific_application_id
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.auth_session_state = auth_session_state
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.gmlc_address = gmlc_address
        self.lra_flags = lra_flags
        self.reporting_plmn_list = reporting_plmn_list
        self.lcs_reference_number = lcs_reference_number
        self.supported_features = supported_features
        self.failed_avp = failed_avp
        self.proxy_info = proxy_info
        self.route_record = route_record
        
        self.setProxiableFlag(True)

    def get_session_id(self):
        return self.session_id

    def get_vendor_specific_application_id(self):
        return self.vendor_specific_application_id

    def get_result_code(self):
        return self.result_code

    def get_experimental_result(self):
        return self.experimental_result

    def get_auth_session_state(self):
        return self.auth_session_state

    def get_origin_host(self):
        return self.origin_host

    def get_origin_realm(self):
        return self.origin_realm

    def get_gmlc_address(self):
        return self.gmlc_address

    def get_lra_flags(self):
        return self.lra_flags

    def get_reporting_plmn_list(self):
        return self.reporting_plmn_list

    def get_lcs_reference_number(self):
        return self.lcs_reference_number

    def get_supported_features(self):
        return self.supported_features

    def get_failed_avp(self):
        return self.failed_avp

    def get_proxy_info(self):
        return self.proxy_info

    def get_route_record(self):
        return self.route_record

    def set_session_id(self, value):
        self.session_id = value

    def set_vendor_specific_application_id(self, value):
        self.vendor_specific_application_id = value

    def set_result_code(self, value):
        self.result_code = value

    def set_experimental_result(self, value):
        self.experimental_result = value

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_origin_host(self, value):
        self.origin_host = value

    def set_origin_realm(self, value):
        self.origin_realm = value

    def set_gmlc_address(self, value):
        self.gmlc_address = value

    def set_lra_flags(self, value):
        self.lra_flags = value

    def set_reporting_plmn_list(self, value):
        self.reporting_plmn_list = value

    def set_lcs_reference_number(self, value):
        self.lcs_reference_number = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value

    def generateMessage(self):
        if self.session_id is None:
            raise MissingMandatoryAVPException('LRA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)

        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('LRA: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(self.auth_session_state['value'])
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)

        if self.origin_host is None:
            raise MissingMandatoryAVPException('LRA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)

        if self.origin_realm is None:
            raise MissingMandatoryAVPException('LRA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
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

        if self.gmlc_address is not None:
            if 'type' in self.gmlc_address and self.gmlc_address['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.GMLC_ADDRESS, self.gmlc_address['value'])
            else:
                avp = GMLCAddressAVP(self.gmlc_address['value'])
                avp.setFlags(self.gmlc_address['flags'])
                if 'vendor' in self.gmlc_address:
                    avp.setVendorID(self.gmlc_address['vendor'])
            self.addAVP(avp)

        if self.lra_flags is not None:
            if 'type' in self.lra_flags and self.lra_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LRA_FLAGS, self.lra_flags['value'])
            else:
                avp = LRAFlagsAVP(self.lra_flags['value'])
                avp.setFlags(self.lra_flags['flags'])
                if 'vendor' in self.lra_flags:
                    avp.setVendorID(self.lra_flags['vendor'])
            self.addAVP(avp)

        if self.reporting_plmn_list is not None:
            if 'type' in self.reporting_plmn_list and self.reporting_plmn_list['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.REPORTING_PLMN_LIST, self.reporting_plmn_list['value'])
            else:
                avp = ReportingPLMNListAVP(self.reporting_plmn_list['value'])
                avp.setFlags(self.reporting_plmn_list['flags'])
                if 'vendor' in self.reporting_plmn_list:
                    avp.setVendorID(self.reporting_plmn_list['vendor'])
            self.addAVP(avp)

        if self.lcs_reference_number is not None:
            if 'type' in self.lcs_reference_number and self.lcs_reference_number['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LCS_REFERENCE_NUMBER, self.lcs_reference_number['value'])
            else:
                avp = LCSReferenceNumberAVP(self.lcs_reference_number['value'])
                avp.setFlags(self.lcs_reference_number['flags'])
                if 'vendor' in self.lcs_reference_number:
                    avp.setVendorID(self.lcs_reference_number['vendor'])
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
            
        if self.failed_avp is not None:
            if not isinstance(self.failed_avp, list):
                self.failed_avp = [self.failed_avp]
                
            for fa in self.failed_avp:
                if fa is not None:
                    if 'type' in fa and fa['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.FAILED_AVP, fa['value'])
                    else:
                        avp = FailedAVP(fa['avps'])
                        avp.setFlags(fa['flags'])
                        if 'vendor' in fa:
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
            if 'type' in self.route_record and self.route_record['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, self.route_record['value'])
            else:
                avp = RouteRecordAVP(self.route_record['value'])
                avp.setFlags(self.route_record['flags'])
                if 'vendor' in self.route_record:
                    avp.setVendorID(self.route_record['vendor'])
            self.addAVP(avp)
''' /3GPP: OCATION REPORT '''
