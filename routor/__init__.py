from bidict import bidict
from threading import RLock

from stem import StreamStatus, CircStatus
from stem.control import EventType

import logging
logger = logging.getLogger(__name__)


class Manager(object):

    def __init__(self, ctrl, path_chooser):

        self.ctrl = ctrl
        self.path_chooser = path_chooser
        self.logger = logger.getChild(repr(self))

        self.waiting_build = bidict()
        self.attached = bidict()
        self.paths = dict()

        self.lock = RLock()

        self.ctrl.add_event_listener(self.handle_stream, EventType.STREAM)
        self.ctrl.add_event_listener(self.handle_circuit, EventType.CIRC)


    def assign_stream(self, sid):
        with self.lock:
            path = self.path_chooser.take()
            self.logger.info('chose path %s for sid %s', path, sid)
            for circ in self.ctrl.get_circuits():
                if circ.path == path:
                    self.ctrl.attach_stream(sid, circ.id)
                    self.attached[sid] = circ.id
                    return
            cid = self.ctrl.new_circuit(path=path)
            self.paths[cid] = path
            self.waiting_build[sid] = cid


    def circuit_built(self, cid):
        with self.lock:
            if cid in self.waiting_build.inv:
                sid = self.waiting_build.inv[cid]
                self.ctrl.attach_stream(sid, cid)
                del self.waiting_build[sid]
                self.attached[sid] = cid


    def cleanup_stream(self, sid):
        with self.lock:
            self.logger.info('cleaning up sid %s', sid)
            cid = None
            if sid in self.waiting_build:
                cid = self.waiting_build[sid]
                del self.waiting_build[sid]
            elif sid in self.attached:
                cid = self.attached[sid]
                del self.attached[sid]
            return cid


    def cleanup_circuit(self, cid, failed=False):
        with self.lock:
            self.logger.info('cleaning up cid %s', cid)
            if cid in self.paths:
                path = self.paths[cid]
                self.path_chooser.release(path, failed=failed)
                del self.paths[cid]
            sid = None
            if cid in self.waiting_build.inv:
                sid = self.waiting_build.inv[cid]
                del self.waiting_build[sid]
            elif cid in self.attached.inv:
                sid = self.attached.inb[cid]
                del self.attached[sid]
            return sid


    def handle_stream(self, ev):
        with self.lock:
            self.logger.info(ev)
            sid = ev.id

            if ev.status == StreamStatus.NEW:
                self.assign_stream(sid)

            elif ev.status == StreamStatus.FAILED:
                cid = self.cleanup_stream(sid)
                if cid is not None:
                    self.cleanup_circuit(cid) # failed=True?

            elif ev.status == StreamStatus.DETACHED:
                self.ctrl.close_stream(sid)
                cid = self.cleanup_stream(sid)
                if cid is not None:
                    self.cleanup_circuit(cid) # failed=True?

            elif ev.status == StreamStatus.CLOSED:
                cid = self.cleanup_stream(sid)
                if cid is not None:
                    self.cleanup_circuit(cid)


    def handle_circuit(self, ev):
        with self.lock:
            self.logger.info(ev)
            cid = ev.id

            if ev.status == CircStatus.BUILT:
                self.circuit_built(cid)

            elif ev.status == CircStatus.FAILED:
                sid = self.cleanup_circuit(cid, failed=True)
                if sid is not None:
                    self.ctrl.close_stream(sid)
                    self.cleanup_stream(sid)
