# Remote.py

The sensing mechanism my motorized projector used to stop itself from rolling when it reached the top had failed. This meant I had to either wait the 37 seconds for it to raise, then press the stop button, or I could let it grind its gears forever after raising. I didn't like either of these options, so I connected the RF remote to my network-connected raspberry pi and created this Python script to handle the timing. I use a generic Android ssh-command-shortcut app to issue the command from my phone. You can also set up speech to text (STT), of which there is much documentation for elsewhere.

Because I have all my raspberry pi GPIO pins in use, one of the remote's buttons had to be connected to a normally-HIGH GPIO. There are only a few of these, which are HIGH at boot. This would be connected to the Stop button, as this will not cuse the screen to raise or lower when the raspberry pi is starting up. The following line was added to crontab with `sudo crontab -e` to initialize all button pins at startup:

`@reboot /usr/local/bin/remote.py -i &`

remote.py usage:

```
remote.py: Control a 3-button remote to raise and lower aprojector screen

Usage: remote.py OPTION

Options:
    -i, --initialize
           Initialize the GPIO pins (set all low)
    -d, --down
           Lower the screen
    -u, --up
           Raise the screen
    -h, --help
           Show this help and exit
```