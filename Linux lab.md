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
