#!/usr/bin/env bash

# Quick start-stop-daemon example, derived from Debian /etc/init.d/ssh
set -e

# Must be a valid filename
NAME=twitch_bot
PIDFILE=/var/run/$NAME.pid
#This is the command to be run, give the full pathname
DAEMON="/usr/bin/python3 path_to_bot/bot.py"

case "$1" in
  start)
        echo -n "Starting daemon: "$NAME
    start-stop-daemon --start --quiet --background --chdir path_to_bot --make-pidfile --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_OPTS
        echo "."
    ;;
  stop)
        echo -n "Stopping daemon: "$NAME
    start-stop-daemon --stop --quiet --oknodo --remove-pidfile --pidfile $PIDFILE
        echo "."
    ;;
  restart)
        echo -n "Restarting daemon: "$NAME
    start-stop-daemon --stop --quiet --oknodo --retry 30 --remove-pidfile --pidfile $PIDFILE
    start-stop-daemon --start --quiet --background --chdir path_to_bot --make-pidfile --pidfile $PIDFILE --exec $DAEMON -- $DAEMON_OPTS
    echo "."
    ;;
  status)
        echo -n "Status daemon: "$NAME
		echo -n `start-stop-daemon --status --pidfile $PIDFILE`
    echo "."
    ;;
  *)
    echo "Usage: "$1" {start|stop|restart|status}"
    exit 1
esac

exit 0
