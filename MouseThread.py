import threading
import usb.core
import usb.util
from directkeys import MoveMouse


class MouseThread(threading.Thread):

    def __init__(self, cache):
        threading.Thread.__init__(self)
        self.mousemovementcache = cache  # left, right, dx, dy30891

    def run(self):
        # find the USB device2522
        busses = usb.busses()
        for bus in busses:
            devices = bus.devices
            for dev in devices:
                print(repr(dev))
                print("  idVendor: %d (0x%04x)" % (dev.idVendor, dev.idVendor))
                print("  idProduct: %d (0x%04x)" % (dev.idProduct, dev.idProduct))
        device = usb.core.find(idVendor=2362,
                               idProduct=9505)

        # use the first/default configuration
        device.set_configuration()
        # first endpoint
        endpoint = device[0][(0, 0)][0]
        add = endpoint.bEndpointAddress
        size = endpoint.wMaxPacketSize
        rprevstate = 0  # 0 = previous wasn't clicked, 1 - was
        lprevstate = 0

        while True:
            try:
                data = device.read(add, size)
                if data[1] > 128:
                    dx = -256 + data[1]
                else:
                    dx = data[1]
                if data[3] > 128:
                    dy = -256 + data[3]
                else:
                    dy = data[3]
                if lprevstate == 0 and (data[0] == 1 or data[0] == 3):
                    lsend = 1
                    lprevstate = 1
                elif lprevstate == 1 and (data[0] == 0 or data[0] == 2):
                    lsend = 2
                    lprevstate = 0
                else:
                    lsend = 0
                if rprevstate == 0 and (data[0] == 2 or data[0] == 3):
                    rsend = 1
                    rprevstate = 1
                elif rprevstate == 1 and (data[0] == 0 or data[0] == 1):
                    rsend = 2
                    rprevstate = 0
                else:
                    rsend = 0
                MoveMouse(dx, dy, lsend, rsend)

                self.mousemovementcache[2] += data[1]
                self.mousemovementcache[3] += data[3]
                if self.mousemovementcache[0] == 0 and (data[0] == 1 or data[0] == 3):
                    self.mousemovementcache[0] = 1
                if self.mousemovementcache[1] == 0 and (data[0] == 2 or data[0] == 3):
                    self.mousemovementcache[1] = 1
            except usb.core.USBError as e:
                if e.args == ('Operation timed out',):
                    continue

