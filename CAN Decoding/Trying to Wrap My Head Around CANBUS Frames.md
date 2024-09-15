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

| motorola             | Hex                                                                |
| ----------------- | ------------------------------------------------------------------ |
| ![motorola](https://github.com/painellope/BRZ-2017/blob/c113d158e0237d8665a8e1dd43bda497d2bf6d48/CAN%20Decoding/referenced%20images/motorola.png) | ![intel](https://github.com/painellope/BRZ-2017/blob/c113d158e0237d8665a8e1dd43bda497d2bf6d48/CAN%20Decoding/referenced%20images/intel.png) |


![motorola](https://github.com/painellope/BRZ-2017/blob/c113d158e0237d8665a8e1dd43bda497d2bf6d48/CAN%20Decoding/referenced%20images/motorola.png)
![intel](https://github.com/painellope/BRZ-2017/blob/c113d158e0237d8665a8e1dd43bda497d2bf6d48/CAN%20Decoding/referenced%20images/intel.png)



## Offset, Length, Bit Position, good lord
