#!/bin/bash
# soak.sh <user> <minutes> — Journey 8: mixed realistic use once a minute, RSS/CPU sampled every minute.
# Actions go through the same paths a user or another app would use (clipboard copy, Link invokes,
# opening/closing windows, Tools quit/start). Output: /home/qa/perf/soak-<user>.csv and soak-<user>.log
u=${1:-maya}; mins=${2:-60}; h="$(getent passwd "$u" | cut -d: -f6)"
csv=/home/qa/perf/soak-$u.csv; log=/home/qa/perf/soak-$u.log
AS=/home/qa/bin/as; L=/home/qa/bin/arcade-link
echo "minute,pid,comm,rss_kib,cpu_ticks" > $csv; : > $log
sample() {
  for p in $(pgrep -u "$u"); do
    c=$(cat /proc/$p/comm 2>/dev/null) || continue
    case "$c" in arcade-*|clipboard|AppRun.wrapped|WebKit*) ;; *) continue;; esac
    r=$(awk '/^VmRSS/{print $2}' /proc/$p/status 2>/dev/null); t=$(awk '{print $14+$15}' /proc/$p/stat 2>/dev/null)
    echo "$1,$p,$c,${r:-0},${t:-0}" >> $csv
  done
}
echo "soak note $(date +%s)" > "$h/soak-note.txt"; chown "$u": "$h/soak-note.txt"
for i in $(seq 0 $mins); do
  start=$SECONDS
  sample $i
  [ $i -eq $mins ] && break
  {
    echo "== minute $i $(date +%T)"
    $AS $u "printf 'soak clip $i %s' \"\$(date +%s)\" | xclip -selection clipboard; sleep 0.3; xclip -selection clipboard -o | head -c 40"; echo
    $AS $u "$L invoke find find.search --text soak 2>&1 | tail -1"
    $AS $u "$L invoke shelf shelf.add --file ~/soak-note.txt 2>&1 | tail -1"
    $AS $u "$L invoke look look.preview --file ~/soak-note.txt 2>&1 | tail -1; sleep 2; wmctrl -c 'soak-note.txt — Arcade Look'"
    if [ $((i % 5)) -eq 0 ]; then
      $AS $u "$L invoke box box:arcade.developer.hash --text abc --option algorithm=sha256 2>&1 | tail -1"
      $AS $u "(setsid arcade-lens --capture >/dev/null 2>&1 &); sleep 2; xdotool key Escape"
    fi
    if [ $((i % 10)) -eq 0 ]; then
      $AS $u "$L settings wheel >/dev/null 2>&1; sleep 2; wmctrl -c 'Arcade Wheel · Settings'"
      $AS $u "$L settings clipboard >/dev/null 2>&1; sleep 2; wmctrl -c 'Arcade Clipboard'"
    fi
    case $i in
      20|40) echo "quit Tools"; $AS $u "$L quit tools";;
      22|42) echo "start Tools"; $AS $u "(setsid arcade-tools --background >/dev/null 2>&1 &)";;
    esac
    $AS $u "$L ls | awk 'NR>1{print \$1, \$4}' | tr '\n' ' '"; echo
  } >> $log 2>&1
  rest=$((60 - (SECONDS - start))); [ $rest -gt 0 ] && sleep $rest
done
echo done >> $log
