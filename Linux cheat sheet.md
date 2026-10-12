# Raspberry Pi OS / Linux cheat sheet

Raspberry Pi OS is based on Debian. Most of your work will happen in a terminal, usually over SSH.
Replace `pi`, `raspberrypi.local` and the paths below with your own values.

## Connect

```
ssh pi@raspberrypi.local        # or ssh pi@192.168.1.100
exit                            # leave the SSH session
scp file.py pi@raspberrypi.local:~/project/       # copy PC -> Pi
scp pi@raspberrypi.local:~/project/out.csv .      # copy Pi -> PC
```

## Files and directories

```
pwd                  # where am I
ls -la               # list everything, with details and hidden files
cd /path/to/dir      # go there      cd ..  one level up     cd ~  home     cd -  previous
mkdir -p a/b         # create folders (also the missing parents)
cp src dst           # copy          cp -r dir1 dir2   copy a folder
mv old new           # move / rename
rm file              # delete (no trash bin!)       rm -r dir   delete a folder
```

Key places: `/home/<user>` your files, `/etc` configuration, `/dev` devices,
`/boot/firmware` boot configuration, `/var/log` logs.

## Looking at and editing files

```
cat file             # print the whole file
less file            # scroll through it (q to quit)
head -n 20 file      # first lines          tail -n 20 file   last lines
tail -f file         # follow a log live (Ctrl+C to stop)
grep "text" file     # lines containing text     grep -rn "text" .   search a whole folder
nano file            # simple editor: Ctrl+O save, Ctrl+X exit
```

## Users and permissions

```
whoami               # who am I
sudo command         # run as administrator (only when needed)
ls -l file           # -rwxr-xr-- = owner rwx, group r-x, others r--
chmod +x script.py   # make executable            chmod 644 file   rw-r--r--
sudo chown pi:pi file
```

"Permission denied" usually means: missing `x` (use `chmod +x`) or the file belongs to someone else (`ls -l`).

## Packages and Python

```
sudo apt update                  # refresh the package list
sudo apt upgrade                 # install updates
sudo apt install package         # install        sudo apt remove package
python3 -m venv .venv            # per-project environment (see Example 01)
source .venv/bin/activate        # enter it       deactivate  to leave
pip install -r requirements.txt
sudo raspi-config                # SSH, I2C, SPI, locale, timezone, ...
```

## Processes

```
top        or   htop              # what is running, CPU and memory (q to quit)
ps aux | grep python              # find a process
kill PID                          # ask it to stop       kill -9 PID   force
python3 script.py &               # run in the background
Ctrl+C                            # stop the program in the foreground
```

## Run a script at boot (systemd service)

Create `/etc/systemd/system/myapp.service` (with `sudo nano`):

```
[Unit]
Description=My Python app
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/project
ExecStart=/home/pi/project/.venv/bin/python /home/pi/project/script.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Then:

```
sudo systemctl daemon-reload        # after creating or editing the file
sudo systemctl enable --now myapp   # start now and at every boot
systemctl status myapp              # is it running?
sudo systemctl restart myapp        # after changing the script     (stop / disable also exist)
journalctl -u myapp -f              # its output (print / logging), live
```

## Network

```
hostname -I                  # my IP address(es)
ip a                         # all interfaces
ping -c 4 8.8.8.8            # is the internet reachable (Ctrl+C to stop without -c)
```

Static IP: see `static on pi.txt`.

## Hardware and system health

```
vcgencmd measure_temp        # CPU temperature
df -h                        # disk space
free -h                      # memory
uptime                       # how long it has been running, load
lsusb                        # USB devices
ls /dev                      # devices appear as files (e.g. serial ports, i2c-1)
sudo apt install i2c-tools && i2cdetect -y 1     # find I2C devices (enable I2C in raspi-config first)
sudo reboot                  # restart             sudo shutdown now   power off safely
```

## Shortcuts

`Tab` completes names · `↑` previous command · `Ctrl+C` stop · `Ctrl+L` clear the screen ·
`history` past commands · `man command` or `command --help` for help.
