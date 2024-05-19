cmake_minimum_required(VERSION 3.27)

project(llvm2py LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17 CACHE STRING "")
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_VERBOSE_MAKEFILE ON)

list(APPEND CMAKE_PREFIX_PATH "${LLVM_INSTALL_DIR}/lib/cmake/llvm/")
list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")

if(UNIX)
    # Custom path to Terminfo in manylinux28 container
    find_library(Terminfo_LIBRARIES libtinfo.so.6 PATHS /usr/lib64/)
endif(UNIX)

find_package(LLVM REQUIRED CONFIG)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")

include_directories(${LLVM_INCLUDE_DIRS})
link_directories(${LLVM_LIBRARY_DIRS})
add_definitions(${LLVM_DEFINITIONS})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall\
    -fdiagnostics-color=always")

if (WIN32)
    message(STATUS "UNIX SYSTEM DETECTED")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static -static-libgcc -static-libstdc++")
endif (WIN32)

include(GNUInstallDirs)
include(FetchContent)

FetchContent_Declare(
        pybind11
        URL https://github.com/pybind/pybind11/archive/refs/tags/v2.10.4.tar.gz
        URL_HASH SHA256=832e2f309c57da9c1e6d4542dedd34b24e4192ecb4d62f6f4866a737454c9970
)
FetchContent_MakeAvailable(pybind11)

set(python_module_name _llvm2py)

pybind11_add_module(${python_module_name}
        src/module.cpp
        src/parser.cpp
        src/bind.cpp
)

target_include_directories(${python_module_name} PRIVATE include)

target_link_libraries(${python_module_name} PRIVATE
    LLVMCore
    LLVMIRReader
    LLVMSupport
)

install(TARGETS ${python_module_name} DESTINATION .)
