#!/usr/bin/env python

import sctp
import binascii
import sys, socket
import time
#per provare in locale: sudo ncat --sctp -l -p 36412/36422

#interface 3GPP S1-MME

#verifcare se i seguenti moduli sono caricati
#sudo insmod /lib/modules/3.6.11-4.fc16.i686/kernel/lib/libcrc32c.ko
#sudo insmod /lib/modules/3.6.11-4.fc16.i686/kernel/net/sctp/sctp.ko

#echo 1 > /proc/sys/net/sctp/max_init_retransmits

def usage():
    print ("usage : python unexpected_messages_x2_s1.py <dst ip > "
           "<interface s1 or x2> <sleep_time>"
           )
    exit(0)

if len(sys.argv) < 4 :
    usage()

dest_ip = sys.argv[1]

interface = sys.argv[2]

sleep_time = float(sys.argv[3])

if interface == 'x2' :
    payloads = [
            ['E-RabSetup Request (MME2eNB)','000500808800000300000005c00ab055a70008000340d54000100071000011006c0c0006090f800a076011342877305d27b5e8ef07036202c101061f0469626f780374696d026974066d6e63303031066d6363323232046770727305010ab563595e06fefe926c02002722808021100300001081060ace388483060acf2b2e000d040ace3884000d040acf2b2e000000'],
            ['Paging(MME2eNB)','000a4027000004005040023180002b40060e10f810a74c006d400180002e400b00002f40060022f210592600'],
            ['downlink-NAS-Transport (MME2eNB)','000b403300000300000005c00ab055a70008000340d540001a001c1b2729e644f20207614301804501804680477150923114128049010100'],
            ['X2-HandoverPreparation Response','4000000f000002000a40020bf900054002070000'],
            ['X2SetupResponse', '4006000d00000200054001680016400130000000']
            ]
    port = 36422
elif interface == 's1' :
    payloads = [['X2-HandoverPreparation Request','0000008188000006000a00020bfa000540020000000b00080022f210f4241020001700070022f2108014b9000e00810b2608c789121c000e000065fd06429f804b65ee5474964cfe7e401285198bd13534be00fbd5e292f8205f4323c346006002faf080000004400e4500070901f00a0760116b986fb880be0a1038c9980054c1060e002058bf8fff17f1ffe2fe3ffc5fc7ff8bf8fff17f1ffdff3ffaea2060090e194e952448e0b1800000000154004000084015d8000002ee04200290265970811430a1b880c118e1b8800004011004e544806f603ff5381703ff538107d44cc07aea71438111f300dde65aae7f2ac7ff0acac30e43670004514214304825b6a0000004888035925dbea804824218081844c23612340992b7ec9688a341c10004000100843bd4aaf0280328af72007417725ec0bc000022f210000f404e600022f210dbea80400000030022f210dbea80400000030022f210dbea80400000020022f210dbea80400000020022f210dbea80400000010022f210dbea80400000010022f210dbc23050000001000000'],
                ['X2SetupRequest','0006008ac9000004001500080022f21000f4241000140089cd054000050022f210f4241015926022f210004c2c05dc55002e0022f210f4242010000105dc0022f210f4242020000005dc0022f210f4242030000205dc0022f210dbedd02000f505dc0022f210dbedd01000f305dc0022f210dbe7f010006005dc0022f210dbe7f030006105dc0022f210dbcd702000ac05dc0022f210dbea8040017b05dc0022f210dbd30020011105dc0022f210dbd30030011305dc0022f210dbf91010002905dc0022f210dbd81020007705dc0022f210dbcb5040003605dc0022f210dbf7f03000e105dc0022f210dbe7f060006105dc0022f210dbc23040010705dc0022f210dbc23050010505dc0022f210dbf7f02000e305dc0022f210dbcb901001e605dc0022f210dbe7f040006005dc0022f210dbcac01001b705dc0022f210dbe7f050006205dc0022f210f424204000050c670022f210f424205000030c670022f210f424206000040c670022f210dbd540100113189c0022f210dbd540200112189c0022f210dbd540300111189c0022f210dbc230100149189c0022f210dbc230200147189c0022f210dbcd50200193189c0022f210dbc4602001bf189c0022f210dbea8010018e189c0022f210dbeb40300092189c0022f210dbdaf01001cc189c0022f210dbd55010010c189c0022f210dbd55020010b189c0022f210dbd55030010d189c0022f210dbe5a010013a189c0022f210dbcb5010012b189c0022f210dbe7f0100162189c0022f210dbe7f0300163189c0022f210dbe66020005a189c0022f210dbcd50300194189c0022f210dbedb0300150189c4000040022f210f4241025926022f210004c2c05dc55001f0022f210f4242020000005dc0022f210f4242010000105dc0022f210f4242030000205dc0022f210dbd30030011305dc0022f210dbcac01001b705dc0022f210dbea8040017b05dc0022f210dbf7f03000e105dc0022f210dbc23050010505dc0022f210dbea8050017a05dc0022f210f424204000050c670022f210f424205000030c670022f210f424206000040c670022f210dbd540100113189c0022f210dbd540200112189c0022f210dbd540300111189c0022f210dbc230200147189c0022f210dbeb40100090189c0022f210dbeb40200091189c0022f210dbeb40300092189c0022f210dbeec01000e0189c0022f210dbdaf01001cc189c0022f210dbdaf02001cb189c0022f210dbdaf03001cd189c0022f210dbd55010010c189c0022f210dbd55020010b189c0022f210dbd55030010d189c0022f210dbdac0200172189c0022f210dbea8020018d189c0022f210dbea8010018e189c0022f210dbcd50300194189c0022f210dbe1302001bc189c4000030022f210f4241035926022f210004c2c05dc5500290022f210f4242010000105dc0022f210f4242030000205dc0022f210f4242020000005dc0022f210dbedd02000f505dc0022f210dbedd01000f305dc0022f210dbcd702000ac05dc0022f210dbd30030011305dc0022f210dbd4202000b105dc0022f210dbf7f03000e105dc0022f210dbca3010010b05dc0022f210dbca3030010d05dc0022f210dbea8040017b05dc0022f210f424204000050c670022f210f424205000030c670022f210f424206000040c670022f210dbd540100113189c0022f210dbd540200112189c0022f210dbd540300111189c0022f210dbe9003001e7189c0022f210dbc4602001bf189c0022f210dbc4603001c0189c0022f210dbcb90400196189c0022f210dbe1303001bd189c0022f210dbea8030018c189c0022f210dbe3201001d4189c0022f210dbedc010009a189c0022f210dbedb0300150189c0022f210dbe7903000ae189c0022f210dbcd705000ee189c0022f210dbd55010010c189c0022f210dbe5a010013a189c0022f210dbe66010005b189c0022f210dbdaf01001cc189c0022f210dbea8010018e189c0022f210dbe66030005c189c0022f210dbd55020010b189c0022f210dbe5a0300139189c0022f210dbcd704000ed189c0022f210dbdaf03001cd189c0022f210dbe66020005a189c0022f210dbe5a0200138189c4000090022f210f4241045926022f2100052b70c6744001a0022f210f424204000050c670022f210f424205000030c670022f210f424206000040c670022f210f4242010000105dc0022f210f4242020000005dc0022f210f4242030000205dc0022f210dbd30020011105dc0022f210dbcd702000ac05dc0022f210dbf7f03000e105dc0022f210dbea8040017b05dc0022f210dbf91010002905dc0022f210dbd540100113189c0022f210dbd540200112189c0022f210dbd540300111189c0022f210dbc230100149189c0022f210dbc230200147189c0022f210dbcd50200193189c0022f210dbc4602001bf189c0022f210dbea8010018e189c0022f210dbeb40300092189c0022f210dbdaf01001cc189c0022f210dbd55010010c189c0022f210dbd55020010b189c0022f210dbd55030010d189c0022f210dbe5a010013a189c0022f210dbe7f0100162189c40000b0022f210f4241055926022f2100052b70c674400180022f210f424204000050c670022f210f424205000030c670022f210f424206000040c670022f210f4242010000105dc0022f210f4242030000205dc0022f210f4242020000005dc0022f210dbea8040017b05dc0022f210dbf7f03000e105dc0022f210dbd540100113189c0022f210dbd540200112189c0022f210dbd540300111189c0022f210dbc230200147189c0022f210dbeb40100090189c0022f210dbeb40200091189c0022f210dbeb40300092189c0022f210dbeec01000e0189c0022f210dbdaf01001cc189c0022f210dbdaf02001cb189c0022f210dbdaf03001cd189c0022f210dbd55010010c189c0022f210dbd55020010b189c0022f210dbd55030010d189c0022f210dbdac0200172189c0022f210dbea8010018e189c40000a0022f210f4241065926022f2100052b70c6744001d0022f210f424204000050c670022f210f424205000030c670022f210f424206000040c670022f210f4242010000105dc0022f210f4242020000005dc0022f210f4242030000205dc0022f210dbcd702000ac05dc0022f210dbd540100113189c0022f210dbd540200112189c0022f210dbd540300111189c0022f210dbe9003001e7189c0022f210dbc4602001bf189c0022f210dbc4603001c0189c0022f210dbcb90400196189c0022f210dbe1303001bd189c0022f210dbea8030018c189c0022f210dbe3201001d4189c0022f210dbedb0300150189c0022f210dbe7903000ae189c0022f210dbd55030010d189c0022f210dbd55010010c189c0022f210dbe5a0300139189c0022f210dbd55020010b189c0022f210dbdaf03001cd189c0022f210dbe66010005b189c0022f210dbe5a010013a189c0022f210dbdaf01001cc189c0022f210dbe66030005c189c0022f210dbe66020005a189c001800060022f210801400c84080d90b0022f210f4241010f80a0a010a000001f4100022f210f4241020f80a0a010b000001f4100022f210f4241030f80a0a010c000001f4100022f210f4241040f80a0a010d000001f4100022f210f4241050f80a0a010e000001f4100022f210f4241060f80a0a010f000001f4100022f210f4241070f80a0a0110000001f4100022f210f4241080f80a0a0111000001f4100022f210f4241090f80a0a0112000001f4100022f210f42410a0f80a0a0113000001f4100022f210f42410b0f80a0a0114000001f4100022f210f42410c0f80a0a0115000001f410'],
                ['Initial Attach Request (eNB2MME)','000c405200000500080004800e7bd2001a00282707417208292210173006481004e0e0c0400005025ed011d15c0a003103e5c0349011035758a6f1004300060022f210000b006440080022f2100a619a1000864001300000'],
                ['E-RabSetup Response (eNB2MME)','0006f6881a80fa163e87019281004f400800454a005c000040004084522f0a0a738c0a0a60058e3c8e3c0a6453e97efb05740003003a1f91b4f70001053d000000122005002600000300004005c00ab055a70008400340d540001c400f000027400a0c1f0a0a738c00007b210000'],
                ['UECapabilityIndication (eNB2ME)','0016402b00000300000005c00ab055a70008000340d540004a40141300880100e81200001083010381d7837620000000'],
                ['InitialContextRequest (eNB2ME)','2009002600000300004005c00ab055a70008400340d5400033400f000032400a0a1f0a0a738c00007b010000'],
                ['downlink-NAS-Transport (MME2eNB)','000b403300000300000005c00ab055a70008000340d540001a001c1b2729e644f20207614301804501804680477150923114128049010100'],
                ['Uplink-NAS-Transport (eNB2ME)','000d403b00000500000005c00ab055a70008000340d540001a000e0d277d57e7ad01074300035200c2006440080022f210f4241010004340060022f210592600'],
                ]
    port = 36412
else:
    print("Errore. Interfaccia %s non supportata."%(interface))
    usage()
    exit(0)

print("Using %s interface."%(interface))  
s = sctp.sctpsocket_tcp(socket.AF_INET)
s.connect((str(dest_ip),port))
for i in range(0, len(payloads)) :
    print("Sending %s"%(payloads[i][0]))
    s.send(binascii.unhexlify(payloads[i][1]))
    if sleep_time > 0:
        time.sleep(sleep_time)

s.close()
print("Sent %d messages."%(len(payloads)))
