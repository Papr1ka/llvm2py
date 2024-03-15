#!/bin/bash

cmake -B build -G Ninja
cd build/
cmake --build .
mv "llvm_python$(python-config --extension-suffix)" ../
echo "Complited, You are Welcome!"
