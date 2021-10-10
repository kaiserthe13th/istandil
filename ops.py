from enum_ import Enum

Operators = Enum(
    "Int", "Float", "Plus", "Dump", "Minus", "Multiply", "Division", "Print",
    "String", "While", "Break", "If", "Else", "Match", "Enum", "Length", "EOF",
    "Duplicate", "StackLength", "Equals", "Do", "Greater", "End", "NotEqual",
    "GreaterEqual", "LesserEqual", "Lesser", "Identifier"
)