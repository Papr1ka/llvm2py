# llvm_python

Инструмент для анализа LLVM_IR в Python

# Установка

0. В системе необходимо иметь установленный cmake

1. Клонирование llvm_python

`git clone git@github.com:Papr1ka/llvm_python.git`

`cd llvm_python`

2. Клонирование репозитория [pybind11](https://github.com/pybind/pybind11)

`git clone git@github.com:pybind/pybind11.git`

Он необходим для компиляции модуля

3. Настройка LLVM

Необходимо иметь в системе установленную библиотеку LLVM

Сделать это можно через пакетный менеджер дистрибутива

Пример:

`sudo dnf install llvm`
`sudo dnf install llvm-devel`

Также можно собрать вручную

По умолчанию поиск libllvm.so будет происходить в /usl/bin

Папку с этим файлом можно указать в переменной окружения

`LLVM_INSTALL_DIR=../llvm-project/build`

Полезным может оказаться страница https://apt.llvm.org/

4. Запустить setup.py

`python setup.py install`
