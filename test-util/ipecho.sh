while true; do
    curl -s -x socks://localhost:9050 http://thyip.com | sed -n 's#^.*<span id="ip">\(.*\)</span>.*$#\1#p'
done
