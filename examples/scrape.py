import sys
import time
import logging
from datetime import datetime, timedelta

from stem.control import Controller, EventType

from routor import Manager
from routor.choosers import ScrapePathChooser

root = logging.getLogger()
hdlr = logging.StreamHandler(sys.stderr)
hdlr.addFilter(logging.Filter('routor'))
root.addHandler(hdlr)
root.setLevel(logging.DEBUG)

middle = 'BC630CBBB518BE7E9F4E09712AB0269E9DC7D626'
ctrl = Controller.from_port(port=9051)
ctrl.authenticate()
Manager(ctrl, ScrapePathChooser(ctrl, middle, wait_time=timedelta(seconds=2))).start()

while True:
    time.sleep(1337)
