# File Descriptions

## rdcan_2024-10-10_09-09-10.csv

A 15 minute drive to work, Inlcudes headlights on and off, high beams, fog lights front and back, handbrake, track VSC abs centre column button presses, door open and close, cruise on, cruise set, seatbelt detection, full turn off, exit car and lock, unlock and enter and startup.

## rdcan_2024-09-12_09-37-00 brake and steering test.csv

this was a test I did to find the brake light and the steering angle, disregard.

## rdcan_2024-09-09_16-13-59.csv

A short regular drive, not super verbose.

## canplayback2.py

An adjusted version of this python script that broadcasts can frames from RDCAN logs locally for realdash to use (this is mainly for testing xml inputs and creating dashboards without needing to sit in your car)
This adjusted version allows you to set the push speed of the frames. It is still limited however as frames with less than 8 bytes are padded with zeroes. eg: 

In a terminal, cd to the file path of your RDCAN log and the "canplayback2.py" file

python3 canplayback2.py rdcan_file.csv "port number" "frame push speed"

I usually set the frame push speed to 89000. In realdash this gives me about 400 frames/sec, which is close enough to what I get directly from my BRZ at 500k baud using a OBDLink SX USB adapter.
