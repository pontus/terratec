#!/usr/bin/env python

import usb
import time
import array

dev = None

for b in usb.busses():
    for d in b.devices:
        if d.idVendor == 0xccd and d.idProduct == 0x3b:
            dev = d
            print "Found terratec"

handle = dev.open()

handle.setConfiguration( dev.configurations[0])

i=None

for p in dev.configurations[0].interfaces:
    for q in p:
        print "Interface %d " %        q.interfaceNumber
        print "Class %d " % q.interfaceClass
        print "Subclass %d " % q.interfaceSubClass
        print "Protocol %d " % q.interfaceProtocol

        print "Endpoints"

        print [ r.address for r in q.endpoints ]
        print "Alt setting %d " % q.alternateSetting
        print "----"

        if q.alternateSetting == 4:
            i=q

handle.claimInterface(i)
handle.setAltInterface(i)

handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x15, 0x720)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0xa015, 0x710)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x20, 0x712)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x7, 0x720)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x23, 0x100)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x1, 0x110)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x3, 0x120)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x1, 0x600)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0xf00, 0x610)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x0, 0x102)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x0, 0x112)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x0, 0x122)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0xffff, 0x950)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0xffff, 0x952)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x20, 0x902)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x2f0, 0x904)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x10, 0x302)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x100, 0x370)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x0, 0x372)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x100, 0x374)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x0, 0x376)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x84, 0x3f0)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x5, 0x900)

handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x4a, 0x922)
handle.controlMsg(  usb.TYPE_VENDOR , 1, "", 0x108, 0x920)



while True:
    handle.controlMsg(  usb.TYPE_VENDOR | usb.ENDPOINT_IN, 0, 2, 0x0, 0x900)

    print dev
    time.sleep(1)
