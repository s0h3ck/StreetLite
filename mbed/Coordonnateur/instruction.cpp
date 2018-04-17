#include "instruction.h"

instruction_t* addElement(instructionList *list)
{
    instruction_t *newInstruction = new instruction_t;
    instruction_t *current;

    newInstruction->next = NULL;
    newInstruction->prev = NULL;

    if (list->first == NULL) {
        list->first = newInstruction;
    } else {
        current = list->first;
        while (current->next != NULL) {
            current = current->next;
        }
        current->next = newInstruction;
        newInstruction->prev = current;
    }
    ++list->size;
    return newInstruction;
}

void closeLoop(instructionList *list)
{
    instruction_t *current = list->first;

    while (current->next != NULL) {
        current = current->next;
    }
    current->next = list->first;
    list->first->prev = current;
}

void deleteList(instructionList *list)
{
    instruction_t *current = list->first;
    instruction_t *next;
    for (uint8_t i = 0; i < list->size; ++i) {
        next = current->next;
        delete(current);
        current = next;
    }
    list->size = 0;
    list->first = NULL;
}

bool operator==(const instruction_t &first, const instruction_t &second)
{
    if (first.len == second.len) {
        for (uint8_t i = 0; i < first.len; ++i) {
            if (first.data[i] != second.data[i]) {
                return false;
            }
        }
        return true;
    }
    return false;
}