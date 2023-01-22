GBDK = ../../gbdk
GBDKLIB = $(GBDK)/lib/small/asxxxx
CC = $(GBDK)/bin/lcc
SDAR = $(GBDK)/bin/sdar

RRGBDS = tools
RGBASM = $(RRGBDS)/rgbasm
RGB2SDAS = python tools/rgb2sdas.py

BUILD_DIR = ./build
OBJ_DIR = ./obj

CVTFLAGS = -b 0

TARGET = $(BUILD_DIR)/hUGEDriver.lib
OBJS = $(OBJ_DIR)/hUGEDriver.o

all: directories $(TARGET)

directories: $(BUILD_DIR) $(OBJ_DIR)

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(OBJ_DIR)/%.obj:	%.asm
	$(RGBASM) -DGBDK -o$@ $<

$(OBJ_DIR)/%.o:	$(OBJ_DIR)/%.obj
	$(RGB2SDAS) $(CVTFLAGS) -o$@ $<

$(TARGET): $(OBJS)
	$(SDAR) -ru $@ $^

clean:
	@echo "CLEANUP..."
	rm -rf $(OBJ_DIR)
	rm -rf $(BUILD_DIR)
