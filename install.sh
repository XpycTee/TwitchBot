#!/usr/bin/env bash

echo "create a test service ..."
useradd -c "User for Bot" -r twitch_bot
sed 's@path_to_bot@'$PWD'@' twitch_bot.sh > /etc/init.d/twitch_bot
sed 's@path_to_bot@'$PWD'@' install.service > /etc/systemd/system/twitch_bot.service
> /var/run/twitch_bot.pid
chmod ugo+rwx /var/run/twitch_bot.pid
chown -R twitch_bot $PWD
chgrp -R twitch_bot $PWD
chmod -R ugo+rw $PWD
chmod +x /etc/init.d/twitch_bot
echo "created the test service"
