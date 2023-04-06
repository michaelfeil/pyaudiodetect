from PyP100 import PyP100
import os
import time


class TapoP100Plug:
    def __init__(self, ip: str, email: str, pw: str):
        self.creds = [
            ip if ip else os.environ.get("TAPO_IP", "192.168.1.100"),
            email if email else os.environ.get("TAPO_MAIL", "me@mailbox.org"),
            pw if pw else os.environ.get("TAPO_PW", "mypw"),
        ]
        self.connect()

    def connect_if_needed(self, delay=True) -> bool:
        """return if device is on"""
        try:
            return self.p100.getDeviceInfo()["result"]["device_on"]
        except:
            self.connect()
            if delay:
                time.sleep(3)
            # recursion
            self.connect_if_needed()

    def connect(self) -> bool:
        try:
            self.p100 = PyP100.P100(*self.creds)
            self.p100.handshake()
            self.p100.login()
            return True
        except:
            return False

    def on(self):
        device_on = self.connect_if_needed()
        if device_on is False:
            self.p100.turnOn()

    def off(self):
        """return True when reconnect needed"""
        device_on = self.connect_if_needed()
        if device_on is True:
            self.p100.turnOff()
