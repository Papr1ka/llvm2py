# llvm_python

Инструмент для работы с LLVM_IR в Python

# Установка

1. Клонирование llvm_python

`git clone git@github.com:Papr1ka/llvm_python.git`

`cd llvm_python`

2. Клонирование репозитория [pybind11](https://github.com/pybind/pybind11)

`git clone git@github.com:pybind/pybind11.git`

3. Настройка LLVM

Необходимо иметь в системе установленную библиотеку LLVM

В файле CMakeLists.txt:

Установить путь к папке с скомпилированной библиотекой LLVM

`set(LLVM_INSTALL_DIR "/home/joe/dev/llvm-project/build" CACHE PATH "LLVM installation directory")`

4. Скачать систему сборки Ninja

[Ninja](https://ninja-build.org/)

[Можно воспользоваться пакетным менеджером](https://github.com/ninja-build/ninja/wiki/Pre-built-Ninja-packages)

5. Скомпилировать

Если всё верно, можно воспользоваться скриптом complile.sh

Если в системе несколько версий Python, pybind11 может найти не ту и название библиотеки может отличаться (в поле версии).

Библиотека будет либо в корне, либо в ./build/llvm_python.{suffix}.so

На данный момент, библиотека скомпилировалась под неподходящую версию предлагается запустить main.py из под этой версии.

6. По желанию скачать requests для компиляции в GodBolt (requirements.txt)

`python -m pip install -r requirements.txt`
