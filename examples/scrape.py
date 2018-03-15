import sys
import time
import logging
from stem.control import Controller
from routor import Manager, PerspectivesPathChooser

root = logging.getLogger()
hdlr = logging.StreamHandler(sys.stderr)
hdlr.addFilter(logging.Filter('routor'))
root.addHandler(hdlr)
root.setLevel(logging.DEBUG)

middle = 'D8FF84E5E29A92F09F8263D4662627ECC479B108'
ctrl = Controller.from_port(port=9051)
ctrl.authenticate()
Manager(ctrl, PerspectivesPathChooser(ctrl, middle)).start()

while True:
    time.sleep(1337)
