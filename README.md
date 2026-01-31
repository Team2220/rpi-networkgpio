# Raspberry Pi – Network GPIO

A series of lightweight scripts to control GPIO pins over the network on a 
Raspberry Pi. 

## Pi Setup

```bash
sudo apt install git python3-pip
git clone https://github.com/Team2220/rpi-networkgpio.git
cd rpi-networkgpio/

# Open the folder for the app you want to use

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Edit constants in the head of the Python file
sudo nano main.py

# Python must be run with sudo for GPIO access
sudo python3 main.py
```


## Example `systemd` service

The below is an example for the `sensorin` app, which would be placed at `/etc/systemd/system/sensorin.service`

```
[Unit]
Description=RPi Network GPIO Sensor Input
After=network.target

[Service]
Type=simple

# Run as root
User=root

# Set working directory
WorkingDirectory=/home/pi/rpi-networkgpio/sensorin

# Use the virtualenv Python
ExecStart=/home/pi/rpi-networkgpio/sensorin/.venv/bin/python main.py

# Restart if it crashes
Restart=always
RestartSec=5

# Environment hygiene
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Then run it with

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable sensorin.service

sudo reboot -h now
```
