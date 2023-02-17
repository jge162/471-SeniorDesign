# EGCP471
Senior design project

[GPIO for Dev board](https://coral.ai/docs/dev-board/gpio/#program-gpios-with-libgpiod)

python3 -m pip install python-periphery

[Connect to dev board serially with mac](https://coral.ai/docs/dev-board/serial-console/#connect-with-macos)

https://user-images.githubusercontent.com/31228460/218235257-5be39c9e-64e6-4411-84d5-363eaad962af.mov


![71PvKR7TpUL _AC_SL1500_](https://user-images.githubusercontent.com/31228460/215386467-6c2f1c0b-feda-44ed-afb5-6997da802b85.jpg)


if  :
  ser = serial.Serial('/dev/ttyACM0', 9600)
  ser.write(b'Waste')
  ser.close()(edited)
elif :
  ser = serial.Serial('/dev/ttyACM0', 9600)
  ser.write(b'Recyling')
  ser.close()(edited)
elif :
  ser = serial.Serial('/dev/ttyACM0', 9600)
  ser.write(b'Compost')
  ser.close()(edited)
else
    return 0;
