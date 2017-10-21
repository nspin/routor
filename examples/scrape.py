import sys
import time
import logging

from stem.control import Controller, EventType

from routor import Manager
from routor.chooser import ScrapePathChooser

root = logging.getLogger()
hdlr = logging.StreamHandler(sys.stderr)
hdlr.addFilter(logging.Filter('routor'))
root.addHandler(hdlr)
root.setLevel(logging.DEBUG)

# middle = '379FB450010D17078B3766C2273303C358C3A442'
middle = 'BC630CBBB518BE7E9F4E09712AB0269E9DC7D626'
ctrl = Controller.from_port(port=9051)
ctrl.authenticate()
Manager(ctrl, ScrapePathChooser(ctrl, middle)).start()

while True:
    time.sleep(1337)
