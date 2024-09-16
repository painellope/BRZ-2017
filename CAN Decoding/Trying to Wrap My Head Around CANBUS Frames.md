This is the example I will use throughout this document of a CAN frame:

```
0x141: 84 26 95 27 B1 82 A7 00
```

`0x141: 84 26 95 27 B1 82 A7 00`

## Endian and Byte Order
There are two sets of terminology when it comes to reading a CAN frame. "Byte Order" and "Endian".

From what I understand, these are the same thing.

Endian comes in two flavours, Big Endian and little Endian.
Byte Order also comes in two, Motorola and Intel.

### To make this quick and easy

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

Then comes the slightly confusing part, out of a 65 bit CANbus frame of 8 bytes (8 bits in 1 byte, 8 bytes in one frame) the bit order of the whole group will NEVER change (at least when within RealDash from my observations).

Byte Order only refers to what order the data is read, not how the data is interpreted as a whole by the program.

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



## Offset, Length, Bit Position, good lord
