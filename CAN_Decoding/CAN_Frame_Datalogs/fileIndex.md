# File Descriptions

## rdcan_2024-10-10_09-09-10.csv

A 15 minute drive to work, Inlcudes headlights on and off, high beams, fog lights front and back, handbrake, track VSC abs centre column button presses, door open and close, cruise on, cruise set, seatbelt detection, full turn off, exit car and lock, unlock and enter and startup.

## rdcan_2024-09-12_09-37-00 brake and steering test.csv

this was a test I did to find the brake light and the steering angle, disregard.

## rdcan_2024-09-09_16-13-59.csv

A short regular drive, not super verbose.

## rdcan_2024-10-10_15-20-00.csv

a test of the keyless entry system, locking system, approach and unlock, lock and leave car deactivation, so on.

## canplayback2.py

An adjusted version of [this](https://github.com/janimm/RealDash-extras/tree/master/CanPlayback) python script that broadcasts can frames from RDCAN logs locally for realdash to use (this is mainly for testing xml inputs and creating dashboards without needing to sit in your car)
This adjusted version allows you to set the push speed of the frames. It is still limited however as frames with less than 8 bytes are padded with zeroes. 
eg: 
```
0x0d3: 00 06 C0 0F 00 00 42
```
becomes 
```
0x0d3: 00 06 C0 0F 00 00 42 00
```
This messes with the endian in places. When using playback, the speed indicator doesn't pull correctly using my XML because the speed value comes from a frame with less than 8 bytes. The padded zeroes mess with the bit counting because the extra zeroes have added 16 more bits to the equation.
___
### Usage
In a terminal, cd to the file path of your RDCAN log and the "canplayback2.py" file
```
python3 canplayback2.py rdcan_file.csv "port number" "frame push speed"
```
I usually set the frame push speed to 89000. In realdash this gives me about 400 frames/sec, which is close enough to what I get directly from my BRZ at 500k baud using a OBDLink SX USB adapter.
___
*Original without frame push speed adjustment*

https://github.com/janimm/RealDash-extras/tree/master/CanPlayback
># **RealDash-extras**
>
>RealDash examples and technical materials
>
>All materials in this repository are licensed with [NoLicense](https://github.com/janimm/RealDash/blob/master/LICENSE)
>
>[realdash.net](https://www.realdash.net)
>
>&nbsp;
>## **CanPlayback**
>
>This is a simple tool to stream RealDash CAN frames from CAN log files recorded in RealDash CAN Monitor. Usage:
>
>     $ python3 canplayback.py CSVFILE PORT
>
>For example:
>
>     $ python3 canplayback.py rdcan_2023-03-31_11-33-36.csv 35000
> 
>Limitations:
> 
>- Only works on <=8 byte frames (0x11223344 frames).
>- Frames with less than 8 bytes are padded with zeroes.
>- Has no timing, it pushes the frames as quickly as possible.
>- Enable 'time.sleep(0.01)' in the code to slow down.
>- Has no proper error checking
>
>&nbsp;
