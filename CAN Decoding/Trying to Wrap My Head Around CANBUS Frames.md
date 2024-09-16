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

To figure out all this hex code crap, I've been using a tool called "Kvaser Database Editor" whose terminology differs from RealDash.

RealDash's CAN XML specification utilises 2 main reference source pages

"Target Identifiers" 
https://realdash.net/manuals/targetid.php

and

"Channel Description File" 
https://github.com/janimm/RealDash-extras/blob/175c6e1c8c08a9c8f1a8e61ca5505b3488e8090e/RealDash-CAN/realdash-can-description-file.md 

I won't be telling you how to construct a RealDash XML File from scratch (henceforth refered as RDXML), but I will try my best to give the basic rundown on the terminology and how to read a "frame description".

Let's use our trusty example canbus frame as a starting point.

`0x141: 84 26 95 27 B1 82 A7 00`
