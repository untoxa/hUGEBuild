#ifndef HUGEDRIVER_H_INCLUDE
#define HUGEDRIVER_H_INCLUDE

// initialize the driver with song data
void hUGE_init(void * song);

// driver routine
void hUGE_dosound();

enum hUGE_channel_t {HT_CH1 = 0, HT_CH2, HT_CH3, HT_CH4};
enum hUGE_mute_t    {HT_CH_PLAY = 0, HT_CH_MUTE};

void hUGE_mute_channel(enum hUGE_channel_t ch, enum hUGE_mute_t mute);

#endif