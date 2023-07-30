# Computer Engineering Capstone Project!

<img src="https://github.com/jge162/471-SeniorDesign/blob/main/Poster.png?raw=true" alt="Poster for project expos" width="700">

<br>

>[!IMPORTANT]\
>Below is a demonstration of the proof of concept:<br>
>Recycling, Composting, and Waste using [Object Detection](https://github.com/jge162/471-SeniorDesign).

https://github.com/jge162/471-SeniorDesign/assets/31228460/0b967d8c-b739-4792-8bc6-f9a21e2802c5

## Coral commands 

- [x] use `mdt shell` to connect to coral via USB
- [x] use `ssh mendel@192.168.100.2` to connect via SSH, then use password to connect. 
- [x] connect board to wifi `nmtui`
- [x] check wifi connection `hostname -I` shows IP address of Coral
- [x] can also pin `ping google.com` verifies your are connected to WIFI
- [x] load file to board `mdt push PycharmProjects/InferenceCoral/main.py`
- [x] run Python script on Coral `python3 main.py`
- [x] `sudo apt-get update && sudo apt-get dist-upgrade`
- [x] `sudo reboot now`
- [x] `sudo shutdown now`
- [x] [Connect to dev board serially with mac](https://coral.ai/docs/dev-board/serial-console/#connect-with-macos)

## Git commands.

- [x] `git config --global user.name "Your username"` setup username for Repo
- [x] `git config --global user.email "Your email address"` setup account email
- [x] `git remote set-url origin 
### After above has been completed does not need to be done again. 
- [x] `git pull origin main` 
- [x] `git add .`
- [x] `git commit -m "message you want to describe commit"`

## Update index.html on Google Coral dev board.

- [x] `cd templates`
- [x] `nano index.html` makes changes then do the following commands
- [x] using `control k` will delete line by line code in index.html file
- [x] then use `control o` to save file, then press enter to make changes
- [x] lastly, use `control x` to exit nano editor (used with bin/bash normally)

<br> </br>


