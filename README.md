# routor

Tor controller library that allows paths to be chosen on a stream-by-stream basis.

Uses the `stem` implementation of the `tor-control` protocol to direct Tor.

Tor must be run with `--__LeaveStreamsUnattached 1`, or else this library will race with Tor to attach streams.

Tested with `Python3.4`.

## Example

```
$ tor --ControlPort 9051 --__LeaveStreamsUnattached 1
```

In another terminal:

```
$ python3 examples/mole.py
```

In yet another teminal:

```
$ while true; do curl -x socks://localhost:9050 http://ipecho.com; echo; done
```

The output of this last command should be a stream of different IP addresses (and some curl failures).

## MORE DOCUMENTATION SOON
