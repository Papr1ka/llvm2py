
# Change Log

All notable changes to this project will be documented in this file.
 
## [0.1.0b] - 2025-02-18
 
### Changes

1. Added support for global variables
2. A different class is created for each type of instruction
3. Added support for attributes
4. Common attributes for global variables and functions have been moved to the new GlobalObject class
5. ListMixin, ParentMixin, CodeMixin removed
6. Classes have been simplified, though still complex
7. Classes with no inheritance and no special initialization method now inherit from NamedTuple, otherwise it is dataclass
8. Instead of inheriting from Value, classes now store it as an attribute
9. The Value class is now used to store constants up to ConstantExpression (val type will be Instruction type)
10. Simplified methods are implemented for classes (do not handle attributes).
11. The minimum supported version of python is now **3.10**
