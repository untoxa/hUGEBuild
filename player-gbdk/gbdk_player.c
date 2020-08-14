#include <gb/gb.h>
#include "hUGEDriver.h"

void main() {
    NR52_REG = 0x80;
    NR51_REG = 0xFF;
    NR50_REG = 0x77;

    init_driver();
    __critical {
        add_VBL(dosound);
    }
    while(1) __asm__("HALT");
}
