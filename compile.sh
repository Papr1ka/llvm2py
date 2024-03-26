#!/bin/bash
rm "./llvm_python_parsing$(python-config --extension-suffix)"
cmake -B build -G Ninja
cd build/
cmake --build .
mv "llvm_python_parsing$(python-config --extension-suffix)" ../llvm_python
echo "Complited, You are Welcome!"
