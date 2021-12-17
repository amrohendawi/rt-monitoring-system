#include <stdio.h> 
#include <stdlib.h> 
#include <stdio.h> 
#include <unistd.h> 
#include <pthread.h>
 
#ifndef AGGRIGATOR
#define	AGGRIGATOR 1
#define FORWARDER  0

//struct sched_param param;
//pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER; 
//pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int turn = AGGRIGATOR;
unsigned int priority=0, duration=0;

/*
*forwards the aggrigated data to the Flask restful API*/
void forward_data(void){
	turn = AGGRIGATOR;
	printf("forwarder running\n");  
	system("python3 data_sender.py");
	printf("sleep....\n");
	sleep(2);
}

/*
* aggrigates lanetcy measurements using cyclictest at realtime speed*/
void aggrigate_latencies(void){
	turn = FORWARDER;
	printf("Aggrigator running\n");
	char c = 34;
	char string3[70] = {0};
	snprintf(string3, 70, "sudo cyclictest -m -Sp%d -h9999 -q -D%ds > output", priority, duration);
	system(string3);
	char string[82] = {0};
	snprintf(string, 82, "max=`grep %cMax Latencies%c output | tr %c %c %c\n%c | sort -n | tail -1 | sed s/^0*//`",c,c,c,c,c,c);
	system(string);
	char string2[55] = {0};
	snprintf(string2, 55, "grep -v -e %c^#%c -e %c^$%c output | tr %c %c %c\t%c >histogram",c,c,c,c,c,c,c,c);
	system(string2);
	printf("sleep....\n");
	sleep(2);
}

void myThread() 
{
    if(turn == AGGRIGATOR){
	aggrigate_latencies();
    }else{
	forward_data();
    }    
}

int input_handler(int argc, char ** argv)
{
    if(argc != 3){
	printf("The Program should be called as following:\n");
	printf("./data_source [priority (80-95)] [duration in minutes]\n");
	return -1;
    }
    priority = (unsigned int) atoi(argv[1]);
    duration = (unsigned int) atoi(argv[2]);
    printf("priority is set to %d duration %d\n",priority,duration);
    
    return 0;
}

int main(int argc, char ** argv) 
{ 

    if (input_handler(argc,argv) != 0) return 0;

    while(1){
	myThread();
    }
    pthread_exit(NULL); 
    return 0; 
} 

#endif
