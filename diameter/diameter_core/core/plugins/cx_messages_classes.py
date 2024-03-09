from ..diameter.diameter_message import DiamMessage
from ..diameter.diam_avp_data import *
from ..diameter.diamCommandCodes import DiamCommandCodes

##
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##

''' >>> Cx INTERFACE <<< '''

''' 3GPP: USER AUTHORIZATION '''
##
## @brief      Class that defines a DIAMETER Message
##
##		< User-Authorization-Request> ::= < Diameter Header: 300, REQ, PXY, 16777216 >
##						< Session-Id >
##						[ DRMP ]
##						{ Vendor-Specific-Application-Id }
##						{ Auth-Session-State }
##						{ Origin-Host }
##						{ Origin-Realm }
##						[ Destination-Host ]
##						{ Destination-Realm }
##						{ User-Name }
##						[ OC-Supported-Features ]
##						*[ Supported-Features ]
##						{ Public-Identity }
##						{ Visited-Network-Identifier }
##						[ User-Authorization-Type ]
##						[ UAR-Flags ]
##						*[ AVP ]
##						*[ Proxy-Info ]
##						*[ Route-Record ]
##
class DiamUserAuthorizationRequest:
	def __init__(self, 
				app_id,
				session_id,
				vendor_specific_application_id,
				auth_session_state,
				origin_host,
				origin_realm,
				destination_realm,
				user_name,
				public_identity,
				visited_network_identifier,
				drmp=None,
				destination_host=None,
				oc_supported_features=None,
				supported_features=None,
				user_authorization_type=None,
				uar_flags=None,
				proxy_info=None,
				route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.USER_AUTHORIZATION, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.destination_realm = destination_realm
		self.user_name = user_name
		self.public_identity = public_identity
		self.visited_network_identifier = visited_network_identifier
		self.drmp = drmp
		self.destination_host = destination_host
		self.oc_supported_features = oc_supported_features
		self.supported_features = supported_features
		self.user_authorization_type = user_authorization_type
		self.uar_flags = uar_flags
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

	def get_destination_realm(self):
		return self.destination_realm

	def get_user_name(self):
		return self.user_name

	def get_public_identity(self):
		return self.public_identity

	def get_visited_network_identifier(self):
		return self.visited_network_identifier

	def get_drmp(self):
		return self.drmp

	def get_destination_host(self):
		return self.destination_host

	def get_oc_supported_features(self):
		return self.oc_supported_features

	def get_supported_features(self):
		return self.supported_features

	def get_user_authorization_type(self):
		return self.user_authorization_type

	def get_uar_flags(self):
		return self.uar_flags

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

	def set_destination_realm(self, value):
		self.destination_realm = value

	def set_user_name(self, value):
		self.user_name = value

	def set_public_identity(self, value):
		self.public_identity = value

	def set_visited_network_identifier(self, value):
		self.visited_network_identifier = value

	def set_drmp(self, value):
		self.drmp = value

	def set_destination_host(self, value):
		self.destination_host = value

	def set_oc_supported_features(self, value):
		self.oc_supported_features = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_user_authorization_type(self, value):
		self.user_authorization_type = value

	def set_uar_flags(self, value):
		self.uar_flags = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('UAR: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('UAR: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]

		for vsid in self.vendor_specific_application_id:
			if vsid!=None:
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

				avp = VendorSpecificApplicationIdAVP(topass['avp_name'], topass['vendor_id'])
				avp.setFlags(vsid['flags'])
			self.addAVP(avp)

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('UAR: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('UAR: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('UAR: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.destination_realm==None:
			raise MissingMandatoryAVPException('UAR: The Destination-Realm AVP is MANDATORY')
		avp = DestinationRealmAVP(self.destination_realm['value'])
		avp.setFlags(self.destination_realm['flags'])
		if 'vendor' in self.destination_realm:
			avp.setVendorID(self.destination_realm['vendor'])
		self.addAVP(avp)

		if self.user_name==None:
			raise MissingMandatoryAVPException('UAR: The User-Name AVP is MANDATORY')
		avp = UserNameAVP(self.user_name['value'])
		avp.setFlags(self.user_name['flags'])
		if 'vendor' in self.user_name:
			avp.setVendorID(self.user_name['vendor'])
		self.addAVP(avp)

		if self.public_identity==None:
			raise MissingMandatoryAVPException('UAR: The Public-Identity AVP is MANDATORY')
		if not isinstance(self.PublicIdentityAVP, list):
			self.public_identity = [self.public_identity]

		for el in self.public_identity:
			if el!=None:
				if 'type' in el and el['type']=='raw':
					avp = GenericAVP(DiamAVPCodes.PUBLIC_IDENTITY, el['value'])
				else:
					avp = PublicIdentityAVP(el['value'])
					avp.setFlags(el['flags'])
					if 'vendor_id' in el:
						avp.setVendorID(el['vendor'])
			self.addAVP(avp)

		if self.visited_network_identifier==None:
			raise MissingMandatoryAVPException('UAR: The Visited-Network-Identifier AVP is MANDATORY')
		avp = VisitedNetworkIdentifierAVP(self.visited_network_identifier['value'])
		avp.setFlags(self.visited_network_identifier['flags'])
		if 'vendor' in self.visited_network_identifier:
			avp.setVendorID(self.visited_network_identifier['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.destination_host!=None:
			avp = DestinationHostAVP(self.destination_host['value'])
			avp.setFlags(self.destination_host['flags'])
			if 'vendor' in self.destination_host:
				avp.setVendorID(self.destination_host['vendor'])
			self.addAVP(avp)

		if self.oc_supported_features!=None:
			avp = OCSupportedFeaturesAVP(self.oc_supported_features['value'])
			avp.setFlags(self.oc_supported_features['flags'])
			if 'vendor' in self.oc_supported_features:
				avp.setVendorID(self.oc_supported_features['vendor'])
			self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]
				
			for sf in self.supported_features:
				if sf!=None:
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

		if self.user_authorization_type!=None:
			avp = UserAuthorizationTypeAVP(self.user_authorization_type['value'])
			avp.setFlags(self.user_authorization_type['flags'])
			if 'vendor' in self.user_authorization_type:
				avp.setVendorID(self.user_authorization_type['vendor'])
			self.addAVP(avp)

		if self.uar_flags!=None:
			avp = UARFlagsAVP(self.uar_flags['value'])
			avp.setFlags(self.uar_flags['flags'])
			if 'vendor' in self.uar_flags:
				avp.setVendorID(self.uar_flags['vendor'])
			self.addAVP(avp)

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)

##
## @brief      Class that defines a DIAMETER Message
##
##		< User-Authorization-Answer> ::= < Diameter Header: 300, PXY, 16777216 >
##						< Session-Id >
##						[ DRMP ]
##						{ Vendor-Specific-Application-Id }
##						[ Result-Code ]
##						[ Experimental-Result ]
##						{ Auth-Session-State }
##						{ Origin-Host }
##						{ Origin-Realm }
##						[ OC-Supported-Features ]
##						[ OC-OLR ]
##						*[ Supported-Features ]
##						[ Server-Name ]
##						[ Server-Capabilities ]
##						*[ AVP ]
##						*[ Failed-AVP ]
##						*[ Proxy-Info ]
##						*[ Route-Record ]
##
class DiamUserAuthorizationAnswer:
	def __init__(self, 
				app_id,
				session_id,
				vendor_specific_application_id,
				auth_session_state,
				origin_host,
				origin_realm,
				drmp=None,
				result_code=None,
				experimental_result=None,
				oc_supported_features=None,
				oc_olr=None,
				supported_features=None,
				server_name=None,
				server_capabilities=None,
				failed_avp=None,
				proxy_info=None,
				route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.USER_AUTHORIZATION, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.drmp = drmp
		self.result_code = result_code
		self.experimental_result = experimental_result
		self.oc_supported_features = oc_supported_features
		self.oc_olr = oc_olr
		self.supported_features = supported_features
		self.server_name = server_name
		self.server_capabilities = server_capabilities
		self.failed_avp = failed_avp
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

	def get_drmp(self):
		return self.drmp

	def get_result_code(self):
		return self.result_code

	def get_experimental_result(self):
		return self.experimental_result

	def get_oc_supported_features(self):
		return self.oc_supported_features

	def get_oc_olr(self):
		return self.oc_olr

	def get_supported_features(self):
		return self.supported_features

	def get_server_name(self):
		return self.server_name

	def get_server_capabilities(self):
		return self.server_capabilities

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

	def set_auth_session_state(self, value):
		self.auth_session_state = value

	def set_origin_host(self, value):
		self.origin_host = value

	def set_origin_realm(self, value):
		self.origin_realm = value

	def set_drmp(self, value):
		self.drmp = value

	def set_result_code(self, value):
		self.result_code = value

	def set_experimental_result(self, value):
		self.experimental_result = value

	def set_oc_supported_features(self, value):
		self.oc_supported_features = value

	def set_oc_olr(self, value):
		self.oc_olr = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_server_name(self, value):
		self.server_name = value

	def set_server_capabilities(self, value):
		self.server_capabilities = value

	def set_failed_avp(self, value):
		self.failed_avp = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('UAA: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('UAA: The Vendor-Specific-Application-Id AVP is MANDATORY')

			if not isinstance(self.vendor_specific_application_id, list):
				self.vendor_specific_application_id = [self.vendor_specific_application_id]
				
			for vsid in self.vendor_specific_application_id:
				if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('UAA: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('UAA: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('UAA: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.result_code!=None:
			avp = ResultCodeAVP(self.result_code['value'])
			avp.setFlags(self.result_code['flags'])
			if 'vendor' in self.result_code:
				avp.setVendorID(self.result_code['vendor'])
			self.addAVP(avp)
			
		if self.experimental_result!=None:
			if 'type' in self.experimental_result and self.experimental_result['type']=='raw':
				avp = GenericAVP(DiamAVPCodes.EXPERIMENTAL_RESULT, self.experimental_result['value'])
			else:
				avp = ExperimentalResultAVP(self.experimental_result['value'])
				avp.setFlags(self.experimental_result['flags'])
				if 'vendor' in self.experimental_result:
					avp.setVendorID(self.experimental_result['vendor'])
			self.addAVP(avp)

		if self.oc_supported_features!=None:
			avp = OCSupportedFeaturesAVP(self.oc_supported_features['value'])
			avp.setFlags(self.oc_supported_features['flags'])
			if 'vendor' in self.oc_supported_features:
				avp.setVendorID(self.oc_supported_features['vendor'])
			self.addAVP(avp)

		if self.oc_olr!=None:
			avp = OCOLRAVP(self.oc_olr['value'])
			avp.setFlags(self.oc_olr['flags'])
			if 'vendor' in self.oc_olr:
				avp.setVendorID(self.oc_olr['vendor'])
			self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]
				
			for sf in self.supported_features:
				if sf!=None:
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

		if self.server_name!=None:
			avp = ServerNameAVP(self.server_name['value'])
			avp.setFlags(self.server_name['flags'])
			if 'vendor' in self.server_name:
				avp.setVendorID(self.server_name['vendor'])
			self.addAVP(avp)

		if self.server_capabilities!=None:
			if not isinstance(self.server_capabilities, list):
				self.server_capabilities = [self.server_capabilities]

			for val in self.server_capabilities:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.SERVER_CAPABILITIES, val['value'])
					else:
						topass = {'mandatory_capability': None,
								  'optional_capability': None,
								  'server_name': None,
								  'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'mandatory-capability':
							topass['mandatory_capability'] = valavp
						if valavp['name'] == 'optional-capability':
							topass['optional_capability'] = valavp
						if valavp['name'] == 'server-name':
							topass['server_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = ServerCapabilitiesAVP(topass['mandatory_capability'], topass['optional_capability'], topass['server_name'],topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.failed_avp!=None:
			if not isinstance(self.failed_avp, list):
				self.failed_avp = [self.failed_avp]
				
			for fa in self.failed_avp:
				if fa!=None:
					if 'type' in fa and fa['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.FAILED_AVP, fa['value'])
					else:
						avp = FailedAVP(fa['value'])
						avp.setFlags(fa['flags'])
						if 'vendor_id' in fa:
							avp.setVendorID(fa['vendor'])
					self.addAVP(avp)

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)
''' /3GPP: USER AUTHORIZATION '''

''' 3GPP: SERVER ASSIGNMENT '''
##
## @brief      Class that defines a DIAMETER Message
##
##		<Server-Assignment-Request> ::= < Diameter Header: 301, REQ, PXY, 16777216 >
##						< Session-Id >
##						[ DRMP ]
##						{ Vendor-Specific-Application-Id }
##						{ Auth-Session-State }
##						{ Origin-Host }
##						{ Origin-Realm }
##						[ Destination-Host ]
##						{ Destination-Realm }
##						[ User-Name ]
##						[ OC-Supported-Features ]
##						*[ Supported-Features ]
##						*[ Public-Identity ]
##						[ Wildcarded-Public-Identity ]
##						{ Server-Name }
##						{ Server-Assignment-Type }
##						{ User-Data-Already-Available }
##						[ SCSCF-Restoration-Info ]
##						[ Multiple-Registration-Indication ]
##						[ Session-Priority ]
##						[ SAR-Flags ]
##						*[ AVP ]
##						*[ Proxy-Info ]
##						*[ Route-Record ]
##
class DiamServerAssignmentRequest:
	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		destination_realm,
		server_name,
		server_assignment_type,
		user_data_already_available,
		drmp=None,
		destination_host=None,
		user_name=None,
		oc_supported_features=None,
		supported_features=None,
		public_identity=None,
		wildcarded_public_identity=None,
		scscf_restoration_info=None,
		multiple_registration_indication=None,
		session_priority=None,
		sar_flags=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.SERVER_ASSIGNMENT, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.destination_realm = destination_realm
		self.server_name = server_name
		self.server_assignment_type = server_assignment_type
		self.user_data_already_available = user_data_already_available
		self.drmp = drmp
		self.destination_host = destination_host
		self.user_name = user_name
		self.oc_supported_features = oc_supported_features
		self.supported_features = supported_features
		self.public_identity = public_identity
		self.wildcarded_public_identity = wildcarded_public_identity
		self.scscf_restoration_info = scscf_restoration_info
		self.multiple_registration_indication = multiple_registration_indication
		self.session_priority = session_priority
		self.sar_flags = sar_flags
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

	def get_destination_realm(self):
		return self.destination_realm

	def get_server_name(self):
		return self.server_name

	def get_server_assignment_type(self):
		return self.server_assignment_type

	def get_user_data_already_available(self):
		return self.user_data_already_available

	def get_drmp(self):
		return self.drmp

	def get_destination_host(self):
		return self.destination_host

	def get_user_name(self):
		return self.user_name

	def get_oc_supported_features(self):
		return self.oc_supported_features

	def get_supported_features(self):
		return self.supported_features

	def get_public_identity(self):
		return self.public_identity

	def get_wildcarded_public_identity(self):
		return self.wildcarded_public_identity

	def get_scscf_restoration_info(self):
		return self.scscf_restoration_info

	def get_multiple_registration_indication(self):
		return self.multiple_registration_indication

	def get_session_priority(self):
		return self.session_priority

	def get_sar_flags(self):
		return self.sar_flags

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

	def set_destination_realm(self, value):
		self.destination_realm = value

	def set_server_name(self, value):
		self.server_name = value

	def set_server_assignment_type(self, value):
		self.server_assignment_type = value

	def set_user_data_already_available(self, value):
		self.user_data_already_available = value

	def set_drmp(self, value):
		self.drmp = value

	def set_destination_host(self, value):
		self.destination_host = value

	def set_user_name(self, value):
		self.user_name = value

	def set_oc_supported_features(self, value):
		self.oc_supported_features = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_public_identity(self, value):
		self.public_identity = value

	def set_wildcarded_public_identity(self, value):
		self.wildcarded_public_identity = value

	def set_scscf_restoration_info(self, value):
		self.scscf_restoration_info = value

	def set_multiple_registration_indication(self, value):
		self.multiple_registration_indication = value

	def set_session_priority(self, value):
		self.session_priority = value

	def set_sar_flags(self, value):
		self.sar_flags = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('SAR: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('SAR: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]
				
		for vsid in self.vendor_specific_application_id:
			if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('SAR: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('SAR: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('SAR: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.destination_realm==None:
			raise MissingMandatoryAVPException('SAR: The Destination-Realm AVP is MANDATORY')
		avp = DestinationRealmAVP(self.destination_realm['value'])
		avp.setFlags(self.destination_realm['flags'])
		if 'vendor' in self.destination_realm:
			avp.setVendorID(self.destination_realm['vendor'])
		self.addAVP(avp)

		if self.server_name==None:
			raise MissingMandatoryAVPException('SAR: The Server-Name AVP is MANDATORY')
		avp = ServerNameAVP(self.server_name['value'])
		avp.setFlags(self.server_name['flags'])
		if 'vendor' in self.server_name:
			avp.setVendorID(self.server_name['vendor'])
		self.addAVP(avp)

		if self.server_assignment_type==None:
			raise MissingMandatoryAVPException('SAR: The Server-Assignment-Type AVP is MANDATORY')
		avp = ServerAssignmentTypeAVP(self.server_assignment_type['value'])
		avp.setFlags(self.server_assignment_type['flags'])
		if 'vendor' in self.server_assignment_type:
			avp.setVendorID(self.server_assignment_type['vendor'])
		self.addAVP(avp)

		if self.user_data_already_available==None:
			raise MissingMandatoryAVPException('SAR: The User-Data-Already-Available AVP is MANDATORY')
		avp = UserDataAlreadyAvailableAVP(self.user_data_already_available['value'])
		avp.setFlags(self.user_data_already_available['flags'])
		if 'vendor' in self.user_data_already_available:
			avp.setVendorID(self.user_data_already_available['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.destination_host!=None:
			avp = DestinationHostAVP(self.destination_host['value'])
			avp.setFlags(self.destination_host['flags'])
			if 'vendor' in self.destination_host:
				avp.setVendorID(self.destination_host['vendor'])
			self.addAVP(avp)

		if self.user_name!=None:
			avp = UserNameAVP(self.user_name['value'])
			avp.setFlags(self.user_name['flags'])
			if 'vendor' in self.user_name:
				avp.setVendorID(self.user_name['vendor'])
			self.addAVP(avp)

		if self.oc_supported_features!=None:
			avp = OCSupportedFeaturesAVP(self.oc_supported_features['value'])
			avp.setFlags(self.oc_supported_features['flags'])
			if 'vendor' in self.oc_supported_features:
				avp.setVendorID(self.oc_supported_features['vendor'])
			self.addAVP(avp)
		
		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]
				
			for sf in self.supported_features:
				if sf!=None:
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

		if self.public_identity!=None:
			if not isinstance(self.PublicIdentityAVP, list):
				self.public_identity = [self.public_identity]

			for el in self.public_identity:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.PUBLIC_IDENTITY, el['value'])
					else:
						avp = PublicIdentityAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)

		if self.wildcarded_public_identity!=None:
			avp = WildcardedPublicIdentityAVP(self.wildcarded_public_identity['value'])
			avp.setFlags(self.wildcarded_public_identity['flags'])
			if 'vendor' in self.wildcarded_public_identity:
				avp.setVendorID(self.wildcarded_public_identity['vendor'])
			self.addAVP(avp)

		if self.scscf_restoration_info!=None:
			if not isinstance(self.scscf_restoration_info, list):
				self.scscf_restoration_info = [self.scscf_restoration_info]

			for val in self.scscf_restoration_info:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.SCSCF_RESTORATION_INFO, val['value'])
					else:
						topass = {'user_name': None,
								  'restoration_info': None,
								  'sip_authentication_scheme': None,
								  'vendor_id': 0}

					for valavp in val['avps']:
						if valavp['name'] == 'user-name':
							topass['user_name'] = valavp
						if valavp['name'] == 'restoration-info':
							topass['restoration_info'] = valavp
						if valavp['name'] == 'sip-authentication-scheme':
							topass['sip_authentication_scheme'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = SCSCFRestorationInfoAVP(topass['user_name'], topass['restoration_info'], topass['sip_authentication_scheme'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.multiple_registration_indication!=None:
			avp = MultipleRegistrationIndicationAVP(self.multiple_registration_indication['value'])
			avp.setFlags(self.multiple_registration_indication['flags'])
			if 'vendor' in self.multiple_registration_indication:
				avp.setVendorID(self.multiple_registration_indication['vendor'])
			self.addAVP(avp)

		if self.session_priority!=None:
			avp = SessionPriorityAVP(self.session_priority['value'])
			avp.setFlags(self.session_priority['flags'])
			if 'vendor' in self.session_priority:
				avp.setVendorID(self.session_priority['vendor'])
			self.addAVP(avp)

		if self.sar_flags!=None:
			avp = SARFlagsAVP(self.sar_flags['value'])
			avp.setFlags(self.sar_flags['flags'])
			if 'vendor' in self.sar_flags:
				avp.setVendorID(self.sar_flags['vendor'])
			self.addAVP(avp)
		
		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)

##
## @brief      Class that defines a DIAMETER Message
##
##		<Server-Assignment-Answer> ::= < Diameter Header: 301, PXY, 16777216 >
##						< Session-Id >
##						[ DRMP ]
##						{ Vendor-Specific-Application-Id }
##						[ Result-Code ]
##						[ Experimental-Result ]
##						{ Auth-Session-State }
##						{ Origin-Host }
##						{ Origin-Realm }
##						[ User-Name ]
##						[ OC-Supported-Features ]
##						[ OC-OLR ]
##						*[ Supported-Features ]
##						[ User-Data ]
##						[ Charging-Information ]
##						[ Associated-Identities ]
##						[ Loose-Route-Indication ]
##						*[ SCSCF-Restoration-Info ]
##						[ Associated-Registered-Identities ]
##						[ Server-Name ]
##						[ Wildcarded-Public-Identity ]
##						[ Priviledged-Sender-Indication ]
##						[ Allowed-WAF-WWSF-Identities ]
##						*[ AVP ]
##						*[ Failed-AVP ]
##						*[ Proxy-Info ]
##						*[ Route-Record ]
##
class DiamServerAssignmentAnswer:
	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		drmp=None,
		result_code=None,
		experimental_result=None,
		user_name=None,
		oc_supported_features=None,
		oc_olr=None,
		supported_features=None,
		user_data=None,
		charging_information=None,
		associated_identities=None,
		loose_route_indication=None,
		scscf_restoration_info=None,
		associated_registered_identities=None,
		server_name=None,
		wildcarded_public_identity=None,
		priviledged_sender_indication=None,
		allowed_waf_wwsf_identities=None,
		failed_avp=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.SERVER_ASSIGNMENT, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.drmp = drmp
		self.result_code = result_code
		self.experimental_result = experimental_result
		self.user_name = user_name
		self.oc_supported_features = oc_supported_features
		self.oc_olr = oc_olr
		self.supported_features = supported_features
		self.user_data = user_data
		self.charging_information = charging_information
		self.associated_identities = associated_identities
		self.loose_route_indication = loose_route_indication
		self.scscf_restoration_info = scscf_restoration_info
		self.associated_registered_identities = associated_registered_identities
		self.server_name = server_name
		self.wildcarded_public_identity = wildcarded_public_identity
		self.priviledged_sender_indication = priviledged_sender_indication
		self.allowed_waf_wwsf_identities = allowed_waf_wwsf_identities
		self.failed_avp = failed_avp
		self.proxy_info = proxy_info
		self.route_record = route_record

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

	def get_drmp(self):
		return self.drmp

	def get_result_code(self):
		return self.result_code

	def get_experimental_result(self):
		return self.experimental_result

	def get_user_name(self):
		return self.user_name

	def get_oc_supported_features(self):
		return self.oc_supported_features

	def get_oc_olr(self):
		return self.oc_olr

	def get_supported_features(self):
		return self.supported_features

	def get_user_data(self):
		return self.user_data

	def get_charging_information(self):
		return self.charging_information

	def get_associated_identities(self):
		return self.associated_identities

	def get_loose_route_indication(self):
		return self.loose_route_indication

	def get_scscf_restoration_info(self):
		return self.scscf_restoration_info

	def get_associated_registered_identities(self):
		return self.associated_registered_identities

	def get_server_name(self):
		return self.server_name

	def get_wildcarded_public_identity(self):
		return self.wildcarded_public_identity

	def get_priviledged_sender_indication(self):
		return self.priviledged_sender_indication

	def get_allowed_waf_wwsf_identities(self):
		return self.allowed_waf_wwsf_identities

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

	def set_auth_session_state(self, value):
		self.auth_session_state = value

	def set_origin_host(self, value):
		self.origin_host = value

	def set_origin_realm(self, value):
		self.origin_realm = value

	def set_drmp(self, value):
		self.drmp = value

	def set_result_code(self, value):
		self.result_code = value

	def set_experimental_result(self, value):
		self.experimental_result = value

	def set_user_name(self, value):
		self.user_name = value

	def set_oc_supported_features(self, value):
		self.oc_supported_features = value

	def set_oc_olr(self, value):
		self.oc_olr = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_user_data(self, value):
		self.user_data = value

	def set_charging_information(self, value):
		self.charging_information = value

	def set_associated_identities(self, value):
		self.associated_identities = value

	def set_loose_route_indication(self, value):
		self.loose_route_indication = value

	def set_scscf_restoration_info(self, value):
		self.scscf_restoration_info = value

	def set_associated_registered_identities(self, value):
		self.associated_registered_identities = value

	def set_server_name(self, value):
		self.server_name = value

	def set_wildcarded_public_identity(self, value):
		self.wildcarded_public_identity = value

	def set_priviledged_sender_indication(self, value):
		self.priviledged_sender_indication = value

	def set_allowed_waf_wwsf_identities(self, value):
		self.allowed_waf_wwsf_identities = value

	def set_failed_avp(self, value):
		self.failed_avp = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('SAA: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('SAA: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]
				
		for vsid in self.vendor_specific_application_id:
			if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('SAA: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('SAA: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('SAA: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.result_code!=None:
			avp = ResultCodeAVP(self.result_code['value'])
			avp.setFlags(self.result_code['flags'])
			if 'vendor' in self.result_code:
				avp.setVendorID(self.result_code['vendor'])
			self.addAVP(avp)
			
		if self.experimental_result!=None:
			if 'type' in self.experimental_result and self.experimental_result['type']=='raw':
				avp = GenericAVP(DiamAVPCodes.EXPERIMENTAL_RESULT, self.experimental_result['value'])
			else:
				avp = ExperimentalResultAVP(self.experimental_result['value'])
				avp.setFlags(self.experimental_result['flags'])
				if 'vendor' in self.experimental_result:
					avp.setVendorID(self.experimental_result['vendor'])
			self.addAVP(avp)

		if self.user_name!=None:
			avp = UserNameAVP(self.user_name['value'])
			avp.setFlags(self.user_name['flags'])
			if 'vendor' in self.user_name:
				avp.setVendorID(self.user_name['vendor'])
			self.addAVP(avp)

		if self.oc_supported_features!=None:
			avp = OCSupportedFeaturesAVP(self.oc_supported_features['value'])
			avp.setFlags(self.oc_supported_features['flags'])
			if 'vendor' in self.oc_supported_features:
				avp.setVendorID(self.oc_supported_features['vendor'])
			self.addAVP(avp)

		if self.oc_olr!=None:
			avp = OCOLRAVP(self.oc_olr['value'])
			avp.setFlags(self.oc_olr['flags'])
			if 'vendor' in self.oc_olr:
				avp.setVendorID(self.oc_olr['vendor'])
			self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]

			for sf in self.supported_features:
				if sf!=None:
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

		if self.user_data!=None:
			avp = UserDataAVP(self.user_data['value'])
			avp.setFlags(self.user_data['flags'])
			if 'vendor' in self.user_data:
				avp.setVendorID(self.user_data['vendor'])
			self.addAVP(avp)

		if self.charging_information!=None:
			if not isinstance(self.charging_information, list):
				self.charging_information = [self.charging_information]

			for val in self.charging_information:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.CHARGING_INFORMATION, val['value'])
					else:
						topass = {'primary_event_charging_function_name': None,
								  'secondary_event_charging_function_name': None,
								  'primary_charging_collection_function_name': None,
								  'secondary_charging_collection_function_name': None,
								  'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'primary-event-charging-function-name':
							topass['primary_event_charging_function_name'] = valavp
						if valavp['name'] == 'secondary-event-charging-function-name':
							topass['secondary_event_charging_function_name'] = valavp
						if valavp['name'] == 'primary-charging-collection-function-name':
							topass['primary_charging_collection_function_name'] = valavp
						if valavp['name'] == 'secondary-charging-collection-function-name':
							topass['secondary_charging_collection_function_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = ChargingInformationAVP(topass['primary_event_charging_function_name'], topass['secondary_event_charging_function_name'], topass['primary_charging_collection_function_name'], topass['secondary_charging_collection_function_name'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.associated_identities!=None:
			if not isinstance(self.associated_identities, list):
				self.associated_identities = [self.associated_identities]

			for val in self.associated_identities:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ASSOCIATED_IDENTITIES, val['value'])
					else:
						topass = {'user_name':None,
								  'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'user-name':
							topass['user_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = AssociatedIdentitiesAVP(topass['user_name'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.loose_route_indication!=None:
			avp = LooseRouteIndicationAVP(self.loose_route_indication['value'])
			avp.setFlags(self.loose_route_indication['flags'])
			if 'vendor' in self.loose_route_indication:
				avp.setVendorID(self.loose_route_indication['vendor'])
			self.addAVP(avp)

		if self.scscf_restoration_info!=None:
			if not isinstance(self.scscf_restoration_info, list):
				self.scscf_restoration_info = [self.scscf_restoration_info]

			for val in self.scscf_restoration_info:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.SCSCF_RESTORATION_INFO, val['value'])
					else:
						topass = {'user_name': None,
								  'restoration_info': None,
								  'sip_authentication_scheme': None,
								  'vendor_id': 0}

					for valavp in val['avps']:
						if valavp['name'] == 'user-name':
							topass['user_name'] = valavp
						if valavp['name'] == 'restoration-info':
							topass['restoration_info'] = valavp
						if valavp['name'] == 'sip-authentication-scheme':
							topass['sip_authentication_scheme'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = SCSCFRestorationInfoAVP(topass['user_name'], topass['restoration_info'], topass['sip_authentication_scheme'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.associated_registered_identities!=None:
			if not isinstance(self.associated_registered_identities, list):
				self.associated_registered_identities = [self.associated_registered_identities]

			for val in self.associated_registered_identities:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ASSOCIATED_REGISTERED_IDENTITIES, val['value'])
					else:
						topass = {'user_name':None,
								  'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'user_name':
							topass['user_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = AssociatedRegisteredIdentitiesAVP(topass['user_name'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.server_name!=None:
			avp = ServerNameAVP(self.server_name['value'])
			avp.setFlags(self.server_name['flags'])
			if 'vendor' in self.server_name:
				avp.setVendorID(self.server_name['vendor'])
			self.addAVP(avp)

		if self.wildcarded_public_identity!=None:
			avp = WildcardedPublicIdentityAVP(self.wildcarded_public_identity['value'])
			avp.setFlags(self.wildcarded_public_identity['flags'])
			if 'vendor' in self.wildcarded_public_identity:
				avp.setVendorID(self.wildcarded_public_identity['vendor'])
			self.addAVP(avp)

		if self.priviledged_sender_indication!=None:
			avp = PriviledgedSenderIndicationAVP(self.priviledged_sender_indication['value'])
			avp.setFlags(self.priviledged_sender_indication['flags'])
			if 'vendor' in self.priviledged_sender_indication:
				avp.setVendorID(self.priviledged_sender_indication['vendor'])
			self.addAVP(avp)

		if self.allowed_waf_wwsf_identities!=None:
			if not isinstance(self.allowed_waf_wwsf_identities, list):
				self.allowed_waf_wwsf_identities = [self.allowed_waf_wwsf_identities]

			for val in self.allowed_waf_wwsf_identities:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ALLOWED_WAF_WWSF_IDENTITIES, val['value'])
					else:
						topass = {'webrtc_authentication_function_name':None,
								  'webrtc_web_server_function_name':None,
						'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'webrtc-authentication-function-name':
							topass['webrtc_authentication_function_name'] = valavp
						if valavp['name'] == 'webrtc-web-server-function-name':
							topass['webrtc_web_server_function_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = AllowedWAFWWSFIdentitiesAVP(topass['webrtc_authentication_function_name'], topass['webrtc_web_server_function_name'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.failed_avp!=None:
			if not isinstance(self.failed_avp, list):
				self.failed_avp = [self.failed_avp]
				
			for fa in self.failed_avp:
				if fa!=None:
					if 'type' in fa and fa['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.FAILED_AVP, fa['value'])
					else:
						avp = FailedAVP(fa['value'])
						avp.setFlags(fa['flags'])
						if 'vendor_id' in fa:
							avp.setVendorID(fa['vendor'])
					self.addAVP(avp)

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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


		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)
''' /3GPP: SERVER ASSIGNMENT '''

''' 3GPP: LOCATION INFO '''
##
## @brief      Class that defines a DIAMETER Message
##
##		<Location-Info-Request> ::= < Diameter Header: 302, REQ, PXY, 16777216 >
##						< Session-Id >
##						[ DRMP ]
##						{ Vendor-Specific-Application-Id }
##						{ Auth-Session-State }
##						{ Origin-Host }
##						{ Origin-Realm }
##						[ Destination-Host ]
##						{ Destination-Realm }
##						[ Originating-Request ]
##						[ OC-Supported-Features ]
##						*[ Supported-Features ]
##						{ Public-Identity }
##						[ User-Authorization-Type ]
##						[ Session-Priority ]
##						*[ AVP ]
##						*[ Proxy-Info ]
##						*[ Route-Record ]
##
class DiamLocationInfoRequest:
	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		destination_realm,
		public_identity,
		drmp=None,
		destination_host=None,
		originating_request=None,
		oc_supported_features=None,
		supported_features=None,
		user_authorization_type=None,
		session_priority=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.LOCATION_INFO, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.destination_realm = destination_realm
		self.public_identity = public_identity
		self.drmp = drmp
		self.destination_host = destination_host
		self.originating_request = originating_request
		self.oc_supported_features = oc_supported_features
		self.supported_features = supported_features
		self.user_authorization_type = user_authorization_type
		self.session_priority = session_priority
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

	def get_destination_realm(self):
		return self.destination_realm

	def get_public_identity(self):
		return self.public_identity

	def get_drmp(self):
		return self.drmp

	def get_destination_host(self):
		return self.destination_host

	def get_originating_request(self):
		return self.originating_request

	def get_oc_supported_features(self):
		return self.oc_supported_features

	def get_supported_features(self):
		return self.supported_features

	def get_user_authorization_type(self):
		return self.user_authorization_type

	def get_session_priority(self):
		return self.session_priority

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

	def set_destination_realm(self, value):
		self.destination_realm = value

	def set_public_identity(self, value):
		self.public_identity = value

	def set_drmp(self, value):
		self.drmp = value

	def set_destination_host(self, value):
		self.destination_host = value

	def set_originating_request(self, value):
		self.originating_request = value

	def set_oc_supported_features(self, value):
		self.oc_supported_features = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_user_authorization_type(self, value):
		self.user_authorization_type = value

	def set_session_priority(self, value):
		self.session_priority = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('LIR: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('LIR: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]

		for vsid in self.vendor_specific_application_id:
				if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('LIR: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('LIR: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('LIR: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.destination_realm==None:
			raise MissingMandatoryAVPException('LIR: The Destination-Realm AVP is MANDATORY')
		avp = DestinationRealmAVP(self.destination_realm['value'])
		avp.setFlags(self.destination_realm['flags'])
		if 'vendor' in self.destination_realm:
			avp.setVendorID(self.destination_realm['vendor'])
		self.addAVP(avp)

		if self.public_identity==None:
			raise MissingMandatoryAVPException('LIR: The Public-Identity AVP is MANDATORY')
		if not isinstance(self.PublicIdentityAVP, list):
			self.public_identity = [self.public_identity]

		for el in self.public_identity:
			if el!=None:
				if 'type' in el and el['type']=='raw':
					avp = GenericAVP(DiamAVPCodes.PUBLIC_IDENTITY, el['value'])
				else:
					avp = PublicIdentityAVP(el['value'])
					avp.setFlags(el['flags'])
					if 'vendor_id' in el:
						avp.setVendorID(el['vendor'])
			self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.destination_host!=None:
			avp = DestinationHostAVP(self.destination_host['value'])
			avp.setFlags(self.destination_host['flags'])
			if 'vendor' in self.destination_host:
				avp.setVendorID(self.destination_host['vendor'])
			self.addAVP(avp)

		if self.originating_request!=None:
			avp = OriginatingRequestAVP(self.originating_request['value'])
			avp.setFlags(self.originating_request['flags'])
			if 'vendor' in self.originating_request:
				avp.setVendorID(self.originating_request['vendor'])
			self.addAVP(avp)

		if self.oc_supported_features!=None:
			avp = OCSupportedFeaturesAVP(self.oc_supported_features['value'])
			avp.setFlags(self.oc_supported_features['flags'])
			if 'vendor' in self.oc_supported_features:
				avp.setVendorID(self.oc_supported_features['vendor'])
			self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]

			for sf in self.supported_features:
				if sf!=None:
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

		if self.user_authorization_type!=None:
			avp = UserAuthorizationTypeAVP(self.user_authorization_type['value'])
			avp.setFlags(self.user_authorization_type['flags'])
			if 'vendor' in self.user_authorization_type:
				avp.setVendorID(self.user_authorization_type['vendor'])
			self.addAVP(avp)

		if self.session_priority!=None:
			avp = SessionPriorityAVP(self.session_priority['value'])
			avp.setFlags(self.session_priority['flags'])
			if 'vendor' in self.session_priority:
				avp.setVendorID(self.session_priority['vendor'])
			self.addAVP(avp)

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)

##
## @brief      Class that defines a DIAMETER Message
##
##		<Location-Info-Answer> ::= < Diameter Header: 302, PXY, 16777216 >
##					< Session-Id >
##					[ DRMP ]
##					{ Vendor-Specific-Application-Id }
##					[ Result-Code ]
##					[ Experimental-Result ]
##					{ Auth-Session-State }
##					{ Origin-Host }
##					{ Origin-Realm }
##					[ OC-Supported-Features ]
##					[ OC-OLR ]
##					*[ Supported-Features ]
##					[ Server-Name ]
##					[ Server-Capabilities ]
##					[ Wildcarded-Public-Identity ]
##					[ LIA-Flags ]
##					*[ AVP ]
##					*[ Failed-AVP ]
##					*[ Proxy-Info ]
##					*[ Route-Record ]
##
class DiamLocationInfoAnswer:
	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		drmp=None,
		result_code=None,
		experimental_result=None,
		oc_supported_features=None,
		oc_olr=None,
		supported_features=None,
		server_name=None,
		server_capabilities=None,
		wildcarded_public_identity=None,
		lia_flags=None,
		failed_avp=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.LOCATION_INFO, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.drmp = drmp
		self.result_code = result_code
		self.experimental_result = experimental_result
		self.oc_supported_features = oc_supported_features
		self.oc_olr = oc_olr
		self.supported_features = supported_features
		self.server_name = server_name
		self.server_capabilities = server_capabilities
		self.wildcarded_public_identity = wildcarded_public_identity
		self.lia_flags = lia_flags
		self.failed_avp = failed_avp
		self.proxy_info = proxy_info
		self.route_record = route_record

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

	def get_drmp(self):
		return self.drmp

	def get_result_code(self):
		return self.result_code

	def get_experimental_result(self):
		return self.experimental_result

	def get_oc_supported_features(self):
		return self.oc_supported_features

	def get_oc_olr(self):
		return self.oc_olr

	def get_supported_features(self):
		return self.supported_features

	def get_server_name(self):
		return self.server_name

	def get_server_capabilities(self):
		return self.server_capabilities

	def get_wildcarded_public_identity(self):
		return self.wildcarded_public_identity

	def get_lia_flags(self):
		return self.lia_flags

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

	def set_auth_session_state(self, value):
		self.auth_session_state = value

	def set_origin_host(self, value):
		self.origin_host = value

	def set_origin_realm(self, value):
		self.origin_realm = value

	def set_drmp(self, value):
		self.drmp = value

	def set_result_code(self, value):
		self.result_code = value

	def set_experimental_result(self, value):
		self.experimental_result = value

	def set_oc_supported_features(self, value):
		self.oc_supported_features = value

	def set_oc_olr(self, value):
		self.oc_olr = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_server_name(self, value):
		self.server_name = value

	def set_server_capabilities(self, value):
		self.server_capabilities = value

	def set_wildcarded_public_identity(self, value):
		self.wildcarded_public_identity = value

	def set_lia_flags(self, value):
		self.lia_flags = value

	def set_failed_avp(self, value):
		self.failed_avp = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('LIA: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('LIA: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]

		for vsid in self.vendor_specific_app_id:
			if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('LIA: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('LIA: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('LIA: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.result_code!=None:
			avp = ResultCodeAVP(self.result_code['value'])
			avp.setFlags(self.result_code['flags'])
			if 'vendor' in self.result_code:
				avp.setVendorID(self.result_code['vendor'])
			self.addAVP(avp)
			
		if self.experimental_result!=None:
			if 'type' in self.experimental_result and self.experimental_result['type']=='raw':
				avp = GenericAVP(DiamAVPCodes.EXPERIMENTAL_RESULT, self.experimental_result['value'])
			else:
				avp = ExperimentalResultAVP(self.experimental_result['value'])
				avp.setFlags(self.experimental_result['flags'])
				if 'vendor' in self.experimental_result:
					avp.setVendorID(self.experimental_result['vendor'])
			self.addAVP(avp)

		if self.oc_supported_features!=None:
			avp = OCSupportedFeaturesAVP(self.oc_supported_features['value'])
			avp.setFlags(self.oc_supported_features['flags'])
			if 'vendor' in self.oc_supported_features:
				avp.setVendorID(self.oc_supported_features['vendor'])
			self.addAVP(avp)

		if self.oc_olr!=None:
			avp = OCOLRAVP(self.oc_olr['value'])
			avp.setFlags(self.oc_olr['flags'])
			if 'vendor' in self.oc_olr:
				avp.setVendorID(self.oc_olr['vendor'])
			self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]

			for sf in self.supported_features:
				if sf!=None:
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

		if self.server_name!=None:
			avp = ServerNameAVP(self.server_name['value'])
			avp.setFlags(self.server_name['flags'])
			if 'vendor' in self.server_name:
				avp.setVendorID(self.server_name['vendor'])
			self.addAVP(avp)

		if self.server_capabilities!=None:
			if not isinstance(self.server_capabilities, list):
				self.server_capabilities = [self.server_capabilities]

			for val in self.server_capabilities:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.SERVER_CAPABILITIES, val['value'])
					else:
						topass = {'mandatory_capability': None,
								  'optional_capability': None,
								  'server_name': None,
								  'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'mandatory-capability':
							topass['mandatory_capability'] = valavp
						if valavp['name'] == 'optional-capability':
							topass['optional_capability'] = valavp
						if valavp['name'] == 'server-name':
							topass['server_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = ServerCapabilitiesAVP(topass['mandatory_capability'], topass['optional_capability'], topass['server_name'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.wildcarded_public_identity!=None:
			avp = WildcardedPublicIdentityAVP(self.wildcarded_public_identity['value'])
			avp.setFlags(self.wildcarded_public_identity['flags'])
			if 'vendor' in self.wildcarded_public_identity:
				avp.setVendorID(self.wildcarded_public_identity['vendor'])
			self.addAVP(avp)

		if self.lia_flags!=None:
			avp = LIAFlagsAVP(self.lia_flags['value'])
			avp.setFlags(self.lia_flags['flags'])
			if 'vendor' in self.lia_flags:
				avp.setVendorID(self.lia_flags['vendor'])
			self.addAVP(avp)

		if self.failed_avp!=None:
			if not isinstance(self.failed_avp, list):
				self.failed_avp = [self.failed_avp]
				
			for fa in self.failed_avp:
				if fa!=None:
					if 'type' in fa and fa['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.FAILED_AVP, fa['value'])
					else:
						avp = FailedAVP(fa['value'])
						avp.setFlags(fa['flags'])
						if 'vendor_id' in fa:
							avp.setVendorID(fa['vendor'])
					self.addAVP(avp)
		
		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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


		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)
''' /3GPP: LOCATION INFO '''

''' 3GPP: MULTIMEDIA AUTH '''
##
## @brief      Class that defines a DIAMETER Message
##
##		< Multimedia-Auth-Request > ::= < Diameter Header: 303, REQ, PXY, 16777216 >
##						< Session-Id >
##						[ DRMP ]
##						{ Vendor-Specific-Application-Id }
##						{ Auth-Session-State }
##						{ Origin-Host }
##						{ Origin-Realm }
##						{ Destination-Realm }
##						[ Destination-Host ]
##						{ User-Name }
##						[ OC-Supported-Features ]
##						*[ Supported-Features ]
##						{ Public-Identity }
##						{ SIP-Auth-Data-Item }
##						{ SIP-Number-Auth-Items }
##						{ Server-Name }
##						*[ AVP ]
##						*[ Proxy-Info ]
##						*[ Route-Record ]
##
class DiamMultimediaAuthRequest:
	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		destination_realm,
		user_name,
		public_identity,
		sip_auth_data_item,
		sip_number_auth_items,
		server_name,
		drmp=None,
		destination_host=None,
		oc_supported_features=None,
		supported_features=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.MULTIMEDIA_AUTH, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.destination_realm = destination_realm
		self.user_name = user_name
		self.public_identity = public_identity
		self.sip_auth_data_item = sip_auth_data_item
		self.sip_number_auth_items = sip_number_auth_items
		self.server_name = server_name
		self.drmp = drmp
		self.destination_host = destination_host
		self.oc_supported_features = oc_supported_features
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

	def get_destination_realm(self):
		return self.destination_realm

	def get_user_name(self):
		return self.user_name

	def get_public_identity(self):
		return self.public_identity

	def get_sip_auth_data_item(self):
		return self.sip_auth_data_item

	def get_sip_number_auth_items(self):
		return self.sip_number_auth_items

	def get_server_name(self):
		return self.server_name

	def get_drmp(self):
		return self.drmp

	def get_destination_host(self):
		return self.destination_host

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

	def set_vendor_specific_application_id(self, value):
		self.vendor_specific_application_id = value

	def set_auth_session_state(self, value):
		self.auth_session_state = value

	def set_origin_host(self, value):
		self.origin_host = value

	def set_origin_realm(self, value):
		self.origin_realm = value

	def set_destination_realm(self, value):
		self.destination_realm = value

	def set_user_name(self, value):
		self.user_name = value

	def set_public_identity(self, value):
		self.public_identity = value

	def set_sip_auth_data_item(self, value):
		self.sip_auth_data_item = value

	def set_sip_number_auth_items(self, value):
		self.sip_number_auth_items = value

	def set_server_name(self, value):
		self.server_name = value

	def set_drmp(self, value):
		self.drmp = value

	def set_destination_host(self, value):
		self.destination_host = value

	def set_oc_supported_features(self, value):
		self.oc_supported_features = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('MAR: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('MAR: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]

		for vsid in self.vendor_specific_app_id:
			if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('MAR: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('MAR: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('MAR: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.destination_realm==None:
			raise MissingMandatoryAVPException('MAR: The Destination-Realm AVP is MANDATORY')
		avp = DestinationRealmAVP(self.destination_realm['value'])
		avp.setFlags(self.destination_realm['flags'])
		if 'vendor' in self.destination_realm:
			avp.setVendorID(self.destination_realm['vendor'])
		self.addAVP(avp)

		if self.user_name==None:
			raise MissingMandatoryAVPException('MAR: The User-Name AVP is MANDATORY')
		avp = UserNameAVP(self.user_name['value'])
		avp.setFlags(self.user_name['flags'])
		if 'vendor' in self.user_name:
			avp.setVendorID(self.user_name['vendor'])
		self.addAVP(avp)

		if self.public_identity==None:
			raise MissingMandatoryAVPException('MAR: The Public-Identity AVP is MANDATORY')
		if not isinstance(self.PublicIdentityAVP, list):
			self.public_identity = [self.public_identity]

		for el in self.public_identity:
			if el!=None:
				if 'type' in el and el['type']=='raw':
					avp = GenericAVP(DiamAVPCodes.PUBLIC_IDENTITY, el['value'])
				else:
					avp = PublicIdentityAVP(el['value'])
					avp.setFlags(el['flags'])
					if 'vendor_id' in el:
						avp.setVendorID(el['vendor'])
			self.addAVP(avp)

		if self.sip_auth_data_item==None:
			raise MissingMandatoryAVPException('MAR: The SIP-Auth-Data-Item AVP is MANDATORY')
		if not isinstance(self.sip_auth_data_item, list):
			self.sip_auth_data_item = [self.sip_auth_data_item]

		for val in self.sip_auth_data_item:
			if val!=None:
				if 'type' in val and val['type']=='raw':
					avp = GenericAVP(DiamAVPCodes.SIP_AUTH_DATA_ITEM, val['value'])
				else:
					topass = {'sip_item_number':None,
							  'sip_authentication_scheme':None,
							  'sip_authenticate':None,
							  'sip_authenticate':None,
							  'sip_authorization':None,
							  'sip_authentication_context':None,
							  'confidentiality_key':None,
							  'integrity_key':None,
							  'sip_digest_authenticate':None,
							  'framed_ip_address':None,
							  'framed_ipv6_prefix':None,
							  'framed_interface_id':None,
							  'line_identifier':None,
							  'vendor_id':0}

				for valavp in val['avps']:
					if valavp['name'] == 'sip-item-number':
						topass['sip_item_number'] = valavp
					if valavp['name'] == 'sip-authentication-scheme':
						topass['sip_authentication_scheme'] = valavp
					if valavp['name'] == 'sip-authenticate':
						topass['sip_authenticate'] = valavp
					if valavp['name'] == 'sip-authorization':
						topass['sip_authorization'] = valavp
					if valavp['name'] == 'sip-authentication-context':
						topass['sip_authentication_context'] = valavp
					if valavp['name'] == 'confidentiality-key':
						topass['confidentiality_key'] = valavp
					if valavp['name'] == 'integrity-key':
						topass['integrity_key'] = valavp
					if valavp['name'] == 'sip-digest-authenticate':
						topass['sip_digest_authenticate'] = valavp
					if valavp['name'] == 'framed-ip-address':
						topass['framed_ip_address'] = valavp
					if valavp['name'] == 'framed-ipv6-prefix':
						topass['framed_ipv6_prefix'] = valavp
					if valavp['name'] == 'framed-interface-id':
						topass['framed_interface_id'] = valavp
					if valavp['name'] == 'line-identifier':
						topass['line_identifier'] = valavp
					if valavp['name'] == 'vendor-id':
						topass['vendor_id'] = valavp

				avp = SIPAuthDataItemAVP(topass['sip_item_number'], topass['sip_authentication_scheme'], topass['sip_authenticate'], topass['sip_authenticate'], topass['sip_authorization'], topass['sip_authentication_context'], topass['confidentiality_key'], topass['integrity_key'], topass['sip_digest_authenticate'], topass['framed_ip_address'], topass['framed_ipv6_prefix'], topass['framed_interface_id'], topass['line_identifier'], topass['vendor_id'])
				avp.setFlags(val['flags'])
			self.addAVP(avp)

		if self.sip_number_auth_items==None:
			raise MissingMandatoryAVPException('MAR: The SIP-Number-Auth-Items AVP is MANDATORY')
		avp = SIPNumberAuthItemsAVP(self.sip_number_auth_items['value'])
		avp.setFlags(self.sip_number_auth_items['flags'])
		if 'vendor' in self.sip_number_auth_items:
			avp.setVendorID(self.sip_number_auth_items['vendor'])
		self.addAVP(avp)

		if self.server_name==None:
			raise MissingMandatoryAVPException('MAR: The Server-Name AVP is MANDATORY')
		avp = ServerNameAVP(self.server_name['value'])
		avp.setFlags(self.server_name['flags'])
		if 'vendor' in self.server_name:
			avp.setVendorID(self.server_name['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.destination_host!=None:
			avp = DestinationHostAVP(self.destination_host['value'])
			avp.setFlags(self.destination_host['flags'])
			if 'vendor' in self.destination_host:
				avp.setVendorID(self.destination_host['vendor'])
			self.addAVP(avp)

		if self.oc_supported_features!=None:
			avp = OCSupportedFeaturesAVP(self.oc_supported_features['value'])
			avp.setFlags(self.oc_supported_features['flags'])
			if 'vendor' in self.oc_supported_features:
				avp.setVendorID(self.oc_supported_features['vendor'])
			self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]

			for sf in self.supported_features:
				if sf!=None:
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

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)

##
## @brief      Class that defines a DIAMETER Message
##
##		< Multimedia-Auth-Answer > ::= < Diameter Header: 303, PXY, 16777216 >
##						< Session-Id >
##						[ DRMP ]
##						{ Vendor-Specific-Application-Id }
##						[ Result-Code ]
##						[ Experimental-Result ]
##						{ Auth-Session-State }
##						{ Origin-Host }
##						{ Origin-Realm }
##						[ User-Name ]
##						[ OC-Supported-Features ]
##						[ OC-OLR ]
##						*[ Supported-Features ]
##						[ Public-Identity ]
##						[ SIP-Number-Auth-Items ]
##						*[SIP-Auth-Data-Item ]
##						*[ AVP ]
##						*[ Failed-AVP ]
##						*[ Proxy-Info ]
##						*[ Route-Record ]
##
class DiamMultimediaAuthAnswer:
	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		drmp=None,
		result_code=None,
		experimental_result=None,
		user_name=None,
		oc_supported_features=None,
		oc_olr=None,
		supported_features=None,
		public_identity=None,
		sip_number_auth_items=None,
		sip_auth_data_item=None,
		failed_avp=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.MULTIMEDIA_AUTH, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.drmp = drmp
		self.result_code = result_code
		self.experimental_result = experimental_result
		self.user_name = user_name
		self.oc_supported_features = oc_supported_features
		self.oc_olr = oc_olr
		self.supported_features = supported_features
		self.public_identity = public_identity
		self.sip_number_auth_items = sip_number_auth_items
		self.sip_auth_data_item = sip_auth_data_item
		self.failed_avp = failed_avp
		self.proxy_info = proxy_info
		self.route_record = route_record

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

	def get_drmp(self):
		return self.drmp

	def get_result_code(self):
		return self.result_code

	def get_experimental_result(self):
		return self.experimental_result

	def get_user_name(self):
		return self.user_name

	def get_oc_supported_features(self):
		return self.oc_supported_features

	def get_oc_olr(self):
		return self.oc_olr

	def get_supported_features(self):
		return self.supported_features

	def get_public_identity(self):
		return self.public_identity

	def get_sip_number_auth_items(self):
		return self.sip_number_auth_items

	def get_sip_auth_data_item(self):
		return self.sip_auth_data_item

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

	def set_auth_session_state(self, value):
		self.auth_session_state = value

	def set_origin_host(self, value):
		self.origin_host = value

	def set_origin_realm(self, value):
		self.origin_realm = value

	def set_drmp(self, value):
		self.drmp = value

	def set_result_code(self, value):
		self.result_code = value

	def set_experimental_result(self, value):
		self.experimental_result = value

	def set_user_name(self, value):
		self.user_name = value

	def set_oc_supported_features(self, value):
		self.oc_supported_features = value

	def set_oc_olr(self, value):
		self.oc_olr = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_public_identity(self, value):
		self.public_identity = value

	def set_sip_number_auth_items(self, value):
		self.sip_number_auth_items = value

	def set_sip_auth_data_item(self, value):
		self.sip_auth_data_item = value

	def set_failed_avp(self, value):
		self.failed_avp = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('MAA: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('MAA: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]

		for vsid in self.vendor_specific_app_id:
			if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('MAA: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('MAA: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('MAA: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.result_code!=None:
			avp = ResultCodeAVP(self.result_code['value'])
			avp.setFlags(self.result_code['flags'])
			if 'vendor' in self.result_code:
				avp.setVendorID(self.result_code['vendor'])
			self.addAVP(avp)
			
		if self.experimental_result!=None:
			if 'type' in self.experimental_result and self.experimental_result['type']=='raw':
				avp = GenericAVP(DiamAVPCodes.EXPERIMENTAL_RESULT, self.experimental_result['value'])
			else:
				avp = ExperimentalResultAVP(self.experimental_result['value'])
				avp.setFlags(self.experimental_result['flags'])
				if 'vendor' in self.experimental_result:
					avp.setVendorID(self.experimental_result['vendor'])
			self.addAVP(avp)
			
		if self.user_name!=None:
			avp = UserNameAVP(self.user_name['value'])
			avp.setFlags(self.user_name['flags'])
			if 'vendor' in self.user_name:
				avp.setVendorID(self.user_name['vendor'])
			self.addAVP(avp)

		if self.oc_supported_features!=None:
			avp = OCSupportedFeaturesAVP(self.oc_supported_features['value'])
			avp.setFlags(self.oc_supported_features['flags'])
			if 'vendor' in self.oc_supported_features:
				avp.setVendorID(self.oc_supported_features['vendor'])
			self.addAVP(avp)

		if self.oc_olr!=None:
			avp = OCOLRAVP(self.oc_olr['value'])
			avp.setFlags(self.oc_olr['flags'])
			if 'vendor' in self.oc_olr:
				avp.setVendorID(self.oc_olr['vendor'])
			self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]

			for sf in self.supported_features:
				if sf!=None:
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

		if self.public_identity!=None:
			if not isinstance(self.PublicIdentityAVP, list):
				self.public_identity = [self.public_identity]

			for el in self.public_identity:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.PUBLIC_IDENTITY, el['value'])
					else:
						avp = PublicIdentityAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)

		if self.sip_number_auth_items!=None:
			avp = SIPNumberAuthItemsAVP(self.sip_number_auth_items['value'])
			avp.setFlags(self.sip_number_auth_items['flags'])
			if 'vendor' in self.sip_number_auth_items:
				avp.setVendorID(self.sip_number_auth_items['vendor'])
			self.addAVP(avp)

		if self.sip_auth_data_item==None:
			raise MissingMandatoryAVPException('MAR: The SIP-Auth-Data-Item AVP is MANDATORY')
		if not isinstance(self.sip_auth_data_item, list):
			self.sip_auth_data_item = [self.sip_auth_data_item]

		for val in self.sip_auth_data_item:
			if val!=None:
				if 'type' in val and val['type']=='raw':
					avp = GenericAVP(DiamAVPCodes.SIP_AUTH_DATA_ITEM, val['value'])
				else:
					topass = {'sip_item_number':None,
							  'sip_authentication_scheme':None,
							  'sip_authenticate':None,
							  'sip_authenticate':None,
							  'sip_authorization':None,
							  'sip_authentication_context':None,
							  'confidentiality_key':None,
							  'integrity_key':None,
							  'sip_digest_authenticate':None,
							  'framed_ip_address':None,
							  'framed_ipv6_prefix':None,
							  'framed_interface_id':None,
							  'line_identifier':None,
							  'vendor_id':0}

				for valavp in val['avps']:
					if valavp['name'] == 'sip-item-number':
						topass['sip_item_number'] = valavp
					if valavp['name'] == 'sip-authentication-scheme':
						topass['sip_authentication_scheme'] = valavp
					if valavp['name'] == 'sip-authenticate':
						topass['sip_authenticate'] = valavp
					if valavp['name'] == 'sip-authorization':
						topass['sip_authorization'] = valavp
					if valavp['name'] == 'sip-authentication-context':
						topass['sip_authentication_context'] = valavp
					if valavp['name'] == 'confidentiality-key':
						topass['confidentiality_key'] = valavp
					if valavp['name'] == 'integrity-key':
						topass['integrity_key'] = valavp
					if valavp['name'] == 'sip-digest-authenticate':
						topass['sip_digest_authenticate'] = valavp
					if valavp['name'] == 'framed-ip-address':
						topass['framed_ip_address'] = valavp
					if valavp['name'] == 'framed-ipv6-prefix':
						topass['framed_ipv6_prefix'] = valavp
					if valavp['name'] == 'framed-interface-id':
						topass['framed_interface_id'] = valavp
					if valavp['name'] == 'line-identifier':
						topass['line_identifier'] = valavp
					if valavp['name'] == 'vendor-id':
						topass['vendor_id'] = valavp

				avp = SIPAuthDataItemAVP(topass['sip_item_number'], topass['sip_authentication_scheme'], topass['sip_authenticate'], topass['sip_authenticate'], topass['sip_authorization'], topass['sip_authentication_context'], topass['confidentiality_key'], topass['integrity_key'], topass['sip_digest_authenticate'], topass['framed_ip_address'], topass['framed_ipv6_prefix'], topass['framed_interface_id'], topass['line_identifier'], topass['vendor_id'])
				avp.setFlags(val['flags'])
			self.addAVP(avp)

		if self.failed_avp!=None:
			if not isinstance(self.failed_avp, list):
				self.failed_avp = [self.failed_avp]
				
			for fa in self.failed_avp:
				if fa!=None:
					if 'type' in fa and fa['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.FAILED_AVP, fa['value'])
					else:
						avp = FailedAVP(fa['value'])
						avp.setFlags(fa['flags'])
						if 'vendor_id' in fa:
							avp.setVendorID(fa['vendor'])
					self.addAVP(avp)

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)
''' /3GPP: MULTIMEDIA AUTH '''

''' 3GPP: REGISTRATION TERMINATION '''
##
## @brief      Class that defines a DIAMETER Message
##
##		<Registration-Termination-Request> ::= < Diameter Header: 304, REQ, PXY, 16777216 >
##							< Session-Id >
##							[ DRMP ]
##							{ Vendor-Specific-Application-Id }
##							{ Auth-Session-State }
##							{ Origin-Host }
##							{ Origin-Realm }
##							{ Destination-Host }
##							{ Destination-Realm }
##							{ User-Name }
##							[ Associated-Identities ]
##							*[ Supported-Features ]
##							*[ Public-Identity ]
##							{Deregistration-Reason }
##							*[ AVP ]
##							*[ Proxy-Info ]
##							*[ Route-Record ]
##
class DiamRegistrationTerminationRequest:
	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		destination_host,
		destination_realm,
		user_name,
		deregistration_reason,
		drmp=None,
		associated_identities=None,
		supported_features=None,
		public_identity=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.REGISTRATION_TERMINATION, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.destination_host = destination_host
		self.destination_realm = destination_realm
		self.user_name = user_name
		self.deregistration_reason = deregistration_reason
		self.drmp = drmp
		self.associated_identities = associated_identities
		self.supported_features = supported_features
		self.public_identity = public_identity
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

	def get_user_name(self):
		return self.user_name

	def get_deregistration_reason(self):
		return self.deregistration_reason

	def get_drmp(self):
		return self.drmp

	def get_associated_identities(self):
		return self.associated_identities

	def get_supported_features(self):
		return self.supported_features

	def get_public_identity(self):
		return self.public_identity

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

	def set_user_name(self, value):
		self.user_name = value

	def set_deregistration_reason(self, value):
		self.deregistration_reason = value

	def set_drmp(self, value):
		self.drmp = value

	def set_associated_identities(self, value):
		self.associated_identities = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_public_identity(self, value):
		self.public_identity = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('RTR: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('RTR: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]

		for vsid in self.vendor_specific_app_id:
			if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('RTR: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('RTR: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('RTR: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.destination_host==None:
			raise MissingMandatoryAVPException('RTR: The Destination-Host AVP is MANDATORY')
		avp = DestinationHostAVP(self.destination_host['value'])
		avp.setFlags(self.destination_host['flags'])
		if 'vendor' in self.destination_host:
			avp.setVendorID(self.destination_host['vendor'])
		self.addAVP(avp)

		if self.destination_realm==None:
			raise MissingMandatoryAVPException('RTR: The Destination-Realm AVP is MANDATORY')
		avp = DestinationRealmAVP(self.destination_realm['value'])
		avp.setFlags(self.destination_realm['flags'])
		if 'vendor' in self.destination_realm:
			avp.setVendorID(self.destination_realm['vendor'])
		self.addAVP(avp)

		if self.user_name==None:
			raise MissingMandatoryAVPException('RTR: The User-Name AVP is MANDATORY')
		avp = UserNameAVP(self.user_name['value'])
		avp.setFlags(self.user_name['flags'])
		if 'vendor' in self.user_name:
			avp.setVendorID(self.user_name['vendor'])
		self.addAVP(avp)

		if self.deregistration_reason==None:
			raise MissingMandatoryAVPException('RTR: The Deregistration-Reason AVP is MANDATORY')
		if not isinstance(self.deregistration_reason, list):
			self.deregistration_reason = [self.deregistration_reason]

		for val in self.deregistration_reason:
			if val!=None:
				if 'type' in val and val['type']=='raw':
					avp = GenericAVP(DiamAVPCodes.DEREGISTRATION_REASON, val['value'])
				else:
					topass = {'reason_code':None,
							  'reason_info':None,
							  'vendor_id':0}

				for valavp in val['avps']:
					if valavp['name'] == 'reason-code':
						topass['reason_code'] = valavp
					if valavp['name'] == 'reason-info':
						topass['reason_info'] = valavp
					if valavp['name'] == 'vendor-id':
						topass['vendor_id'] = valavp

				avp = DeregistrationReasonAVP(topass['reason_code'], topass['reason_info'], topass['vendor_id'])
				avp.setFlags(val['flags'])
			self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.associated_identities!=None:
			if not isinstance(self.associated_identities, list):
				self.associated_identities = [self.associated_identities]

			for val in self.associated_identities:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ASSOCIATED_IDENTITIES, val['value'])
					else:
						topass = {'user_name':None,
								  'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'user-name':
							topass['user_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = AssociatedIdentitiesAVP(topass['user_name'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]

			for sf in self.supported_features:
				if sf!=None:
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

		if self.public_identity!=None:
			if not isinstance(self.PublicIdentityAVP, list):
				self.public_identity = [self.public_identity]

			for el in self.public_identity:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.PUBLIC_IDENTITY, el['value'])
					else:
						avp = PublicIdentityAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)

class DiamRegistrationTerminationAnswer:
	'''
		Class that defines a DIAMETER Message

		<Registration-Termination-Answer> ::= < Diameter Header: 304, PXY, 16777216 >
							< Session-Id >
							< Session-Id >
							[ DRMP ]
							{ Vendor-Specific-Application-Id }
							[ Result-Code ]
							[ Experimental-Result ]
							{ Auth-Session-State }
							{ Origin-Host }
							{ Origin-Realm }
							[ Associated-Identities ]
							*[ Supported-Features ]
							*[ Identity-with-Emergency-Registration ]
							*[ AVP ]
							*[ Failed-AVP ]
							*[ Proxy-Info ]
							*[ Route-Record ]
	'''
		

	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		drmp=None,
		result_code=None,
		experimental_result=None,
		associated_identities=None,
		supported_features=None,
		identity_with_emergency_registration=None,
		failed_avp=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.REGISTRATION_TERMINATION, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.drmp = drmp
		self.result_code = result_code
		self.experimental_result = experimental_result
		self.associated_identities = associated_identities
		self.supported_features = supported_features
		self.identity_with_emergency_registration = identity_with_emergency_registration
		self.failed_avp = failed_avp
		self.proxy_info = proxy_info
		self.route_record = route_record

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

	def get_drmp(self):
		return self.drmp

	def get_result_code(self):
		return self.result_code

	def get_experimental_result(self):
		return self.experimental_result

	def get_associated_identities(self):
		return self.associated_identities

	def get_supported_features(self):
		return self.supported_features

	def get_identity_with_emergency_registration(self):
		return self.identity_with_emergency_registration

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

	def set_auth_session_state(self, value):
		self.auth_session_state = value

	def set_origin_host(self, value):
		self.origin_host = value

	def set_origin_realm(self, value):
		self.origin_realm = value

	def set_drmp(self, value):
		self.drmp = value

	def set_result_code(self, value):
		self.result_code = value

	def set_experimental_result(self, value):
		self.experimental_result = value

	def set_associated_identities(self, value):
		self.associated_identities = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_identity_with_emergency_registration(self, value):
		self.identity_with_emergency_registration = value

	def set_failed_avp(self, value):
		self.failed_avp = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('RTA: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('RTA: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]

		for vsid in self.vendor_specific_app_id:
			if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('RTA: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('RTA: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('RTA: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.result_code!=None:
			avp = ResultCodeAVP(self.result_code['value'])
			avp.setFlags(self.result_code['flags'])
			if 'vendor' in self.result_code:
				avp.setVendorID(self.result_code['vendor'])
			self.addAVP(avp)
			
		if self.experimental_result!=None:
			if 'type' in self.experimental_result and self.experimental_result['type']=='raw':
				avp = GenericAVP(DiamAVPCodes.EXPERIMENTAL_RESULT, self.experimental_result['value'])
			else:
				avp = ExperimentalResultAVP(self.experimental_result['value'])
				avp.setFlags(self.experimental_result['flags'])
				if 'vendor' in self.experimental_result:
					avp.setVendorID(self.experimental_result['vendor'])
			self.addAVP(avp)

		if self.associated_identities!=None:
			if not isinstance(self.associated_identities, list):
				self.associated_identities = [self.associated_identities]

			for val in self.associated_identities:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ASSOCIATED_IDENTITIES, val['value'])
					else:
						topass = {'user_name':None,
								  'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'user-name':
							topass['user_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = AssociatedIdentitiesAVP(topass['user_name'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]

			for sf in self.supported_features:
				if sf!=None:
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

		if self.identity_with_emergency_registration!=None:
			if not isinstance(self.identity_with_emergency_registration, list):
				self.identity_with_emergency_registration = [self.identity_with_emergency_registration]

			for val in self.identity_with_emergency_registration:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.IDENTITY_WITH_EMERGENCY_REGISTRATION, val['value'])
					else:
						topass = {'user_name':None,
								  'public_identity':None,
								  'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'user-name':
							topass['user_name'] = valavp
						if valavp['name'] == 'public-identity':
							topass['public_identity'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = IdentitywithEmergencyRegistrationAVP(topass['user_name'], topass['public_identity'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.failed_avp!=None:
			if not isinstance(self.failed_avp, list):
				self.failed_avp = [self.failed_avp]
				
			for fa in self.failed_avp:
				if fa!=None:
					if 'type' in fa and fa['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.FAILED_AVP, fa['value'])
					else:
						avp = FailedAVP(fa['value'])
						avp.setFlags(fa['flags'])
						if 'vendor_id' in fa:
							avp.setVendorID(fa['vendor'])
					self.addAVP(avp)

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)
''' /3GPP: REGISTRATION TERMINATION '''

''' 3GPP: PUSH PROFILE '''
class DiamPushProfileRequest:
	'''
		Class that defines a DIAMETER Message

		< Push-Profile-Request > ::= < Diameter Header: 305, REQ, PXY, 16777216 >
					< Session-Id >
					[ DRMP ]
					{ Vendor-Specific-Application-Id }
					{ Auth-Session-State }
					{ Origin-Host }
					{ Origin-Realm }
					{ Destination-Host }
					{ Destination-Realm }
					{ User-Name }
					*[ Supported-Features ]
					[ User-Data ]
					[ Charging-Information ]
					[ SIP-Auth-Data-Item ]
					[ Allowed-WAF-WWSF-Identities ]
					*[ AVP ]
					*[ Proxy-Info ]
					*[ Route-Record ]
	'''
		

	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		destination_host,
		destination_realm,
		user_name,
		drmp=None,
		supported_features=None,
		user_data=None,
		charging_information=None,
		sip_auth_data_item=None,
		allowed_waf_wwsf_identities=None,
		avp=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.PUSH_PROFILE, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.destination_host = destination_host
		self.destination_realm = destination_realm
		self.user_name = user_name
		self.drmp = drmp
		self.supported_features = supported_features
		self.user_data = user_data
		self.charging_information = charging_information
		self.sip_auth_data_item = sip_auth_data_item
		self.allowed_waf_wwsf_identities = allowed_waf_wwsf_identities
		self.avp = avp
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

	def get_user_name(self):
		return self.user_name

	def get_drmp(self):
		return self.drmp

	def get_supported_features(self):
		return self.supported_features

	def get_user_data(self):
		return self.user_data

	def get_charging_information(self):
		return self.charging_information

	def get_sip_auth_data_item(self):
		return self.sip_auth_data_item

	def get_allowed_waf_wwsf_identities(self):
		return self.allowed_waf_wwsf_identities

	def get_avp(self):
		return self.avp

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

	def set_user_name(self, value):
		self.user_name = value

	def set_drmp(self, value):
		self.drmp = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_user_data(self, value):
		self.user_data = value

	def set_charging_information(self, value):
		self.charging_information = value

	def set_sip_auth_data_item(self, value):
		self.sip_auth_data_item = value

	def set_allowed_waf_wwsf_identities(self, value):
		self.allowed_waf_wwsf_identities = value

	def set_avp(self, value):
		self.avp = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('PPR: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('PPR: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]

		for vsid in self.vendor_specific_app_id:
			if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('PPR: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('PPR: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('PPR: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.destination_host==None:
			raise MissingMandatoryAVPException('PPR: The Destination-Host AVP is MANDATORY')
		avp = DestinationHostAVP(self.destination_host['value'])
		avp.setFlags(self.destination_host['flags'])
		if 'vendor' in self.destination_host:
			avp.setVendorID(self.destination_host['vendor'])
		self.addAVP(avp)

		if self.destination_realm==None:
			raise MissingMandatoryAVPException('PPR: The Destination-Realm AVP is MANDATORY')
		avp = DestinationRealmAVP(self.destination_realm['value'])
		avp.setFlags(self.destination_realm['flags'])
		if 'vendor' in self.destination_realm:
			avp.setVendorID(self.destination_realm['vendor'])
		self.addAVP(avp)

		if self.user_name==None:
			raise MissingMandatoryAVPException('PPR: The User-Name AVP is MANDATORY')
		avp = UserNameAVP(self.user_name['value'])
		avp.setFlags(self.user_name['flags'])
		if 'vendor' in self.user_name:
			avp.setVendorID(self.user_name['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]

			for sf in self.supported_features:
				if sf!=None:
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

		if self.user_data!=None:
			avp = UserDataAVP(self.user_data['value'])
			avp.setFlags(self.user_data['flags'])
			if 'vendor' in self.user_data:
				avp.setVendorID(self.user_data['vendor'])
			self.addAVP(avp)

		if self.charging_information!=None:
			if not isinstance(self.charging_information, list):
				self.charging_information = [self.charging_information]

			for val in self.charging_information:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.CHARGING_INFORMATION, val['value'])
					else:
						topass = {'primary_event_charging_function_name': None,
								  'secondary_event_charging_function_name': None,
								  'primary_charging_collection_function_name': None,
								  'secondary_charging_collection_function_name': None,
								  'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'primary-event-charging-function-name':
							topass['primary_event_charging_function_name'] = valavp
						if valavp['name'] == 'secondary-event-charging-function-name':
							topass['secondary_event_charging_function_name'] = valavp
						if valavp['name'] == 'primary-charging-collection-function-name':
							topass['primary_charging_collection_function_name'] = valavp
						if valavp['name'] == 'secondary-charging-collection-function-name':
							topass['secondary_charging_collection_function_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = ChargingInformationAVP(topass['primary_event_charging_function_name'], topass['secondary_event_charging_function_name'], topass['primary_charging_collection_function_name'], topass['secondary_charging_collection_function_name'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.sip_auth_data_item==None:
			raise MissingMandatoryAVPException('MAR: The SIP-Auth-Data-Item AVP is MANDATORY')
		if not isinstance(self.sip_auth_data_item, list):
			self.sip_auth_data_item = [self.sip_auth_data_item]

		for val in self.sip_auth_data_item:
			if val!=None:
				if 'type' in val and val['type']=='raw':
					avp = GenericAVP(DiamAVPCodes.SIP_AUTH_DATA_ITEM, val['value'])
				else:
					topass = {'sip_item_number':None,
							  'sip_authentication_scheme':None,
							  'sip_authenticate':None,
							  'sip_authenticate':None,
							  'sip_authorization':None,
							  'sip_authentication_context':None,
							  'confidentiality_key':None,
							  'integrity_key':None,
							  'sip_digest_authenticate':None,
							  'framed_ip_address':None,
							  'framed_ipv6_prefix':None,
							  'framed_interface_id':None,
							  'line_identifier':None,
							  'vendor_id':0}

				for valavp in val['avps']:
					if valavp['name'] == 'sip-item-number':
						topass['sip_item_number'] = valavp
					if valavp['name'] == 'sip-authentication-scheme':
						topass['sip_authentication_scheme'] = valavp
					if valavp['name'] == 'sip-authenticate':
						topass['sip_authenticate'] = valavp
					if valavp['name'] == 'sip-authorization':
						topass['sip_authorization'] = valavp
					if valavp['name'] == 'sip-authentication-context':
						topass['sip_authentication_context'] = valavp
					if valavp['name'] == 'confidentiality-key':
						topass['confidentiality_key'] = valavp
					if valavp['name'] == 'integrity-key':
						topass['integrity_key'] = valavp
					if valavp['name'] == 'sip-digest-authenticate':
						topass['sip_digest_authenticate'] = valavp
					if valavp['name'] == 'framed-ip-address':
						topass['framed_ip_address'] = valavp
					if valavp['name'] == 'framed-ipv6-prefix':
						topass['framed_ipv6_prefix'] = valavp
					if valavp['name'] == 'framed-interface-id':
						topass['framed_interface_id'] = valavp
					if valavp['name'] == 'line-identifier':
						topass['line_identifier'] = valavp
					if valavp['name'] == 'vendor-id':
						topass['vendor_id'] = valavp

				avp = SIPAuthDataItemAVP(topass['sip_item_number'], topass['sip_authentication_scheme'], topass['sip_authenticate'], topass['sip_authenticate'], topass['sip_authorization'], topass['sip_authentication_context'], topass['confidentiality_key'], topass['integrity_key'], topass['sip_digest_authenticate'], topass['framed_ip_address'], topass['framed_ipv6_prefix'], topass['framed_interface_id'], topass['line_identifier'], topass['vendor_id'])
				avp.setFlags(val['flags'])
			self.addAVP(avp)

		if self.allowed_waf_wwsf_identities!=None:
			if not isinstance(self.allowed_waf_wwsf_identities, list):
				self.allowed_waf_wwsf_identities = [self.allowed_waf_wwsf_identities]

			for val in self.allowed_waf_wwsf_identities:
				if val!=None:
					if 'type' in val and val['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ALLOWED_WAF_WWSF_IDENTITIES, val['value'])
					else:
						topass = {'webrtc_authentication_function_name':None,
								  'webrtc_web_server_function_name':None,
						'vendor_id':0}

					for valavp in val['avps']:
						if valavp['name'] == 'webrtc-authentication-function-name':
							topass['webrtc_authentication_function_name'] = valavp
						if valavp['name'] == 'webrtc-web-server-function-name':
							topass['webrtc_web_server_function_name'] = valavp
						if valavp['name'] == 'vendor-id':
							topass['vendor_id'] = valavp

					avp = AllowedWAFWWSFIdentitiesAVP(topass['webrtc_authentication_function_name'], topass['webrtc_web_server_function_name'], topass['vendor_id'])
					avp.setFlags(val['flags'])
				self.addAVP(avp)

		if self.avp!=None:
			avp = AVPAVP(self.avp['value'])
			avp.setFlags(self.avp['flags'])
			if 'vendor' in self.avp:
				avp.setVendorID(self.avp['vendor'])
			self.addAVP(avp)

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)

class DiamPushProfileAnswer:
	'''
		Class that defines a DIAMETER Message

		< Push-Profile-Answer > ::= < Diameter Header: 305, PXY, 16777216 >
					< Session-Id >
					[ DRMP ]
					{ Vendor-Specific-Application-Id }
					[Result-Code ]
					[ Experimental-Result ]
					{ Auth-Session-State }
					{ Origin-Host }
					{ Origin-Realm }
					*[ Supported-Features ]
					*[ AVP ]
					*[ Failed-AVP ]
					*[ Proxy-Info ]
					*[ Route-Record ]
	'''
		

	def __init__(self, 
		app_id,
		session_id,
		vendor_specific_application_id,
		auth_session_state,
		origin_host,
		origin_realm,
		drmp=None,
		result_code=None,
		experimental_result=None,
		supported_features=None,
		failed_avp=None,
		proxy_info=None,
		route_record=None):

		DiamMessage.__init__(self, DiamCommandCodes.PUSH_PROFILE, app_id)

		self.session_id = session_id
		self.vendor_specific_application_id = vendor_specific_application_id
		self.auth_session_state = auth_session_state
		self.origin_host = origin_host
		self.origin_realm = origin_realm
		self.drmp = drmp
		self.result_code = result_code
		self.experimental_result = experimental_result
		self.supported_features = supported_features
		self.failed_avp = failed_avp
		self.proxy_info = proxy_info
		self.route_record = route_record

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

	def get_drmp(self):
		return self.drmp

	def get_result_code(self):
		return self.result_code

	def get_experimental_result(self):
		return self.experimental_result

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

	def set_auth_session_state(self, value):
		self.auth_session_state = value

	def set_origin_host(self, value):
		self.origin_host = value

	def set_origin_realm(self, value):
		self.origin_realm = value

	def set_drmp(self, value):
		self.drmp = value

	def set_result_code(self, value):
		self.result_code = value

	def set_experimental_result(self, value):
		self.experimental_result = value

	def set_supported_features(self, value):
		self.supported_features = value

	def set_failed_avp(self, value):
		self.failed_avp = value

	def set_proxy_info(self, value):
		self.proxy_info = value

	def set_route_record(self, value):
		self.route_record = value


	def generateMessage(self):
		if self.session_id==None:
			raise MissingMandatoryAVPException('PPA: The Session-ID AVP is MANDATORY')
		avp = SessionIDAVP(self.session_id['value'])
		avp.setFlags(self.session_id['flags'])
		if 'vendor' in self.session_id:
			avp.setVendorID(self.session_id['vendor'])
		self.addAVP(avp)

		if self.vendor_specific_application_id==None:
			raise MissingMandatoryAVPException('PPA: The Vendor-Specific-Application-Id AVP is MANDATORY')
		if not isinstance(self.vendor_specific_application_id, list):
			self.vendor_specific_application_id = [self.vendor_specific_application_id]

		for vsid in self.vendor_specific_app_id:
			if vsid!=None:
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

		if self.auth_session_state==None:
			raise MissingMandatoryAVPException('PPA: The Auth-Session-State AVP is MANDATORY')
		avp = AuthSessionStateAVP(self.auth_session_state['value'])
		avp.setFlags(self.auth_session_state['flags'])
		if 'vendor' in self.auth_session_state:
			avp.setVendorID(self.auth_session_state['vendor'])
		self.addAVP(avp)

		if self.origin_host==None:
			raise MissingMandatoryAVPException('PPA: The Origin-Host AVP is MANDATORY')
		avp = OriginHostAVP(self.origin_host['value'])
		avp.setFlags(self.origin_host['flags'])
		if 'vendor' in self.origin_host:
			avp.setVendorID(self.origin_host['vendor'])
		self.addAVP(avp)

		if self.origin_realm==None:
			raise MissingMandatoryAVPException('PPA: The Origin-Realm AVP is MANDATORY')
		avp = OriginRealmAVP(self.origin_realm['value'])
		avp.setFlags(self.origin_realm['flags'])
		if 'vendor' in self.origin_realm:
			avp.setVendorID(self.origin_realm['vendor'])
		self.addAVP(avp)

		if self.drmp!=None:
			avp = DRMPAVP(self.drmp['value'])
			avp.setFlags(self.drmp['flags'])
			if 'vendor' in self.drmp:
				avp.setVendorID(self.drmp['vendor'])
			self.addAVP(avp)

		if self.result_code!=None:
			avp = ResultCodeAVP(self.result_code['value'])
			avp.setFlags(self.result_code['flags'])
			if 'vendor' in self.result_code:
				avp.setVendorID(self.result_code['vendor'])
			self.addAVP(avp)
			
		if self.experimental_result!=None:
			if 'type' in self.experimental_result and self.experimental_result['type']=='raw':
				avp = GenericAVP(DiamAVPCodes.EXPERIMENTAL_RESULT, self.experimental_result['value'])
			else:
				avp = ExperimentalResultAVP(self.experimental_result['value'])
				avp.setFlags(self.experimental_result['flags'])
				if 'vendor' in self.experimental_result:
					avp.setVendorID(self.experimental_result['vendor'])
			self.addAVP(avp)

		if self.supported_features!=None:
			if not isinstance(self.supported_features, list):
				self.supported_features = [self.supported_features]

			for sf in self.supported_features:
				if sf!=None:
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

		if self.failed_avp!=None:
			if not isinstance(self.failed_avp, list):
				self.failed_avp = [self.failed_avp]
				
			for fa in self.failed_avp:
				if fa!=None:
					if 'type' in fa and fa['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.FAILED_AVP, fa['value'])
					else:
						avp = FailedAVP(fa['value'])
						avp.setFlags(fa['flags'])
						if 'vendor_id' in fa:
							avp.setVendorID(fa['vendor'])
					self.addAVP(avp)

		if self.proxy_info!=None:
			if not isinstance(self.proxy_info, list):
				self.proxy_info = [self.proxy_info]
				
			for pi in self.proxy_info:
				if pi!=None:
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

		if self.route_record!=None:
			if not isinstance(self.RouteRecordAVP, list):
				self.route_record = [self.route_record]

			for el in self.route_record:
				if el!=None:
					if 'type' in el and el['type']=='raw':
						avp = GenericAVP(DiamAVPCodes.ROUTE_RECORD, el['value'])
					else:
						avp = RouteRecordAVP(el['value'])
						avp.setFlags(el['flags'])
						if 'vendor_id' in el:
							avp.setVendorID(el['vendor'])
				self.addAVP(avp)
''' /3GPP: PUSH PROFILE '''