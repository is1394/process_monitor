#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define max_req 500000/2 // veces que se requiere memoria
#define max_mem 1024000 //1000 KB

void main(int argc, char *argv[])
{
int i, interval;
interval=atoi(argv[1]);

void * mem_array[max_req];

for (i=0;i< max_req;i++)
{
	usleep(interval);
	mem_array[i]=malloc(max_mem);
}

for (i=0; i< max_req;i++)
	free(mem_array[i]);


}