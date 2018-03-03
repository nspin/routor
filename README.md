# routor

Tor controller that allows paths to be chosen on a stream-by-stream basis.

Requires the Python packages `stem` and `bidict`.
Tested with `Tor 0.3.2.9`, `Python 3.6.4`, `stem-1.6.0`, and `bidict-0.13.0`.


## Usage

Tor must be run with `--__LeaveStreamsUnattached 1`, or else this library will race with Tor to attach streams.

```
$ tor --ControlPort 9051 --__LeaveStreamsUnattached 1
```

In another terminal:

```
$ python3 examples/scrape.py
```

In yet another teminal:

```
$ while true; do curl -s -x socks://localhost:9050 http://ipecho.net/plain; echo; done
```

The output of this last command should be a stream of different IP addresses (and some curl failures):

```
37.187.129.166
197.231.221.211
78.109.23.1
62.210.245.158
192.42.116.16
185.129.62.63
109.163.234.4
109.163.234.7
62.210.245.138
94.242.246.23
```
