#!/bin/bash

rm ./llvm_python_parsing.cpython-311-x86_64-linux-gnu.so
cd build/
cmake --build .
mv ./llvm_python_parsing.cpython-311-x86_64-linux-gnu.so ../llvm_python
cd ../
python main.py
