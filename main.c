#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(){
	FILE *fp = fopen("/tmp/deleteme", "a");
	if (!fp) {
		return -1;
	}
	char *a = strdup("asdf");
	if (!a) {
		return -1;
	}
	fprintf(fp, "some string %s\n", a);
	fclose(fp);
	free(a);

	void *ptr = malloc(1024);
	free(ptr);

	printf("this is something too");
	return 0;
}
