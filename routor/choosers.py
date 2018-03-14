"""Provides some general-purpose path choosers."""

from datetime import datetime, timedelta


def can_exit(rstat):
    return all((
        'Exit' in rstat.flags,
        'Running' in rstat.flags,
        'Valid' in rstat.flags,
        'BadExit' not in rstat.flags,
        ))


class ConstPathChooser(object):
    """
    Always chooses the same path

    Args:
        path (tuple of fingerprints): Path that is always chosen
    """

    def __init__(self, path):
        self.path = path

    def take(self, stream_event):
        return self.path

    def release(self, path, failed=False):
        pass


class PerspectivesPathChooser(object):
    """
    Chooses single-hop paths through the given middle node,
    always choosing the "best" exit node that has not yet been used.

    See the score method for the definition of "best".

    Args:
        ctrl (stem.control.Controller): Tor controller handle
        middle (str): Fingerprint of middle node
    """

    def __init__(self, ctrl, middle):
        self.ctrl = ctrl
        self.middle = middle
        self.history = set()

    def check(self, exit):
        return exit != self.middle and exit not in self.history

    def score(self, rstat):
        return ('FAST' in rstat.flags, rstat.bandwidth)

    def take(self, stream_event):
        def f(rstat):
            return can_exit(rstat) and self.check(rstat.fingerprint)
        exit = max(filter(f, self.ctrl.get_network_statuses()), key=self.score).fingerprint
        self.history.add(exit)
        return (self.middle, exit)

    def release(self, path, failed=False):
        exit = path[-1]
        if failed:
            self.bad.add(exit)


class ScrapePathChooser(object):
    """
    Chooses single-hop paths through the given middle node,
    always choosing the "best" exit node that hasn't been used within the last wait_time.

    See the score method for the definition of "best".

    Args:
        ctrl (stem.control.Controller): Tor controller handle
        middle (str): Fingerprint of middle node
        wait_time=timedelta(minutes=2): Minimum time between path release and re-use
    """

    def __init__(self, ctrl, middle, wait_time=timedelta(minutes=2)):
        self.ctrl = ctrl
        self.middle = middle
        self.wait_time = wait_time
        self.history = {}
        self.bad = set()

    def check(self, exit):
        return all((
            exit != self.middle,
            exit not in self.bad,
            exit not in self.history or \
                (self.history[exit] is not None and datetime.now() - self.history[exit] > self.wait_time),
            ))

    def score(self, rstat):
        return ('FAST' in rstat.flags, rstat.bandwidth)

    def take(self, stream_event):
        def f(rstat):
            return can_exit(rstat) and self.check(rstat.fingerprint)
        exit = max(filter(f, self.ctrl.get_network_statuses()), key=self.score).fingerprint
        self.history[exit] = None
        return (self.middle, exit)

    def release(self, path, failed=False):
        exit = path[-1]
        self.history[exit] = datetime.now()
        if failed:
            self.bad.add(exit)
