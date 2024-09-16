This is the example I will use throughout this document of a CAN frame:

```
0x141: 84 26 95 27 B1 82 A7 00
```

`0x141: 84 26 95 27 B1 82 A7 00`

# Endian and Byte Order
There are two sets of terminology when it comes to reading a CAN frame. "Byte Order" and "Endian".

From what I understand, these are the same thing.

Endian comes in two flavours, Big Endian and little Endian.
Byte Order also comes in two, Motorola and Intel.
 
To summarise quick and dirty...

Motorola = Big Endian

Intel = little Endian

From what I can gather, little endian means reading by increasing byte address, and Big endian is reading by decreasing byte address

(byte address is simply the position of the byte within a can frame, low address is byte 0, high address would be byte 7)

The order and the number sequence / position of the bits doesn't change, 0010110 won't flip around to become 0110100 ever.
However the order of which you read bit groups (bytes) in succession will change:

big endian
| byte 1 | byte 0 |
| ------- | ------- |
| 00110111 | 11010000 |

little endian
| byte 0 | byte 1 |
| ------- | ------- |
| 11010000 | 00110111 |


| motorola, big endian        | intel, little endian                                                      |
| ----------------- | ------------------------------------------------------------------ |
| ![motorola](https://github.com/painellope/BRZ-2017/blob/c113d158e0237d8665a8e1dd43bda497d2bf6d48/CAN%20Decoding/referenced%20images/motorola.png) | ![intel](https://github.com/painellope/BRZ-2017/blob/c113d158e0237d8665a8e1dd43bda497d2bf6d48/CAN%20Decoding/referenced%20images/Intel.png) |


# Offset, Length, Bit Position, good lord

Now comes the slightly confusing part, out of a 64 bit CANbus frame of 8 bytes (8 bits in 1 byte, 8 bytes in one frame) the bit order of the whole group will NEVER change (at least when within RealDash from my observations).

Byte Order only refers to what order the data is read, not how the data is interpreted or labeled as a whole by the program.

The sequence or position name (or whatever you want to call it) of each bit is as follows:

|       | **7** | **6** | **5** | **4** | **3** | **2** | **1** | **0** |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **0** | _7_   | _6_   | _5_   | _4_   | _3_   | _2_   | _1_   | _0_   |
| **1** | _15_  | _14_  | _13_  | _12_  | _11_  | _10_  | _9_   | _8_   |
| **2** | _23_  | _22_  | _21_  | _20_  | _19_  | _18_  | _17_  | _16_  |
| **3** | _31_  | _30_  | _29_  | _28_  | _27_  | _26_  | _25_  | _24_  |
| **4** | _39_  | _38_  | _37_  | _36_  | _35_  | _34_  | _33_  | _32_  |
| **5** | _47_  | _46_  | _45_  | _44_  | _43_  | _42_  | _41_  | _40_  |
| **6** | _55_  | _54_  | _53_  | _52_  | _51_  | _50_  | _49_  | _48_  |
| **7** | _63_  | _62_  | _61_  | _60_  | _59_  | _58_  | _57_  | _56_  |


With the table above, let's use our example and try to find the 43rd bit.

| frameId | 0        | 1        | 2        | 3        | 4        | 5        | 6        | 7        |
|---------|----------|----------|----------|----------|----------|----------|----------|----------|
| 0x141   | 84       | 26       | 95       | 27       | B1       | 82       | A7       | 00       |
|         | 10000100 | 00100110 | 10010101 | 00100111 | 10110001 | 10000010 | 10100111 | 00000000 |

Now remember, the bit position doesn't change, regardless of whether we are using Big or Little Endian.


So, Bit number 43 is in the 5th byte, as we can see from the main table above. The 5th byte in the second table is byte value "82".
Bit 43 is in the column labelled 3 (which is the 4th column from the right because we start counting from 0). Now, in the binary conversion of byte "82" we start counting from the right till we reach bit position 3 within this byte.

| **7** | **6** | **5** | **4** | **3** | **2** | **1** | **0** |
|-------|-------|-------|-------|-------|-------|-------|-------|
| 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| - | - | - | - | ^ | - | - | - |

Therefore our current value, for bit position 43 is "0".

RealDash orders the bytes oddly, so just keep that in mind.

<img src="https://github.com/painellope/BRZ-2017/blob/86723ae7b57d732e43ebadeb511f8fd433573165/CAN%20Decoding/referenced%20images/realdash%20byte%20order.png" width="484" height="381">
<img src="https://github.com/painellope/BRZ-2017/blob/b8e7bec423e73d6953f52c157df50c9de8b5d64b/CAN%20Decoding/referenced%20images/realdash%20byte%20order%20copy.png" width="484" height="381">

Further details regarding bitPosition vs startBit vs offset vs length vs etc will be covered below.

# RealDash Canbus XML Configurations: Explored and Explained

To figure out all this hex code crap, I've been using a tool called "Kvaser Database Editor" whose terminology differs from RealDash. It allows you to play around with different values and has a handy visualisation on the right hand side so you can experiment and deduce what each part means.

RealDash's CAN XML specification utilises 2 main reference source pages

"Target Identifiers" 
https://realdash.net/manuals/targetid.php

and

"Channel Description File" 
https://github.com/janimm/RealDash-extras/blob/175c6e1c8c08a9c8f1a8e61ca5505b3488e8090e/RealDash-CAN/realdash-can-description-file.md 

I won't be telling you how to construct a RealDash XML File from scratch (henceforth refered as RDXML), but I will try my best to give the basic rundown on the terminology and how to read a "frame description".

Let's use our trusty example canbus frame as a starting point.

`0x141: 84 26 95 27 B1 82 A7 00`

and here is an example frame

````
<frame id="0x141">
  <value name="Custom_Engine_Torque" bitcount="15"/>
  <value name="Engine_Engine_Stop" startbit="15" bitcount="1" units="bit"/>
  <value name="Wheel_Torque" offset="2"/>
  <value targetId="37" offset="4" length="6"/>
</frame>
````

Lets go through line by line and figure this thing out.

## **frame 'id' attribute**
https://github.com/janimm/RealDash-extras/blob/master/RealDash-CAN/realdash-can-description-file.md#frame
> Every **frame** must have an **id** number, specified either in decimal or hexadecimal number (to specify hexadecimal, use the **0x** prefix). Note that if enclosing **frames** have a **baseId** specified, the resulting id number will be **baseId + id**.
```
    <frame id="321">
    or
    <frame id="0x141">
```
0x141 is the same as 321 (hex to decimal conversion)

## **'baseId' attribute**

Now this isn't relevant to our example and I'm not 100% certain on what the purpose of this attribute actually is, but I think it's probably used for when the length of a bit value stretches over multiple bytes. I haven't used this so far within my use case but if I do I'll update this with whatever I can glean.

https://github.com/janimm/RealDash-extras/blob/master/RealDash-CAN/realdash-can-description-file.md#baseid-attribute-optional
> **frames** may optionally contain a attribute **baseId** that is used for the enclosed **frame** tags. Example:
> ```
>    <frames baseId="321">
> ```
> Specifies the **baseId** of 321. Any id value in later **frame** is added to the base id. For example, if **frames baseId** is 321 and it contains a frame with **id** 1, then the frame is considered to have an **id** of 322.
>
> The **baseId** and the **id** in **frame** can also be specified as hexadecimal value with prefix of **0x**. Example:
> ```
>    <frames baseId="0x141"> <!-- same as baseId="321"-->
> ```

## **value 'targetId' attribute**
This attribute links the frame to whatever RealDash value you want, RPM, Fuel Level, Headlight Status etc.. The **targetId="37"** writes whatever value the CAN frame specifies to RealDash's RPM input. Check out the full listing of [RealDash targetIds](www.realdash.net/manuals/targetid.php).


## **value 'name' (optional to targetId)**
Instead of mapping the value to existing RealDash input, **name** attribute can be used to create new input into RealDash *ECU Specific* category. Name attribute is used only if **targetId** is not present in command. Example:
```
     <value name="Custom_Engine_Torque" bitcount="15"/>
```
> Note that the above example does not use **targetId**, but **name** instead. When RealDash reads the XML file, a NEW custom input is created into the *ECU Specific* category called **Custom_Engine_Torque**. This new custom input can be used like any other input in RealDash for gauges and triggers/actions.

> Note: if you make your own dashboard that links into custom inputs, remember that other users need to have same XML available for the dashboard to work correctly. Another solution would be to make the dashboard use [RealDash > build-in inputs](www.realdash.net/manuals/targetid.php) and use the *Input Mapping* feature in RealDash *Settings->Units & Values->Input Mapping*.

When building the XML for my BRZ via the preglobal_2015 dbc file, many new Custom inputs were created as the DBC file used generic labels and names for each frame rather than the RealDash specific targetId's. I've been going through RealDash and manually assigning each value with the custom input created when I converted the dbc file.

[_subaru_preglobal_2015.dbc](https://github.com/painellope/BRZ-2017/tree/0accce7f69cb0569dd85316c4a633274736cdf04/CAN%20Decoding/CAN%20Database%20Files)

https://my.realdash.net has a tool built in that allows you to upload dbc files, which it will then convert to xml and upload to your "Garage". I believe you need to have the paid subscription to RealDash to use this feature, however.

startbit = which bit to start reading from

bitcount = how many bits to read together to get value

offset = which hex byte to start reading from

length = how many hex bytes to read together to get the value
