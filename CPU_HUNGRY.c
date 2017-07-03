#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
void main(int argc, char *argv[])
{
int i, interval;
interval=atoi(argv[1]);
while(1){
	for (i=0; i< 10000;i++);
	usleep(interval);	
 }
}