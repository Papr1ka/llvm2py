#!/bin/bash

rm ./llvm_python.cpython-311-x86_64-linux-gnu.so
cd build/
cmake --build .
mv ./llvm_python.cpython-311-x86_64-linux-gnu.so ../
cd ../
python main.py
