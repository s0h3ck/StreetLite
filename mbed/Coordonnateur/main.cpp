#include "Websocket.h"
#include "EthernetInterface.h"
#include "XBeeLib.h"
#include "mbed.h"

#include "instruction.h"
#include "constant.h"

#define MAXROUTERS 2

using namespace XBeeLib;

typedef struct router router;
struct router {
    uint8_t id;
    char ni;
    RemoteXBeeZB xbee;
    bool pedestrian;
    bool interrupt;
    uint8_t interruptDir;
};

XBeeZB xbee = XBeeZB(RADIO_TX, RADIO_RX, RADIO_RESET, NC, NC, 9600);
router routers[MAXROUTERS];
uint8_t nbRouters = 0;
Timer timeout;

Websocket *ws;
FILE *fp;

instructionList list;
instruction_t *current = NULL;
instruction_t *interrupt = NULL;
instruction_t emergency;
instruction_t *lastSent = NULL;

bool emergencyDetect = 0;

void nextInstruction();

void discovery_function(const RemoteXBeeZB& remote, char const * const node_id)
{
    if (nbRouters < MAXROUTERS) {
        for (uint8_t i = 0; i < nbRouters; ++i) {
            if ( remote.get_addr64() == routers[i].xbee.get_addr64()) {
                return;
            }
        }
        routers[nbRouters].xbee = remote;
        routers[nbRouters].id = nbRouters;
        routers[nbRouters].ni = node_id[0];
        printf("%s\n\r", node_id);
        nbRouters++;
    }
}

void receive_cb(const RemoteXBeeZB& remote, bool broadcast, const uint8_t *const data, uint16_t len)
{
    if (data[0] == PEDESTRIAN) {
        for (uint8_t i = 0; i < nbRouters; ++i) {
            if (routers[i].xbee.get_addr64() == remote.get_addr64()) {
                routers[i].pedestrian = 1;
                printf("Pedestrian id : %x\n\r", routers[i].id);
            }
        }
    } else if (data[0] == INTERRUPT) {
        for (uint8_t i = 0; i < nbRouters; ++i) {
            if (routers[i].xbee.get_addr64() == remote.get_addr64()) {
                routers[i].interrupt = 1;

                if (interrupt != NULL) {
                    interrupt->data[2] = data[1];
                    routers[i].interruptDir = data[1];
                }
                printf("Interrupt id : %x\n\r", routers[i].id);
            }
        }
    } else if (data[0] == EMERGENCY) {
        for (uint8_t i = 0; i < nbRouters; ++i) {
            if (routers[i].xbee.get_addr64() == remote.get_addr64()) {
                printf("C'Est une URGENCE!!!!!\n\r");
                emergencyDetect = 1;
            }
        }
    }
}

void discover()
{
    printf("Discovering\n\r");
    xbee.start_node_discovery();
    do {
        xbee.process_rx_frames();
        wait_ms(100);
        printf(".");
    } while(xbee.is_node_discovery_in_progress());
}

void removeRouter(uint8_t id)
{
    for (uint8_t i = id; i < nbRouters-1; ++i) {
        routers[i] = routers[i+1];
        --routers[i].id;
    }
    --nbRouters;
}

void sendInstruction(uint8_t id, uint8_t *data, uint8_t len)
{
    TxStatus txStatus = TxStatusTimeout;
    uint8_t count = 0;

    if (id >= nbRouters)
        return;

    while (txStatus != TxStatusSuccess && count < 3)  {
        txStatus = xbee.send_data(routers[id].xbee, data, len);

        if (txStatus != TxStatusSuccess) {
            printf("TXStatus: %x\n\rNON\n\r", txStatus);
            ++count;
        }
    }
    if (txStatus != TxStatusSuccess)
        removeRouter(id);

    uint8_t toSend[10], i;

    for (i = 0; i < len; ++i) {
        toSend[i] = data[i];
    }

    toSend[i] = routers[id].ni;
    toSend[++i] = '\0';

    uint8_t sended = ws->send((char*) toSend);

    if (sended == 0) {
        ws->close();
        printf("Reconnecting\n\r");
        ws->connect();
    }
}

void sendInstructionAll(uint8_t *data, uint8_t len)
{
    for (uint8_t i = 0; i < len; ++i)
        printf("Sending ALL : %x\n\r", data[i]);

    for (uint8_t i = 0; i < nbRouters; ++i) {
        sendInstruction(i, data, len);
    }
}

void nextInstruction()
{
    timeout.stop();
    timeout.reset();
    bool noBool = true;

    printf("NEXT : %x\n\r", current->data[0]);

    if (current->data[0] == EMERGENCY || current->data[0] == INTERRUPT) {
        if ( current->data[1] == lastSent->data[0] && current->data[2] == lastSent->data[1]) {
            current = current->next;
            timeout.start();
            return;
        }
    }

    if (current == lastSent) {
        current = current->next;
    } else if (current->data[0] == INTERRUPT) {
        if (current->data[1] == lastSent->data[0] && current->data[2] == lastSent->data[1]) {
            current = current->next;
            timeout.start();
            return;
        }

        for (uint8_t i = 0; i < nbRouters; ++i) {
            if (routers[i].interrupt == 1) {
                current->data[2] = routers[i].interruptDir;
                sendInstruction(routers[i].id, current->data, current->len);
                lastSent = current;
                noBool = false;
                routers[i].interrupt = 0;
            }
        }

        current = current->next;
        if (noBool) {
            nextInstruction();
        }
    } else if (current->data[0] == PEDESTRIAN) {
        for (uint8_t i = 0; i < nbRouters; ++i) {
            if (routers[i].pedestrian == 1) {
                sendInstruction(routers[i].id, current->data, current->len);
                lastSent = current;
                noBool = false;
                routers[i].pedestrian = 0;
            }
        }

        current = current->next;
        if (noBool) {
            nextInstruction();
        }
    } else {
        sendInstructionAll(current->data, current->len);
        lastSent = current;
        current = current->next;
    }
    timeout.start();
}

void instructionConstruction(uint8_t *data, uint8_t len)
{
    uint8_t i = 0;
    instruction_t *instruction;
    deleteList(&list);

    printf("Data : %x\n\r", data[0]);
    while (i < len) {

        switch (data[i]) {
            case FLASHRED:
            case PEDESTRIAN:
                instruction = addElement(&list);
                instruction->data[0] = data[i];
                instruction->len = 2;
                instruction->time = data[++i];
                instruction->data[1] = instruction->time;
                break;

            case GREEN:
            case FLASHGREEN:

                instruction = addElement(&list);
                instruction->data[0] = data[i];
                instruction->data[1] = data[++i];
                printf("Data1 : %x\n\r", instruction->data[1]);
                instruction->len = 2;
                instruction->time = data[++i];
                printf("Time : %x\n\r", instruction->time);
                break;

            case EMERGENCY:
                emergency.data[0] = data[i];
                emergency.data[1] = data[++i];
                emergency.data[2] = data[++i];
                emergency.len = 3;
                emergency.time = data[++i];
                break;

            case INTERRUPT:
                instruction = addElement(&list);
                instruction->data[0] = data[i];
                instruction->data[1] = data[++i];
                instruction->len = 3;
                instruction->time = data[++i];
                interrupt = instruction;
                printf("Doing Fine\n\r");
                break;
        }
        ++i;
    }

    closeLoop(&list);
    current = list.first;
    printf("current : data : %x\n\r", current->data[0]);
    nextInstruction();
}

bool readWebSocket(Websocket *ws, char *data)
{

    if (ws->read(data)) {
        for (uint8_t i = 0; i < strlen(data); ++i)
            printf("%x\n\r", data[i]);

        instructionConstruction((uint8_t *) data, strlen(data));

        return true;
    }
    return false;
}

void defaultData(uint8_t *data)
{
    data[0] = GREEN;
    data[1] = EAST;
    data[2] = 20;
    data[3] = INTERRUPT;
    data[4] = FLASHGREEN;
    data[5] = 20;
    data[6] = PEDESTRIAN;
    data[7] = 20;


    instructionConstruction(data, 8);
}

int main()
{
    EthernetInterface * eth = new EthernetInterface();
    eth->set_network("192.168.0.245", "255.255.255.0", "192.168.0.1");
    eth->connect();

    printf("%s\n\r", eth->get_ip_address());
    uint8_t nbTimes;

    ws = new Websocket("ws://192.168.0.230:8000/", eth);

    while (!ws->connect() && nbTimes < 100) {
        wait_ms(100);
        ++nbTimes;
    }
    nbTimes = 0;

    xbee.register_node_discovery_cb(&discovery_function);
    xbee.register_receive_cb(&receive_cb);
    xbee.init();
    xbee.set_panid(0x12);

    while (nbRouters < 1) {
        discover();
    }

    printf("nbRouters : %x\n\r", nbRouters);

    uint8_t data[80];

    list.size = 0;
    list.first = NULL;

    emergency.data[0] = EMERGENCY;
    emergency.data[1] = FLASHGREEN;
    emergency.data[2] = EAST;
    emergency.len = 3;
    emergency.time = 30;

    while(!readWebSocket(ws, (char *) data) && nbTimes < 100) {
        wait_ms(100);
        ++nbTimes;
    }

    if (nbTimes == 100) {
        defaultData(data);

    }
    nbTimes = 0;

    while (1) {

        if (nbRouters < MAXROUTERS && nbTimes > 200) {
            discover();
            printf("nbRouters : %x\n\r", nbRouters);
            nbTimes = 0;
        }

        xbee.process_rx_frames();

        if (emergencyDetect) {
            emergency.next = current->next;
            current = &emergency;
            wait_ms(100);
            nextInstruction();
            emergencyDetect = 0;
        }

        if (current != NULL) {
            if (current->time == 0) {
                if (timeout.read() > 30) {
                    readWebSocket(ws, (char *) data);
                }

                for (uint8_t i = 0; i < nbRouters; ++i) {
                    if ((routers[i].pedestrian || routers[i].interrupt) && timeout.read() > 15) {
                        nextInstruction();
                    }
                }
            } else if (lastSent->time < timeout.read()) {
                printf("Current Time : %x\n\r", lastSent->time);
                readWebSocket(ws, (char *) data);
                nextInstruction();
            }
        }
        wait_ms(100);
        ++nbTimes;
    }
}
