#include <gb/gb.h>
#include "hUGEDriver.h"

extern void Intro[];

void main() {
    NR52_REG = 0x80;
    NR51_REG = 0xFF;
    NR50_REG = 0x77;

    hUGE_init(Intro);
    __critical {
        add_VBL(hUGE_dosound);
    }
    while(1) __asm__("HALT");
}
