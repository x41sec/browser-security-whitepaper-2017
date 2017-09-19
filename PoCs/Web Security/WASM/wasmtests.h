#include <stdlib.h>

char access_code() {
	// try to access ourselves
//	return *( (char *) &access_code );
	return NULL;
}

int intover(int x) {
  return x+1;
}

long arg_over(unsigned long val) {
	// checks if there was an overflow while passing val
	return val;
}

unsigned char stack_oobread() {
	char buf[256];
	for (int i = 0; i < sizeof(buf); i++)
		buf[i] = i;
	return buf[256]; //oob
}

int stack_oobwrite_overflow() {
	char buf[256] = { 0 };
	for(size_t i = 0; i < 5000000; i++) {
		buf[i] = 0x41;
	}
	return buf[0];
}

int stack_oobwrite_underflow() {
	char buf[256] = { 0 };
	char *ptr = &buf;
	ptr -= 100000;
	for(size_t i = 0; i < 5000000; i++) {
		ptr[i] = 0x41;
	}
	return buf[0];
}

int stack_recursion_overflow(size_t count, size_t stop) {

	if (count < stop) {
		return stack_recursion_overflow(++count, stop);
	} else {
	// should never be reached since it should trap
		return count;
	}
}

int unreachable() {
	while(1);
}

char work(unsigned i) {
	char buf[1000];
	for (; i > 0; i--)
		buf[i % 1000] = i;
	return buf[0];
}
int hang() {
	size_t i = 10000000;
	size_t j;
	while(--i) j = work(190000);

	return i;
}

