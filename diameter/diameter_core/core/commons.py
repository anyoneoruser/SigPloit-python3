#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, random
import datetime
import time

##
## @author: Ilario Dal Grande <ilario.dalgrande@guest.telecomitalia.it>
##

''' Logger methods '''

##
## @brief      This method retrieve the python module name
##
## @param      back  NON LO SO
##
## @return     the module name
##
def FUNC( back = 0):
    return sys._getframe( back + 1 ).f_code.co_name

##
## @brief      This method prints the passed text in GREEN
##
## @param      text     the string to be printed
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def printGreen(text, newLine=True):
    if newLine:
        print('\033[0;32m%s\033[0m'%text)
    else:
        print('\033[0;32m%s\033[0m'%text, end=' ')
        
##
## @brief      This method prints the passed text in RED
##
## @param      text     the string to be printed
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def printRed(text, newLine=True):
    if newLine:
        print('\033[0;31m%s\033[0m'%text)
    else:
        print('\033[0;31m%s\033[0m'%text, end=' ')

##
## @brief      This method prints the passed text in YELLOW
##
## @param      text     the string to be printed
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def printYellow(text, newLine=True):
    if newLine:
        print('\033[1;33m%s\033[0m'%text)
    else:
        print('\033[1;33m%s\033[0m'%text, end=' ')

##
## @brief      Gets the current timestamp in log format (Y-m-d H:M:S)
##
## @return     the current timestamp
##
def getCurrTimestamp():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

##
## @brief      Logs a normal message
##
## @param      text     the text to be logged
## @param      TAG      the reference of the file that call the log function
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def logNormal(text, TAG=None, newLine=True):
    if TAG is not None:
        s_text = "%s\t%s :: %s" % (getCurrTimestamp(), TAG, text)
    else:
        s_text = text
    
    if newLine:
        print(s_text)
    else:
        print(s_text, end=' ')

##
## @brief      Logs an ok message
##
## @param      text     the text to be logged
## @param      TAG      the reference of the file that call the log function
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def logOk(text, TAG=None, newLine=True):
    if TAG is not None:
        s_text = "%s\t%s :: %s" % (getCurrTimestamp(), TAG, text)
    else:
        s_text = text
    
    printGreen(s_text, newLine)

##
## @brief      Logs a warning message
##
## @param      text     the text to be logged
## @param      TAG      the reference of the file that call the log function
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def logWarn(text, TAG=None, newLine=True):
    if TAG is not None:
        s_text = "%s\t%s :: %s" % (getCurrTimestamp(), TAG, text)
    else:
        s_text = text
    
    printYellow(s_text, newLine)

##
## @brief      Logs an error message
##
## @param      text     the text to be logged
## @param      TAG      the reference of the file that call the log function
## @param      newLine  an optional boolean to specify if it's an inline print
##                      or not
##
def logErr(text, TAG=None, newLine=True):
    if TAG is not None:
        s_text = "%s\t%s :: %s" % (getCurrTimestamp(), TAG, text)
    else:
        s_text = text
    
    printRed(s_text, newLine)

''' /Logger methods '''

##
## @brief      Generates a slug form of the passed text (a dash separated text)
##
## @param      text  the text to be converted
##
## @return     the slug of the text
##
def slugfy(text):
    s = text.lower()
    s = re.sub(r"(_|\s+)", "-", s)
    
    return s

##
## @brief      This method generates a random hex string of the passed length
##
## @param      ln    the length of the string
##
## @return     a random hex string of the specified length
##
def generateRandomHexString(ln):
    return '0x'+''.join([random.choice('0123456789ABCDEF') for _ in range(ln)])

##
## @brief      This method generates a random hex byte string of the passed length
##
## @param      ln    the length of the byte string
##
## @return     a random byte string of the specified length
##
def generateRandomHexByte(ln):
    if ln%2==1: ln = ln+1
    hStr = ''.join([random.choice('0123456789ABCDEF') for _ in range(ln)])
    return bytearray.fromhex(hStr)

##
## @brief      This method generates a random message string with the characters in the passed regexp
##
## @param      regexp  the regular expression that match the characters to use
##
## @return     a random generated string based on the passed regular expression
##
def generateRandomMsg(regexp=None):
    allowed = 'abcdefghijklmnopqrstuvwxyz' + \
              'ABCDEFGHIJKLMNOPQRSTUVWXYZ' + \
              '012345678' + \
              '\\|!"£$%&/()=?^\'[]+*@#§-_:.;,' + \
              'òàùèé'
    if regexp is not None:
        chars = re.findall(regexp, allowed)
    else:
        chars = []
        match = re.findall('.*', allowed)
        for c in match[0]:
            chars.append(c)
    
    if chars == []:
        chars = allowed
            
    seed = random.randrange(0, 10)
    random.seed(seed)
    ln = random.randrange(5, 50)
    outStr = ""
    for _ in range(5, ln):
        idx = random.randrange(0, len(chars))
        outStr += chars[idx]

##
## @brief      This method prints a hex text in a well formatted way
##
## @param      text  the hex text to be formatted
##
def pprintHex(text):
    gap = 0
    line = 0
    s = ""
    
    for t in text:
        s += "{:02x} ".format(ord(t))
        
        gap+=1
        line+=1
        
        if line==16:
            print(s)
            s = ""
            line = 0
            gap = 0
            continue
        
        if gap==8:
            s += ""
            gap = 0
    print(s)
    
##
## @brief      This method prints a hex text in the wireshark format
##
## @param      text  the hex text to be formatted
##
def pprintWiresharkPacket(text):
    line = 0
    s = ""
    
    for i in range(0, len(text), 2):
        s += text[i:i+2] + " "
        
        line+=1
        
        if line%8==0:
            print("{:06x}".format(line-8), end=' ')
            print("%s%s"%(s, "."*8))
            s = ""
            continue
    print(s)
    
##
## @brief      Convert a byte string to it's hex string representation e.g. for output.
##
## @param      byteStr  the byte string to be converted
##
## @return     the hex version of the byte string
##
def byteToHex( byteStr ):
    return ''.join( [ "%02X" % ord(x) for x in byteStr])
