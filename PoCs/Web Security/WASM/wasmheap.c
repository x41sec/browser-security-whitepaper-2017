#include <stdlib.h>

void abort() {
//	exit(1);
}

int heap_oobread() {
	char *buf = calloc(256, sizeof( char ));
	if (!buf) {
		abort();
	}
	char a = buf[256];
	free(buf);
	return a;
}

int heap_oobwrite_overflow() {
	char *buf = calloc(256, sizeof (char) );
	if (!buf) {
		abort();
	}
	memset(buf, 0x41, 5000000);
	char a = buf[0];
	free(buf);
	return a;
}

int heap_oobwrite_underflow() {
	char *buf = calloc(256, sizeof (char) );
	if (!buf) {
		abort();
	}
	char *ptr = buf;
	ptr -= 100000;
	memset(ptr, 0x41, 5000000);
	char a = buf[0];
	free(buf);
	return a;
}

int heap_uaf() {

	char *buf = malloc(256);
	memset(buf, 0x41, 256);
	free(buf);
	char *buf2 = malloc(256);
	if (!buf2) {
		abort();
	}
	memset(buf2, 0x42, 256);
	return buf[0];
}
