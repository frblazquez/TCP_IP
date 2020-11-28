CFLAGS = -W -Wall -g -O2
CC     = gcc

PROG = tcpclient tcpserver

all: $(PROG)

%: %.c 
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f *.o $(PROG) *.core core


