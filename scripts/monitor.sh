#!/bin/zsh

if [ "$1" = "off" ]; then
    xrandr --output HDMI2 --off
else
    xrandr --output HDMI2 --auto --left-of eDP1
fi
