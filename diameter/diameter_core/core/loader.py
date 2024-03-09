import os
import importlib

DEFAULT_PLUGIN_LOCATION = "core/plugins"
DEFAULT_PLUGIN_MODULE = "core.plugins"

##
## @brief      Helper class to dinamically load required interfaces
## 
## @author: Ilario Dal Grande
##
class PluginLoader:
    def __init__(self, conf):
        self.TAG_NAME = 'PLUGIN_LOADER'
        
        if conf is None or conf == "" :
            raise Exception("%s :: Missing config for module", self.TAG_NAME)
        
        self.conf = conf
    
    ##
    ## @brief      Private function that actually load the plugin
    ##
    ## @param      self        the specified plugin by name
    ## @param      module      the module name
    ## @param      class_name  the class name
    ##
    ## @return     the loaded class
    ##
    def __loadPlugin(self, module, class_name):
        mod = importlib.import_module(module, DEFAULT_PLUGIN_MODULE)
        
        myClass = getattr(mod, class_name)()
        
        myClass.loadConfig(self.conf)
        
        return myClass
    
    ##
    ## @brief      Loads the specified plugin by name
    ##
    ## @param      self  refers to the class itself
    ## @param      name  the name of the plugin (eg. common, fuzzy, raw, s6a_3gpp, slg_3gpp,...)
    ##                   all the plugins are in the plugin/ folder. 
    ##                   The name is the filename withouth the _interface.py suffix
    ##
    ## @return     the reference of the loaded plugin
    ##
    def callPlugin(self, name):
        class_name = ""
        
        if name is None or name == "" :
            raise Exception("%s :: Missing module name", self.TAG_NAME)
        
        thep = "%s/%s_interface.py" % (DEFAULT_PLUGIN_LOCATION, name)
        
        if os.path.isdir(thep) or not os.path.exists(thep):
            raise Exception("No such file '%s'" % self.module)
        
        module = ".%s_interface" % name
        v = module[1:].split('_')
        for e in v:
            class_name = "%s%s" % (class_name, e.capitalize())
            
        return self. __loadPlugin(module, class_name).generateMessages()
