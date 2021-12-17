#include <pthread.h>
#include <sched.h>
#include <stdlib.h>
#include <stdio.h>

void *inc_x(void *x_void_ptr)
{
    /* increment x to 100 */
    int *x_ptr = (int *)x_void_ptr;
    while(++(*x_ptr) < 100);

    printf("x increment finished\n");

    /* the function must return something - NULL will do */
    return NULL;
}

// void *tast(void *){

// }

int main()
{


    pthread_attr_t tattr;
    pthread_attr_t tattr2;
    pthread_t inc_x_thread;
    pthread_t inc_y_thread;
    int ret;
    int ret2;
    struct sched_param param;
    struct sched_param param2;
    int x = 0, y = 0;

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


    /* show the initial values of x and y */
    printf("x: %d, y: %d\n", x, y);

    /* this variable is our reference to the second thread */

    /* create a second thread which executes inc_x(&x) */
    if(pthread_create(&inc_x_thread, &tattr, inc_x, &x)) {
        fprintf(stderr, "Error creating thread\n");
        return 1;
    }
    if(pthread_create(&inc_y_thread, &tattr2, inc_x, &y)) {
        fprintf(stderr, "Error creating thread\n");
        return 1;
    }

    printf("y increment finished\n");

    /* wait for the second thread to finish */
    if(pthread_join(inc_x_thread, NULL)) {

    fprintf(stderr, "Error joining thread\n");
    return 2;

    }

    /* show the results - x is now 100 thanks to the second thread */
    printf("x: %d, y: %d\n", x, y);

    return 0;

}

