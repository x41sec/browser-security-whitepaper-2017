#include <stdio.h>
#include <stdlib.h>

int main() {
	char buf[] = "ABCDEFG"; // some marker
	char *ptr = &buf[2];
	for (size_t i = 0; i < 0x71727374; i++) {
		//buf[sizeof(buf)-1] = i % 256;
		*ptr += i;
	}
	return buf[0]-buf[sizeof(buf)-1];
}
