#include <stdlib.h>
#include "wasmtests.h"

#define INT_MAX 2147483647

void main() {
	access_code();
	intover(INT_MAX);
	arg_over(INT_MAX);
	stack_oobread();
	stack_oobwrite_overflow();
	stack_oobwrite_underflow();
	//stack_recursion_overflow(size_t count, size_t stop) {
	//work();
	//hang();
	//unreachable();
}
