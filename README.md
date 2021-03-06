## remote.py

The sensing mechanism my motorized projector used to stop itself from rolling when it reached the top had failed. This meant I had to either wait the 37 seconds for it to raise, then press the stop button, or I could let it grind its gears forever after raising. I didn't like either of these options, so I connected the RF remote to my network-connected raspberry pi and created this Python script to handle the timing. I use a generic Android ssh-command-shortcut app to issue the command from my phone. You can also set up speech to text (STT), of which there is much documentation for elsewhere.

### Setup

```
cd $HOME
git clone https://github.com/kizniche/projector-remote
```

Because all my GPIO pins were in use, one of the remote buttons had to be connected to a GPIO which is HIGH at boot. Only one of these normally-HIGH pins should be used, and it should be connected to the Stop button, as this is the button that will be activated before cron initializes and sets all pins LOW at system startup (essential step). The following line was added to crontab with `sudo crontab -e`:

`@reboot /home/user/projector-remote/remote.py -i &`

Edit `remote.py` to point to the correct GPIO pins (BCM numbering) that are connected to the up, down, and stop buttons of your projector remote.

### Usage

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