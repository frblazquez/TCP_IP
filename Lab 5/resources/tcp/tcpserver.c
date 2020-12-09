/* This code is public domain
   
   Author: Nicolas Gast, 2013
   nicolas.gast@epfl.ch
 */

#include <stdio.h>      /* for printf() and fprintf() */
#include <sys/socket.h> /* for socket(), bind(), and connect() */
#include <arpa/inet.h>  /* for sockaddr_in and inet_ntoa() */
#include <stdlib.h>     /* for atoi() and exit() */
#include <string.h>     /* for memset() */
#include <unistd.h>     /* for close() */
#include <sys/wait.h>   /* for waitpid() */

#define RCVBUFSIZE 1500 /* Size of receive buffer */
#define MAXPENDING 5    /* Maximum outstanding connection requests */


void DieWithError(char *errorMessage)
{
	perror(errorMessage);
	exit(1);
}


int CreateTCPServerSocket(unsigned short port)
{
	int sock;                    /* socket to create */
	struct sockaddr_in servAddr; /* local address */

	/* Create socket for incoming connections */
	if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
		DieWithError("socket() failed");
      
	/* Construct local address structure */
	memset(&servAddr, 0, sizeof(servAddr));   /* Zero out structure */
	servAddr.sin_family = AF_INET;                /* Internet address family */
	servAddr.sin_addr.s_addr = htonl(INADDR_ANY); /* Any incoming interface */
	servAddr.sin_port = htons(port);              /* Local port */

	/* Bind to the local address */
	if (bind(sock, (struct sockaddr *) &servAddr, sizeof(servAddr)) < 0)
		DieWithError("bind() failed");

	/* Mark the socket so it will listen for incoming connections */
	if (listen(sock, MAXPENDING) < 0)
		DieWithError("listen() failed");

	return sock;
}

int AcceptTCPConnection(int servSock)
{
	int clntSock;                    /* Socket descriptor for client */
	struct sockaddr_in ClntAddr; /* Client address */
	unsigned int clntLen;            /* Length of client address data structure */

	/* Set the size of the in-out parameter */
	clntLen = sizeof(ClntAddr);
    
	/* Wait for a client to connect */
	if ((clntSock = accept(servSock, (struct sockaddr *) &ClntAddr, 
			       &clntLen)) < 0)
		DieWithError("accept() failed");
    
	/* clntSock is connected to a client! */
    
	printf("Handling client %s\n", inet_ntoa(ClntAddr.sin_addr));

	return clntSock;
}

void HandleTCPClient(int clntSocket) 
{
	char recvBuffer[RCVBUFSIZE];        /* Buffer for string */
	int recvMsgSize;                    /* Size of received message */

	do 
	{
		/* Receive message from client */
		recvMsgSize = recv(clntSocket, recvBuffer, RCVBUFSIZE, 0);
	} 
	while (recvMsgSize > 0);     /* zero indicates end of transmission */

	if (recvMsgSize < 0)
		DieWithError("recv() failed");

	close(clntSocket);    /* Close client socket */
}

int main(int argc, char *argv[])
{
	int servSock;                    /* Socket descriptor for server */
	int clntSock;                    /* Socket descriptor for client */
	unsigned short servPort;         /* Server port */
	pid_t processID;                 /* Process ID from fork() */
	unsigned int childProcCount = 0; /* Number of child processes */ 

	if (argc != 2)     /* Test for correct number of arguments */
		{
			fprintf(stderr, "Usage:  %s <Server Port>\n", argv[0]);
			exit(1);
		}

	servPort = atoi(argv[1]);  /* First arg:  local port */

	servSock = CreateTCPServerSocket(servPort);

	for (;;) 
	{ 	/* Run forever */
		clntSock = AcceptTCPConnection(servSock);
		/* Fork child process and report any errors */
		if ((processID = fork()) < 0)
			DieWithError("fork() failed");
		else if (processID == 0) {  /* If this is the child process */

			close(servSock);   /* Child closes parent socket */
			HandleTCPClient(clntSock);

			exit(0);           /* Child process terminates */
		}

		printf("with child process: %d\n", (int) processID);
		close(clntSock);       /* Parent closes child socket descriptor */
		childProcCount++;      /* Increment number of outstanding child processes */

		while (childProcCount) 
		{ /* Clean up all zombies */
			processID = waitpid((pid_t) -1, NULL, WNOHANG);  /* Non-blocking wait */
			if (processID < 0)  /* waitpid() error? */
				DieWithError("waitpid() failed");
			else if (processID == 0)  /* No zombie to wait on */
				break;
			else
				childProcCount--;  /* Cleaned up after a child */
		}
	}
	/* NOT REACHED */
}
