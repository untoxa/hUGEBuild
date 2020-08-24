#ifndef HUGEDRIVER_H_INCLUDE
#define HUGEDRIVER_H_INCLUDE

// initialize the driver with song data
void hUGE_init(void * song);

// driver routine
void hUGE_dosound();

// mute/unmute channel; ch: is a channel number 0..3, mute: 1 to mute, 0 to unmute.
void hUGE_mute_channel(unsigned char ch, unsigned char mute);

#endif