import sys
import os
from abc import ABC, abstractmethod

from pydivert import WinDivert, Packet


# from pydivert.consts import *


def get_exe_dir():
    """Returns the directory where the .exe (or script) is located."""
    if getattr(sys, 'frozen', False):
        # Running as a PyInstaller EXE
        return os.path.dirname(sys.executable)
    else:
        # Running as a normal Python script
        return os.path.dirname(os.path.abspath(__file__))


class TcpInjector(ABC):
    def __init__(self, w_filter: str):
        # self.interface_ipv4 = interface_ipv4
        # self.interface_ipv6 = interface_ipv6
        # ip_filter = ip4_filter = ip6_filter = ""
        # if self.interface_ipv4:
        #     ip4_filter = "(ip.SrcAddr == " + self.interface_ipv4 + " or ip.DstAddr == " + self.interface_ipv4 + ")"
        #     ip_filter = ip4_filter
        # if self.interface_ipv6:
        #     ip6_filter = "(ipv6.SrcAddr == " + self.interface_ipv6 + " or ipv6.DstAddr == " + self.interface_ipv6 + ")"
        #     ip_filter = ip6_filter
        # if self.interface_ipv4 and self.interface_ipv6:
        #     ip_filter = "(" + ip4_filter + " or " + ip6_filter + ")"
        #
        # self.filter = "tcp"
        # if ip_filter:
        #     self.filter += " and " + ip_filter
        
        # Load WinDivert.dll directly from the executable's directory for robust portable deployment
        dll_dir = get_exe_dir()
        dll_file = os.path.join(dll_dir, "WinDivert.dll")
        if os.path.exists(dll_file):
            self.w: WinDivert = WinDivert(w_filter, dll_path=dll_file)
        else:
            self.w: WinDivert = WinDivert(w_filter)

    @abstractmethod
    def inject(self, packet: Packet):
        sys.exit("Not implemented")

    def run(self):
        with self.w:
            while True:
                packet = self.w.recv(65575)
                self.inject(packet)
