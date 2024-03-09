#!/usr/bin/env  python
# -*- coding: utf-8 -*-

from ..utilities import getFuzzyAvpCodes

from ..diameter.diamApplicationIDs import DiamApplicationIDs


from ..commons import logNormal

from ..diameter.diam_avp_data import DiamAVP_Unsigned32, DiamAVP_Integer32,\
    DiamAVP_Unsigned64, SessionIDAVP, DiamAVP_DiamIdent,  DiamAVP_OctetString, \
    DiamAVP_Time, DiamAVP_UTF8String, DiamAVP_Address, DiamAVP_Grouped
from ..fuzzy.fuzzer import Fuzzer

from ...core.diameter.diamAVPCodes import DiamAVPCodes
import random
##
## @brief      Generates FUZZY Diameter's messages
## 
##
##
class FuzzyInterface():
    def __init__(self, conf, msgs):
        self.__loadConfig(conf)
        self.appid = DiamApplicationIDs.DIAMETER_COMMON_MESSAGES
        self.fuzzyAvpCodes = getFuzzyAvpCodes(self.conf['avps'])
        self.TAG_NAME = "FuzzyInterface :: "
        
        self.msgs= msgs
 
    def __loadConfig(self, conf):
        if len(conf) == 0 or conf is None:
            raise Exception("Missing config file")
        self.conf = conf  
        
    def __setFuzzyValues(self, a, fuzzyData): 
        avps = []
        if a is None:
            return avps

        for f in fuzzyData:
            b = a.deepcopy()
            b.setData(f)
            avps.append(b)
        return avps       
    
    def __fuzzyIdentities(self, a):    
        if a is None :
            return []
        identities = Fuzzer.getDiamIdentities(a.getData) 
        return self.__setFuzzyValues(a, identities)
             
    def __fuzzyStrings(self, a):
        if a is None :
            return []            
        fuzzied = []
        xss = Fuzzer.getXSSStrings()
 
        fuzzied.extend(self.__setFuzzyValues(a, xss))
 
        sqp = Fuzzer.getSQPStrings()
        fuzzied.extend(self.__setFuzzyValues(a, sqp))
             
        xpath = Fuzzer.getXPATHInjectionStrings()
         
        fuzzied.extend(self.__setFuzzyValues(a, xpath))   
         
        fuzzied.extend(self.__setFuzzyValues(a, 
                                             Fuzzer.getLDAPInjectionStrings()))
        fuzzied.extend(self.__setFuzzyValues(a, 
                                             Fuzzer.getPathTraversalStrings()))
         
        fuzzied.extend(self.__setFuzzyValues(a, 
                                             Fuzzer.getRandomHTMLStrings()))
         
        fuzzied.extend(self.__setFuzzyValues(a, 
                                             Fuzzer.getXMLInjectionStrings()))
        
        fuzzied.extend(self.__setFuzzyValues(a, 
                                              Fuzzer.getRandomStrings()))
        fuzzied.extend(self.__setFuzzyValues(a, 
                                             Fuzzer.getRandomStrings(regexp="[0-9]")))      
        fuzzied.extend(self.__setFuzzyValues(a, 
                                             Fuzzer.getRandomStrings(regexp="[0-9]",
                                             minLen=15, maxLen=16)))          
        return fuzzied    

    def __fuzzyAddresses(self, a):
        return self.__setFuzzyValues(a, Fuzzer.getAddress())
    
    def __fuzzySessionID(self, a):
        if a is None:
            return []
        val = a.getData()
        
        avps = []
        sessionId = "%s;%s;%s" 
        
        strings = Fuzzer.getXSSStrings()
        strings.extend(Fuzzer.getDiamIdentities(val.split(";")[0]))
        strings.extend(Fuzzer.getLDAPInjectionStrings())
        strings.extend(Fuzzer.getPathTraversalStrings())
        strings.extend(Fuzzer.getRandomHTMLStrings())
        strings.extend(Fuzzer.getSQPStrings())
        strings.extend(Fuzzer.getXMLInjectionStrings())
        strings.extend(Fuzzer.getXPATHInjectionStrings())
        strings.extend(Fuzzer.getXSSStrings())
        strings.extend(Fuzzer.getRandomStrings())
        strings.extend(Fuzzer.getRandomStrings(regexp="[0-9]"))
        strings.extend(Fuzzer.getAddress())
        for s in strings:
            b = a.deepcopy()
            b.setData(sessionId%(s,
                    ''.join([random.choice('0123456789') for _ in range(9)]),
                    ''.join([random.choice('0123456789') for _ in range(9)])))
            avps.append(b)
        return avps
          
    def __fuzzy(self, a): 
        if isinstance(a, DiamAVP_Unsigned32):
            return [a]
        if isinstance(a, DiamAVP_Integer32):
            return [a]
        if isinstance(a, DiamAVP_Unsigned64):
            return [a]
        if isinstance(a, SessionIDAVP):
            return self.__fuzzySessionID(a)
        
        if isinstance(a, DiamAVP_DiamIdent):
            avps = self.__fuzzyIdentities(a)
            return avps.extend(self.__fuzzyStrings(a))
        
        if isinstance(a, DiamAVP_OctetString):
            return self.__fuzzyStrings(a)
        
        if isinstance(a, DiamAVP_UTF8String):
            return self.__fuzzyStrings(a)   
              
        if isinstance(a, DiamAVP_Address):
            avps = self.__fuzzyAddresses(a)
            return avps.extend(self.__fuzzyStrings(a))            
        
        if isinstance(a, DiamAVP_Time):
            return [a]          
   
           
    def generateMessages(self):
        msgs_list = []
                  
        for m in self.msgs:
            m.generateMessage()
            logNormal("%s has %d AVPS"%(m.__class__.__name__, len(m.getAVPs())))
            fuzzyAvps = []
            for a in m.getAVPs():
                if a.getAVPCode() in self.fuzzyAvpCodes:
                    logNormal("%s:%d to fuzzy"%(DiamAVPCodes.code2name(a.getAVPCode()), 
                                                a.getAVPCode()))
                               
                    if isinstance(a, DiamAVP_Grouped):
                        for i in a.getAVPs():
                            fuzzyAvps.extend(self.__fuzzy(i))                       
                    else:
                        fuzzyAvps.extend(self.__fuzzy(a))
            for av in fuzzyAvps:
                m2 = m.deepcopy()              
                m2.replaceAVP(av)
                msgs_list.append(m2)
            msgs_list.append(m)                                                                                                                              
        logNormal("Generated a total of %d fuzzy messages" % len(msgs_list))
        
        return msgs_list
