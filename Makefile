CC = gcc
PY = python3
CFLAGS = -Wall -fPIC
ASFLAGS = 
DEBUG_CFLAGS = -Wall -fPIC -g -O0
DEBUG_ASFLAGS = --64 -g

SRC_DIR = src
BUILD_DIR = build
OUTPUT = $(BUILD_DIR)/to_int_plus_one.so

ASM_OBJ = $(BUILD_DIR)/to_int.o $(BUILD_DIR)/plus_one.o
C_OBJ = $(BUILD_DIR)/converter.o
ALL_OBJ = $(ASM_OBJ) $(C_OBJ)

.PHONY: all clean run rebuild debug

all: $(OUTPUT)

$(OUTPUT): $(ALL_OBJ)
	$(CC) -shared -o $@ $^


$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/to_int.o: $(SRC_DIR)/to_int.s | $(BUILD_DIR)
	as $(ASFLAGS) -o $@ $<

$(BUILD_DIR)/plus_one.o: $(SRC_DIR)/plus_one.s | $(BUILD_DIR)
	as $(ASFLAGS) -o $@ $<

$(BUILD_DIR)/converter.o: $(SRC_DIR)/converter.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -c -o $@ $<

run: $(OUTPUT)
	$(PY) main.py

clean:
	rm -rf $(BUILD_DIR)

rebuild: clean all

debug: clean
	$(MAKE) ASFLAGS="$(DEBUG_ASFLAGS)" CFLAGS="$(DEBUG_CFLAGS)" all
