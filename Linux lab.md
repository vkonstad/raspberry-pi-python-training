- We will need multiple terminal windows.

- Find out useful info:
  ```
  uname -a                  # kernel version and architecture
  cat /etc/os-release       # which operating system / version we run
  nproc                     # number of CPU cores
  free -h                   # memory used and free (-h = human readable)
  vcgencmd measure_temp     # CPU temperature (Raspberry Pi specific)
  ```

- Install tools with apt:
  ```
  sudo apt update
  ```

  Read about a package *before* installing it:
  ```
  apt show stress-ng            # description, version, size, dependencies
  apt-cache policy stress-ng    # installed version and the version available to install
  ```

  Install two tools:
  ```
  sudo apt install htop stress-ng    # htop: process viewer, stress-ng: generates CPU load
  ```

  Find out what you got:
  ```
  which stress-ng           # where the program was installed
  stress-ng --version       # check that it runs
  ```

- In one of the terminals start a process viewer:
  ```
  htop                      # run console task manager (q to quit)
  ```

- In another terminal show the temperature every second:
  ```
  watch -n 1 vcgencmd measure_temp    # watch repeats a command every 1 second (Ctrl+C to stop)
  ```

- Put the Pi under load: open a third terminal and run a 60 second CPU stress test using all four cores:
  ```
  stress-ng --cpu 4 --timeout 60s --metrics-brief    # 4 CPU workers for 60 s, then a short summary
  ```

- Experiment running a tool with/without the stress.

  Copy the example to the Pi:
  ```
  scp "Example Simple timing.py" pi@ipaddress:~/    # copy a file over SSH to the Pi's home folder
  ```

  Without stress:
  ```
  python3 "Example Simple timing.py" 5000000    # run the script, sum the numbers up to 5000000
  ```

  With stress:
  ```
  stress-ng --cpu 4 --timeout 60s                      # start the load (wait a few seconds, or run it in another terminal)
  python3 "Example Simple timing.py" 5000000      # run the same script again and compare the times
  ```

- Compare the two times. Discover if the Pi had to throttle (`throttled=0x0` means no issue. Anything else means undervoltage or too hot that slowed it down):
  ```
  vcgencmd get_throttled    # flags telling if the Pi was undervolted or slowed down by heat
  ```

- Clean up and conclusions:
  ```
  sudo apt remove stress-ng    # uninstall the package
  which stress-ng              # prints nothing if it is gone
  ```

- Record your results in a log file on the Pi (`>` creates the file, `>>` appends to it):
  ```
  echo "Lab results of <your names>" > ~/lab.log           # start a new log file with a title line
  date >> ~/lab.log                                        # when the measurement was taken
  nproc >> ~/lab.log                                       # number of CPU cores
  vcgencmd measure_temp >> ~/lab.log                       # current temperature
  vcgencmd get_throttled >> ~/lab.log                      # throttling flags
  python3 "Example Simple timing.py" 5000000 >> ~/lab.log  # the timing result, saved instead of printed
  cat ~/lab.log                                            # check what was recorded
  ```

- Bring the log back to your PC. Open a terminal **on the PC** (not inside the SSH session) and run:
  ```
  scp pi@ipaddress:~/lab.log .    # copy the file from the Pi to the current folder of the PC (the dot)
  ```
  Open `lab.log` on the PC and check that it contains your results. Submit it as the outcome of the lab.

## Two small tasks

Both tasks use `Example 12 - CPU Temperature to SQLite.py`: a script that stores the CPU temperature
in a local SQLite file (`temperature.db`, created next to the script). Copy it to the Pi, run it by hand
once and check the data with `sqlite3 temperature.db "SELECT * FROM cpu_temperature;"`
(`sudo apt install sqlite3` if the command is missing).

### Task 1 - Run it periodically with cron

`cron` runs commands on a schedule. Your goal: **a new temperature row every minute, without you being logged in.**

What you need to find out and write down:
- Where the schedule lives, and the command to edit it (`crontab -e`, list it with `crontab -l`).
- The line to add. It has 5 time fields followed by the command: `minute hour day-of-month month day-of-week command`
  (`*` means "every"). Work out which values mean "every minute".
- The command part must use **absolute paths** for both `python3` (find it with `which python3`) and the script,
  because cron does not start in your folder. Think about where the output of the script should go
  (e.g. `>> /home/pi/cron.log 2>&1`) so you can see errors.

Check: after 2-3 minutes `sqlite3 temperature.db "SELECT COUNT(*) FROM cpu_temperature;"` returns more than the number of manual runs, and the timestamps are a minute apart.
Finally remove your line from the crontab so it stops.

### Task 2 - Run it as a systemd service

A service is better than cron when the program must keep running and be restarted if it fails.
Your goal: **the script records a reading every 10 seconds (use its `--every 10` option), starts at boot, and restarts itself if it crashes.**

What you need to find out and write down (see `Linux cheat sheet.md`):
- The file you create and where it must be placed (`/etc/systemd/system/<name>.service`, edit it with `sudo`).
- The sections and settings it needs: `[Unit]` (a description), `[Service]` (the user, the working directory, `ExecStart` with absolute paths, `Restart`) and `[Install]` (`WantedBy`).
- The commands to make systemd read the new file, start it now and at every boot, check its state, and read its output (`systemctl`, `journalctl`).

Check: `systemctl status` shows `active (running)`, new rows appear every 10 seconds, and after `kill` of the python process (find it with `ps aux | grep Example`) the service starts it again.
Reboot the Pi to confirm that it comes back by itself, then disable and remove the service.

Which one would you use for a program that must run once an hour? And for one that must never stop? Write your answer in the `lab.log` you hand in.
