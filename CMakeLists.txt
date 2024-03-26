cmake_minimum_required(VERSION 3.27)
project(llvm_python_parsing)

#set(LLVM_INSTALL_DIR "/usr/bin" CACHE PATH "LLVM installation directory")
list(APPEND CMAKE_PREFIX_PATH "${LLVM_INSTALL_DIR}/lib/cmake/llvm/")

find_package(LLVM REQUIRED CONFIG)

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")

include_directories(${LLVM_INCLUDE_DIRS})
link_directories(${LLVM_LIBRARY_DIRS})
add_definitions(${LLVM_DEFINITIONS})

set(CMAKE_CXX_STANDARD 17 CACHE STRING "")

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall\
    -fdiagnostics-color=always")

add_subdirectory(pybind11)

pybind11_add_module(llvm_python_parsing
        src/module.cpp
        src/parser.cpp
        src/bind.cpp
)

target_include_directories(llvm_python_parsing PRIVATE include)

target_link_libraries(llvm_python_parsing PRIVATE
    LLVMCore
    LLVMIRReader
    LLVMSupport)
