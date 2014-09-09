CC=gcc
LD=gcc

EXE=generator
OBJS = $(patsubst %.c,%.o,$(wildcard *.c))

all : $(EXE)

$(EXE) : $(OBJS)
	$(LD) -o $@ $<

%.o : %.c
	$(CC) -c $< -o $@

clean:
	rm -rf *.o $(EXE)
