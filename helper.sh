#!/bin/bash

rm ./llvm_python/_llvm_python.cpython-311-x86_64-linux-gnu.so
cd build/
cmake --build .
mv ./_llvm_python.cpython-311-x86_64-linux-gnu.so ../llvm_python
cd ../
python main.py
