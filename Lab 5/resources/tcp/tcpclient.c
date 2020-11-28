/* This code is public domain
   
   Authors: Nicolas Gast, 2013
   nicolas.gast@epfl.ch
   
   Jean-Yves Le Boudec, 2019
   jean-yves.leboudec@epfl.ch
   
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/time.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <strings.h>
#include <netinet/tcp.h>
#include <sys/ioctl.h>

#include <errno.h>
       
extern int errno;

#define BUF_SIZE 1000
#define	MICROSEC 1000000
#define MILLISECOND 1000.0
#define KILO 1000.0
#define BYTE 8.0
#define DEADTIME 1.0          // seconds
#define SLOW_START_DELAY 5.0
#define ALPHA 0.1

double get_time() {
  struct timeval t;
  gettimeofday(&t, 0);
  return t.tv_sec + (double) t.tv_usec / MICROSEC;
}

int main(int argc, char **argv) {
  char *dst_name;
  struct hostent *dst_ptr;
  struct sockaddr_in dst_addr;
  
  short port;
  int sockfd;
  char data_buf[BUF_SIZE];
  int i; for (i=0;i<BUF_SIZE;i++) data_buf[i]=0; 
  
  struct tcp_info info;
  socklen_t info_len = sizeof(struct tcp_info);
  
  unsigned int prev_cwnd = 0;
  
  if (argc < 3) {
    fprintf(stderr, "Usage: %s <dst address> <port>\n", argv[0]);
    exit(1);
  } else {
    dst_name = argv[1];
    port = atoi(argv[2]);
  }
  
  if ((dst_ptr = gethostbyname(dst_name)) == 0) {
    perror ("gethostbyname");
    exit(1);
  }
  bcopy(dst_ptr->h_addr, (char *)&dst_addr.sin_addr, dst_ptr->h_length);
  dst_addr.sin_family = AF_INET ;
  dst_addr.sin_port = htons(port) ;
  
  /* create socket */
  if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
    perror ("socket");
    exit(1);
  }
  
  /* connect to destination */
  if (connect(sockfd, (struct sockaddr *)&dst_addr, sizeof(dst_addr)) < 0){
    perror("connect error");
    close(sockfd);
    exit(1);
  }
  
  double now, prev_time, start_time;
  int bytes_written = 0;
  double rate = 0, cr = 0, total_rate=0;
  double total_bytes_written = 0;
  int buffer_size = 0;
  
  
  // First, we set the timeout to 0.1 second. 
  struct timeval tv; tv.tv_sec=1; tv.tv_usec = 0; 
  setsockopt(sockfd, SOL_SOCKET, SO_SNDTIMEO, (char*)&tv, sizeof(tv) );	

  start_time = prev_time = get_time();
  
  /* infinite loop for sending packets */
  for (;;) 
    {
      int n = write(sockfd, data_buf, BUF_SIZE);
      if (n <= 0) {
	     if (!(errno == EWOULDBLOCK) ) { // if error is not caused by TIMEOUT, we die.
	        perror("tcp: write error");
	        exit(1);
      	    }
      }
      bytes_written += n;
      total_bytes_written += n;
      
      now = get_time();
      
      getsockopt(sockfd, SOL_TCP, TCP_INFO, (void *) &info, &info_len);
      if (info.tcpi_snd_cwnd != prev_cwnd || now - prev_time >= DEADTIME) 
	     {
	       if (now - prev_time >= DEADTIME) 
	         {
	          int current_buffer_size; 
	          ioctl(sockfd, TIOCOUTQ, &current_buffer_size);
	          cr = (double) (bytes_written-current_buffer_size+buffer_size) * BYTE / KILO / (now - prev_time);
	          total_rate = (double) (total_bytes_written-current_buffer_size) * BYTE / KILO / (now - start_time);
	          buffer_size = current_buffer_size;
	          /* ignore slowstart in EWMA */
	          if (now - start_time < SLOW_START_DELAY) rate = cr;
	          else                        rate = (1.0 - ALPHA) * rate + ALPHA * cr;
	          prev_time = now;
	          bytes_written = 0;
	         }
	       //else 

              printf("%5.1f:%8.1fkb/s avg (%7.1f[inst],%7.1f[mov.avg]) cwnd %2i rtt%5.1fms\n",
		      now - start_time, 
		      total_rate, cr, rate, info.tcpi_snd_cwnd,
		      info.tcpi_rtt/MILLISECOND);
             // }
           prev_cwnd = info.tcpi_snd_cwnd;   
	     }
    }
  
  close (sockfd);
  return 0;
}
