#ifndef INSTRUCTION_H_
#define INSTRUCTION_H_

#include <stdint.h>
#include <stdlib.h>

typedef struct instruction_t instruction_t;
struct instruction_t {
    uint8_t data[3];
    uint8_t len;
    uint16_t time;
    instruction_t *next, *prev;
};

typedef struct instructionList instructionList;
struct instructionList {
    instruction_t *first;
    uint8_t size;
};

instruction_t* addElement(instructionList *list);
void closeLoop(instructionList *list);
void deleteList(instructionList *list);
bool operator==(const instruction_t &first, const instruction_t &second);

#endif // INSTRUCTION_H_
