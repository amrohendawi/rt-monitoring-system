#include <stdio.h> 
#include <stdlib.h> 
#include <stdio.h> 
#include <unistd.h> 
#include <pthread.h>
#include <string.h>

#ifndef AGGRIGATOR
#define	AGGRIGATOR 1
#define FORWARDER  0

//struct sched_param param;
//pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER; 
//pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int turn = AGGRIGATOR;
unsigned int priority=95, duration=5;
char duration_str[5] = "5m";

/*
*forwards the aggrigated data to the Flask restful API*/
void forward_data(void){
	turn = AGGRIGATOR;
	printf("forwarder running\n");  
	if(system("python3 src/data_source/data_sender.py") == -1){
		perror("failed creating child process\n");
	}
	printf("sleep....\n");
	sleep(1);
}
/*
* aggrigates lanetcy measurements using cyclictest at realtime speed*/
void aggrigate_latencies(void){
	turn = FORWARDER;
	printf("Aggrigator running\n");
	char string3[70] = {0};
	snprintf(string3, 70, "sudo ./cyclictest -p%d -t -a -h9999 -q -D%s > output", priority, duration_str);
	if(system(string3) == -1){
	  perror("failed creating child process\n");
	}
	char string[82] = {0};
	snprintf(string, 82, "max=`grep \"Max Latencies\" output | tr \" \" \"\n\" | sort -n | tail -1 | sed s/^0*//`");
	if(system(string) == -1){
	  perror("failed creating child process\n");
	}
	char string2[55] = {0};
	snprintf(string2, 55, "grep -v -e \"^#\" -e \"^$\" output | tr \" \" \"\t\" >histogram");
	if(system(string2) == -1){
	  perror("failed creating child process\n");
	}
	printf("sleep....\n");
	sleep(1);
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
    if(argc>1 && !strcmp(argv[1],"--help")){
        printf("The Program is running with default values:\n");
        printf("./data_source -p[priority (95)] , -d[duration (5m)]\n");
	    return -1;
    }
    else if(argc > 1)
    {
        for(int i=1; i<argc; i++){
            if(argv[i][0] == '-' && argv[i][1] == 'p')
                priority = (unsigned int) atoi(argv[i]+2);
            else if(argv[i][0] == '-' && argv[i][1] == 'd'){
                duration = (unsigned int) atoi(argv[i]+2);
		memset(duration_str,0,strlen(duration_str));
		memcpy(duration_str,(argv[i]+2),strlen((argv[i]+2)));
	    }
            
        }
    }
    
    printf("priority is set to priority [%d] duration [%s ]\n",priority,duration_str);
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
