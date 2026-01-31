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
