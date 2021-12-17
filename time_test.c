#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>



struct timeval start, stop;
int useconds = 0;


int main(){
    gettimeofday(&start, NULL);
    int res = 0;
    for(int volatile i=0; i<999999;i++){
        res += 1;
    }
    gettimeofday(&stop, NULL);
    useconds = (stop.tv_usec - start.tv_usec)/1000;
    printf("time taken %d\n",useconds);
    return 0;
}