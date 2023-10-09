// Novi Sandlin
// 11-12-2022
// Techshell final proj CSC222

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>
#include <fcntl.h>
#include <errno.h>
#include <err.h>
#include <sys/wait.h>

#define MAX_LEN 256

struct command tokenize(char cmd[]);
struct path format_dir(char cwd_pert[]);
int execute(struct command t, char cwd[]);
int execwreds(struct command t, char cwd[], int redl[], int redr[], int lc, int rc);

// custum structs to help object returns in functions
struct command {
    int num_toks; // tokens recieved in parse of command
    char* tokens[200];
};

struct path {
    int levels; // depth of current path
    char* comps[50];
};

/* This variable is used to keep the previous command entered without
needing to return it through a function. This is because it was a last minute edition
and functions were already made. */
// static char cmd[200];

int main() {
    static char* t[200];
    static char user[] = "novisandlin";

    chdir(getenv("HOME"));

    for (;;) {
        char cwd[PATH_MAX];

        // update cwd
        getcwd(cwd, sizeof(cwd));

        // so output does not feed into next print and make infinite loop
        fflush(stdin); // have to have for single command
        fflush(stderr);

        // copy cwd for use in modified path so cwd does not change
        char* temp_cwd = (char*) malloc(sizeof(char)*strlen(cwd)+1);
        for (int k=0; cwd[k]!='\0'; ++k) {
            temp_cwd[k] = cwd[k];
        }

        // convert cwd string into path obj
        struct path f = format_dir(temp_cwd);

        // format command prompt
        if (f.levels < 2) {
            printf("%s$ ", cwd);
        } else if (!strcmp(f.comps[0], "Users") && !strcmp(f.comps[1], user) && f.levels == 2) {
            printf("~$ ");
        } else if (!strcmp(f.comps[0], "Users") && f.levels > 2) {
            printf("%s$ ", f.comps[f.levels-1]);
        } else {
            printf("%s$ ", cwd);
        }

        // get user input
        char *cmd = (char*) malloc(MAX_LEN);
        if (fgets(cmd, 200, stdin) == NULL) {
            err(1, "fgets error");
            continue;
        }
        cmd[strcspn(cmd, "\n\r")] = '\0'; // remove newline

        // convert command string to command obj
        struct command t;

        // tokenize command
        t = tokenize(cmd);

        // execute command
        if (execute(t, cwd) == -1) {
            printf("Error with execution\n");
        }
    }
}

int execute(struct command t, char cwd[]) {
    int stdinredirectindex = -1;
    int stdoutredirectindex = -1;
    char *infile = NULL;
    char *outfile = NULL;
    
    // get index of in-redirect and identify infile
    for (int g=0; g<t.num_toks; g++) {
        if (!strcmp(t.tokens[g], "<")) {
            stdinredirectindex = g;
            infile = strdup(t.tokens[g+1]);
            break;
        }
    }

    // get index of out-redirect and identify outfile
    for (int g=0; g<t.num_toks; g++) {
        if (!strcmp(t.tokens[g], ">")) {
            stdoutredirectindex = g;
            outfile = strdup(t.tokens[g+1]);
            break;
        }

    }

    // for command section of command input
    struct command r1;
    r1.num_toks = 0;


    // save stdout and stdin
    int stdoutfd = dup(1);
    int mystdin = dup(0);

    // if there are two redirects
    if (stdinredirectindex > 0 && stdoutredirectindex > 0) {
        // get command and put in r1
        for (int i=0; i<stdinredirectindex; i++) {
            r1.tokens[i] = t.tokens[i];
            r1.num_toks++;
        }

        // check if infile exists
        int acc = access(infile, F_OK);
        if (acc == -1) {
            printf("File does not exist\n");
            return 0;
        }

        // get infile save infile to stdin
        FILE* ifile = fopen(infile, "r");
        int h = dup2(fileno(ifile), 0);
        fclose(ifile);

        // get outfile and save to stdout
        FILE* ofile = fopen(outfile, "w");
        dup2(fileno(ofile), 1);
        fclose(ofile);

    } else if (stdinredirectindex == -1 && stdoutredirectindex > 0) {
        // get command
        for (int i=0; i<stdoutredirectindex; i++) {
            r1.tokens[i] = t.tokens[i];
            r1.num_toks++;
        }

        // get outfile and save to stdout
        FILE* ofile = fopen(outfile, "w");
        dup2(fileno(ofile), 1);
        fclose(ofile);
    } else if (stdinredirectindex > 0 && stdoutredirectindex == -1) {
        // get command
        for (int i=0; i<stdinredirectindex; i++) {
            r1.tokens[i] = t.tokens[i];
            r1.num_toks++;
        }

        // check if infile exists
        int acc = access(infile, F_OK);
        if (acc == -1) {
            printf("File does not exist\n");
            return 0;
        }

        // get infile and save to stdin
        FILE* ifile = fopen(infile, "r");
        int h = dup2(fileno(ifile), 0);
        fclose(ifile);
    }

    // I forgot what this does but it breaks without it. I believe it copies
    // r1 back to t but idk why that is necessary. I'm leaving it be.
    if (stdinredirectindex > 0 || stdoutredirectindex > 0) {
        t.num_toks = r1.num_toks;
        for (int i=0; i<r1.num_toks; i++) {
            t.tokens[i] = r1.tokens[i];
        }
    }

    // filter standard commands
    if (!strcmp(t.tokens[0], "cd")) {
        if (chdir(t.tokens[1]) == -1) {
            printf("%s\n", strerror(errno));
        }
    } else if (!strcmp(t.tokens[0], "pwd")) {
        printf("%s\n", cwd);
    } else if (!strcmp(t.tokens[0], "exit")) {
        exit(0);

    // if not a standard command
    } else {
        char** args = (char**) malloc((t.num_toks+1)*sizeof(char*));

        // format command array
        for (int w=0; w<t.num_toks; w++) {
            args[w] = t.tokens[w];
        }
        args[t.num_toks] = NULL;

        // fork
        if (fork() == 0) {
            // execute command
            if (execvp(t.tokens[0], args) == -1) {
                fprintf(stderr, "%s\n", strerror(errno));
                exit(1);
            }
            exit(0);
        }
        // wait on child so NO MORE FORK BOMB!!
        wait(NULL);
        free(args);
    }

    // reassign stdin stdout to original fds
    if (stdinredirectindex > 0 || stdoutredirectindex > 0) {
        dup2(stdoutfd, 1);
        dup2(mystdin, 0);
    } else if (stdoutredirectindex > 0) {
        dup2(stdoutfd, 1);
    } else if (stdinredirectindex > 0) {
        dup2(mystdin, 0);
    }

    return 0;
}

// Returns command, containing tokenized cmdline input
struct command tokenize(char cmd[]) {
    struct command t;
    t.num_toks = 0;
    char* token = strtok(cmd, " ");

    while (token != NULL) {
        t.tokens[t.num_toks++] = token;
        token = strtok(NULL, " ");
    }

    return t;
}

// Returns path, containing tokenized path and path depth
struct path format_dir(char cwd[]) {

    struct path t;
    t.levels = 0;

    char* token = strtok(cwd, "/");

    while (token != NULL) {
        t.comps[t.levels] = token;
        token = strtok(NULL, "/");
        t.levels++;
    }

    return t;
}
