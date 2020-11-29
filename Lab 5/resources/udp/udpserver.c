/* This code is public domain
   
   Authors: Nicolas Gast, 2013
   nicolas.gast@epfl.ch
   
   Jean-Yves Le Boudec, 2019
   jean-yves.leboudec@epfl.ch
 */

#include <stdio.h>      /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket(), bind(), and connect() */
#include <arpa/inet.h>  /* for sockaddr_in and inet_ntoa() */
#include <stdlib.h>     /* for atoi() and exit() */
#include <string.h>     /* for memset() */
#include <unistd.h>     /* for close() */
//#include <sys/wait.h>   /* for waitpid() */

#include <sys/time.h> // gettimeofday

#define PACKETSIZE 1000 /* Size of receive buffer */
#define TEN_TO_6 1000000

int max(int a, int b){
  return  a>b?a:b;
}

void dieWithError(char *errorMessage)
{
  perror(errorMessage);
  exit(1);
}

void  dieCauseMultipleClients(){
  printf("\n%s\n%s\n%s\n%s\n%s\n%s\n", 
	 "###################################################",
	 "##  Error: more packets were received than sent  ##",
	 "###################################################",
	 "For the test with UDP in this lab, you need to run ONE SERVER PER CLIENT",
	 "  i.e.: two clients requires two servers!!!", 
	 "Exiting... "); 
  exit(2);
}


double get_time() {
  struct timeval t;
  gettimeofday(&t, 0);
  return t.tv_sec + (double) t.tv_usec / TEN_TO_6;
}

int main(int argc, char *argv[])
{
  unsigned short port;         /* Server port */
  
  if (argc != 2)     /* Test for correct number of arguments */
    {
      fprintf(stderr, "Usage:  %s <Server Port>\n", argv[0]);
      exit(1);
    }
  
  port = atoi(argv[1]);  /* First arg:  local port */
  
  int sock;                                 /* socket to create */
  struct sockaddr_in servAddr; /* local address */
  struct sockaddr_in clientAddr; /* address of client */
  socklen_t addrlen = sizeof(clientAddr); 
  
  /* Create socket for incoming connections */
  if ((sock = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0)
    dieWithError("socket() failed");
  
  /* Construct local address structure */
  memset(&servAddr, 0, sizeof(servAddr));   /* Zero out structure */
  servAddr.sin_family = AF_INET;                /* Internet address family */
  servAddr.sin_addr.s_addr = htonl(INADDR_ANY); /* Any incoming interface */
  servAddr.sin_port = htons(port);              /* Local port */
  
  /* Bind to the local address */
  if (bind(sock, (struct sockaddr *) &servAddr, sizeof(servAddr)) < 0)
    dieWithError("bind() failed");
  
  int recv_len; char buf[PACKETSIZE];
  double start_time = get_time();
  double time = get_time();
  int nb_packets = 0; // number of packets received
  int bytes_ack = 0; // number of bytes received
  int sent = 0;      // number of packets sent by the clients (obtained via the sequence number that client writes in the packets)

  // Infinite loop for listening
  while(1) {
    if ( (recv_len = recvfrom(sock,buf,PACKETSIZE,0,(struct sockaddr *)&clientAddr,&addrlen))<0){
      dieWithError("recvfrom()");
    }
    // For each received packet:
    if (buf[0]==0) {
      /* If the packet starts with 0, this means that this was the
         last packet sent by this client. In that case, we print a
         summary, reset the counters and send an ack to the client */
      if(sent>0) {
	    printf("packets received: %d out of %d ; loss = %2.3f%% \n", nb_packets, sent, 100*(1-((double)nb_packets)/sent));
        }
      sendto(sock, buf, PACKETSIZE,0,(const struct sockaddr*)&clientAddr,addrlen);
      nb_packets = 0;
      sent = 0;
      }
    else{
      /* If the packet does not start with 0, then the packet contains
	 an integer that corresponds to its number (the first packet
	 sent by the client has number 1, then 2, etc...) */
      sent = max( sent, atoi(buf) ); 
      nb_packets ++;
      if (nb_packets > sent) dieCauseMultipleClients(); // If we received more packets that the sequence number, there is a problem. In that case, we print a message and die. 
      bytes_ack += recv_len;
      if (get_time() >= time+1){
	   // We print a summary every second
	   printf("%5.1fs - received:%6d out of %6d pkts (loss%7.3f%%),%7.1f kb/s\n", 
	       time-start_time, nb_packets, sent, 100*(1-((double)nb_packets)/sent),
	       bytes_ack / (get_time()-time)*8/1000);
	   bytes_ack = 0;
	   time = get_time();
       }
    }
  }
  close(sock);
  exit(0);
  
}
