from ..diameter.diam_avp_data import *
from ..diameter.diameter_message import DiamMessage
from ..diameter.diamCommandCodes import DiamCommandCodes
from ..commons import FUNC
from ...core.commons import printYellow
#from dpkt.diameter import AVP
__MULTIPLE_DST_REALM__ = 0
__MULTIPLE_DST_HOST__  = 0

##
## @author: Ilario Dal Grande
##

''' >>> S6a INTERFACE <<< '''

''' 3GPP: CANCEL LOCATION '''
##
## @brief      Class that defines a DIAMETER Message 
##  
##        < Cancel-Location-Request> ::= < Diameter Header: 317, REQ, PXY, 16777251 >
##                                   < Session-Id >
##                                   [ Vendor-Specific-Application-Id ]
##                                   { Auth-Session-State }
##                                   { Origin-Host }
##                                   { Origin-Realm }
##                                   { Destination-Host }
##                                   { Destination-Realm }
##                                   { User-Name }
##                                 * [Supported-Features ]
##                                   { Cancellation-Type }
##                                   [ CLR-Flags ]
##                                 * [ Proxy-Info ]
##                                 * [ Route-Record ]
##
class DiamCancelLocationRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 origin_host, 
                 origin_realm, 
                 destination_host, 
                 destination_realm, 
                 auth_session_state,
                 user_name, 
                 cancellation_type, 
                 supported_features=None, 
                 clr_flags=None,
                 vendor_specific_app_id=None,
                 proxy_info=None, 
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.CANCEL_LOCATION_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_host = destination_host
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.user_name = user_name
        self.cancellation_type = cancellation_type
        self.supported_features = supported_features
        self.clr_flags = clr_flags
        self.vendor_specific_app_id = vendor_specific_app_id
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

    def get_destination_host(self):
        return self.destination_host

    def get_destination_realm(self):
        return self.destination_realm

    def get_auth_session_state(self):
        return self.auth_session_state

    def get_user_name(self):
        return self.user_name

    def get_cancellation_type(self):
        return self.cancellation_type

    def get_supported_features(self):
        return self.supported_features

    def get_clr_flags(self):
        return self.clr_flags

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

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

    def set_destination_host(self, value):
        self.destination_host = value

    def set_destination_realm(self, value):
        self.destination_realm = value

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_user_name(self, value):
        self.user_name = value

    def set_cancellation_type(self, value):
        self.cancellation_type = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_clr_flags(self, value):
        self.clr_flags = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('CLR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('CLR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('CLR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.destination_host is None:
            raise MissingMandatoryAVPException('CLR: The Destination-Host AVP is MANDATORY')
        avp = DestinationHostAVP(self.destination_host['value'])
        avp.setFlags(self.destination_host['flags'])
        if 'vendor' in self.destination_host:
            avp.setVendorID(self.destination_host['vendor'])
        self.addAVP(avp)
        
        if __MULTIPLE_DST_HOST__:
            self.addAVP(avp)
            
        if self.destination_realm is None:
            raise MissingMandatoryAVPException('CLR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('CLR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.user_name is None:
            raise MissingMandatoryAVPException('CLR: The User-Name AVP is MANDATORY')
        avp = UserNameAVP(self.user_name['value'])
        avp.setFlags(self.user_name['flags'])
        if 'vendor' in self.user_name:
            avp.setVendorID(self.user_name['vendor'])
        self.addAVP(avp)
        
        if self.cancellation_type is None:
            raise MissingMandatoryAVPException('CLR: The Cancellation-Type AVP is MANDATORY')
        avp = CancellationTypeAVP(int(self.cancellation_type['value']))
        avp.setFlags(self.cancellation_type['flags'])
        if 'vendor' in self.cancellation_type:
            avp.setVendorID(self.cancellation_type['vendor'])
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
        
        if self.clr_flags is not None:
            if 'type' in self.clr_flags and self.clr_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.CLR_FLAGS, self.clr_flags['value'])
            else:
                avp = CLRFlagsAVP(self.clr_flags['value'])
                avp.setFlags(self.clr_flags['flags'])
                if 'vendor' in self.clr_flags:
                    avp.setVendorID(self.clr_flags['vendor'])
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
##        < Cancel-Location-Answer> ::= < Diameter Header: 317, PXY, 16777251 >
##                                  < Session-Id >
##                                  [ Vendor-Specific-Application-Id ]
##                                  *[ Supported-Features ]
##                                  [ Result-Code ]
##                                  [ Experimental-Result ]
##                                  { Auth-Session-State }
##                                  { Origin-Host }
##                                  { Origin-Realm }
##                                  *[ Failed-AVP ]
##                                  *[ Proxy-Info ]
##                                  *[ Route-Record ]
##
class DiamCancelLocationAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 origin_host, 
                 origin_realm, 
                 auth_session_state,
                 result_code=None,
                 experimental_result=None,
                 supported_features=None, 
                 vendor_specific_app_id=None,
                 failed_avp=None,
                 proxy_info=None, 
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.CANCEL_LOCATION_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.auth_session_state = auth_session_state
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.failed_avp = failed_avp
        self.supported_features = supported_features
        self.vendor_specific_app_id = vendor_specific_app_id
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

    def get_result_code(self):
        return self.result_code

    def get_experimental_result(self):
        return self.experimental_result

    def get_failed_avp(self):
        return self.failed_avp

    def get_supported_features(self):
        return self.supported_features

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

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

    def set_result_code(self, value):
        self.result_code = value

    def set_experimental_result(self, value):
        self.experimental_result = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value

    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('CLA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('CLA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('CLA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
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
''' /3GPP: CANCEL LOCATION '''

''' 3GPP: UPDATE LOCATION '''
##
## @brief      Class that defines a DIAMETER Message 
##  
##        < Update-Location-Request> ::= < Diameter Header: 316, REQ, PXY, 16777251 >
##                                  < Session-Id >
##                                  [ Vendor-Specific-Application-Id ]
##                                  { Auth-Session-State }
##                                  { Origin-Host }
##                                  { Origin-Realm }
##                                  [ Destination-Host ]
##                                  { Destination-Realm }
##                                  { User-Name }
##                                  [ OC-Supported-Features ]
##                                  *[ Supported-Features ]
##                                  [ Terminal-Information ]
##                                  { RAT-Type }
##                                  { ULR-Flags }
##                                  [UE-SRVCC-Capability ]
##                                  { Visited-PLMN-Id }
##                                  [ SGSN-Number ]
##                                  [ Homogeneous-Support-of-IMS-Voice-Over-PS-Sessions ]
##                                  [ GMLC-Address ]
##                                  *[ Active-APN ]
##                                  [ Equivalent-PLMN-List ]
##                                  [ MME-Number-for-MT-SMS ]
##                                  [ SMS-Register-Request ]
##                                  [ SGs-MME-Identity ]
##                                  [ Coupled-Node-Diameter-ID ]
##                                  *[ AVP ]
##                                  *[ Proxy-Info ]
##                                  *[ Route-Record ]
##
class DiamUpdateLocationRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 origin_host, 
                 origin_realm, 
                 destination_realm,
                 auth_session_state,
                 user_name, 
                 rat_type,
                 ulr_flags,
                 visited_plmn_id, 
                 supported_features=None, 
                 vendor_specific_app_id=None,
                 destination_host=None,
                 oc_supported_features=None,
                 ue_srvcc_capability=None,
                 sgsn_number=None,
                 homogeneous_support_ims_voice_over_ps_sessions=None,
                 gmlc_address=None,
                 active_apn=None,
                 equivalent_plmn_list=None,
                 mme_number_for_mt_sms=None,
                 sms_register_request=None,
                 sgs_mme_identity=None,
                 coupled_node_diameter_id=None,
                 proxy_info=None, 
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.UPDATE_LOCATION_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.user_name = user_name
        self.rat_type = rat_type
        self.ulr_flags = ulr_flags
        self.visited_plmn_id = visited_plmn_id
        self.supported_features = supported_features
        self.destination_host = destination_host
        self.vendor_specific_app_id = vendor_specific_app_id
        self.oc_supported_features = oc_supported_features
        self.ue_srvcc_capability = ue_srvcc_capability
        self.sgsn_number = sgsn_number
        self.homogeneous_support_ims_voice_over_ps_sessions = homogeneous_support_ims_voice_over_ps_sessions
        self.gmlc_address = gmlc_address
        self.active_apn = active_apn
        self.equivalent_plmn_list = equivalent_plmn_list
        self.mme_number_for_mt_sms = mme_number_for_mt_sms
        self.sms_register_request = sms_register_request
        self.sgs_mme_identity = sgs_mme_identity
        self.coupled_node_diameter_id = coupled_node_diameter_id
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

    def get_user_name(self):
        return self.user_name

    def get_rat_type(self):
        return self.rat_type

    def get_ulr_flags(self):
        return self.ulr_flags

    def get_visited_plmn_id(self):
        return self.visited_plmn_id

    def get_supported_features(self):
        return self.supported_features

    def get_destination_host(self):
        return self.destination_host

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_oc_supported_features(self):
        return self.oc_supported_features

    def get_ue_srvcc_capability(self):
        return self.ue_srvcc_capability

    def get_sgsn_number(self):
        return self.sgsn_number

    def get_homogeneous_support_ims_voice_over_ps_sessions(self):
        return self.homogeneous_support_ims_voice_over_ps_sessions

    def get_gmlc_address(self):
        return self.gmlc_address

    def get_active_apn(self):
        return self.active_apn

    def get_equivalent_plmn_list(self):
        return self.equivalent_plmn_list

    def get_mme_number_for_mt_sms(self):
        return self.mme_number_for_mt_sms

    def get_sms_register_request(self):
        return self.sms_register_request

    def get_sgs_mme_identity(self):
        return self.sgs_mme_identity

    def get_coupled_node_diameter_id(self):
        return self.coupled_node_diameter_id

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

    def set_user_name(self, value):
        self.user_name = value

    def set_rat_type(self, value):
        self.rat_type = value

    def set_ulr_flags(self, value):
        self.ulr_flags = value

    def set_visited_plmn_id(self, value):
        self.visited_plmn_id = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_destination_host(self, value):
        self.destination_host = value
        
    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_oc_supported_features(self, value):
        self.oc_supported_features = value

    def set_ue_srvcc_capability(self, value):
        self.ue_srvcc_capability = value

    def set_sgsn_number(self, value):
        self.sgsn_number = value

    def set_homogeneous_support_ims_voice_over_ps_sessions(self, value):
        self.homogeneous_support_ims_voice_over_ps_sessions = value

    def set_gmlc_address(self, value):
        self.gmlc_address = value

    def set_active_apn(self, value):
        self.active_apn = value

    def set_equivalent_plmn_list(self, value):
        self.equivalent_plmn_list = value

    def set_mme_number_for_mt_sms(self, value):
        self.mme_number_for_mt_sms = value

    def set_sms_register_request(self, value):
        self.sms_register_request = value

    def set_sgs_mme_identity(self, value):
        self.sgs_mme_identity = value

    def set_coupled_node_diameter_id(self, value):
        self.coupled_node_diameter_id = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('ULR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('ULR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('ULR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.destination_realm is None:
            raise MissingMandatoryAVPException('ULR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)
        
        if self.rat_type is None:
            raise MissingMandatoryAVPException('ULR: The RAT-Type AVP is MANDATORY')
        avp = RATAVP(self.rat_type['value'])
        avp.setFlags(self.rat_type['flags'])
        if 'vendor' in self.rat_type:
            avp.setVendorID(self.rat_type['vendor'])
        self.addAVP(avp)
        
        if self.ulr_flags is None:
            raise MissingMandatoryAVPException('ULR: The ULR-Flags AVP is MANDATORY')
        avp = ULRFlagsAVP(self.ulr_flags['value'])
        avp.setFlags(self.ulr_flags['flags'])
        if 'vendor' in self.ulr_flags:
            avp.setVendorID(self.ulr_flags['vendor'])
        self.addAVP(avp)
        
        if self.visited_plmn_id is None:
            raise MissingMandatoryAVPException('ULR: The Visited-PLMN-ID AVP is MANDATORY')
        avp = VisitedPLMNIDAVP(self.visited_plmn_id['value'])
        avp.setFlags(self.visited_plmn_id['flags'])
      
        if 'vendor' in self.visited_plmn_id:
            avp.setVendorID(self.visited_plmn_id['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('ULR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.user_name is None:
            raise MissingMandatoryAVPException('ULR: The User-Name AVP is MANDATORY')
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
        
        #if self.destination_host is not None:
        #    if 'type' in self.destination_host and self.destination_host['type']=='raw':
        #        avp = GenericAVP(DiamAVPCodes.DESTINATION_HOST, self.destination_host['value'])
        #    else:
        #        avp = DestinationHostAVP(self.destination_host['value'])
        #        avp.setFlags(self.destination_host['flags'])
        #        if 'vendor' in self.destination_host:
        #            avp.setVendorID(self.destination_host['vendor'])
        #    self.addAVP(avp)
        
        if self.oc_supported_features is not None:
            if not isinstance(self.oc_supported_features, list):
                self.oc_supported_features = [self.oc_supported_features]
                
            for sf in self.oc_supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.OC_SUPPORTED_FEATURES, sf['value'])
                    else:
                        topass = {'oc_feature_vector':None,
                                  'vendor_id':0}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'oc-feature-vector':
                                topass['oc_feature_vector'] = savp
                            if savp['name'] == 'vendor-id':
                                topass['vendor_id'] = savp
                                
                        avp = OCSupportedFeaturesAVP(topass['oc_feature_vector'], topass['vendor_id'])
                        avp.setFlags(sf['flags'])
                    self.addAVP(avp)
        
        if self.ue_srvcc_capability is not None:
            if 'type' in self.ue_srvcc_capability and self.ue_srvcc_capability['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.UE_SRVCC_CAPABILITY, self.ue_srvcc_capability['value'])
            else:
                avp = UESRVCCCapabilityAVP(self.ue_srvcc_capability['value'])
                avp.setFlags(self.ue_srvcc_capability['flags'])
                if 'vendor' in self.ue_srvcc_capability:
                    avp.setVendorID(self.ue_srvcc_capability['vendor'])
            self.addAVP(avp)
        
        if self.sgsn_number is not None:
            if 'type' in self.sgsn_number and self.sgsn_number['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.SGSN_NUMBER, self.sgsn_number['value'])
            else:
                avp = SGSNNumberAVP(self.sgsn_number['value'])
                avp.setFlags(self.sgsn_number['flags'])
                if 'vendor' in self.sgsn_number:
                    avp.setVendorID(self.sgsn_number['vendor'])
            self.addAVP(avp)
        
        if self.homogeneous_support_ims_voice_over_ps_sessions is not None:
            if 'type' in self.homogeneous_support_ims_voice_over_ps_sessions and self.homogeneous_support_ims_voice_over_ps_sessions['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.HOMOGENEOUS_SUPPORT_OF_IMS_VOICE_OVER_PS_SESSIONS, self.homogeneous_support_ims_voice_over_ps_sessions['value'])
            else:
                avp = HomogeneousSupportIMSVoiceOverPSSessionsAVP(self.homogeneous_support_ims_voice_over_ps_sessions['value'])
                avp.setFlags(self.homogeneous_support_ims_voice_over_ps_sessions['flags'])
                if 'vendor' in self.homogeneous_support_ims_voice_over_ps_sessions:
                    avp.setVendorID(self.homogeneous_support_ims_voice_over_ps_sessions['vendor'])
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
        
        if self.active_apn is not None:
            if not isinstance(self.active_apn, list):
                self.active_apn = [self.active_apn]
                
            for aa in self.active_apn:
                if aa is not None:
                    if 'type' in aa and aa['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.ACTIVE_APN, aa['value'])
                    else:
                        topass = {'context_id':None, 
                                  'service_selection':None, 
                                  'mip6_agent_info':None, 
                                  'visited_network_id':None, 
                                  'specific_apn_info':None,
                                  'vendor_id':0}
                        
                        for aavp in aa['avps']:
                            if aavp['name'] == 'context-id':
                                topass['context_id'] = aavp
                            if aavp['name'] == 'service-selection':
                                topass['service_selection'] = aavp
                            if aavp['name'] == 'mip6-agent-info':
                                topass['mip6_agent_info'] = aavp
                            if aavp['name'] == 'visited-network-id':
                                topass['visited_network_id'] = aavp
                            if aavp['name'] == 'specific-apn-info':
                                topass['specific_apn_info'] = aavp
                            if aavp['name'] == 'vendor-id':
                                topass['vendor_id'] = aavp
                                
                        avp = ActiveAPNAVP(topass['context_id'], topass['service_selection'], topass['mip6_agent_info'], topass['visited_network_id'], topass['specific_apn_info'], topass['vendor_id'])
                        avp.setFlags(aa['flags'])
                    self.addAVP(avp)
                    
        if self.equivalent_plmn_list is not None:
            if not isinstance(self.equivalent_plmn_list, list):
                self.equivalent_plmn_list = [self.equivalent_plmn_list]
                
            for epl in self.equivalent_plmn_list:
                if epl is not None:
                    if 'type' in epl and epl['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.EQUIVALENT_PLMN_LIST, epl['value'])
                    else:
                        topass = {'visited_plmn_id':None, 
                                  'vendor_id':0}
                        
                        for eavp in epl['avps']:
                            if eavp['name'] == 'visited-plmn-id':
                                topass['visited_plmn_id'] = eavp
                            if eavp['name'] == 'vendor-id':
                                topass['vendor_id'] = eavp
                                
                        avp = EquivalentPLMNListAVP(topass['visited_plmn_id'], topass['vendor_id'])
                        avp.setFlags(epl['flags'])
                    self.addAVP(avp)
        
        if self.mme_number_for_mt_sms is not None:
            if 'type' in self.mme_number_for_mt_sms and self.mme_number_for_mt_sms['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.MME_NUMBER_FOR_MT_SMS, self.mme_number_for_mt_sms['value'])
            else:
                avp = MMENumberForMTSMSAVP(self.mme_number_for_mt_sms['value'])
                avp.setFlags(self.mme_number_for_mt_sms['flags'])
                if 'vendor' in self.mme_number_for_mt_sms:
                    avp.setVendorID(self.mme_number_for_mt_sms['vendor'])
            self.addAVP(avp)
        
        if self.sms_register_request is not None:
            if 'type' in self.sms_register_request and self.sms_register_request['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.SMS_REGISTER_REQUEST, self.sms_register_request['value'])
            else:
                avp = SMSRegisterRequestAVP(self.sms_register_request['value'])
                avp.setFlags(self.sms_register_request['flags'])
                if 'vendor' in self.sms_register_request:
                    avp.setVendorID(self.sms_register_request['vendor'])
            self.addAVP(avp)
        
        if self.sgs_mme_identity is not None:
            if 'type' in self.sgs_mme_identity and self.sgs_mme_identity['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.SGS_MME_IDENTITY, self.sgs_mme_identity['value'])
            else:
                avp = SGsMMEIdentityAVP(self.sgs_mme_identity['value'])
                avp.setFlags(self.sgs_mme_identity['flags'])
                if 'vendor' in self.sgs_mme_identity:
                    avp.setVendorID(self.sgs_mme_identity['vendor'])
            self.addAVP(avp)
        
        if self.coupled_node_diameter_id is not None:
            if 'type' in self.coupled_node_diameter_id and self.coupled_node_diameter_id['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.COUPLED_NODE_DIAMETER_ID, self.coupled_node_diameter_id['value'])
            else:
                avp = CoupledNodeDiameterIDAVP(self.coupled_node_diameter_id['value'])
                avp.setFlags(self.coupled_node_diameter_id['flags'])
                if 'vendor' in self.coupled_node_diameter_id:
                    avp.setVendorID(self.coupled_node_diameter_id['vendor'])
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
##        < Update-Location-Answer> ::= < Diameter Header: 316, PXY, 16777251 >
##                                  < Session-Id >
##                                  [ Vendor-Specific-Application-Id ]
##                                  [ Result-Code ]
##                                  [ Experimental-Result ]
##                                  [ Error-Diagnostic ]
##                                  { Auth-Session-State }
##                                  { Origin-Host }
##                                  { Origin-Realm }
##                                  [ OC-Supported-Features ]
##                                  [ OC-OLR ]
##                                  *[ Supported-Features ]
##                                  [ ULA-Flags ]
##                                  [ Subscription-Data ]
##                                  *[ Reset-ID ]
##                                  *[ Failed-AVP ]
##                                  *[ Proxy-Info ]
##                                  *[ Route-Record ]
##
class DiamUpdateLocationAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 vendor_specific_app_id=None,
                 result_code=None,
                 experimental_result=None,
                 error_diagnostic=None,
                 oc_supported_features=None,
                 oc_olr=None,
                 supported_features=None,
                 ula_flags=None,
                 subscription_data=None,
                 reset_id=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.UPDATE_LOCATION_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.auth_session_state = auth_session_state
        self.vendor_specific_app_id = vendor_specific_app_id
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.error_diagnostic = error_diagnostic
        self.oc_supported_features = oc_supported_features
        self.oc_olr = oc_olr
        self.supported_features = supported_features
        self.ula_flags = ula_flags
        self.subscription_data = subscription_data
        self.reset_id = reset_id
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

    def get_error_diagnostic(self):
        return self.error_diagnostic

    def get_oc_supported_features(self):
        return self.oc_supported_features

    def get_oc_olr(self):
        return self.oc_olr

    def get_supported_features(self):
        return self.supported_features

    def get_ula_flags(self):
        return self.ula_flags

    def get_subscription_data(self):
        return self.subscription_data

    def get_reset_id(self):
        return self.reset_id

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

    def set_error_diagnostic(self, value):
        self.error_diagnostic = value

    def set_oc_supported_features(self, value):
        self.oc_supported_features = value

    def set_oc_olr(self, value):
        self.oc_olr = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_ula_flags(self, value):
        self.ula_flags = value

    def set_subscription_data(self, value):
        self.subscription_data = value

    def set_reset_id(self, value):
        self.reset_id = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('ULA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('ULA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('ULA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('ULA: The Auth-Session-State AVP is MANDATORY')
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
            
        if self.error_diagnostic is not None:
            if 'type' in self.error_diagnostic and self.error_diagnostic['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ERROR_DIAGNOSTIC, self.error_diagnostic['value'])
            else:
                avp = ErrorDiagnosticAVP(self.error_diagnostic['value'])
                avp.setFlags(self.error_diagnostic['flags'])
                if 'vendor' in self.error_diagnostic:
                    avp.setVendorID(self.error_diagnostic['vendor'])
            self.addAVP(avp)
        
        if self.oc_supported_features is not None:
            if not isinstance(self.oc_supported_features, list):
                self.oc_supported_features = [self.oc_supported_features]
                
            for sf in self.oc_supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.OC_SUPPORTED_FEATURES, sf['value'])
                    else:
                        topass = {'oc_feature_vector':None,
                                  'vendor_id':0}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'oc-feature-vector':
                                topass['oc_feature_vector'] = savp
                            if savp['name'] == 'vendor-id':
                                topass['vendor_id'] = savp
                                
                        avp = OCSupportedFeaturesAVP(topass['oc_feature_vector'], topass['vendor_id'])
                        avp.setFlags(sf['flags'])
                    self.addAVP(avp)
        
        if self.oc_olr is not None:
            if 'type' in self.oc_olr and self.oc_olr['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.OC_OLR, self.oc_olr['value'])
            else:
                avp = OCOLRAVP(self.oc_olr['value'])
                avp.setFlags(self.oc_olr['flags'])
                if 'vendor' in self.oc_olr:
                    avp.setVendorID(self.oc_olr['vendor'])
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
        
        if self.ula_flags is not None:
            if 'type' in self.ula_flags and self.ula_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ULA_FLAGS, self.ula_flags['value'])
            else:
                avp = ULAFlagsAVP(self.ula_flags['value'])
                avp.setFlags(self.ula_flags['flags'])
                if 'vendor' in self.ula_flags:
                    avp.setVendorID(self.ula_flags['vendor'])
            self.addAVP(avp)
        
        if self.subscription_data is not None:
            if not isinstance(self.subscription_data, list):
                self.subscription_data = [self.subscription_data]
                
            for sd in self.subscription_data:
                if sd is not None:
                    if 'type' in sd and sd['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.SUBSCRIPTION_DATA, sd['value'])
                    else:
                        '''TODO: add all the AVPs '''
                    self.addAVP(avp)
        
        if self.reset_id is not None:
            if not isinstance(self.reset_id, list):
                self.reset_id = [self.reset_id]
                
            for ri in self.reset_id:
                if ri is not None:
                    if 'type' in ri and ri['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.RESET_ID, ri['value'])
                    else:
                        avp = ResetIDAVP(ri['value'])
                        avp.setFlags(ri['flags'])
                        if 'vendor_id' in ri:
                            avp.setVendorID(ri['vendor'])
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
''' /3GPP: UPDATE LOCATION '''

''' 3GPP: AUTHENTICATION INFORMATION '''
##
## @brief      Class that defines a DIAMETER Message 
##  
##       < Authentication-Information-Request> ::= < Diameter Header: 318, REQ, PXY, 16777251 >
##                                              < Session-Id >
##                                              [ Vendor-Specific-Application-Id ]
##                                              { Auth-Session-State }
##                                              { Origin-Host }
##                                              { Origin-Realm }
##                                              [ Destination-Host ]
##                                              { Destination-Realm }
##                                              { User-Name }
##                                              [ OC-Supported-Features ]
##                                              *[Supported-Features]
##                                              [ Requested-EUTRAN-Authentication-Info ]
##                                              [ Requested-UTRAN-GERAN-Authentication-Info ]
##                                              { Visited-PLMN-Id }
##                                              *[ Proxy-Info ]
##                                              *[ Route-Record ]  
##
class DiamAuthenticationInformationRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 destination_realm,
                 user_name,
                 visited_plmn_id,
                 vendor_specific_app_id=None,
                 destination_host=None,
                 oc_supported_features=None,
                 supported_features=None,
                 requested_eutran_authentication_info=None,
                 requested_utran_geran_authentication_info=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.AUTHENTICATION_INFORMATION_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.destination_realm = destination_realm
        self.visited_plmn_id = visited_plmn_id
        self.requested_eutran_authentication_info = requested_eutran_authentication_info
        self.requested_utran_geran_authentication_info = requested_utran_geran_authentication_info
        self.user_name = user_name
        self.destination_host = None #TODO: destination_host
        self.vendor_specific_app_id = vendor_specific_app_id
        self.oc_supported_features = oc_supported_features
        self.supported_features = supported_features
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

    def get_visited_plmn_id(self):
        return self.visited_plmn_id

    def get_requested_eutran_authentication_info(self):
        return self.requested_eutran_authentication_info

    def get_requested_utran_geran_authentication_info(self):
        return self.requested_utran_geran_authentication_info

    def get_user_name(self):
        return self.user_name

    def get_destination_host(self):
        return self.destination_host

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_oc_supported_features(self):
        return self.oc_supported_features

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

    def set_visited_plmn_id(self, value):
        self.visited_plmn_id = value

    def set_requested_eutran_authentication_info(self, value):
        self.requested_eutran_authentication_info = value

    def set_requested_utran_geran_authentication_info(self, value):
        self.requested_utran_geran_authentication_info = value

    def set_user_name(self, value):
        self.user_name = value

    def set_destination_host(self, value):
        self.destination_host = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_oc_supported_features(self, value):
        self.oc_supported_features = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('AIR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('AIR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('AIR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)

        if self.destination_realm is None:
            raise MissingMandatoryAVPException('AIR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        
        self.addAVP(avp)
        if __MULTIPLE_DST_REALM__:
            self.addAVP(avp)
            
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('AIR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.user_name is None:
            raise MissingMandatoryAVPException('AIR: The User-Name AVP is MANDATORY')
        avp = UserNameAVP(self.user_name['value'])
        avp.setFlags(self.user_name['flags'])
        if 'vendor' in self.user_name:
            avp.setVendorID(self.user_name['vendor'])
        self.addAVP(avp)
        
        if self.visited_plmn_id is None:
            raise MissingMandatoryAVPException('AIR: The Visited-PLMN-ID AVP is MANDATORY')
        avp = VisitedPLMNIDAVP(self.visited_plmn_id['value'])
        avp.setFlags(self.visited_plmn_id['flags'])
        if 'vendor' in self.visited_plmn_id:
            avp.setVendorID(self.visited_plmn_id['vendor'])
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

        if self.requested_eutran_authentication_info is not None:
            if not isinstance(self.requested_eutran_authentication_info, list):
                self.requested_eutran_authentication_info = [self.requested_eutran_authentication_info]
                
            for reai in self.requested_eutran_authentication_info:
                if reai is not None:
                    if 'type' in reai and reai['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.REQUESTED_EUTRAN_AUTHENTICATION_INFO, reai['value'])
                    else:
                        vendor = 0
                        if 'vendor' in reai :
                            vendor = reai['vendor']                        
                        topass = {'number_requested_vectors':None,
                                  'immediate_response_preferred':None,
                                  're_sync_info':None}
                        for ravp in reai['avps']:
                            if ravp['name'] == 'number-requested-vectors':
                                topass['number_requested_vectors'] = ravp
                                
                            if ravp['name'] == 'immediate-response-preferred':
                                topass['immediate_response_preferred'] = ravp
                            
                            if ravp['name'] == 're-sync-info':
                                topass['re_sync_info'] = ravp  

                        avp = RequestedEUTRANAuthenticationInfoAVP(topass['number_requested_vectors'], 
                                                        topass['immediate_response_preferred'], 
                                                        topass['re_sync_info'], vendor)
                        avp.setFlags(reai['flags'])

                    self.addAVP(avp)
                
        if self.oc_supported_features is not None:
            if not isinstance(self.oc_supported_features, list):
                self.oc_supported_features = [self.oc_supported_features]
                
            for sf in self.oc_supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.OC_SUPPORTED_FEATURES, sf['value'])
                    else:
                        vendor = 0
                        if 'vendor' in sf :
                            vendor = sf['vendor']  
                        oc_feature_vector = None
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'oc-feature-vector':
                                oc_feature_vector = savp

                                
                        avp = OCSupportedFeaturesAVP(oc_feature_vector, vendor)
                        avp.setFlags(sf['flags'])
                    self.addAVP(avp)
        
        #if self.destination_host is not None:
        #    if 'type' in self.destination_host and self.destination_host['type']=='raw':
        #        avp = GenericAVP(DiamAVPCodes.DESTINATION_HOST, self.destination_host['value'])
        #    else:
        #        avp = DestinationHostAVP(self.destination_host['value'])
        #        avp.setFlags(self.destination_host['flags'])
        #        if 'vendor' in self.destination_host:
        #            avp.setVendorID(self.destination_host['vendor'])
        #    self.addAVP(avp)

        if self.proxy_info is not None:
            if not isinstance(self.proxy_info, list):
                self.proxy_info = [self.proxy_info]
                
            for pi in self.proxy_info:
                if pi is not None:
                    if 'type' in pi and pi['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.PROXY_INFO, pi['value'])
                    else:
                        vendor = 0
                        if 'vendor' in pi :
                            vendor = pi['vendor']                         
                        topass = {'proxy_host':None,
                                  'proxy_state':None}
                        
                        for pavp in pi['avps']:
                            if pavp['name'] == 'proxy-host':
                                topass['proxy_host'] = pavp
                            if pavp['name'] == 'proxy-state':
                                topass['proxy_state'] = pavp
                            
                        avp = ProxyInfoAVP(topass['proxy_host'], topass['proxy_state'], 
                                           vendor)
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
##         < Authentication-Information-Answer> ::= < Diameter Header: 318, PXY, 16777251 >
##                                                < Session-Id >
##                                                [ Vendor-Specific-Application-Id ]
##                                                [ Result-Code ]
##                                                [ Experimental-Result ]
##                                                [ Error-Diagnostic ]
##                                                { Auth-Session-State }
##                                                { Origin-Host }
##                                                { Origin-Realm }
##                                                [ OC-Supported-Features ]
##                                                [ OC-OLR ]
##                                                * [Supported-Features]
##                                                [ Authentication-Info ]  
##                                                *[ Failed-AVP ]
##                                                *[ Proxy-Info ]
##                                                *[ Route-Record ]
##
class DiamAuthenticationInformationAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 vendor_specific_app_id=None,
                 result_code=None,
                 experimental_result=None,
                 error_diagnostic=None,
                 oc_supported_features=None,
                 oc_olr=None,
                 supported_features=None,
                 authentication_info=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.AUTHENTICATION_INFORMATION_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.auth_session_state = auth_session_state
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.error_diagnostic = error_diagnostic
        self.oc_olr = oc_olr
        self.authentication_info = authentication_info
        self.failed_avp = failed_avp
        self.vendor_specific_app_id = vendor_specific_app_id
        self.oc_supported_features = oc_supported_features
        self.supported_features = supported_features
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

    def get_result_code(self):
        return self.result_code

    def get_experimental_result(self):
        return self.experimental_result

    def get_error_diagnostic(self):
        return self.error_diagnostic

    def get_oc_olr(self):
        return self.oc_olr

    def get_authentication_info(self):
        return self.authentication_info

    def get_failed_avp(self):
        return self.failed_avp

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_oc_supported_features(self):
        return self.oc_supported_features

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

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_result_code(self, value):
        self.result_code = value

    def set_experimental_result(self, value):
        self.experimental_result = value

    def set_error_diagnostic(self, value):
        self.error_diagnostic = value

    def set_oc_olr(self, value):
        self.oc_olr = value

    def set_authentication_info(self, value):
        self.authentication_info = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_oc_supported_features(self, value):
        self.oc_supported_features = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value

    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('AIA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('AIA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('AIA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)

        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('AIA: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.supported_features is not None:
            if not isinstance(self.supported_features, list):
                self.supported_features = [self.supported_features]
                
            for sf in self.supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.SUPPORTED_FEATURES, sf['value'])
                    else:
                        vendor = 0
                        if 'vendor' in sf :
                            vendor = sf['vendor'] 
                        topass = {'feature_list_id':None,
                                  'feature_list':None}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'feature-list-id':
                                topass['feature_list_id'] = savp
                            if savp['name'] == 'feature-list':
                                topass['feature_list'] = savp
                                
                        avp = SupportedFeaturesAVP(vendor, 
                                                   topass['feature_list_id'], 
                                                   topass['feature_list'])
                        avp.setFlags(sf['flags'])
                    self.addAVP(avp)
        
        if self.vendor_specific_app_id is not None:
            if not isinstance(self.vendor_specific_app_id, list):
                self.vendor_specific_app_id = [self.vendor_specific_app_id]
                
            for vsid in self.vendor_specific_app_id:
                if vsid is not None:
                    if 'type' in vsid and vsid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.VENDOR_SPECIFIC_APPLICATION_ID, vsid['value'])
                    else:
                        vendor = 0
                        if 'vendor' in vsid :
                            vendor = vsid['vendor']                         
                        topass = {'auth_app_id':None,
                                  'acct_app_id':None}
                        
                        for vavp in vsid['avps']:
                            if vavp['name'] == 'auth-application-id':
                                topass['auth_app_id'] = vavp
                            if vavp['name'] == 'acct-application-id':
                                topass['acct_app_id'] = vavp
                            
                        avp = VendorSpecificApplicationIDAVP(topass['auth_app_id'], 
                                                             topass['acct_app_id'], 
                                                             vendor)
                        avp.setFlags(vsid['flags'])
                        
                    self.addAVP(avp)

        if self.oc_supported_features is not None:
            if not isinstance(self.oc_supported_features, list):
                self.oc_supported_features = [self.oc_supported_features]
                
            for sf in self.oc_supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.OC_SUPPORTED_FEATURES, sf['value'])
                    else:
                        vendor = 0
                        if 'vendor' in sf :
                            vendor = sf['vendor']                         
                        oc_feature_vector = None
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'oc-feature-vector':
                                oc_feature_vector = savp
                                
                        avp = OCSupportedFeaturesAVP(oc_feature_vector, vendor)
                        avp.setFlags(sf['flags'])
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
            
        if self.error_diagnostic is not None:
            if 'type' in self.error_diagnostic and self.error_diagnostic['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ERROR_DIAGNOSTIC, self.error_diagnostic['value'])
            else:
                avp = ErrorDiagnosticAVP.tele(self.error_diagnostic['value'])
                avp.setFlags(self.error_diagnostic['flags'])
                if 'vendor' in self.error_diagnostic:
                    avp.setVendorID(self.error_diagnostic['vendor'])
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
        
        if self.oc_olr is not None:
            if 'type' in self.oc_olr and self.oc_olr['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.OC_OLR, self.oc_olr['value'])
            else:
                avp = OCOLRAVP(self.oc_olr['value'])
                avp.setFlags(self.oc_olr['flags'])
                if 'vendor' in self.oc_olr:
                    avp.setVendorID(self.oc_olr['vendor'])
            self.addAVP(avp)
        
        if self.authentication_info is not None:
            if 'type' in self.authentication_info and self.authentication_info['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.AUTHENTICATION_INFO, self.authentication_info['value'])
            else:
                logging.warning(FUNC() + ': AIA : Authentication-Information AVP NOT YET IMPLEMENTED')
        
        if self.proxy_info is not None:
            if not isinstance(self.proxy_info, list):
                self.proxy_info = [self.proxy_info]
                
            for pi in self.proxy_info:
                if pi is not None:
                    if 'type' in pi and pi['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.PROXY_INFO, pi['value'])
                    else:
                        vendor = 0
                        if 'vendor' in pi :
                            vendor = pi['vendor']                         
                        topass = {'proxy_host':None,
                                  'proxy_state':None}
                        
                        for pavp in pi['avps']:
                            if pavp['name'] == 'proxy-host':
                                topass['proxy_host'] = pavp
                            if pavp['name'] == 'proxy-state':
                                topass['proxy_state'] = pavp
                            
                        avp = ProxyInfoAVP(topass['proxy_host'], topass['proxy_state'], 
                                           vendor)
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
''' /3GPP: AUTHENTICATION INFORMATION '''

''' 3GPP: INSERT SUBSCRIBER DATA '''
##
## @brief      Class that defines a DIAMETER Message 
##    
##          < Insert-Subscriber-Data-Request> ::= < Diameter Header: 319, REQ, PXY, 16777251 >
##                                            < Session-Id >
##                                            [ Vendor-Specific-Application-Id ]
##                                            { Auth-Session-State }
##                                            { Origin-Host }
##                                            { Origin-Realm }
##                                            { Destination-Host }
##                                            { Destination-Realm }
##                                            { User-Name }
##                                            *[ Supported-Features]
##                                            { Subscription-Data}
##                                            [ IDR-Flags ]
##                                            *[ Reset-ID ]
##                                            *[ Proxy-Info ]
##                                            *[ Route-Record ]
##
class DiamInsertSubscriberDataRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 destination_host,
                 destination_realm,
                 user_name,
                 subscription_data,
                 vendor_specific_app_id=None,
                 supported_features=None,
                 idr_flags=None,
                 reset_id=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.INSERT_SUBSCRIBER_DATA_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_host = destination_host
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.user_name = user_name
        self.subscription_data = subscription_data
        self.idr_flags = idr_flags
        self.reset_id = reset_id
        self.supported_features = supported_features
        self.vendor_specific_app_id = vendor_specific_app_id
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

    def get_destination_host(self):
        return self.destination_host

    def get_destination_realm(self):
        return self.destination_realm

    def get_auth_session_state(self):
        return self.auth_session_state

    def get_user_name(self):
        return self.user_name

    def get_subscription_data(self):
        return self.subscription_data

    def get_idr_flags(self):
        return self.idr_flags

    def get_reset_id(self):
        return self.reset_id

    def get_supported_features(self):
        return self.supported_features

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

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

    def set_destination_host(self, value):
        self.destination_host = value

    def set_destination_realm(self, value):
        self.destination_realm = value

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_user_name(self, value):
        self.user_name = value

    def set_subscription_data(self, value):
        self.subscription_data = value

    def set_idr_flags(self, value):
        self.idr_flags = value

    def set_reset_id(self, value):
        self.reset_id = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('IDR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('IDR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('IDR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.destination_host is None:
            raise MissingMandatoryAVPException('IDR: The Destination-Host AVP is MANDATORY')
        avp = DestinationHostAVP(self.destination_host['value'])
        avp.setFlags(self.destination_host['flags'])
        if 'vendor' in self.destination_host:
            avp.setVendorID(self.destination_host['vendor'])
        self.addAVP(avp)
        
        if self.destination_realm is None:
            raise MissingMandatoryAVPException('IDR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('IDR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.user_name is None:
            raise MissingMandatoryAVPException('IDR: The User-Name AVP is MANDATORY')
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
                        vendor = 0
                        if 'vendor' in sf :
                            vendor = sf['vendor']                         
                        topass = {'feature_list_id':None,
                                  'feature_list':None}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'feature-list-id':
                                topass['feature_list_id'] = savp
                            if savp['name'] == 'feature-list':
                                topass['feature_list'] = savp
     
                                
                        avp = SupportedFeaturesAVP(vendor, 
                                                   topass['feature_list_id'], 
                                                   topass['feature_list'])
                        avp.setFlags(sf['flags'])
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
                        vendor = 0
                        if 'vendor' in vsid :
                            vendor = vsid['vendor'] 
                        for vavp in vsid['avps']:
                            if vavp['name'] == 'auth-application-id':
                                topass['auth_app_id'] = vavp
                            if vavp['name'] == 'acct-application-id':
                                topass['acct_app_id'] = vavp
                            if vavp['name'] == 'vendor-id':
                                topass['vendor_id'] = vavp
                            
                        avp = VendorSpecificApplicationIDAVP(topass['auth_app_id'], 
                                                             topass['acct_app_id'], 
                                                             vendor)
                        avp.setFlags(vsid['flags'])
                    self.addAVP(avp)
                
        if self.reset_id is not None:
            if not isinstance(self.reset_id, list):
                self.reset_id = [self.reset_id]
                
            for ri in self.reset_id:
                if ri is not None:
                    if 'type' in ri and ri['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.RESET_ID, ri['value'])
                    else:
                        avp = ResetIDAVP(ri['value'])
                        avp.setFlags(ri['flags'])
                        if 'vendor_id' in ri:
                            avp.setVendorID(ri['vendor'])
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
                        vendor = 0
                        if 'vendor' in pi :
                            vendor = pi['vendor']                         
                        for pavp in pi['avps']:
                            if pavp['name'] == 'proxy-host':
                                topass['proxy_host'] = pavp
                            if pavp['name'] == 'proxy-state':
                                topass['proxy_state'] = pavp
                            if pavp['name'] == 'vendor-id':
                                topass['vendor_id'] = pavp
                            
                        avp = ProxyInfoAVP(topass['proxy_host'], topass['proxy_state'], 
                                           vendor)
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
        
        if self.subscription_data is None:
            raise MissingMandatoryAVPException('IDR: The Subscription-Data AVP is MANDATORY')
        if not isinstance(self.subscription_data, list):
            self.subscription_data = [self.subscription_data]
        
        for sd in self.subscription_data:
            if not isinstance(self.subscription_data, list):
                self.subscription_data = [self.subscription_data]
                
            for sd in self.subscription_data:
                if sd is not None:
                    if 'type' in sd and sd['type']=='raw':
                        print(type(sd['value']))
                        avp = GenericAVP(DiamAVPCodes.SUBSCRIPTION_DATA, sd['value'])
                    else:
                        '''TODO: add all the AVPs '''
                    self.addAVP(avp)
                
        if self.idr_flags is not None:
            if 'type' in self.idr_flags and self.idr_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.IDR_FLAGS, self.idr_flags['value'])
            else:
                avp = IDRFlagsAVP(self.idr_flags['value'])
                avp.setFlags(self.idr_flags['flags'])
                if 'vendor' not in self.idr_flags:
                    raise AVPParametersException('DSR: Vendor-Id for IDR-Flags is MANDATORY')
                avp.setVendorID(self.idr_flags['vendor'])
            self.addAVP(avp)

##
## @brief      Class that defines a DIAMETER Message 
##    
##          < Insert-Subscriber-Data-Answer> ::= < Diameter Header: 319, PXY, 16777251 >
##                                            < Session-Id >
##                                            [ Vendor-Specific-Application-Id ]
##                                            *[ Supported-Features ]
##                                            [ Result-Code ]
##                                            [ Experimental-Result ]
##                                            { Auth-Session-State }
##                                            { Origin-Host }
##                                            { Origin-Realm }
##                                            [ IMS-Voice-Over-PS-Sessions-Supported ]
##                                            [ Last-UE-Activity-Time ]
##                                            [ RAT-Type ]
##                                            [ IDA-Flags ]
##                                            [ EPS-User-State ]
##                                            [ EPS-Location-Information ]
##                                            [Local-Time-Zone ]
##                                            *[ Failed-AVP ]
##                                            *[ Proxy-Info ]
##                                            *[ Route-Record ]
##
class DiamInsertSubscriberDataAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 vendor_specific_app_id=None,
                 supported_features=None,
                 result_code=None,
                 experimental_result=None,
                 ims_voice_over_ps_sessions_supported=None,
                 last_ue_activity_time=None,
                 rat_type=None,
                 ida_flags=None,
                 eps_user_state=None,
                 eps_location_information=None,
                 local_time_zone=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.INSERT_SUBSCRIBER_DATA_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.auth_session_state = auth_session_state
        self.vendor_specific_app_id = vendor_specific_app_id
        self.supported_features = supported_features
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.ims_voice_over_ps_sessions_supported = ims_voice_over_ps_sessions_supported
        self.last_ue_activity_time = last_ue_activity_time
        self.rat_type = rat_type
        self.ida_flags = ida_flags
        self.eps_user_state = eps_user_state
        self.eps_location_information = eps_location_information
        self.local_time_zone = local_time_zone
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

    def get_supported_features(self):
        return self.supported_features

    def get_result_code(self):
        return self.result_code

    def get_experimental_result(self):
        return self.experimental_result

    def get_ims_voice_over_ps_sessions_supported(self):
        return self.ims_voice_over_ps_sessions_supported

    def get_last_ue_activity_time(self):
        return self.last_ue_activity_time

    def get_rat_type(self):
        return self.rat_type

    def get_ida_flags(self):
        return self.ida_flags

    def get_eps_user_state(self):
        return self.eps_user_state

    def get_eps_location_information(self):
        return self.eps_location_information

    def get_local_time_zone(self):
        return self.local_time_zone

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

    def set_supported_features(self, value):
        self.supported_features = value

    def set_result_code(self, value):
        self.result_code = value

    def set_experimental_result(self, value):
        self.experimental_result = value

    def set_ims_voice_over_ps_sessions_supported(self, value):
        self.ims_voice_over_ps_sessions_supported = value

    def set_last_ue_activity_time(self, value):
        self.last_ue_activity_time = value

    def set_rat_type(self, value):
        self.rat_type = value

    def set_ida_flags(self, value):
        self.ida_flags = value

    def set_eps_user_state(self, value):
        self.eps_user_state = value

    def set_eps_location_information(self, value):
        self.eps_location_information = value

    def set_local_time_zone(self, value):
        self.local_time_zone = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('IDA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('IDA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('IDA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('IDA: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
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
                        vendor = 0
                        if 'vendor' in sf :
                            vendor = sf['vendor'] 
                        for savp in sf['avps']:
                            if savp['name'] == 'feature-list-id':
                                topass['feature_list_id'] = savp
                            if savp['name'] == 'feature-list':
                                topass['feature_list'] = savp
                            if savp['name'] == 'vendor-id':
                                topass['vendor_id'] = savp
                                
                        avp = SupportedFeaturesAVP(vendor, topass['feature_list_id'], topass['feature_list'])
                        avp.setFlags(sf['flags'])
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
                        vendor = 0
                        if 'vendor' in vsid :
                            vendor = vsid['vendor']                         
                        for vavp in vsid['avps']:
                            if vavp['name'] == 'auth-application-id':
                                topass['auth_app_id'] = vavp
                            if vavp['name'] == 'acct-application-id':
                                topass['acct_app_id'] = vavp
                            if vavp['name'] == 'vendor-id':
                                topass['vendor_id'] = vavp
                            
                        avp = VendorSpecificApplicationIDAVP(topass['auth_app_id'], 
                                                             topass['acct_app_id'], 
                                                             vendor)
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
        
        if self.rat_type is not None:
            if 'type' in self.rat_type and self.rat_type['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.RAT, self.rat_type['value'])
            else:
                avp = RATAVP(self.rat_type['value'])
                avp.setFlags(self.rat_type['flags'])
                if 'vendor' in self.rat_type:
                    avp.setVendorID(self.rat_type['vendor'])
            self.addAVP(avp)
                
        if self.ims_voice_over_ps_sessions_supported is not None:
            if 'type' in self.ims_voice_over_ps_sessions_supported and self.ims_voice_over_ps_sessions_supported['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.IMS_VOICE_OVER_PS_SESSION_SUPPORTED, self.ims_voice_over_ps_sessions_supported['value'])
            else:
                avp = IMSVoiceOverPSSessionSupportedAVP(self.ims_voice_over_ps_sessions_supported['value'])
                avp.setFlags(self.ims_voice_over_ps_sessions_supported['flags'])
                if 'vendor' in self.ims_voice_over_ps_sessions_supported:
                    avp.setVendorID(self.ims_voice_over_ps_sessions_supported['vendor'])
            self.addAVP(avp)
        
        if self.last_ue_activity_time is not None:
            if 'type' in self.last_ue_activity_time and self.last_ue_activity_time['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LAST_UE_ACTIVITY_TIME, self.last_ue_activity_time['value'])
            else:
                avp = LastUEActivityTimeAVP(self.last_ue_activity_time['value'])
                avp.setFlags(self.last_ue_activity_time['flags'])
                if 'vendor' in self.last_ue_activity_time:
                    avp.setVendorID(self.last_ue_activity_time['vendor'])
            self.addAVP(avp)
        
        if self.ida_flags is not None:
            if 'type' in self.ida_flags and self.ida_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.IDA_FLAGS, self.ida_flags['value'])
            else:
                avp = IDAFlagsAVP(self.ida_flags['value'])
                avp.setFlags(self.ida_flags['flags'])
                if 'vendor' in self.ida_flags:
                    avp.setVendorID(self.ida_flags['vendor'])
            self.addAVP(avp)
        
        if self.eps_user_state is not None:
            if 'type' in self.eps_user_state and self.eps_user_state['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.EPS_USER_STATE, self.eps_user_state['value'])
            else:
                avp = EPSUserStateAVP(self.eps_user_state['value'])
                avp.setFlags(self.eps_user_state['flags'])
                if 'vendor' in self.eps_user_state:
                    avp.setVendorID(self.eps_user_state['vendor'])
            self.addAVP(avp)
        
        if self.eps_location_information is not None:
            if 'type' in self.eps_location_information and self.eps_location_information['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.EPS_LOCATION_INFORMATION, self.eps_location_information['value'])
            else:
                logging.warning(FUNC() + ': IDA : EPS-Location-Information AVP NOT YET IMPLEMENTED')
        
        if self.local_time_zone is not None:
            if 'type' in self.local_time_zone and self.local_time_zone['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.LOCAL_TIME_ZONE, self.local_time_zone['value'])
            else:
                avp = LocalTimeZoneAVP(self.local_time_zone['value'])
                avp.setFlags(self.local_time_zone['flags'])
                if 'vendor' in self.local_time_zone:
                    avp.setVendorID(self.local_time_zone['vendor'])
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
                        vendor = 0
                        if 'vendor' in pi :
                            vendor = pi['vendor'] 
                        for pavp in pi['avps']:
                            if pavp['name'] == 'proxy-host':
                                topass['proxy_host'] = pavp
                            if pavp['name'] == 'proxy-state':
                                topass['proxy_state'] = pavp
                            if pavp['name'] == 'vendor-id':
                                topass['vendor_id'] = pavp
                            
                        avp = ProxyInfoAVP(topass['proxy_host'], topass['proxy_state'], 
                                           vendor)
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
''' /3GPP: INSERT SUBSCRIBER DATA '''

''' 3GPP: DELETE SUBSCRIBER DATA '''
##
## @brief      Class that defines a DIAMETER Message 
##    
##          < Delete-Subscriber-Data-Request > ::= < Diameter Header: 320, REQ, PXY, 16777251 >
##                                                < Session-Id >
##                                                [ Vendor-Specific-Application-Id ]
##                                                { Auth-Session-State }
##                                                { Origin-Host }
##                                                { Origin-Realm }
##                                                { Destination-Host }
##                                                { Destination-Realm }
##                                                { User-Name }
##                                                *[ Supported-Features ]
##                                                { DSR-Flags }
##                                                *[ Context-Identifier ]
##                                                [ Trace-Reference ]
##                                                *[ TS-Code ]
##                                                *[ SS-Code ]
##                                                *[ Proxy-Info ]
##                                                *[ Route-Record ]
##
class DiamDeleteSubscriberDataRequest(DiamMessage):    
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 destination_host,
                 destination_realm,
                 user_name,
                 dsr_flags,
                 vendor_specific_app_id=None,
                 supported_features=None,
                 context_identifier=None,
                 trace_reference=None,
                 ts_code=None,
                 ss_code=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.DELETE_SUBSCRIBER_DATA_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_host = destination_host
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.user_name = user_name
        self.dsr_flags = dsr_flags
        self.context_identifier = context_identifier
        self.trace_reference = trace_reference
        self.ts_code = ts_code
        self.ss_code = ss_code
        self.supported_features = supported_features
        self.vendor_specific_app_id = vendor_specific_app_id
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

    def get_destination_host(self):
        return self.destination_host

    def get_destination_realm(self):
        return self.destination_realm

    def get_auth_session_state(self):
        return self.auth_session_state

    def get_user_name(self):
        return self.user_name

    def get_dsr_flags(self):
        return self.dsr_flags

    def get_context_identifier(self):
        return self.context_identifier

    def get_trace_reference(self):
        return self.trace_reference

    def get_ts_code(self):
        return self.ts_code

    def get_ss_code(self):
        return self.ss_code

    def get_supported_features(self):
        return self.supported_features

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

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

    def set_destination_host(self, value):
        self.destination_host = value

    def set_destination_realm(self, value):
        self.destination_realm = value

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_user_name(self, value):
        self.user_name = value

    def set_dsr_flags(self, value):
        self.dsr_flags = value

    def set_context_identifier(self, value):
        self.context_identifier = value

    def set_trace_reference(self, value):
        self.trace_reference = value

    def set_ts_code(self, value):
        self.ts_code = value

    def set_ss_code(self, value):
        self.ss_code = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('DSR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('DSR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('DSR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.destination_host is None:
            raise MissingMandatoryAVPException('DSR: The Destination-Host AVP is MANDATORY')
        avp = DestinationHostAVP(self.destination_host['value'])
        avp.setFlags(self.destination_host['flags'])
        if 'vendor' in self.destination_host:
            avp.setVendorID(self.destination_host['vendor'])
        self.addAVP(avp)
        
        if self.destination_realm is None:
            raise MissingMandatoryAVPException('DSR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('DSR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.user_name is None:
            raise MissingMandatoryAVPException('DSR: The User-Name AVP is MANDATORY')
        avp = UserNameAVP(self.user_name['value'])
        avp.setFlags(self.user_name['flags'])
        if 'vendor' in self.user_name:
            avp.setVendorID(self.user_name['vendor'])
        self.addAVP(avp)
        
        if self.dsr_flags is None:
            raise MissingMandatoryAVPException('DSR: The DSR-Flags AVP is MANDATORY')
        avp = DSRFlagsAVP(self.dsr_flags['value'])
        avp.setFlags(self.dsr_flags['flags'])
        if 'vendor' in self.dsr_flags:
            avp.setVendorID(self.dsr_flags['vendor'])
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
                        vendor = 0
                        if 'vendor' in sf :
                            vendor = sf['vendor']                         
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
                
        if self.context_identifier is not None:
            if not isinstance(self.context_identifier, list):
                self.context_identifier = [self.context_identifier]
                
            for ci in self.context_identifier:
                if ci is not None:
                    if 'type' in ci and ci['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.CONTEXT_IDENTIFIER, ci['value'])
                    else:
                        avp = ContextIentifierAVP(ci['value'])
                        avp.setFlags(ci['flags'])
                        if 'vendor_id' in ci:
                            avp.setVendorID(ci['vendor'])
                    self.addAVP(avp)
                
        if self.trace_reference is not None:
            if 'type' in self.trace_reference and self.trace_reference['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.TRACE_REFERENCE, self.trace_reference['value'])
            else:
                avp = TraceReferenceAVP(self.trace_reference['value'])
                avp.setFlags(self.trace_reference['flags'])
                if 'vendor' in self.trace_reference:
                    avp.setVendorID(self.trace_reference['vendor'])
            self.addAVP(avp)

        if self.ts_code is not None:
            if not isinstance(self.ts_code, list):
                self.ts_code = [self.ts_code]
            
            for ts in self.ts_code:
                if ts is not None:
                    if 'type' in ts and ts['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.TS_CODE, ts['value'])
                    else:
                        avp = TSCodeAVP(ts['value'])
                        avp.setFlags(ts['flags'])
                        if 'vendor' not in ts:
                            raise AVPParametersException('DSR: Vendor-ID for TS is MANDATORY')
                        avp.setVendorID(ts['vendor'])
                    self.addAVP(avp)
                    
        if self.ss_code is not None:
            if not isinstance(self.ss_code, list):
                self.ss_code = [self.ss_code]
                
            for ss in self.ss_code:
                if ss is not None:
                    if 'type' in ss and ss['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.SS_CODE, ss['value'])
                    else:
                        avp = SSCodeAVP(ss['value'])
                        avp.setFlags(ss['flags'])
                        if 'vendor' not in ss:
                            raise AVPParametersException('DSR: Vendor-ID for SS is MANDATORY')
                        avp.setVendorID(ss['vendor'])
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
##          < Delete-Subscriber-Data-Answer> ::= < Diameter Header: 320, PXY, 16777251 >
##                                            < Session-Id >
##                                            [ Vendor-Specific-Application-Id ]
##                                            *[ Supported-Features ]
##                                            [ Result-Code ]
##                                            [ Experimental-Result ]
##                                            { Auth-Session-State }
##                                            { Origin-Host }
##                                            { Origin-Realm }
##                                            [ DSA-Flags ]
##                                            *[ Failed-AVP ]
##                                            *[ Proxy-Info ]
##                                            *[ Route-Record ]
##
class DiamDeleteSubscriberDataAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 vendor_specific_app_id=None,
                 supported_features=None,
                 result_code=None,
                 experimental_result=None,
                 dsa_flags=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.DELETE_SUBSCRIBER_DATA_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.auth_session_state = auth_session_state
        self.vendor_specific_app_id = vendor_specific_app_id
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.dsa_flags = dsa_flags
        self.failed_avp = failed_avp
        self.supported_features = supported_features
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

    def get_dsa_flags(self):
        return self.dsa_flags

    def get_failed_avp(self):
        return self.failed_avp

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

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_result_code(self, value):
        self.result_code = value

    def set_experimental_result(self, value):
        self.experimental_result = value

    def set_dsa_flags(self, value):
        self.dsa_flags = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('DSA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('DSA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('DSA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('DSA: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
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
            
        if self.dsa_flags is not None:
            if 'type' in self.dsa_flags and self.dsa_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.DSA_FLAGS, self.dsa_flags['value'])
            else:
                avp = DSAFlagsAVP(self.dsa_flags['value'])
                avp.setFlags(self.dsa_flags['flags'])
                if 'vendor' in self.dsa_flags:
                    avp.setVendorID(self.dsa_flags['vendor'])
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
''' /3GPP: DELETE SUBSCRIBER DATA '''

''' 3GPP: PURGE UE '''
##
## @brief      Class that defines a DIAMETER Message 
##
##         < Purge-UE-Request> ::= < Diameter Header: 321, REQ, PXY, 16777251 >
##                                < Session-Id >
##                                [ Vendor-Specific-Application-Id ]
##                                { Auth-Session-State }
##                                { Origin-Host }
##                                { Origin-Realm }
##                                [ Destination-Host ]
##                                { Destination-Realm }
##                                { User-Name }
##                                [ OC-Supported-Features ]
##                                [ PUR-Flags ]
##                                *[ Supported-Features ]
##                                [ EPS-Location-Information ]
##                                *[ Proxy-Info ]
##                                *[ Route-Record ] 
##
class DiamPurgeUERequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 destination_realm,
                 user_name,
                 vendor_specific_app_id=None,
                 destination_host=None,
                 oc_supported_features=None,
                 pur_flags=None,
                 supported_features=None,
                 eps_location_information=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.PURGE_UE_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.user_name = user_name
        self.destination_host = destination_host
        self.vendor_specific_app_id = vendor_specific_app_id
        self.oc_supported_features = oc_supported_features
        self.pur_flags = pur_flags
        self.supported_features = supported_features
        self.eps_location_information = eps_location_information
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

    def get_user_name(self):
        return self.user_name

    def get_destination_host(self):
        return self.destination_host

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_oc_supported_features(self):
        return self.oc_supported_features

    def get_pur_flags(self):
        return self.pur_flags

    def get_supported_features(self):
        return self.supported_features

    def get_eps_location_information(self):
        return self.eps_location_information

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

    def set_user_name(self, value):
        self.user_name = value

    def set_destination_host(self, value):
        self.destination_host = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_oc_supported_features(self, value):
        self.oc_supported_features = value

    def set_pur_flags(self, value):
        self.pur_flags = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_eps_location_information(self, value):
        self.eps_location_information = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('PUR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('PUR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('PUR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)

        if self.destination_realm is None:
            raise MissingMandatoryAVPException('PUR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('PUR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.user_name is None:
            raise MissingMandatoryAVPException('PUR: The User-Name AVP is MANDATORY')
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
                
        if self.pur_flags is not None:
            if 'type' in self.pur_flags and self.pur_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.PUR_FLAGS, self.pur_flags['value'])
            else:
                avp = PURFlagsAVP(self.pur_flags['value'])
                avp.setFlags(self.pur_flags['flags'])
                if 'vendor' in self.pur_flags:
                    avp.setVendorID(self.pur_flags['vendor'])
            self.addAVP(avp)
            
        if self.eps_location_information is not None:
            if 'type' in self.eps_location_information and self.eps_location_information['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.EPS_LOCATION_INFORMATION, self.eps_location_information['value'])
            else:
                logging.warning(FUNC() + ': PUR : EPS-Location-Information AVP NOT YET IMPLEMENTED')
        
        if self.oc_supported_features is not None:
            if not isinstance(self.oc_supported_features, list):
                self.oc_supported_features = [self.oc_supported_features]
                
            for sf in self.oc_supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.OC_SUPPORTED_FEATURES, sf['value'])
                    else:
                        topass = {'oc_feature_vector':None,
                                  'vendor_id':0}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'oc-feature-vector':
                                topass['oc_feature_vector'] = savp
                            if savp['name'] == 'vendor-id':
                                topass['vendor_id'] = savp
                                
                        avp = OCSupportedFeaturesAVP(topass['oc_feature_vector'], topass['vendor_id'])
                        avp.setFlags(sf['flags'])
                    self.addAVP(avp)
        
        #if self.destination_host is not None:
        #    if 'type' in self.destination_host and self.destination_host['type']=='raw':
        #        avp = GenericAVP(DiamAVPCodes.DESTINATION_HOST, self.destination_host['value'])
        #    else:
        #        avp = DestinationHostAVP(self.destination_host['value'])
        #        avp.setFlags(self.destination_host['flags'])
        #        if 'vendor' in self.destination_host:
        #            avp.setVendorID(self.destination_host['vendor'])
        #    self.addAVP(avp)

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
##         < Purge-UE-Answer> ::= < Diameter Header: 321, PXY, 16777251 >
##                                < Session-Id >
##                                [ Vendor-Specific-Application-Id ]
##                                *[ Supported-Features ]
##                                [ Result-Code ]
##                                [ Experimental-Result ]
##                                { Auth-Session-State }
##                                { Origin-Host }
##                                { Origin-Realm }
##                                [ OC-Supported-Features ]
##                                [ OC-OLR ]
##                                [ PUA-Flags ]
##                                *[ AVP ]
##                                *[ Failed-AVP ]
##                                *[ Proxy-Info ]
##                                *[ Route-Record ]
##
class DiamPurgeUEAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 vendor_specific_app_id=None,
                 supported_features=None,
                 result_code=None,
                 experimental_result=None,
                 oc_supported_features=None,
                 oc_olr=None,
                 pua_flags=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.PURGE_UE_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.auth_session_state = auth_session_state
        self.vendor_specific_app_id = vendor_specific_app_id
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.oc_olr = oc_olr
        self.pua_flags = pua_flags
        self.failed_avp = failed_avp                 
        self.oc_supported_features = oc_supported_features
        self.supported_features = supported_features
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

    def get_oc_olr(self):
        return self.oc_olr

    def get_pua_flags(self):
        return self.pua_flags

    def get_failed_avp(self):
        return self.failed_avp

    def get_oc_supported_features(self):
        return self.oc_supported_features

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

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_result_code(self, value):
        self.result_code = value

    def set_experimental_result(self, value):
        self.experimental_result = value

    def set_oc_olr(self, value):
        self.oc_olr = value

    def set_pua_flags(self, value):
        self.pua_flags = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_oc_supported_features(self, value):
        self.oc_supported_features = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('PUA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('PUA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('PUA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('PUA: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
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
        
        if self.oc_olr is not None:
            if 'type' in self.oc_olr and self.oc_olr['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.OC_OLR, self.oc_olr['value'])
            else:
                avp = OCOLRAVP(self.oc_olr['value'])
                avp.setFlags(self.oc_olr['flags'])
                if 'vendor' in self.oc_olr:
                    avp.setVendorID(self.oc_olr['vendor'])
            self.addAVP(avp)
                
        if self.pua_flags is not None:
            if 'type' in self.pua_flags and self.pua_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.PUA_FLAGS, self.pua_flags['value'])
            else:
                avp = PUAFlagsAVP(self.pua_flags['value'])
                avp.setFlags(self.pua_flags['flags'])
                if 'vendor' in self.pua_flags:
                    avp.setVendorID(self.pua_flags['vendor'])
            self.addAVP(avp)

        if self.oc_supported_features is not None:
            if not isinstance(self.oc_supported_features, list):
                self.oc_supported_features = [self.oc_supported_features]
                
            for sf in self.oc_supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.OC_SUPPORTED_FEATURES, sf['value'])
                    else:
                        topass = {'oc_feature_vector':None,
                                  'vendor_id':0}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'oc-feature-vector':
                                topass['oc_feature_vector'] = savp
                            if savp['name'] == 'vendor-id':
                                topass['vendor_id'] = savp
                                
                        avp = OCSupportedFeaturesAVP(topass['oc_feature_vector'], topass['vendor_id'])
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
''' /3GPP: PURGE UE '''

''' 3GPP: RESET '''
##
## @brief      Class that defines a DIAMETER Message 
##    
##         < Reset-Request> ::= < Diameter Header: 322, REQ, PXY, 16777251 >
##                            < Session-Id >
##                            [ Vendor-Specific-Application-Id ]
##                            { Auth-Session-State }
##                            { Origin-Host }
##                            { Origin-Realm }
##                            { Destination-Host }
##                            { Destination-Realm }
##                            *[ Supported-Features ]
##                            *[ User-Id ]
##                            *[ Reset-ID ]
##                            *[ Proxy-Info ]
##                            *[ Route-Record ]
##
class DiamResetRequest(DiamMessage):    
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 destination_host,
                 destination_realm,
                 vendor_specific_app_id=None,
                 supported_features=None,
                 user_id=None,
                 reset_id=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.RESET_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_host = destination_host
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.vendor_specific_app_id = vendor_specific_app_id
        self.user_id = user_id
        self.reset_id = reset_id
        self.supported_features = supported_features
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

    def get_destination_host(self):
        return self.destination_host

    def get_destination_realm(self):
        return self.destination_realm

    def get_auth_session_state(self):
        return self.auth_session_state

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_user_id(self):
        return self.user_id

    def get_reset_id(self):
        return self.reset_id

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

    def set_destination_host(self, value):
        self.destination_host = value

    def set_destination_realm(self, value):
        self.destination_realm = value

    def set_auth_session_state(self, value):
        self.auth_session_state = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_user_id(self, value):
        self.user_id = value

    def set_reset_id(self, value):
        self.reset_id = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('RSR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('RSR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('RSR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)

        if self.destination_host is None:
            raise MissingMandatoryAVPException('RSR: The Destination-Host AVP is MANDATORY')
        avp = DestinationHostAVP(self.destination_host['value'])
        avp.setFlags(self.destination_host['flags'])
        if 'vendor' in self.destination_host:
            avp.setVendorID(self.destination_host['vendor'])
        self.addAVP(avp)

        if self.destination_realm is None:
            raise MissingMandatoryAVPException('RSR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('RSR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
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
                
        if self.reset_id is not None:
            if not isinstance(self.reset_id, list):
                self.reset_id = [self.reset_id]
                
            for ri in self.reset_id:
                if ri is not None:
                    if 'type' in ri and ri['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.RESET_ID, ri['value'])
                    else:
                        avp = ResetIDAVP(ri['value'])
                        avp.setFlags(ri['flags'])
                        if 'vendor_id' in ri:
                            avp.setVendorID(ri['vendor'])
                    self.addAVP(avp)
                
        if self.user_id is not None:
            if not isinstance(self.user_id, list):
                self.user_id = [self.user_id]
            for ui in self.user_id:
                ui['flags'] = 'V'
                if ui is not None:
                    if 'type' in ui and ui['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.USER_ID, ui['value'])
                    else:                    
                        avp = UserIDAVP(ui['value'])
                        avp.setFlags(ui['flags'])

                        if 'vendor_id' in ui or 'vendor' in ui:
                            avp.setVendorID(ui['vendor'])                    
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
##         < Reset-Answer> ::= < Diameter Header: 322, PXY, 16777251 >
##                            < Session-Id >
##                            [ Vendor-Specific-Application-Id ]
##                            *[ Supported-Features ]
##                            [ Result-Code ]
##                            [ Experimental-Result ]
##                            { Auth-Session-State }
##                            { Origin-Host }
##                            { Origin-Realm }
##                            *[ Failed-AVP ]
##                            *[ Proxy-Info ]
##                            *[ Route-Record ]
##
class DiamResetAnswer(DiamMessage):    
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 vendor_specific_app_id=None,
                 supported_features=None,
                 result_code=None,
                 experimental_result=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.RESET_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.auth_session_state = auth_session_state
        self.vendor_specific_app_id = vendor_specific_app_id
        self.supported_features = supported_features
        self.result_code = result_code
        self.experimental_result = experimental_result
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

    def get_supported_features(self):
        return self.supported_features

    def get_result_code(self):
        return self.result_code

    def get_experimental_result(self):
        return self.experimental_result

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

    def set_supported_features(self, value):
        self.supported_features = value

    def set_result_code(self, value):
        self.result_code = value

    def set_experimental_result(self, value):
        self.experimental_result = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('RSA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('RSA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('RSA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('RSA: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
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
''' /3GPP: RESET '''

''' 3GPP: NOTIFY '''
##
## @brief      Class that defines a DIAMETER Message 
##    
##         < Notify-Request> ::= < Diameter Header: 323, REQ, PXY, 16777251 >
##                            < Session-Id >
##                            [ Vendor-Specific-Application-Id ]
##                            { Auth-Session-State }
##                            { Origin-Host }
##                            { Origin-Realm }
##                            [ Destination-Host ]
##                            { Destination-Realm }
##                            { User-Name }
##                            [ OC-Supported-Features ]
##                            * [ Supported-Features ]
##                            [ Terminal-Information ]
##                            [ MIP6-Agent-Info ]
##                            [ Visited-Network-Identifier ]
##                            [ Context-Identifier ]
##                            [Service-Selection]
##                            [ Alert-Reason ]
##                            [ UE-SRVCC-Capability ]
##                            [ NOR-Flags ]
##                            [ Homogeneous-Support-of-IMS-Voice-Over-PS-Sessions ]
##                            *[ Proxy-Info ]
##                            *[ Route-Record ] 
##
class DiamNotifyRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 destination_realm,
                 user_name,
                 vendor_specific_app_id=None,
                 destination_host=None,
                 oc_supported_features=None,
                 supported_features=None,
                 terminal_information=None,
                 mip6_agent_info=None,
                 visited_network_identifier=None,
                 context_identifier=None,
                 service_selection=None,
                 alert_reason=None,
                 ue_srvcc_capability=None,
                 nor_flags=None,
                 homogeneous_support_ims_voice_over_ps_sessions=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.NOTIFY_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.destination_realm = destination_realm
        self.user_name = user_name
        self.vendor_specific_app_id = vendor_specific_app_id
        self.terminal_information = terminal_information
        self.mip6_agent_info = mip6_agent_info
        self.visited_network_identifier = visited_network_identifier
        self.context_identifier = context_identifier
        self.service_selection = service_selection
        self.alert_reason = alert_reason
        self.nor_flags = nor_flags
        self.supported_features = supported_features
        self.destination_host = destination_host
        self.oc_supported_features = oc_supported_features
        self.ue_srvcc_capability = ue_srvcc_capability
        self.homogeneous_support_ims_voice_over_ps_sessions = homogeneous_support_ims_voice_over_ps_sessions
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

    def get_user_name(self):
        return self.user_name

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_terminal_information(self):
        return self.terminal_information

    def get_mip6_agent_info(self):
        return self.mip6_agent_info

    def get_visited_network_identifier(self):
        return self.visited_network_identifier

    def get_context_identifier(self):
        return self.context_identifier

    def get_service_selection(self):
        return self.service_selection

    def get_alert_reason(self):
        return self.alert_reason

    def get_nor_flags(self):
        return self.nor_flags

    def get_supported_features(self):
        return self.supported_features

    def get_destination_host(self):
        return self.destination_host

    def get_oc_supported_features(self):
        return self.oc_supported_features

    def get_ue_srvcc_capability(self):
        return self.ue_srvcc_capability

    def get_homogeneous_support_ims_voice_over_ps_sessions(self):
        return self.homogeneous_support_ims_voice_over_ps_sessions

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

    def set_user_name(self, value):
        self.user_name = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_terminal_information(self, value):
        self.terminal_information = value

    def set_mip6_agent_info(self, value):
        self.mip6_agent_info = value

    def set_visited_network_identifier(self, value):
        self.visited_network_identifier = value

    def set_context_identifier(self, value):
        self.context_identifier = value

    def set_service_selection(self, value):
        self.service_selection = value

    def set_alert_reason(self, value):
        self.alert_reason = value

    def set_nor_flags(self, value):
        self.nor_flags = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_destination_host(self, value):
        self.destination_host = value

    def set_oc_supported_features(self, value):
        self.oc_supported_features = value

    def set_ue_srvcc_capability(self, value):
        self.ue_srvcc_capability = value

    def set_homogeneous_support_ims_voice_over_ps_sessions(self, value):
        self.homogeneous_support_ims_voice_over_ps_sessions = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('NOR: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('NOR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('NOR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)

        if self.destination_realm is None:
            raise MissingMandatoryAVPException('NOR: The Destination-Realm AVP is MANDATORY')
        avp = DestinationRealmAVP(self.destination_realm['value'])
        avp.setFlags(self.destination_realm['flags'])
        if 'vendor' in self.destination_realm:
            avp.setVendorID(self.destination_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('NOR: The Auth-Session-State AVP is MANDATORY')
        avp = AuthSessionStateAVP(int(self.auth_session_state['value']))
        avp.setFlags(self.auth_session_state['flags'])
        if 'vendor' in self.auth_session_state:
            avp.setVendorID(self.auth_session_state['vendor'])
        self.addAVP(avp)
        
        if self.user_name is None:
            raise MissingMandatoryAVPException('NOR: The User-Name AVP is MANDATORY')
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
        
        #if self.destination_host is not None:
        #    if 'type' in self.destination_host and self.destination_host['type']=='raw':
        #        avp = GenericAVP(DiamAVPCodes.DESTINATION_HOST, self.destination_host['value'])
        #    else:
        #        avp = DestinationHostAVP(self.destination_host['value'])
        #        avp.setFlags(self.destination_host['flags'])
        #        if 'vendor' in self.destination_host:
        #            avp.setVendorID(self.destination_host['vendor'])
        #    self.addAVP(avp)
        
        if self.oc_supported_features is not None:
            if not isinstance(self.oc_supported_features, list):
                self.oc_supported_features = [self.oc_supported_features]
                
            for sf in self.oc_supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.OC_SUPPORTED_FEATURES, sf['value'])
                    else:
                        topass = {'oc_feature_vector':None,
                                  'vendor_id':0}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'oc-feature-vector':
                                topass['oc_feature_vector'] = savp
                            if savp['name'] == 'vendor-id':
                                topass['vendor_id'] = savp
                                
                        avp = OCSupportedFeaturesAVP(topass['oc_feature_vector'], topass['vendor_id'])
                        avp.setFlags(sf['flags'])
                    self.addAVP(avp)
        
        if self.ue_srvcc_capability is not None:
            if 'type' in self.ue_srvcc_capability and self.ue_srvcc_capability['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.UE_SRVCC_CAPABILITY, self.ue_srvcc_capability['value'])
            else:
                avp = UESRVCCCapabilityAVP(self.ue_srvcc_capability['value'])
                avp.setFlags(self.ue_srvcc_capability['flags'])
                if 'vendor' in self.ue_srvcc_capability:
                    avp.setVendorID(self.ue_srvcc_capability['vendor'])
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
                 
        if self.terminal_information is not None:
            if not isinstance(self.terminal_information, list):
                self.terminal_information = [self.terminal_information]
                
            for ti in self.terminal_information:
                if ti is not None:
                    if 'type' in ti and ti['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.TERMINAL_INFORMATION, ti['value'])
                    else:
                        topass = {'imei':None,
                                  'meid_3gpp2':None,
                                  'software_version':None,
                                  'vendor_id':0}
                        
                        for tavp in ti['avps']:
                            if tavp['name'] == 'imei':
                                topass['imei'] = tavp
                            if tavp['name'] == '3gpp2-meid':
                                topass['meid_3gpp2'] = tavp
                            if tavp['name'] == 'software-version':
                                topass['software_version'] = tavp
                            if tavp['name'] == 'vendor-id':
                                topass['vendor_id'] = tavp
                            
                        avp = TerminalInformationAVP(topass['imei'], topass['meid_3gpp2'], topass['software_version'], topass['vendor_id'])
                        avp.setFlags(ti['flags'])
                    self.addAVP(avp)
            
        if self.mip6_agent_info is not None:
            if not isinstance(self.mip6_agent_info, list):
                self.mip6_agent_info = [self.mip6_agent_info]
                
            for mai in self.mip6_agent_info:
                if mai is not None:
                    if 'type' in mai and mai['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.MIP6_AGENT_INFO, mai['value'])
                    else:
                        topass = {'home_agent_address':None,
                                  'home_agent_host':None,
                                  'home_link_prefix':None,
                                  'vendor_id':0}
    
                        for mavp in mai['avps']:
                            if mavp['name'] == 'home-agent-address':
                                topass['home_agent_address'] = mavp
                            if mavp['name'] == 'home-agent-host':
                                topass['home_agent_host'] = mavp
                            if mavp['name'] == 'home-link-prefix':
                                topass['home_link_prefix'] = mavp
                            if mavp['name'] == 'vendor-id':
                                topass['vendor_id'] = mavp
                            
                        avp = MIP6AgentInfoAVP(topass['home_agent_address'], topass['home_agent_host'], topass['home_link_prefix'], topass['vendor_id'])
                        avp.setFlags(mai['flags'])
                    self.addAVP(avp)
            
        if self.visited_network_identifier is not None:
            if 'type' in self.visited_network_identifier and self.visited_network_identifier['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.VISITED_NETWORK_IDENTIFIER, self.visited_network_identifier['value'])
            else:
                avp = VisitedNetworkIdentifierAVP(self.visited_network_identifier['value'])
                avp.setFlags(self.visited_network_identifier['flags'])
                if 'vendor' in self.visited_network_identifier:
                    avp.setVendorID(self.visited_network_identifier['vendor'])
            self.addAVP(avp)
            
        if self.context_identifier is not None:
            if 'type' in self.context_identifier and self.context_identifier['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.CONTEXT_IDENTIFIER, self.context_identifier['value'])
            else:
                avp = ContextIentifierAVP(self.context_identifier['value'])
                avp.setFlags(self.context_identifier['flags'])
                if 'vendor' in self.context_identifier:
                    avp.setVendorID(self.context_identifier['vendor'])
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
            
        if self.alert_reason is not None:
            if 'type' in self.alert_reason and self.alert_reason['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, self.alert_reason['value'])
            else:
                avp = AlertReasonAVP(self.alert_reason['value'])
                avp.setFlags(self.alert_reason['flags'])
                if 'vendor' in self.alert_reason:
                    avp.setVendorID(self.alert_reason['vendor'])
            self.addAVP(avp)
            
        if self.nor_flags is not None:
            if 'type' in self.nor_flags and self.nor_flags['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.NOR_FLAGS, self.nor_flags['value'])
            else:
                avp = NORFlagsAVP(self.nor_flags['value'])
                avp.setFlags(self.nor_flags['flags'])
                if 'vendor' in self.nor_flags:
                    avp.setVendorID(self.nor_flags['vendor'])
            self.addAVP(avp)
        
        if self.homogeneous_support_ims_voice_over_ps_sessions is not None:
            if 'type' in self.homogeneous_support_ims_voice_over_ps_sessions and self.homogeneous_support_ims_voice_over_ps_sessions['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.HOMOGENEOUS_SUPPORT_OF_IMS_VOICE_OVER_PS_SESSIONS, self.homogeneous_support_ims_voice_over_ps_sessions['value'])
            else:
                avp = HomogeneousSupportIMSVoiceOverPSSessionsAVP(self.homogeneous_support_ims_voice_over_ps_sessions['value'])
                avp.setFlags(self.homogeneous_support_ims_voice_over_ps_sessions['flags'])
                if 'vendor' in self.homogeneous_support_ims_voice_over_ps_sessions:
                    avp.setVendorID(self.homogeneous_support_ims_voice_over_ps_sessions['vendor'])
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
##         < Notify-Answer> ::= < Diameter Header: 323, PXY, 16777251 >
##                            < Session-Id >
##                            [ Vendor-Specific-Application-Id ]
##                            [ Result-Code ]
##                            [ Experimental-Result ]
##                            { Auth-Session-State }
##                            { Origin-Host }
##                            { Origin-Realm }
##                            [ OC-Supported-Features ]
##                            [ OC-OLR ]
##                            *[ Supported-Features ]
##                            *[ Failed-AVP ]
##                            *[ Proxy-Info ]
##                            *[ Route-Record ] 
##
class DiamNotifyAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host, 
                 origin_realm,
                 vendor_specific_app_id=None,
                 result_code=None,
                 experimental_result=None,
                 oc_supported_features=None,
                 oc_olr=None,
                 supported_features=None,
                 failed_avp=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.NOTIFY_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.auth_session_state = auth_session_state
        self.vendor_specific_app_id = vendor_specific_app_id
        self.result_code = result_code
        self.experimental_result = experimental_result
        self.oc_olr = oc_olr
        self.failed_avp = failed_avp
        self.supported_features = supported_features
        self.oc_supported_features = oc_supported_features
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

    def get_oc_olr(self):
        return self.oc_olr

    def get_failed_avp(self):
        return self.failed_avp

    def get_supported_features(self):
        return self.supported_features

    def get_oc_supported_features(self):
        return self.oc_supported_features

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

    def set_oc_olr(self, value):
        self.oc_olr = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_supported_features(self, value):
        self.supported_features = value

    def set_oc_supported_features(self, value):
        self.oc_supported_features = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
        if self.session_id is None:
            raise MissingMandatoryAVPException('NOA: The Session-ID AVP is MANDATORY')
        avp = SessionIDAVP(self.session_id['value'])
        avp.setFlags(self.session_id['flags'])
        if 'vendor' in self.session_id:
            avp.setVendorID(self.session_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('NOA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('NOA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.auth_session_state is None:
            raise MissingMandatoryAVPException('NOA: The Auth-Session-State AVP is MANDATORY')
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
        
        if self.oc_olr is not None:
            if 'type' in self.oc_olr and self.oc_olr['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.OC_OLR, self.oc_olr['value'])
            else:
                avp = OCOLRAVP(self.oc_olr['value'])
                avp.setFlags(self.oc_olr['flags'])
                if 'vendor' in self.oc_olr:
                    avp.setVendorID(self.oc_olr['vendor'])
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
        
        if self.oc_supported_features is not None:
            if not isinstance(self.oc_supported_features, list):
                self.oc_supported_features = [self.oc_supported_features]
                
            for sf in self.oc_supported_features:
                if sf is not None:
                    if 'type' in sf and sf['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.OC_SUPPORTED_FEATURES, sf['value'])
                    else:
                        topass = {'oc_feature_vector':None,
                                  'vendor_id':0}
                        
                        for savp in sf['avps']:
                            if savp['name'] == 'oc-feature-vector':
                                topass['oc_feature_vector'] = savp
                            if savp['name'] == 'vendor-id':
                                topass['vendor_id'] = savp
                                
                        avp = OCSupportedFeaturesAVP(topass['oc_feature_vector'], topass['vendor_id'])
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
''' /3GPP: NOTIFY '''

''' 3GPP: ME IDENTITY CHECK '''
##
## @brief      Class that defines a DIAMETER Message 
##    
##         < ME-Identity-Check-Request > ::= < Diameter Header: 324, REQ, PXY, 16777252 >
##                                        < Session-Id >
##                                        [ Vendor-Specific-Application-Id ]
##                                        { Auth-Session-State }
##                                        { Origin-Host }
##                                        { Origin-Realm }
##                                        [ Destination-Host ]
##                                        { Destination-Realm }
##                                        { Terminal-Information }
##                                        [ User-Name ]
##                                        *[ Proxy-Info ]
##                                        *[ Route-Record ]
##
class DiamMEIdentityCheckRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 destination_realm,
                 terminal_information,
                 vendor_specific_app_id=None,
                 destination_host=None,
                 user_name=None,
                 proxy_info=None,
                 route_record=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.ME_IDENTITY_CHECK_3GPP, app_id)

        self.session_id = session_id
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.destination_realm = destination_realm
        self.auth_session_state = auth_session_state
        self.destination_realm = destination_realm        
        self.terminal_information = terminal_information
        self.vendor_specific_app_id = vendor_specific_app_id
        self.destination_host = destination_host
        self.user_name = user_name
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

    def get_terminal_information(self):
        return self.terminal_information

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_destination_host(self):
        return self.destination_host

    def get_user_name(self):
        return self.user_name

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

    def set_terminal_information(self, value):
        self.terminal_information = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_destination_host(self, value):
        self.destination_host = value

    def set_user_name(self, value):
        self.user_name = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
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
        
        if self.terminal_information is None:
            raise MissingMandatoryAVPException('ECR: The Terminal-Information AVP is MANDATORY')
        if not isinstance(self.terminal_information, list):
            self.terminal_information = [self.terminal_information]
            
        for ti in self.terminal_information:
            if ti is not None:
                topass = {'imei':None,
                          'meid_3gpp2':None,
                          'software_version':None,
                          'vendor_id':0}
                
                for tavp in ti['avps']:
                    if tavp['name'] == 'imei':
                        topass['imei'] = tavp
                    if tavp['name'] == '3gpp2-meid':
                        topass['meid_3gpp2'] = tavp
                    if tavp['name'] == 'software-version':
                        topass['software_version'] = tavp
                    if tavp['name'] == 'vendor-id':
                        topass['vendor_id'] = tavp
                    
                avp = TerminalInformationAVP(topass['imei'], topass['meid_3gpp2'], topass['software_version'], topass['vendor_id'])
                avp.setFlags(ti['flags'])
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
##         < ME-Identity-Check-Answer> ::= < Diameter Header: 324, PXY, 16777252 >
##                                        < Session-Id >
##                                        [ Vendor-Specific-Application-Id ]
##                                        [ Result-Code ]
##                                        [ Experimental-Result ]
##                                        { Auth-Session-State }
##                                        { Origin-Host }
##                                        { Origin-Realm }
##                                        [ Equipment-Status ]
##                                        *[ Failed-AVP ]
##                                        *[ Proxy-Info ] 
##                                        *[ Route-Record ]
##
class DiamMEIdentityCheckAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 session_id,
                 auth_session_state,
                 origin_host,
                 origin_realm,
                 vendor_specific_app_id=None,
                 result_code=None,
                 experimental_result=None,
                 equipment_status=None,
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
        self.equipment_status = equipment_status
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

    def get_equipment_status(self):
        return self.equipment_status

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

    def set_equipment_status(self, value):
        self.equipment_status = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_proxy_info(self, value):
        self.proxy_info = value

    def set_route_record(self, value):
        self.route_record = value
    
    def generateMessage(self):
        self.avps = []
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
            
        if self.equipment_status is not None:
            if 'type' in self.equipment_status and self.equipment_status['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.EQUIPMENT_STATUS, self.equipment_status['value'])
            else:
                avp = EquipmentStatusAVP(self.equipment_status['value'])
                avp.setFlags(self.equipment_status['flags'])
                if 'vendor' in self.equipment_status:
                    avp.setVendorID(self.equipment_status['vendor'])
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
''' /3GPP: ME IDENTITY CHECK '''
