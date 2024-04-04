from skbuild import setup
from os import environ
import platform

paths = {
    "Linux": "/usr/bin",
}


def get_llvm_path():
    env_path = environ.get("LLVM_INSTALL_DIR")
    if env_path:
        return env_path

    os = platform.system()
    path = paths.get(os)
    if path is None:
        raise ValueError("LLVM path is not defined, set the $LLVM_INSTALL_DIR environment variable.")
    return path


setup(
    name="llvm_python",
    version="0.0.1",
    description="A tool for analyzing LLVM IR in Python",
    author="Papr1ka",
    licence="MIT",
    packages=['llvm_python', 'llvm_python/ir'],
    python_requires=">=3.6",
    cmake_args=[f'-DLLVM_INSTALL_DIR:PATH={get_llvm_path()}'],
    cmake_install_dir="llvm_python"
)
