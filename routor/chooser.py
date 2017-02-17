from datetime import datetime, timedelta


class LamePathChooser(object):

    def __init__(self, path):
        self.path = path

    def take(self):
        return self.path

    def release(self, path, failed=False):
        pass


class MolePathChooser(object):

    def __init__(self, ctrl, middle, wait_time=timedelta(minutes=2)):
        self.ctrl = ctrl
        self.middle = middle
        self.wait_time = wait_time
        self.history = {}
        self.bad = set()


    def check(self, exit):
        return all([
            exit != self.middle,
            exit not in self.bad,
            exit not in self.history or (
                self.history[exit] is not None and datetime.now() - self.history[exit] > self.wait_time
                )
            ])


    def score(score, rstat):
        return ('FAST' in rstat.flags, rstat.bandwidth)


    def take(self):
        def f(rstat):
            return all([
                'Exit' in rstat.flags,
                'Running' in rstat.flags,
                'Valid' in rstat.flags,
                'BadExit' not in rstat.flags,
                self.check(rstat.fingerprint),
                ])
        exit = max(filter(f, self.ctrl.get_network_statuses()), key=self.score).fingerprint
        self.history[exit] = None
        return (self.middle, exit)


    def release(self, path, failed=False):
        exit = path[-1]
        self.history[exit] = datetime.now()
        if failed:
            self.bad.add(exit)
