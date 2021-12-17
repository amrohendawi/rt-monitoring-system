#include <stdio.h> 
#include <sys/types.h> 
#include <unistd.h>  
#include <stdlib.h> 
#include <errno.h>   
#include <sys/wait.h> 


int child_status;

int main() {
  for(int i=0; i<3; i++){
    pid_t pid = fork();
    if (pid == 0) {
      printf("HC: hello from child\n");
      exit(17);
    } else {
      int child_status;
      printf("HP: hello from parent\n");
      waitpid(pid, &child_status, 0);
      printf("CT: child result %d\n",
      WEXITSTATUS(child_status));
    }
    printf("Bye\n");
  }
  return 0;
}


// int children, returnStatus, t,interval;

// int main(){ 
//   pid_t child = 1;
//   for(int i=1;i<=3; i++){
//     if ((child = fork()) > 0){
//       // waitpid(child, &returnStatus, 0);  // Parent process waits here for child to terminate.
//       sleep(1);
//       // printf("%d: Parent %d\n", i,getpid());
//       waitpid(child, &returnStatus, 0);  // Parent process waits here for child to terminate.
//       if (returnStatus == 0){  // Verify child process terminated without error.  
//         printf("%d: parent working\n\n",i);
//       }
//     }
//     // if(child != 0){
//     // }
//     else if(child == 0){
//         printf("%d: Child %d, sired by %d\n", i, getpid(), getppid());
//     }
//     printf("\n-------------------\n");
//   }
// 	return 0;
// } 