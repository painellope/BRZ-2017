Unsure if any of these will be useful at any point but better safe than sorry.

https://www.reddit.com/r/CarHacking/comments/15h8k4a/toyota_canbus_help_2014_scion_frs/

```
I'm trying to remote start, door lock/unlock/ window lock/unlock, trunk/ control AC (HVAC) with the BRZ and remotely over 4g network.. and I'm getting [sorta] close.

I already know how to quite a few of the info using techstream and Arduino.

door lock and unlock and other are pretty straight forward.

The window is slightly difficult. For now I have to send command to turn the acc car on so it sends power to the BCM responsible for the window control..but I think there is a way to send a command to just power up the control module without putting the car in ACC.
I've complied quote a few documentation.
To get you going these are the supported canid responsible for each aspect of the vehicle - category-wise:

ECU Description RX

0x727 Transmission 0x72F

0x750 Main Body 0x758

0x780 AirBag 0x788

0x781 Precrash 0x789

0x790 Distance 0x798 - Radar

0x791 Precrash2 0x799

0x7A1 Steering Assist 0x7A9 - Power Steering

0x7A2 Park Assist 0x7AA - APGS

0x7B0 ABS Brake 0x7B8

0x7C0 Instrument 0x7C8 - ComboMeter

0x7C4 Air Conditioner 0x7CC

0x7D0 Navigation 0x7D8

0x7E0 Engine Controls 0x7E8 - ECT

0x7E1 Transmission 0x7E9 - Auto Only

0x7E2 Hybrid System 0x7EA - Cruise Control

The "ECU" is for listening to that particular category..basically receving messages like when door is locked/unlock/open/closed, car started/rpm/oil temp/, current gear..and so on and so forth.

The "RX" (Request) is when sending a command to that particular category.. like i want to lock/unlock the door, turn on HVAC, get current tire pressure/temp,....

Hopefully that would points you in the right direct. I have more documentation on the specific completed message to send/receive (if you are interested - still work in progress).

A tip: any entries stuff (like door/trunk/window/lights/sounds/ etc.. and stuff ;)
Cheers!
```

https://racechrono.com/forum/discussion/1764/custom-pids-for-frs-brz-gt86

```
timurrrr
April 2021
Another PID I found on the ft86club forum (thanks map@!) is "fuel remaining".
Even though there's a standard PID for that, it's known that the standard PID it fluctuates a lot and isn't very useful.

Here's a comparison between the custom PID I found (green) and the standard one (orange) during my recent track day:
https://imgur.com/mxo9h2p

Channel: Fuel level (L)
OBD-II header: 0x7C0
PID: 0x2129
Equation: A/2

timurrrr
July 2021
minor correction: a better "fuel remaining (liters)" equation would be "A * 0.5"
```

https://forum.realdash.net/t/can-example-for-indicator-lights/5514/8

Some good explainations in here about certain parts.

Ci_eav May 27
>So you need to build the frame and values;
>first find your targetID use the information found here: RealDash | Manuals | Target Identifiers 8
> 
>Then looking at your example; you will need something like
> 
>your frameID will be; frame id=“0x140”
> 
>Left Indicator;
>```
>offset="2"
>length="1"
>units="bit"
>conversion="V &amp; 6 >> 2"
>```
>Right Indicator
>```
>offset="2"
>length="1"
>units="bit"
>conversion="V &amp; 9 >> 3"
>```
>Basically offset to get the byte position starts at 0, length of 1 means single byte or 8 bits, then the conversion uses BITWISE AND to capture the bits required then shifts the bit you need to the LSB position.
> 
>Hope this helps


Ci_eav May 28
>The reason for the BITSHIFT is, if the targetID is only expecting a single bit (yes/no) then you need to move the bit to the LSB for it to work.
> 
>if offset 0 shows 00010000 highbeam off and 10110000 for on then bit 5 and 7 are changing to high, so this could be two things turning on, if turning the high beams on always turns bit 5 and 7 high then you could use either bit to set your TargetID;
>
>```
>offset=“0”
>Length=“1”
>conversion=“V>>5”
>```
> 
>this would then look like this 10110000 >> 5 = 00000101

