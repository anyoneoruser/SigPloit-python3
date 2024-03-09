from .base_interface import BaseInterface
from ..utilities import parseRawConfigs
import os
    
##
## @brief      Generates RAW Diameter's messages
## 
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##
class RawInterface(BaseInterface):
    def __init__(self):
        super(RawInterface, self).__init__()
        self.TAG_NAME = "RawInterface"
    
    def generateMessages(self):
        fpath = self.conf['raw_config_file']
        
        if os.path.isdir(fpath) or not os.path.exists(fpath):
            raise Exception("Defined raw file '%s' does not exist" % fpath)
        
        return parseRawConfigs(fpath)
    
