# Remote.py

The sensing mechanism my motorized projector used to stop itself from rolling when it reached the top had failed. This meant I had to either wait the 37 seconds for it to raise, then press the stop button, or I could let it grind its gears forever after raising. I didn't like either of these options, so I connected the RF remote to my network-connected raspberry pi and created this Python script to handle the timing. I use a generic Android ssh-command-shortcut app to issue the command from my phone. You can also set up speech to text (STT), of which there is much documentation for elsewhere.

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
