## EGCP471 Senior design project


"""

scp /Users/csuftitan/Downloads/ngrok-v3-stable-linux-amd64.tgz mendel@192.168.100.2:/home/mendel

sudo tar xvzf ~/Downloads/ngrok-v3-stable-linux-amd64.tgz -C /usr/local/bin

curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok

ngrok config add-authtoken 2MwRUF5A9ahpdmsatjlHkqQGEYE_2r2cjHWeoabJqcARNWQSi

ngrok http 5000

"""

- [x] connect board to wifi `nmtui`
- [x] check wifi connection `nmcli connection show`
- [x] can also pin `ping google.com`
- [x] load file to board `mdt push PycharmProjects/InferenceCoral/main.py`
- [x] run if script on board `python3 main.py`
- [x] install rpi `sudo apt-get install python-rpi.gpio python3-rpi.gpio`
- [x] `sudo apt-get update && sudo apt-get install python3-tk`
- [x] to install GPIO pins`python3 -m pip install python-periphery`

## If while running periphery u get error do this
- [x] `sudo apt-get update && sudo apt-get dist-upgrade`
- [x] `sudo reboot now`


- [x] python3 -m pip install python-periphery

- [x] [Connect to dev board serially with mac](https://coral.ai/docs/dev-board/serial-console/#connect-with-macos)

https://user-images.githubusercontent.com/31228460/218235257-5be39c9e-64e6-4411-84d5-363eaad962af.mov


