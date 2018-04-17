#ifndef CONSTANT_H_
#define CONSTANT_H_

// Codes
#define SETID 0x31
#define FLASHRED 0x32
#define GREEN 0x33
#define FLASHGREEN 0x34
#define PEDESTRIAN 0x35
#define INTERRUPT 0x36
#define EMERGENCY 0x37

#define YELLOW 0x40
#define REFRESH 500
#define YELLOWTIME 3000

// Direction
#define NORTH 0x00
#define EAST 1
#define SOUTH 2
#define WEST 3

//Pin for lights
#define NGREEN p30
#define NYELLOW p29
#define NRED p28

#define EGREEN p27
#define EYELLOW p26
#define ERED p25

#define SGREEN p24
#define SYELLOW p23
#define SRED p22

#define WGREEN p21
#define WYELLOW p20
#define WRED p19

#define PED p10
#define PEDFLASH p11
#define PEDBUTTON p9

#define INTERRUPTNORTH p16
#define INTERRUPTSOUTH p15

#define EMERGENGYIN p12

#endif //CONSTANT_H_