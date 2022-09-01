#!/bin/bash
TMPBG=~/.config/lockscreen.png
RES=1366x768
W="00000000"
HL="fd9a85ff"
 
ffmpeg -f x11grab -video_size $RES -y -i $DISPLAY -filter_complex "boxblur=5:1,overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2" -vframes 1 $TMPBG
i3lock -i $TMPBG -C -e -k \
	--inside-color=$W \
	--ring-color=$W \
	--insidever-color=$W \
	--ringver-color=$W \
	--insidewrong-color=$W \
	--ringwrong-color=$W \
	--line-color=$W \
	--keyhl-color=$HL \
	--bshl-color=$HL \
	--separator-color=$HL \
	--verif-color=$W \
	--wrong-color=$W \
	--time-str="%H:%M:%S" \
	--date-str="%A %m %Y" \
	--verif-text="" \
	--wrong-text="" \
	--time-font="hack 10" \
	--date-font="hack 10" 
