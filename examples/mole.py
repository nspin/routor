import sys
import time
import logging

from stem.control import Controller, EventType

from routor import Manager
from routor.chooser import MolePathChooser


class JustManagers(object):
    def filter(self, record):
        return 1 if 'Manager object' in record.name else 0

root = logging.getLogger()
hdlr = logging.StreamHandler(sys.stderr)
hdlr.addFilter(JustManagers())
root.addHandler(hdlr)
root.setLevel(logging.DEBUG)

middle = '379FB450010D17078B3766C2273303C358C3A442'
ctrl = Controller.from_port(port=9051)
ctrl.authenticate()
man = Manager(ctrl, MolePathChooser(ctrl, middle))

while True:
    time.sleep(100)
