#ifndef INTERSECTION_H_
#define INTERSECTION_H_

#include "mbed.h"
#include "constant.h"
#include "XBeeLib.h"

extern XBeeLib::XBeeZB router;

typedef struct {
    DigitalOut *red, *yellow, *green;
} light_t;

class Intersection
{
    public:
        Intersection();
        
        void setAllRed();
        void flashRed();
        void setGreen();
        void flashGreen();
        void setYellow();
        void setYellowDir();
        void setPedestrian();
        void setFlashPedestrian();
        
        void buttonPressed();
        void emergencyAlert();
        void interruptAlert();
        
        void setDirection(const uint8_t &direction);
        void setPedBool(bool value);
        void setInterruptBool(bool value);
        void setEmergencyBool();
        
        uint8_t getDirection() const;
        
    private:
        light_t lights[4];
        DigitalOut ped, pedFlash;
        DigitalIn emergency, button, *interrupt[2];
        uint8_t currentDir;
        bool sentPed, sentInterrupt, sentEmergency;
};

#endif // INTERSECTION_H_