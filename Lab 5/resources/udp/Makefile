CFLAGS = -W -Wall -g -O2
CC     = gcc

PROG = udpclient udpserver

all: $(PROG)

%: %.c 
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(PROG) *.core core
