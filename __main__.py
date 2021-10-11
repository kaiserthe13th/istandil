#!/usr/bin/env python3
from warnerr import IstandilWarning, IstandilError, SpecialWarnings
import colorama
from colorama import Fore, Style
from ops import Operators
from lex_ import lex

colorama.init(autoreset=True)

__version__ = "0.1.0"
__release_date__ = "10 Oct 2021"

DEBUG = False

def info_print(*args, **kwargs):
    if DEBUG:
        print(f"{Style.BRIGHT+Fore.BLUE}[INFO]{Style.RESET_ALL}", *args, **kwargs)

def help_msg():
    print(f"İstandil Version {__version__} released at {__release_date__}")
    print()
    print("    isd <subcommand>")
    print()
    print("usage:")
    print("    run <FILE> [-o(<FILE>.ist)]       transpile <FILE> to [-o] and run")
    print("    transpile <FILE> [-o(<FILE>.ist)] transpile <FILE> to [-o]")
    print("    help [hdir(:)]                    get help for [hdir]")
    print("    version                           get version info")
    print("    alias <subcommmand>               get aliases for <subcommand>")

def run_from_source(src):
    with open(src, "r") as f:
        info_print("Lexing Started")
        lxd = lex(src, f.read())
        lexed = lxd["l"]
        lxerr = lxd["errs"]
        lxwarn = lxd["warns"]
    for idx, i in enumerate(lexed):
        info_print(f"lexed[{idx}]:", i)
    info_print("Executing")
    execute_program(lexed, lxerr, lxwarn)

def preprocess_program(prog):
    stack = []
    rprog = []
    for ip, [file, op, line, col] in enumerate(prog):
        if op[0] == Operators.If:
            stack.append(ip)
            rprog.append([file, [Operators.If], line, col])
        elif op[0] == Operators.Else:
            a = stack.pop()
            rprog[a][1] = [rprog[a][1][0], ip + 1]
            stack.append(ip)
            rprog.append([file, [Operators.Else], line, col])
        elif op[0] == Operators.End:
            a = stack.pop()
            rprog[a][1] = [rprog[a][1][0], ip]
            rprog.append([file, op, line, col])
        else:
            rprog.append([file, op, line, col])
    for i in rprog:
        info_print(i[1])
    return rprog + [[file, [Operators.EOF], line, col]]

def execute_program(prog, enc_err, enc_warn):
    encountered_err, encountered_warn, stack = enc_err, enc_warn, []
    prog = preprocess_program(prog)
    proglen = len(prog)
    ip = 0
    if encountered_err:
        for err in encountered_err: print(err)
        exit()

    while proglen > ip:
        file = prog[ip][0]
        op = prog[ip][1]
        line = prog[ip][2]
        col = prog[ip][3]
        if op[0] in (Operators.Int, Operators.Float, Operators.String):
            stack.append(op[1])
            ip += 1
        elif op[0] == Operators.Plus:
            a = stack.pop()
            b = stack.pop()
            stack.append(a+b)
            ip += 1
        elif op[0] == Operators.Minus:
            a = stack.pop()
            b = stack.pop()
            stack.append(b-a)
            ip += 1
        elif op[0] == Operators.Multiply:
            a = stack.pop()
            b = stack.pop()
            stack.append(a*b)
            ip += 1
        elif op[0] == Operators.If:
            if stack.pop(): ip += 1
            else: ip = op[1]
        elif op[0] == Operators.Else:
            ip = op[1]
        elif op[0] in (Operators.End, Operators.EOF): ip += 1
        elif op[0] == Operators.StackLength:
            stack.append(len(stack))
            ip += 1
        elif op[0] == Operators.Duplicate:
            stack.append(stack[-1])
            ip += 1
        elif op[0] == Operators.Length:
            stack.append(len(stack.pop()))
            ip += 1
        elif op[0] == Operators.Print:
            print(stack.pop())
            ip += 1
        elif op[0] == Operators.Dump:
            stack.pop()
            ip += 1
        elif op[0] == Operators.Division:
            a = stack.pop()
            b = stack.pop()
            stack.append(b/a)
            ip += 1
        elif op[0] == Operators.Modulus:
            a = stack.pop()
            b = stack.pop()
            stack.append(b%a)
            ip += 1
        elif op[0] == Operators.Equals:
            a = stack.pop()
            b = stack.pop()
            stack.append(a==b)
            ip += 1
        elif op[0] == Operators.NotEqual:
            a = stack.pop()
            b = stack.pop()
            stack.append(a!=b)
            ip += 1
        else: assert False, "Unknown or Unimplemented Operator: %s" % op[0]
    if len(stack) > 0: encountered_warn.append(SpecialWarnings.StackNotEmpty(stack, line, col, file))
    for warn in encountered_warn: print(warn)
    for err  in  encountered_err: print(err)
    if  len(encountered_err) > 0: exit(1)

if __name__ == "__main__":
    import sys
    argv = sys.argv
    if len(argv) < 2:
        help_msg()
    elif len(argv) == 2:
        run_from_source(argv[1])
    elif len(argv) >= 3:
        if '--debug' in argv or '-d' in argv: DEBUG = True
        run_from_source(argv[1])
