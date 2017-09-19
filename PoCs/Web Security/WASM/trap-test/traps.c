
/* testcases by ben smith */
int foo(int* x) {
  return x[0];
}

int bar(int x, int y) {
  return x / y;
}

// x41 testcase
//
int foo_oob1000(int* x) {
  return x[1000];
}

/* complains about missing _llvm_trap when importing
int indirect_foo() {
	return foo(0); // invalid pointer?
} */

unsigned char stack_oobread() {
        char buf[256];
        for (int i = 0; i < sizeof(buf); i++)
                buf[i] = i;
        return buf[256]; //oob
}


