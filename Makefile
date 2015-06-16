LANG=C
SHELL=bash
SOURCES=main.c
TARGET=kubius
BUILD_DIR=build/

OBJECTS=$(SOURCES:%.c=$(BUILD_DIR)%.o)

#PYTHON_VERSION=3.4m
INCLUDE_DIRS=

CC=gcc
CFLAGS= $(INCLUDE_DIRS) -O3 -march=native -std=gnu99
#LINK_FLAGS= -lm -lpython$(PYTHON_VERSION)
LINK_FLAGS=-lGL -lm -lSOIL -lglfw


TARGET_PATH=$(BUILD_DIR)$(TARGET)

.DEFAULT: all

all: $(TARGET_PATH)

$(BUILD_DIR)%.o: %.c
	$(CC) $< -c $(CFLAGS) -o $@

$(BUILD_DIR)%.e: %.c
	$(CC) $< -c $(CFLAGS) -E > $@


$(TARGET_PATH): $(OBJECTS)
	$(CC) -o $@ $(LINK_FLAGS) $(OBJECTS)

run: $(TARGET_PATH)
	$(TARGET_PATH)

livecoding:
	watch -n1 $(MAKE) run

clean:
	rm -f $(OBJECTS) $(TARGET_PATH)

.PHONY: all clean run livecoding