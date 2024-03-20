#!/bin/bash
rm "./llvm_python$(python-config --extension-suffix)"
cmake -B build -G Ninja
cd build/
cmake --build .
mv "llvm_python$(python-config --extension-suffix)" ../
echo "Complited, You are Welcome!"
