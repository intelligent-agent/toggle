

all: 
	gcc -o example example.c  `pkg-config clutter-1.0 --libs --cflags`
