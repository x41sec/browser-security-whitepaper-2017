# needs emcscripten
echo "Buiding wasmtests..."
emcc wasmtests.c -O2 -s "LEGALIZE_JS_FFI=0" -s "BINARYEN_TRAP_MODE='allow'" -s WASM=1 -s SIDE_MODULE=1 -o wasmtests.wasm
#emcc wasmtests.c -s "BINARYEN_TRAP_MODE='js'" -O0 -s WASM=1 -s SIDE_MODULE=1 -o wasmtests.wasm
