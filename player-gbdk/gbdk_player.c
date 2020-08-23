#include <gb/gb.h>
#include "hUGEDriver.h"

extern void Intro[];

UBYTE joy;
UBYTE c0 = 0, c1 = 0, c2 = 0, c3 = 0;

void main() {
    NR52_REG = 0x80;
    NR51_REG = 0xFF;
    NR50_REG = 0x77;

    hUGE_init(Intro);
    __critical {
        add_VBL(hUGE_dosound);
    }
    while(1) {
        wait_vbl_done();
        joy = joypad();
        switch (joy) {
            case J_UP    : c0 ^= 1; hUGE_mute_channel(0, c0); waitpadup(); break;
            case J_DOWN  : c1 ^= 1; hUGE_mute_channel(1, c1); waitpadup(); break;
            case J_LEFT  : c2 ^= 1; hUGE_mute_channel(2, c2); waitpadup(); break;
            case J_RIGHT : c3 ^= 1; hUGE_mute_channel(3, c3); waitpadup(); break;
        }
    }
}
