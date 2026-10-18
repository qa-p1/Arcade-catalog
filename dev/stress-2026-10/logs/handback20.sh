#!/bin/bash
# handback20.sh <user> <runs> — repeat: Tools hosting -> kill -9 -> time each app's own item -> restart Tools
u=$1; n=${2:-20}; out=/home/qa/perf/handback-$u.jsonl; : > $out
for i in $(seq $n); do
  for w in $(seq 60); do
    T=$(/home/qa/bin/sni $u | awk '/arcade-tools/{sub("pid=","",$2); print $2}' | head -1)
    own=$(/home/qa/bin/sni $u | grep -v -e arcade-tools -e 'pid= ' | wc -l)
    [ -n "$T" ] && [ "$own" -eq 0 ] && break; sleep 0.5
  done
  sleep 2
  /home/qa/bin/as $u "/usr/bin/python3.12 /home/qa/bin/handback.py $T 7" >> $out
  sleep 1
  /home/qa/bin/as $u '(setsid arcade-tools --background >/dev/null 2>&1 &)'
done
