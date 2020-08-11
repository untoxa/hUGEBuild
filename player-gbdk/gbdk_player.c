#include <gb/gb.h>
#include "hUGEDriver.h"

void main() {
    NR52_REG = 0x80;
    init_driver();
    __critical {
        add_VBL(dosound);
    }
    while(1) __asm__("HALT");
}
