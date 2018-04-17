#include "mbed.h"
#include "XBeeLib.h"
#include "constant.h"
#include "intersection.h"

using namespace XBeeLib;

typedef struct {
    uint8_t data[50];
    uint8_t len;
} message_t;

XBeeZB router(RADIO_TX, RADIO_RX, RADIO_RESET, NC, NC, 9600);
Ticker loop;
Timeout pedestrian, emergency;
Intersection intersection;
LocalFileSystem local("local");

uint8_t currentFunc;

void flashPedestrian()
{
    loop.detach();
    loop.attach_us(callback(&intersection, &Intersection::setFlashPedestrian), REFRESH*1000);
}

void receive_cb(const RemoteXBeeZB& remote, bool broadcast, const uint8_t *const data, uint16_t len)
{
    for (uint8_t i = 0; i < len; ++i)
        printf("%x\n\r", data[i]);

    uint8_t newFunc, newDir;

    if (len > 1) {
        if (data[0] == INTERRUPT || data[0] == EMERGENCY) {
            newFunc = data[1];
            newDir = data[2];
        } else {
            newFunc = data[0];
            newDir = data[1];
        }
    }

    if (currentFunc == GREEN || currentFunc == FLASHGREEN) {
        if (len > 1) {
            if (newFunc == currentFunc && newDir == intersection.getDirection()) {
                return;
            } else if (currentFunc == FLASHGREEN && newFunc == GREEN && newDir%2 == intersection.getDirection()%2 ) {

            } else if (currentFunc == GREEN && newFunc == FLASHGREEN && newDir%2 == intersection.getDirection()%2) {
                loop.detach();
                if (newDir >=2) {
                    intersection.setDirection(newDir-2);
                } else {
                    intersection.setDirection(newDir+2);
                }

                loop.attach_us(callback(&intersection, &Intersection::setYellowDir), REFRESH*1000);
                wait_ms(YELLOWTIME);
            } else {
                loop.detach();
                loop.attach_us(callback(&intersection, &Intersection::setYellow), REFRESH*1000);
                wait_ms(YELLOWTIME);
                intersection.setAllRed();
                wait(1);
            }
        } else {
            loop.detach();
            loop.attach_us(callback(&intersection, &Intersection::setYellow), REFRESH*1000);
            wait_ms(YELLOWTIME);
            intersection.setAllRed();
            wait(1);
        }
    }

    switch (data[0]) {
        case FLASHRED:
            loop.detach();
            currentFunc = FLASHRED;
            loop.attach_us(callback(&intersection, &Intersection::flashRed), REFRESH*1000);
            break;

        case FLASHGREEN:
            if (len > 1) {
                if (data[1] < 0x05) {
                    loop.detach();
                    currentFunc = FLASHGREEN;
                    intersection.setDirection(data[1]);
                    loop.attach_us(callback(&intersection, &Intersection::flashGreen), REFRESH*1000);
                }
            }
            break;

        case GREEN:
            if (len > 1) {
                if (data[1] < 0x05) {
                    loop.detach();
                    currentFunc = GREEN;
                    intersection.setDirection(data[1]);
                    loop.attach_us(callback(&intersection, &Intersection::setGreen), REFRESH*1000);
                }
            }
            break;

        case PEDESTRIAN:
            if (len > 1) {
                loop.detach();
                currentFunc = PEDESTRIAN;
                intersection.setPedBool(false);
                printf("PED\n\r");
                loop.attach_us(callback(&intersection, &Intersection::setPedestrian), REFRESH*1000);
                pedestrian.attach(flashPedestrian, data[1]-10);
            }
            break;

        case INTERRUPT:
            if (len > 2) {
                if (data[1] == GREEN || data[1] == FLASHGREEN) {
                    loop.detach();
                    currentFunc = data[1];
                    intersection.setDirection(data[2]);
                    intersection.setInterruptBool(false);

                    if (data[1] == GREEN)
                        loop.attach_us(callback(&intersection, &Intersection::setGreen), REFRESH*1000);
                    else
                        loop.attach_us(callback(&intersection, &Intersection::flashGreen), REFRESH*1000);
                }
            }
            break;

        case EMERGENCY:
            if (len > 2) {
                if (data[1] == GREEN || data[1] == FLASHGREEN) {
                    loop.detach();
                    currentFunc = data[1];
                    intersection.setDirection(data[2]);
                    emergency.attach(callback(&intersection, &Intersection::setEmergencyBool), 15);

                    if (data[1] == GREEN)
                        loop.attach_us(callback(&intersection, &Intersection::setGreen), REFRESH*1000);
                    else
                        loop.attach_us(callback(&intersection, &Intersection::flashGreen), REFRESH*1000);
                }
            }
            break;
    }
}

char getNI()
{
    FILE *fp = fopen("/local/config.txt", "r");

    if (fp != NULL) {
        printf("File is open!\n\r");
        char c = fgetc(fp);
        fclose(fp);
        return c;
    }
    return 'z';
}

int main()
{
    char ni[] = {getNI()};

    router.register_receive_cb(&receive_cb);
    router.init();
    router.set_panid(0x12);
    router.set_node_identifier(ni);

    loop.attach_us(callback(&intersection, &Intersection::flashRed), REFRESH*1000);
    currentFunc = FLASHRED;

    while (1) {
        router.process_rx_frames();
        for (uint8_t i = 0; i < 5; ++i) {
            intersection.emergencyAlert();
            intersection.buttonPressed();
            intersection.interruptAlert();
            wait_ms(REFRESH/10);
        }
    }
}
