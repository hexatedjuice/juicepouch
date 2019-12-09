#!/bin/zsh

if [ "$1" = "off" ]; then
    xrandr --output HDMI-2 --off
else
    xrandr --output HDMI-2 --auto --left-of eDP-1
fi
