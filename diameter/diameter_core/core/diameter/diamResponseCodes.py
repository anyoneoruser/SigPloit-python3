##
## @brief      Class that defines Diameter's Response Codes
## 
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##
class DiamResponseCodes(object):
    ''' Informational '''
    DIAMETER_MULTI_ROUND_AUTH           = 1001
    
    ''' Success '''
    DIAMETER_SUCCESS                    = 2001
    DIAMETER_LIMITED_SUCCESS            = 2002
    
    ''' Protocol Errors '''
    DIAMETER_COMMAND_UNSUPPORTED        = 3001
    DIAMETER_UNABLE_TO_DELIVER          = 3002
    DIAMETER_REALM_NOT_SERVED           = 3003
    DIAMETER_TOO_BUSY                   = 3004
    DIAMETER_LOOP_DETECTED              = 3005
    DIAMETER_REDIRECT_INDICATION        = 3006
    DIAMETER_APPLICATION_UNSUPPORTED    = 3007
    DIAMETER_INVALID_HDR_BITS           = 3008
    DIAMETER_INVALID_AVP_BITS           = 3009
    DIAMETER_UNKNOWN_PEER               = 3010
    
    ''' Transient Failures '''
    DIAMETER_AUTHENTICATION_REJECTED    = 4001
    DIAMETER_OUT_OF_SPACE               = 4002
    ELECTION_LOST                       = 4003
    
    ''' Permanent Failure '''
    DIAMETER_AVP_UNSUPPORTED            = 5001
    DIAMETER_UNKNOWN_SESSION_ID         = 5002
    DIAMETER_AUTHORIZATION_REJECTED     = 5003
    DIAMETER_INVALID_AVP_VALUE          = 5004
    DIAMETER_MISSING_AVP                = 5005
    DIAMETER_RESOURCES_EXCEEDED         = 5006
    DIAMETER_CONTRADICTING_AVPS         = 5007
    DIAMETER_AVP_NOT_ALLOWED            = 5008
    DIAMETER_AVP_OCCURS_TOO_MANY_TIMES  = 5009
    DIAMETER_NO_COMMON_APPLICATION      = 5010
    DIAMETER_UNSUPPORTED_VERSION        = 5011
    DIAMETER_UNABLE_TO_COMPLY           = 5012
    DIAMETER_INVALID_BIT_IN_HEADER      = 5013
    DIAMETER_INVALID_AVP_LENGTH         = 5014
    DIAMETER_INVALID_MESSAGE_LENGTH     = 5015
    DIAMETER_INVALID_AVP_BIT_COMBO      = 5016
    DIAMETER_NO_COMMON_SECURITY         = 5017
    