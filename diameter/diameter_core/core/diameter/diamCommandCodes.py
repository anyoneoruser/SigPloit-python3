##
## @brief      Class that defines all the Diameter AVP's Command Codes
## 
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##
class DiamCommandCodes:
    CAPABILITIES_EXCHANGE               = 257
    RE_AUTH                             = 258
    SESSION_TERMINATION                 = 275
    AA                                  = 265
    DIAMETER_EAP                        = 268
    ACCOUNTING                          = 271
    CREDIT_CONTROL                      = 272
    ABORT_SESSION                       = 274
    DEVICE_WATCHDOG                     = 280
    DISCONNECT_PEER                     = 282
    USER_DATA                           = 306
    PROFILE_UPDATE                      = 307
    SUBSCRIBE_NOTIFICATIONS             = 308
    PUSH_NOTIFICATION                   = 309
    BOOTSTRAPPING_INFO                  = 310
    MESSAGE_PROCESS                     = 311
    
    ''' 3GPP S6a CODES '''
    UPDATE_LOCATION_3GPP                = 316       # ULR/ULA    3GPP TS 29.272
    CANCEL_LOCATION_3GPP                = 317       # CLR/CLA    3GPP TS 29.272
    AUTHENTICATION_INFORMATION_3GPP     = 318       # AIR/AIA    3GPP TS 29.272
    INSERT_SUBSCRIBER_DATA_3GPP         = 319       # IDR/IDA    3GPP TS 29.272
    DELETE_SUBSCRIBER_DATA_3GPP         = 320       # DSR/DSA    3GPP TS 29.272
    PURGE_UE_3GPP                       = 321       # PUR/PUA    3GPP TS 29.272
    RESET_3GPP                          = 322       # RSR/RSA    3GPP TS 29.272
    NOTIFY_3GPP                         = 323       # NOR/NOA    3GPP TS 29.272
    ME_IDENTITY_CHECK_3GPP              = 324       # ECR/ECA    3GPP TS 29.272
    
    ''' 3GPP SLh CODES '''
    LCS_ROUTING_INFO                    = 8388622   # RIR/RIA    3GPP TS 29.273
    
    ''' 3GPP SLg CODES '''
    PROVIDE_LOCATION                    = 8388620   # PLR/PLA    3GPP TS 29.172
    LOCATION_REPORT                     = 8388621   # LRR/LRA    3GPP TS 29.172
    
    ''' 3GPP Cx/Dx (VoLTE) CODES '''
    # Command-Codes are taken from the range allocated by IANA in IETF RFC 3589 #
    USER_AUTHORIZATION                  = 300       # UAR/UAA    3GPP TS 29.229
    SERVER_ASSIGNMENT                   = 301       # SAR/SAA    3GPP TS 29.229
    LOCATION_INFO                       = 302       # LIR/LIA    3GPP TS 29.229
    MULTIMEDIA_AUTH                     = 303       # MAR/MAA    3GPP TS 29.229
    REGISTRATION_TERMINATION            = 304       # RTR/RTA    3GPP TS 29.229
    PUSH_PROFILE                        = 305       # PPR/PPA    3GPP TS 29.229
    