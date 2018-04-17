#include "intersection.h"

Intersection::Intersection() : ped(PED), pedFlash(PEDFLASH), button(PEDBUTTON), emergency(EMERGENGYIN), currentDir(0), sentPed(false), sentInterrupt(false), sentEmergency(false)
{
    lights[NORTH].green = new DigitalOut(NGREEN);
    lights[NORTH].yellow = new DigitalOut(NYELLOW);
    lights[NORTH].red = new DigitalOut(NRED);

    lights[EAST].green = new DigitalOut(EGREEN);
    lights[EAST].yellow = new DigitalOut(EYELLOW);
    lights[EAST].red = new DigitalOut(ERED);

    lights[SOUTH].green = new DigitalOut(SGREEN);
    lights[SOUTH].yellow = new DigitalOut(SYELLOW);
    lights[SOUTH].red = new DigitalOut(SRED);

    lights[WEST].green = new DigitalOut(WGREEN);
    lights[WEST].yellow = new DigitalOut(WYELLOW);
    lights[WEST].red = new DigitalOut(WRED);

    interrupt[0] = new DigitalIn(INTERRUPTNORTH);
    interrupt[1] = new DigitalIn(INTERRUPTSOUTH);

    setAllRed();
}

void Intersection::setAllRed()
{
    for (uint8_t i = 0; i < 4; ++i) {
        *lights[i].yellow = *lights[i].green = 0;
        *lights[i].red = 1;
    }
}

void Intersection::flashRed()
{
    static bool on = true;
    for (uint8_t i = 0; i < 4; ++i) {
        *lights[i].yellow = *lights[i].green = 0;
    }
    ped = pedFlash = 0;

    *lights[NORTH].red = *lights[SOUTH].red = on;
    *lights[EAST].red = *lights[WEST].red = !on;
    on = !on;
}

void Intersection::setGreen()
{
    uint8_t direction = currentDir % 2;
    for (uint8_t i = 0; i < 4; ++i) {
        if (i%2 != direction) {
            *lights[i].green = *lights[i].yellow = 0;
            *lights[i].red = 1;
        }
    }
    ped = pedFlash = 0;

    *lights[direction].red = *lights[direction].yellow = 0;
    *lights[direction].green = 1;
    direction += 2;
    *lights[direction].red = *lights[direction].yellow = 0;
    *lights[direction].green = 1;
}

void Intersection::flashGreen()
{
    static bool on = true;
    for (uint8_t i = 0; i < 4; ++i) {
        if (i != currentDir) {
            *lights[i].green = *lights[i].yellow = 0;
            *lights[i].red = 1;
        }
    }
    ped = pedFlash = 0;

    *lights[currentDir].red = *lights[currentDir].yellow = 0;
    *lights[currentDir].green = on;
    on = !on;
}

void Intersection::setYellow()
{
    for (uint8_t i = 0; i < 4; ++i) {
        if (*lights[i].red != 1) {
            *lights[i].green = 0;
            *lights[i].yellow = 1;
        }
    }
    ped = pedFlash = 0;
}

void Intersection::setYellowDir()
{
    *lights[currentDir].green = *lights[currentDir].red = 0;
    *lights[currentDir].yellow = 1;
}

void Intersection::setPedestrian()
{
    setAllRed();
    ped = 1;
    pedFlash = 0;
}

void Intersection::setFlashPedestrian()
{
    setAllRed();
    ped = 0;

    pedFlash = !pedFlash;
}

void Intersection::buttonPressed()
{
    if (button == 1) {
        if (!sentPed) {
            uint8_t data[] = {PEDESTRIAN};
            XBeeLib::TxStatus status = router.send_data_to_coordinator(data, 1);
            sentPed = 1;
        }
    }
}

void Intersection::emergencyAlert()
{
    if (emergency == 1) {
        if (!sentEmergency) {
            uint8_t data[] = {EMERGENCY};
            XBeeLib::TxStatus status = router.send_data_to_coordinator(data, 1);
            sentEmergency = 1;
        }
    }
}

void Intersection::interruptAlert()
{
    uint8_t direction;

    if (*interrupt[0] == 1) {
        direction = NORTH;
    } else if (*interrupt[1] == 1) {
        direction = SOUTH;
    } else {
        return;
    }

    uint8_t data[] = {INTERRUPT, direction};
    if (!sentInterrupt) {
        XBeeLib::TxStatus status = router.send_data_to_coordinator(data, 2);
        sentInterrupt = 1;
    }
}

void Intersection::setDirection(const uint8_t &direction)
{
    if (direction == 4) {
        currentDir = NORTH;
    } else {
        currentDir = direction;
    }
}

void Intersection::setPedBool(bool value)
{
    sentPed = value;
}

void Intersection::setInterruptBool(bool value)
{
    sentInterrupt = value;
}

void Intersection::setEmergencyBool()
{
    sentEmergency = false;
}

uint8_t Intersection::getDirection() const
{
    return currentDir;
}