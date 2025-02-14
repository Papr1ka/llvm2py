python setup.py build
rm -r ./llvm2py/*.so
mv ./build/lib.linux-x86_64-cpython-312/llvm2py/*.so ./llvm2py
python test.py
