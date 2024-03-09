from ..diameter.diameter_message import DiamMessage
import struct
from ..diameter.diamCommandCodes import DiamCommandCodes
import logging
from ..diameter.diamAVPExceptions import MissingMandatoryAVPException
from ..diameter.diam_avp_data import *
from ..commons import FUNC

##
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##

##
## @brief      Class that handles a generic Diameter message
##
class DiamGenericMessage(DiamMessage):
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.hdata = bytearray.fromhex(raw_data)
        self.is_request = False
        self.is_proxiable = False 
        self.is_error = False
        self.is_retrasmitted = False
        
        # analyze bytes to get infos
        (b1, b2, app_id, hophop_id, endend_id) = struct.unpack("!LLLLL", self.hdata[:20])
        self.cmd_code = int(b2 & 0x00ffffff)
        
        DiamMessage.__init__(self, self.cmd_code, app_id)
        self.setHopHopID(hophop_id)
        self.setEndEndID(endend_id)
        
        self.message_length = b1 & 0x00ffffff
        self.version = int(b1>>24)
        self.flags = int(b2 >> 24)
        
        bflags = bin(self.flags)[2:]
        n = 8-len(bflags)
        if n > 0:
            bflags = '0'*n + bflags
        if bflags[0] == '1':
            self.is_request = True
        if bflags[1] == '1':
            self.is_proxiable = True
        if bflags[2] == '1':
            self.is_error = True
        if bflags[3] == '1':
            self.is_retrasmitted = True
    
    def getMessageLength(self):
        return self.message_length
    
    def generateByteMessage(self):
        return self.hdata
    
    def generateStringfiedMessage(self):
        return "".join("{:02x}".format(ord(c)) for c in self.hdata)
    
    def str_prefix__(self):
        """Return a string prefix suitable for building a __str__ result"""
        s = str(self.getCommandCode())
        if self.isRequest():
            s+= ".r"
        if self.isProxiable():
            s+= ".p"
        if self.isError():
            s+= ".e"
        if self.isRetrasmission():
            s+= ".t"
        return s
    
    def __str__(self):
        return self.str_prefix__() + " - " + str(self.message_length)

''' CAPABILITIES EXCHANGE '''
##
## @brief      Class that defines a DIAMETER Message
##    
##          <CER> ::= < Diameter Header: 257, REQ >
##                { Origin-Host }
##                { Origin-Realm }
##             1* { Host-IP-Address }
##                { Vendor-Id }
##                { Product-Name }
##                [ Origin-State-Id ]
##              * [ Supported-Vendor-Id ]
##              * [ Auth-Application-Id ]
##              * [ Inband-Security-Id ]
##              * [ Acct-Application-Id ]
##              * [ Vendor-Specific-Application-Id ]
##                [ Firmware-Revision ]
##
class DiamCapabilitiesExchangeRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 origin_host, 
                 origin_realm, 
                 host_ip, 
                 vendor_id, 
                 product_name, 
                 origin_state_id=None, 
                 supported_vendor_id=None, 
                 auth_app_id=None,
                 inband_security_id=None, 
                 acct_app_id=None, 
                 vendor_specific_app_id=None, 
                 firmware=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.CAPABILITIES_EXCHANGE, app_id)

        self.origin_host = origin_host
        self.origin_realm = origin_realm
        
        self.host_ip = host_ip
        if not isinstance(self.host_ip, list):
            self.host_ip = [self.host_ip]
        
        self.vendor_id = vendor_id
        if self.vendor_id == 0:
            logging.warning(FUNC() + ': CER : The Vendor-ID value of zero is reserved and indicates that this field is ignored.')
        
        self.product_name = product_name
        
        self.origin_state_id = origin_state_id
        self.supported_vendor_id = supported_vendor_id
        self.auth_app_id = auth_app_id
        self.inband_security_id = inband_security_id
        self.acct_app_id = acct_app_id
        self.vendor_specific_app_id = vendor_specific_app_id
        self.firmware = firmware
        
        self.setRequestFlag(True)

    def get_origin_host(self):
        return self.origin_host

    def get_origin_realm(self):
        return self.origin_realm

    def get_host_ip(self):
        return self.host_ip

    def get_vendor_id(self):
        return self.vendor_id

    def get_product_name(self):
        return self.product_name

    def get_origin_state_id(self):
        return self.origin_state_id

    def get_supported_vendor_id(self):
        return self.supported_vendor_id

    def get_auth_app_id(self):
        return self.auth_app_id

    def get_inband_security_id(self):
        return self.inband_security_id

    def get_acct_app_id(self):
        return self.acct_app_id

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_firmware(self):
        return self.firmware

    def set_origin_host(self, value):
        self.origin_host = value

    def set_origin_realm(self, value):
        self.origin_realm = value

    def set_host_ip(self, value):
        self.host_ip = value

    def set_vendor_id(self, value):
        self.vendor_id = value

    def set_product_name(self, value):
        self.product_name = value

    def set_origin_state_id(self, value):
        self.origin_state_id = value

    def set_supported_vendor_id(self, value):
        self.supported_vendor_id = value

    def set_auth_app_id(self, value):
        self.auth_app_id = value

    def set_inband_security_id(self, value):
        self.inband_security_id = value

    def set_acct_app_id(self, value):
        self.acct_app_id = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_firmware(self, value):
        self.firmware = value

    def generateMessage(self):
        self.avps = []
        if self.origin_host is None:
            raise MissingMandatoryAVPException('CER: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('CER: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.product_name is None:
            raise MissingMandatoryAVPException('CER: The Product-Name AVP is MANDATORY')
        avp = ProductNameAVP(self.product_name['value'])
        avp.setFlags(self.product_name['flags'])
        if 'vendor' in self.product_name:
            avp.setVendorID(self.product_name['vendor'])
        self.addAVP(avp)
        
        if self.host_ip is None:
            raise MissingMandatoryAVPException('CER: The Host-IP-Address AVP is MANDATORY')
        for ip in self.host_ip:
            if ip is not None:
                avp = HostIPAddressAVP(ip['value'])
                avp.setFlags(ip['flags'])
                if 'vendor' in self.host_ip:
                    avp.setVendorID(self.host_ip['vendor'])
                self.addAVP(avp)
        
        if self.vendor_id is None:
            raise MissingMandatoryAVPException('CER: The Vendor-ID AVP is MANDATORY')
        avp = VendorIDAVP(int(self.vendor_id['value']))
        avp.setFlags(self.vendor_id['flags'])
        if 'vendor' in self.vendor_id:
            avp.setVendorID(self.vendor_id['vendor'])
        self.addAVP(avp)
        
        if self.origin_state_id is not None:
            if 'type' in self.origin_state_id and self.origin_state_id['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ORIGIN_STATE_ID, self.origin_state_id['value'])
            else:
                avp = OriginStateIDAVP(int(self.origin_state_id['value']))
                avp.setFlags(self.origin_state_id['flags'])
                if 'vendor' in self.origin_state_id:
                    avp.setVendorID(self.origin_state_id['vendor'])
            self.addAVP(avp)
            
        if self.supported_vendor_id is not None:
            if not isinstance(self.supported_vendor_id, list):
                self.supported_vendor_id = [self.supported_vendor_id]
                
            for vid in self.supported_vendor_id:
                if vid is not None:
                    if 'type' in vid and vid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.SUPPORTED_VENDOR_ID, vid['value'])
                    else:
                        avp = SupportedVendorIDAVP(int(vid['value']))
                        avp.setFlags(vid['flags'])
                        if 'vendor' in vid:
                            avp.setVendorID(vid['vendor'])
                    self.addAVP(avp)
        
        if self.auth_app_id is not None:
            if not isinstance(self.auth_app_id, list):
                self.auth_app_id = [self.auth_app_id]
                
            for aid in self.auth_app_id:
                if aid is not None:
                    if 'type' in aid and aid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.AUTH_APPLICATION_ID, aid['value'])
                    else:
                        avp = AuthApplicationIDAVP(int(aid['value']))
                        avp.setFlags(aid['flags'])
                        if 'vendor' in aid:
                            avp.setVendorID(aid['vendor'])
                    self.addAVP(avp)
            
        if self.inband_security_id is not None:
            if not isinstance(self.inband_security_id, list):
                self.inband_security_id = [self.inband_security_id]
                
            for iid in self.inband_security_id:
                if iid is not None:
                    if 'type' in iid and iid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.INBAND_SECURITY_ID, iid['value'])
                    else:
                        avp = InbandSecurityIDAVP(int(iid['value']))
                        avp.setFlags(iid['flags'])
                        if 'vendor' in iid:
                            avp.setVendorID(iid['vendor'])
                    self.addAVP(avp)
            
        if self.acct_app_id is not None:
            if not isinstance(self.acct_app_id, list):
                self.acct_app_id = [self.acct_app_id]
                
            for aid in self.acct_app_id:
                if aid is not None:
                    if 'type' in aid and aid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.ACCT_APPLICATION_ID, aid['value'])
                    else:
                        avp = AcctApplicationIDAVP(int(aid['value']))
                        avp.setFlags(aid['flags'])
                        if 'vendor' in aid:
                            avp.setVendorID(aid['vendor'])
                    self.addAVP(avp)
        
        if self.vendor_specific_app_id is not None:
            if not isinstance(self.vendor_specific_app_id, list):
                self.vendor_specific_app_id = [self.vendor_specific_app_id]
                
            for vsid in self.vendor_specific_app_id:
                if vsid is not None:
                    if 'type' in vsid and vsid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.VENDOR_SPECIFIC_APPLICATION_ID, vsid['value'])
                    else:
                        topass = {'auth_app_id': None,
                                  'acct_app_id': None,
                                  'vendor_id': 0}
                        
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
            
        if self.firmware is not None:
            if 'type' in self.firmware and self.firmware['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.FIRMWARE_REVISION, self.firmware['value'])
            else:
                avp = FirmwareRevisionAVP(int(self.firmware['value']))
                avp.setFlags(self.firmware['flags'])
                if 'vendor' in self.firmware:
                    avp.setVendorID(self.firmware['vendor'])
            self.addAVP(avp)

##
## @brief      Class that defines a DIAMETER Message 
##    
##          <CEA> ::= < Diameter Header: 257 >
##                { Result-Code }
##                { Origin-Host }
##                { Origin-Realm }
##             1* { Host-IP-Address }
##                { Vendor-Id }
##                { Product-Name }
##                [ Origin-State-Id ]
##                [ Error-Message ]
##              * [ Failed-AVP ]
##              * [ Supported-Vendor-Id ]
##              * [ Auth-Application-Id ]
##              * [ Inband-Security-Id ]
##              * [ Acct-Application-Id ]
##              * [ Vendor-Specific-Application-Id ]
##                [ Firmware-Revision ]
##              * [ AVP ]
##
class DiamCapabilitiesExchangeAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 result_code, 
                 origin_host, 
                 origin_realm, 
                 host_ip, 
                 vendor_id, 
                 product_name, 
                 origin_state_id=None, 
                 error_message=None, 
                 failed_avp=[], 
                 supported_vendor_id=[], 
                 auth_app_id=[],
                 inband_security_id=[], 
                 acct_app_id=[], 
                 vendor_specific_app_id=[], 
                 firmware=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.CAPABILITIES_EXCHANGE, app_id)

        self.result_code = result_code
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        
        self.host_ip = host_ip
        if not isinstance(self.host_ip, list):
            self.host_ip = [self.host_ip]
        
        self.vendor_id = vendor_id
        if self.vendor_id == 0:
            logging.warning(FUNC() + ': CEA : The Vendor-ID value of zero is reserved and indicates that this field is ignored.')
        
        self.product_name = product_name
        self.origin_state_id = origin_state_id
        self.error_message = error_message
        self.failed_avp = failed_avp
        self.supported_vendor_id = supported_vendor_id
        self.auth_app_id = auth_app_id
        self.inband_security_id = inband_security_id
        self.acct_app_id = acct_app_id
        self.vendor_specific_app_id = vendor_specific_app_id
        self.firmware = firmware

    def get_result_code(self):
        return self.result_code

    def get_origin_host(self):
        return self.origin_host

    def get_origin_realm(self):
        return self.origin_realm

    def get_host_ip(self):
        return self.host_ip

    def get_vendor_id(self):
        return self.vendor_id

    def get_product_name(self):
        return self.product_name

    def get_origin_state_id(self):
        return self.origin_state_id

    def get_error_message(self):
        return self.error_message

    def get_failed_avp(self):
        return self.failed_avp

    def get_supported_vendor_id(self):
        return self.supported_vendor_id

    def get_auth_app_id(self):
        return self.auth_app_id

    def get_inband_security_id(self):
        return self.inband_security_id

    def get_acct_app_id(self):
        return self.acct_app_id

    def get_vendor_specific_app_id(self):
        return self.vendor_specific_app_id

    def get_firmware(self):
        return self.firmware

    def set_result_code(self, value):
        self.result_code = value

    def set_origin_host(self, value):
        self.origin_host = value

    def set_origin_realm(self, value):
        self.origin_realm = value

    def set_host_ip(self, value):
        self.host_ip = value

    def set_vendor_id(self, value):
        self.vendor_id = value

    def set_product_name(self, value):
        self.product_name = value

    def set_origin_state_id(self, value):
        self.origin_state_id = value

    def set_error_message(self, value):
        self.error_message = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_supported_vendor_id(self, value):
        self.supported_vendor_id = value

    def set_auth_app_id(self, value):
        self.auth_app_id = value

    def set_inband_security_id(self, value):
        self.inband_security_id = value

    def set_acct_app_id(self, value):
        self.acct_app_id = value

    def set_vendor_specific_app_id(self, value):
        self.vendor_specific_app_id = value

    def set_firmware(self, value):
        self.firmware = value

    def generateMessage(self):
        self.avps = []
        if self.result_code is None:
            raise MissingMandatoryAVPException('CEA: The Result-Code AVP is MANDATORY')
        avp = ResultCodeAVP(int(self.result_code['value']))
        avp.setFlags(self.result_code['flags'])
        if 'vendor' in self.result_code:
            avp.setVendorID(self.result_code['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('CEA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('CEA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
        
        if self.host_ip is None:
            raise MissingMandatoryAVPException('CEA: The Host-IP-Address AVP is MANDATORY')
        for ip in self.host_ip:
            if ip is not None:
                avp = HostIPAddressAVP(ip['value'])
                avp.setFlags(ip['flags'])
                if 'vendor' in ip:
                    avp.setVendorID(ip['vendor'])
                self.addAVP(avp)
        
        if self.vendor_id is None:
            raise MissingMandatoryAVPException('CEA: The Vendor-ID AVP is MANDATORY')
        avp = VendorIDAVP(int(self.vendor_id['value']))
        avp.setFlags(self.vendor_id['flags'])
        if 'vendor' in self.vendor_id:
            avp.setVendorID(self.vendor_id['vendor'])
        self.addAVP(avp)
        
        if self.product_name is None:
            raise MissingMandatoryAVPException('CEA: The Product-Name AVP is MANDATORY')
        avp = ProductNameAVP(self.product_name['value'])
        avp.setFlags(self.product_name['flags'])
        if 'vendor' in self.product_name:
            avp.setVendorID(self.product_name['vendor'])
        self.addAVP(avp)
        
        if self.origin_state_id is not None:
            if 'type' in self.origin_state_id and self.origin_state_id['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ORIGIN_STATE_ID, self.origin_state_id['value'])
            else:
                avp = OriginStateIDAVP(int(self.origin_state_id['value']))
                avp.setFlags(self.origin_state_id['flags'])
                if 'vendor' in self.origin_state_id:
                    avp.setVendorID(self.origin_state_id['vendor'])
            self.addAVP(avp)
            
        if self.error_message is not None:
            if 'type' in self.error_message and self.error_message['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ERROR_MESSAGE, self.error_message['value'])
            else:
                avp = ErrorMessageAVP(self.error_message['value'])
                avp.setFlags(self.error_message['flags'])
                if 'vendor' in self.error_message:
                    avp.setVendorID(self.error_message['vendor'])
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
        
        if self.supported_vendor_id is not None:
            if not isinstance(self.supported_vendor_id, list):
                self.supported_vendor_id = [self.supported_vendor_id]
                
            for vid in self.supported_vendor_id:
                if vid is not None:
                    if 'type' in vid and vid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.SUPPORTED_VENDOR_ID, vid['value'])
                    else:
                        avp = SupportedVendorIDAVP(int(vid['value']))
                        avp.setFlags(vid['flags'])
                        if 'vendor' in vid:
                            avp.setVendorID(vid['vendor'])
                    self.addAVP(avp)
        
        if self.auth_app_id is not None:
            if not isinstance(self.auth_app_id, list):
                self.auth_app_id = [self.auth_app_id]
                
            for aid in self.auth_app_id:
                if aid is not None:
                    if 'type' in aid and aid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.AUTH_APPLICATION_ID, aid['value'])
                    else:
                        avp = AuthApplicationIDAVP(int(aid['value']))
                        avp.setFlags(aid['flags'])
                        if 'vendor' in aid:
                            avp.setVendorID(aid['vendor'])
                    self.addAVP(avp)
        
        if self.inband_security_id is not None:
            if not isinstance(self.inband_security_id, list):
                self.inband_security_id = [self.inband_security_id]
                
            for iid in self.inband_security_id:
                if iid is not None:
                    if 'type' in iid and iid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.INBAND_SECURITY_ID, iid['value'])
                    else:
                        avp = InbandSecurityIDAVP(int(iid['value']))
                        avp.setFlags(iid['flags'])
                        if 'vendor' in iid:
                            avp.setVendorID(iid['vendor'])
                    self.addAVP(avp)
            
        if self.acct_app_id is not None:
            if not isinstance(self.acct_app_id, list):
                self.acct_app_id = [self.acct_app_id]
                
            for aid in self.acct_app_id:
                if aid is not None:
                    if 'type' in aid and aid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.ACCT_APPLICATION_ID, aid['value'])
                    else:
                        avp = AcctApplicationIDAVP(int(aid['value']))
                        avp.setFlags(aid['flags'])
                        if 'vendor' in aid:
                            avp.setVendorID(aid['vendor'])
                    self.addAVP(avp)
        
        if self.vendor_specific_app_id is not None:
            if not isinstance(self.vendor_specific_app_id, list):
                self.vendor_specific_app_id = [self.vendor_specific_app_id]
                
            for vsid in self.vendor_specific_app_id:
                if vsid is not None:
                    if 'type' in vsid and vsid['type']=='raw':
                        avp = GenericAVP(DiamAVPCodes.VENDOR_SPECIFIC_APPLICATION_ID, vsid['value'])
                    else:
                        topass = {'auth_app_id': None,
                                  'acct_app_id': None,
                                  'vendor_id': 0}
                        
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
        
        if self.firmware is not None:
            if 'type' in self.firmware and self.firmware['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.FIRMWARE_REVISION, self.firmware['value'])
            else:
                avp = FirmwareRevisionAVP(int(self.firmware['value']))
                avp.setFlags(self.firmware['flags'])
                if 'vendor' in self.firmware:
                    avp.setVendorID(self.firmware['vendor'])
            self.addAVP(avp)
''' /CAPPABILITIES EXCHANGE '''

''' WATCHDOG '''
##
## @brief      Class that defines a DIAMETER Message  
##    
##         <DWR>  ::= < Diameter Header: 280, REQ >
##                 { Origin-Host }
##                 { Origin-Realm }
##                 [ Origin-State-Id ]
##
class DiamDeviceWatchdogRequest(DiamMessage):
    def __init__(self, 
                 app_id, 
                 origin_host,
                 origin_realm,
                 origin_state_id=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.DEVICE_WATCHDOG, app_id)

        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.origin_state_id = origin_state_id
        
        self.setRequestFlag(True)

    def get_origin_host(self):
        return self.origin_host

    def get_origin_realm(self):
        return self.origin_realm

    def get_origin_state_id(self):
        return self.origin_state_id

    def set_origin_host(self, value):
        self.origin_host = value

    def set_origin_realm(self, value):
        self.origin_realm = value

    def set_origin_state_id(self, value):
        self.origin_state_id = value
    
    def generateMessage(self):
        self.avps = []
        if self.origin_host is None:
            raise MissingMandatoryAVPException('DWR: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('DWR: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)

        if self.origin_state_id is not None:
            if 'type' in self.origin_state_id and self.origin_state_id['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ORIGIN_STATE_ID, self.origin_state_id['value'])
            else:
                avp = OriginStateIDAVP(int(self.origin_state_id['value']))
                avp.setFlags(self.origin_state_id['flags'])
                if 'vendor' in self.origin_state_id:
                    avp.setVendorID(self.origin_state_id['vendor'])
            self.addAVP(avp)

##
## @brief      Class that defines a DIAMETER Message
##    
##         <DWA>  ::= < Diameter Header: 280 >
##                 { Result-Code }
##                 { Origin-Host }
##                 { Origin-Realm }
##                 [ Error-Message ]
##               * [ Failed-AVP ]
##                 [ Origin-State-Id ]  
##
class DiamDeviceWatchdogAnswer(DiamMessage):
    def __init__(self, 
                 app_id, 
                 result_code, 
                 origin_host,
                 origin_realm,
                 error_message=None,
                 failed_avp=None,
                 origin_state_id=None):
        
        DiamMessage.__init__(self, DiamCommandCodes.DEVICE_WATCHDOG, app_id)

        self.result_code = result_code
        self.origin_host = origin_host
        self.origin_realm = origin_realm
        self.error_message = error_message
        self.failed_avp = failed_avp
        self.origin_state_id = origin_state_id

    def get_result_code(self):
        return self.result_code

    def get_origin_host(self):
        return self.origin_host

    def get_origin_realm(self):
        return self.origin_realm

    def get_error_message(self):
        return self.error_message

    def get_failed_avp(self):
        return self.failed_avp

    def get_origin_state_id(self):
        return self.origin_state_id

    def set_result_code(self, value):
        self.result_code = value

    def set_origin_host(self, value):
        self.origin_host = value

    def set_origin_realm(self, value):
        self.origin_realm = value

    def set_error_message(self, value):
        self.error_message = value

    def set_failed_avp(self, value):
        self.failed_avp = value

    def set_origin_state_id(self, value):
        self.origin_state_id = value

    def generateMessage(self):
        self.avps = []
        if self.result_code is None:
            raise MissingMandatoryAVPException('DWA: The Result-Code AVP is MANDATORY')
        avp = ResultCodeAVP(int(self.result_code['value']))
        avp.setFlags(self.result_code['flags'])
        if 'vendor' in self.result_code:
            avp.setVendorID(self.result_code['vendor'])
        self.addAVP(avp)
        
        if self.origin_host is None:
            raise MissingMandatoryAVPException('DWA: The Origin-Host AVP is MANDATORY')
        avp = OriginHostAVP(self.origin_host['value'])
        avp.setFlags(self.origin_host['flags'])
        if 'vendor' in self.origin_host:
            avp.setVendorID(self.origin_host['vendor'])
        self.addAVP(avp)
        
        if self.origin_realm is None:
            raise MissingMandatoryAVPException('DWA: The Origin-Realm AVP is MANDATORY')
        avp = OriginRealmAVP(self.origin_realm['value'])
        avp.setFlags(self.origin_realm['flags'])
        if 'vendor' in self.origin_realm:
            avp.setVendorID(self.origin_realm['vendor'])
        self.addAVP(avp)
            
        if self.error_message is not None:
            if 'type' in self.error_message and self.error_message['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ERROR_MESSAGE, self.error_message['value'])
            else:
                avp = ErrorMessageAVP(self.error_message['value'])
                avp.setFlags(self.error_message['flags'])
                if 'vendor' in self.error_message:
                    avp.setVendorID(self.error_message['vendor'])
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

        if self.origin_state_id is not None:
            if 'type' in self.origin_state_id and self.origin_state_id['type']=='raw':
                avp = GenericAVP(DiamAVPCodes.ORIGIN_STATE_ID, self.origin_state_id['value'])
            else:
                avp = OriginStateIDAVP(int(self.origin_state_id['value']))
                avp.setFlags(self.origin_state_id['flags'])
                if 'vendor' in self.origin_state_id:
                    avp.setVendorID(self.origin_state_id['vendor'])
            self.addAVP(avp)
''' /WATCHDOG '''
