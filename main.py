from enum_ import Enum
from warnerr import IstandilWarning, IstandilError, SpecialWarnings

Operators = Enum(
    "true", "false", "Int", "Float", "Plus", "Dump", "Minus", "Multiply", "Division",
    "Print", "DumpAll", "Back", "Forward", "String", "While", "For", "Loop", "Break",
    "If", "Else", "Elif", "Match", "Enum", "Length", "Duplicate"
)

program = [
    (Operators.Int, 34),
    (Operators.Int, 35),
    (Operators.Plus, ),
    (Operators.Print, ),
]

def execute_program(prog):
    stack = []
    encountered_err, encountered_warn = [], []
    for i in prog:
        match i[0]:
            case Operators.Int | Operators.Float | Operators.String: stack.append(i[1])
            case Operators.Plus:
                a = stack.pop()
                b = stack.pop()
                stack.append(a+b)
            case Operators.Minus:
                a = stack.pop()
                b = stack.pop()
                stack.append(b-a)
            case Operators.Duplicate: stack.append(stack[-1])
            case Operators.Length: stack.append(len(stack.pop()))
            case Operators.DumpAll: stack = []
            case Operators.Print: print(stack.pop())
            case Operators.Dump: stack.pop()
            case Operators.true: stack.append(True)
            case Operators.false: stack.append(False)
            case _: raise NotImplemented("Unknown or Unimplemented Operator")
    if len(stack) > 0: encountered_warn.append(SpecialWarnings.StackNotEmpty(stack))
    for warn in encountered_warn: print(warn)
    for err  in  encountered_err: print(err)
    if  len(encountered_err) > 0: exit(1)

