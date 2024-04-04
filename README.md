# llvm_python

Инструмент для анализа LLVM_IR в Python

На данный момент, предполагается работа библиотеки в OS Linux.

Протестировано на Fedora 38, Python3.11, LLVM 16.

# Установка

1. Клонирование llvm_python

`git clone git@github.com:Papr1ka/llvm_python.git`

`cd llvm_python`

2. Настройка LLVM

Необходимо иметь в системе установленную библиотеку LLVM версии >= 16

Сделать это можно через пакетный менеджер дистрибутива

Пример:

`sudo dnf install llvm`

! Важно - также установить дев-версии пакета

`sudo dnf install llvm-devel`

По умолчанию поиск libllvm.so будет происходить в **/usr/bin** (Linux)

Также можно собрать вручную и указать путь через переменную окружения

`LLVM_INSTALL_DIR=../llvm-project/build`

Если .so файл не будет найден, компиляция библиотеки провалится

Полезным может оказаться страница https://apt.llvm.org/

3. Запустить setup.py

В директории самой верхней директории `./llvm_python`

`python -m pip install .`
