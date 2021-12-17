#define _GNU_SOURCE
#include <stdio.h> 
#include <stdlib.h> 
#include <stdio.h> 
#include <unistd.h> 
#include <pthread.h>
#include <sched.h>
#include <string.h>
#include <sys/time.h>               // get time in microseconds
#include <sys/sysinfo.h>            // to get number of CPU cores
#include <signal.h>
#include <assert.h>
#include <sched.h>
#include <stdbool.h>

#define MAX_CORES 8
#ifndef AGGRIGATOR
#define	AGGRIGATOR 1
#define FORWARDER  0

// struct arg_struct {
//     int cpu;
//     int *latency_array;
// }args;


/* thread parameters */
pthread_mutex_t lock1 = PTHREAD_MUTEX_INITIALIZER; 
pthread_cond_t cond1 = PTHREAD_COND_INITIALIZER; 
pthread_t tid, tid2;
struct sched_param param;
pthread_attr_t tattr;
int ret;

/* latencybench parameters */
int cpu_numb = 0;
unsigned int priority=90,duration=5;
unsigned int latency_array_size = 100;
int ** latency_array;

/* pointer where output file will be stored */
FILE *fp;

int turn = AGGRIGATOR;

void exit_handler(){
    printf("CTRL + C pressed \n exiting..\n");
    free(latency_array);
    exit(0);

}

void initialize_array(void){
    latency_array = malloc((cpu_numb+2)*sizeof(int *));
    for(int i=0; i<cpu_numb+2; i++){
        latency_array[i] = malloc(latency_array_size*sizeof(int));
    }
}

void write_output(void){
    if((fp=fopen("histogram.txt", "w"))==NULL) {
        printf("Cannot open file.\n");
    }
    printf("latency array has:\n");
    for(int i=0; i<100; i++){
        printf("array %d:\t",i);
        fprintf(fp,"%05d\t",i);
        for(int x=0; x<cpu_numb; x++){
            printf("%d\t",latency_array[x][i]);
            fprintf(fp,"%04d\t",latency_array[x][i]);
        }
        fprintf(fp,"\n");
        printf("\n");
    }
    fclose(fp);
}

void *task(void *vargp){
    struct timeval start, stop;
    int time_taken = 0;
    int res = 0;
    int *x = (int *) vargp;
    gettimeofday(&start, NULL);
    for(int i=0; i<999999;i++){
        res += 1;
    }
    gettimeofday(&stop, NULL);
    time_taken = (stop.tv_usec - start.tv_usec)/1000;
    if(time_taken < latency_array_size)
        latency_array[*x][time_taken]++;
}

void aggregator(void) 
{     
    for(int cpu=0; cpu<cpu_numb; cpu++){
        printf("running for core %d\n",cpu);
        cpu_set_t my_set;        /* Define your cpu_set bit mask. */
        CPU_ZERO(&my_set);       /* Initialize it all to 0, i.e. no CPUs selected. */
        CPU_SET(cpu, &my_set);     /* set the bit that represents core 7. */
        ret = pthread_attr_init (&tattr);
        ret = pthread_attr_getschedparam (&tattr, &param);
        param.sched_priority = priority;
        ret = pthread_attr_setschedparam (&tattr, &param);

        for(int j=0; j<1000; j++){
            sched_setaffinity(tid, sizeof(cpu_set_t), &my_set); /* Set affinity of tihs process to */
            pthread_create(&tid, &tattr, task, (void *)&cpu);
        }
    }

    write_output();
}

void data_sender(void) 
{ 
    printf("data_sender: working\n");
    system("python3 data_sender.py");
    printf("sleep....\n");
    sleep(1);
} 

int input_handler(int argc, char ** argv)
{
    if(argc>1 && !strcmp(argv[1],"--help")){
        printf("The Program should be called as following:\n");
        printf("./data_source -p[priority (80-95)] , -d[duration in minutes] , -l[latency interval]\n");
	    return -1;
    }
    else if(argc > 1)
    {
        for(int i=1; i<argc; i++){
            if(argv[i][0] == '-' && argv[i][1] == 'p')
                priority = (unsigned int) atoi(argv[i]+2);
            else if(argv[i][0] == '-' && argv[i][1] == 'd')
                duration = (unsigned int) atoi(argv[i]+2);
            else if(argv[i][0] == '-' && argv[i][1] == 'l')
                latency_array_size = (unsigned int) atoi(argv[i]+2);
        }
    }

    printf("priority is set to priority [%d]  latency_array_size [%d]  duration [%d] seconds\n",priority,duration,latency_array_size);
    return 0;
}

int main(int argc, char ** argv) 
{ 

    if (input_handler(argc,argv) != 0) return 0;
    signal(SIGINT, exit_handler);
    printf("This system has %d processors configured and %d processors available.\n",
    get_nprocs_conf(), get_nprocs());
    cpu_numb = get_nprocs();

    initialize_array();

    for(int i=0; i<latency_array_size; i++){
        for(int x=0; x<cpu_numb+2; x++){
            latency_array[x][i] = 0;
        }
    }
    aggregator();
    printf("sleep....\n");
    sleep(1);
    data_sender();

    free(latency_array);
    return 0; 
} 


#endif