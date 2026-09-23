#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void)
{
    pid_t pid = fork();

    if (pid < 0) {                      /* case 1: fork failed */
        perror("fork");
        return EXIT_FAILURE;
    }

    if (pid == 0) {                     /* case 2: we are the child */
        char *argv[] = { "ls", "-l", NULL };
        execvp("ls", argv);
        /* only reached if execvp failed: the image was never replaced */
        perror("execvp");
        _exit(127);
    }

    /* case 3: we are the parent, pid holds the child's pid */
    int status;
    if (waitpid(pid, &status, 0) < 0) {
        perror("waitpid");
        return EXIT_FAILURE;
    }

    if (WIFEXITED(status))
        printf("parent: child %d exited with status %d\n",
               (int) pid, WEXITSTATUS(status));
    else if (WIFSIGNALED(status))
        printf("parent: child %d killed by signal %d\n",
               (int) pid, WTERMSIG(status));

    return EXIT_SUCCESS;
}
