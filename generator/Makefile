CC=gcc
LD=gcc

CFLAGS= -g 

EXE=generator
OBJS = $(patsubst %.c,%.o,$(wildcard *.c))

all : $(EXE)

$(EXE) : $(OBJS)
	$(LD) -o $@ $<

%.o : %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf *.o $(EXE)
