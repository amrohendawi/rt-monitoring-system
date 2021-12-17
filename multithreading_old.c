#include <stdio.h> 
#include <stdlib.h> 
#include <stdio.h> 
#include <unistd.h> 
#include <pthread.h> 
  
// Let us create a global variable to change it in threads 
int g = 0; 
pthread_mutex_t lock1 = PTHREAD_MUTEX_INITIALIZER, lock2 = PTHREAD_MUTEX_INITIALIZER; 
pthread_cond_t cond1 = PTHREAD_COND_INITIALIZER, cond2 = PTHREAD_COND_INITIALIZER; 
int start_signal = 0;
pthread_t tid, tid2;

pthread_attr_t tattr;
pthread_attr_t tattr2;
pthread_t inc_x_thread;
pthread_t inc_y_thread;
int ret;
int ret2;
struct sched_param param;
struct sched_param param2;
int x = 0, y = 0;

// The function to be executed by all threads 
void *myThread1(void *vargp) 
{ 
    if(start_signal){
        pthread_mutex_lock(&lock2);
        pthread_cond_wait(&cond2, &lock2); 
    }else{
        start_signal = 1;
    }
    // Store the value argument passed to this thread 
    int *myid = (int *)vargp; 
    // Let us create a static variable to observe its changes 
    static int s = 0; 
    // Change static and global variables 
    ++s; ++g; 
    // Print the argument, static and global variables 
    printf("Thread1 ID: %d, Static: %d, Global: %d\n", *myid, ++s, ++g); 
    printf("sleep....\n");
    sleep(3);
    // ret = pthread_attr_init (&tattr);
    // ret = pthread_attr_getschedparam (&tattr, &param);
    // param.sched_priority = 20;
    // ret = pthread_attr_setschedparam (&tattr, &param);
    pthread_cond_signal(&cond1);

    pthread_create(&tid, &tattr, myThread1, (void *)&tid);

}

void *myThread2(void *vargp) 
{ 
    pthread_mutex_lock(&lock1);
    pthread_cond_wait(&cond1, &lock1); 
    // Store the value argument passed to this thread 
    int *myid = (int *)vargp; 
    // Let us create a static variable to observe its changes 
    static int s = 0; 
    // Change static and global variables 
    ++s; ++g; 
    // Print the argument, static and global variables 
    printf("Thread2 ID: %d, Static: %d, Global: %d\n", *myid, ++s, ++g); 
    printf("sleep....\n");
    sleep(2);
    pthread_cond_signal(&cond2);
    pthread_create(&tid2, &tattr2, myThread2, (void *)&tid2); 

} 

int input_handler(int argc, char ** argv)
{
    if(argc == 1){
        printf("The Program should be executed as followed:")
        printf("");
    }
}

int main(int argc, char ** argv) 
{ 

    if (input_handler(argc,argv) != 0) return 0;

    /* initialized with default attributes */
    ret = pthread_attr_init (&tattr);
    /* safe to get existing scheduling param */
    ret = pthread_attr_getschedparam (&tattr, &param);
    /* set the priority; others are unchanged */
    param.sched_priority = 20;
    /* setting the new scheduling param */
    ret = pthread_attr_setschedparam (&tattr, &param);

    /* initialized with default attributes */
    ret2 = pthread_attr_init (&tattr2);
    /* safe to get existing scheduling param */
    ret2 = pthread_attr_getschedparam (&tattr2, &param2);
    /* set the priority; others are unchanged */
    param2.sched_priority = 80;
    /* setting the new scheduling param */
    ret2 = pthread_attr_setschedparam (&tattr2, &param2);


    pthread_create(&tid, &tattr, myThread1, (void *)&tid); 
    pthread_create(&tid2, &tattr2, myThread2, (void *)&tid2); 
  
    // pthread_create(&tid, &tattr, myThread1, (void *)&tid); 
    // pthread_create(&tid2, &tattr2, myThread2, (void *)&tid2); 
  
    pthread_exit(NULL); 
    return 0; 
} 