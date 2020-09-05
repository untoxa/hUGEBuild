#ifndef HUGEDRIVER_H_INCLUDE
#define HUGEDRIVER_H_INCLUDE

typedef void (*hUGERoutine_t)(unsigned char ch, unsigned char param, unsigned char tick);

typedef struct hUGESong_t {
  unsigned char tempo;
  const unsigned char * order_cnt;
  const unsigned char ** order1, ** order2, ** order3, ** order4;
  const unsigned char * duty_instruments, * wave_instruments, * noise_instruments;
  const hUGERoutine_t ** routines;
  const unsigned char * waves;
} hUGESong_t;

// initialize the driver with song data
void hUGE_init(const hUGESong_t * song);

// driver routine
void hUGE_dosound();

enum hUGE_channel_t {HT_CH1 = 0, HT_CH2, HT_CH3, HT_CH4};
enum hUGE_mute_t    {HT_CH_PLAY = 0, HT_CH_MUTE};

void hUGE_mute_channel(enum hUGE_channel_t ch, enum hUGE_mute_t mute);

#endif