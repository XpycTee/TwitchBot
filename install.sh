#!/usr/bin/env bash

echo "create a test service ..."
sed 's@path_to_bot@'$PWD'@' twitch_bot.sh > /etc/init.d/twitch_bot
sed 's@path_to_bot@'$PWD'@' install.service > /etc/systemd/system/twitch_bot.service
chmod +x /etc/init.d/twitch_bot
# sed -i "s/Your_User_Name/you_path/g" /etc/init.d/test
echo "created the test service"