#!/usr/bin/env python3
from warnerr import IstandilWarning, IstandilError, SpecialWarnings
import colorama
from colorama import Fore, Style
from ops import Operators
from lex_ import lex

colorama.init(autoreset=True)

__version__ = "0.1.0"
__release_date__ = "12 Oct 2021"

DEBUG = False


def info_print(*args, **kwargs):
    if DEBUG:
        print(f"{Style.BRIGHT+Fore.BLUE}[INFO]{Style.RESET_ALL}", *args, **kwargs)


def help_msg(s=""):
    helpfs = {
        "": """\
    run <FILE> [-o(<FILE>.ist)]       transpile <FILE> to [-o] and run
    transpile <FILE> [-o(<FILE>.ist)] transpile <FILE> to [-o]
    help [hdir(:)]                    get help for [hdir]
    --version                         get version info
    alias <subcommmand>               get aliases for <subcommand>""",
        "run": {
            "": "    run <FILE> [-o(<FILE>.ist)]       transpile <FILE> to [-o] and run",
            "FILE": "    run <FILE> [-o(<FILE>.ist)]       <FILE> to transpile into [-o] and run",
            "-o": "    run <FILE> [-o(<FILE>.ist)]       location to transpile to",
        },
        "transpile": {
            "": "    transpile <FILE> [-o(<FILE>.ist)] transpile <FILE> to [-o]",
            "FILE": "    transpile <FILE> [-o(<FILE>.ist)] <FILE> to transpile into [-o]",
            "-o": "    transpile <FILE> [-o(<FILE>.ist)] location to transpile to",
        },
    }
    hp = helpfs
    for i in s.split(":"):
        hp = hp[i]
    print(
        f"""İstandil Version {__version__} released at {__release_date__}

    isd <subcommand>

usage:"""
    )
    if isinstance(hp, str):
        print(hp)
    else:
        for i in hp.values():
            print(i)


def write_bytecode(prog, err, warn):
    BYT_STRG = "__isd_byt_store__/"
    import os

    if not os.path.exists(BYT_STRG):
        os.mkdir(BYT_STRG)
    with open(BYT_STRG + "byt.py", "w") as f:
        f.write(f"prog={[prog, err, warn]}")


def run_from_source(src):
    with open(src, "r") as f:
        info_print("Lexing Started")
        lxd = lex(src, f.read())
        lexed = lxd["l"]
        lxerr = lxd["errs"]
        lxwarn = lxd["warns"]
    info_print("Preprocessing")
    prog = preprocess_program(lexed)
    info_print("Executing")
    execute_program(prog, lxerr, lxwarn)


def byt_from_source(src):
    with open(src, "r") as f:
        info_print("Lexing Started")
        lxd = lex(src, f.read())
        lexed = lxd["l"]
        lxerr = lxd["errs"]
        lxwarn = lxd["warns"]
    info_print("Preprocessing")
    prog = preprocess_program(lexed)
    info_print("Writing Bytecode")
    write_bytecode(prog, lxerr, lxwarn)


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
    return rprog + [[file, [Operators.EOF], line, col]]


def execute_program(prog, enc_err, enc_warn):
    encountered_err, encountered_warn, stack = enc_err, enc_warn, []
    proglen = len(prog)
    ip = 0
    if encountered_err:
        for err in encountered_err:
            print(err)
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
            stack.append(a + b)
            ip += 1
        elif op[0] == Operators.Minus:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
            ip += 1
        elif op[0] == Operators.Multiply:
            a = stack.pop()
            b = stack.pop()
            stack.append(a * b)
            ip += 1
        elif op[0] == Operators.If:
            if stack.pop():
                ip += 1
            else:
                ip = op[1]
        elif op[0] == Operators.Else:
            ip = op[1]
        elif op[0] in (Operators.End, Operators.EOF):
            ip += 1
        elif op[0] == Operators.StackLength:
            stack.append(len(stack))
            ip += 1
        elif op[0] == Operators.Duplicate:
            stack.append(stack[-1])
            ip += 1
        elif op[0] == Operators.Length:
            stack.append(len(stack.pop()))
            ip += 1
        elif op[0] == Operators.PrintLine:
            print(stack.pop())
            ip += 1
        elif op[0] == Operators.Print:
            print(stack.pop(), end="")
            ip += 1
        elif op[0] == Operators.Dump:
            stack.pop()
            ip += 1
        elif op[0] == Operators.Division:
            a = stack.pop()
            b = stack.pop()
            stack.append(b / a)
            ip += 1
        elif op[0] == Operators.Modulus:
            a = stack.pop()
            b = stack.pop()
            stack.append(b % a)
            ip += 1
        elif op[0] == Operators.MinMin:
            stack[-1] = stack[-1] - 1
            ip += 1
        elif op[0] == Operators.PlusPlus:
            stack[-1] = stack[-1] + 1
            ip += 1
        elif op[0] == Operators.Modulus:
            a = stack.pop()
            b = stack.pop()
            stack.append(b % a)
            ip += 1
        elif op[0] == Operators.Equals:
            a = stack.pop()
            b = stack.pop()
            stack.append(a == b)
            ip += 1
        elif op[0] == Operators.NotEqual:
            a = stack.pop()
            b = stack.pop()
            stack.append(a != b)
            ip += 1
        elif op[0] == Operators.LesserEqual:
            a = stack.pop()
            b = stack.pop()
            stack.append(b <= a)
            ip += 1
        elif op[0] == Operators.GreaterEqual:
            a = stack.pop()
            b = stack.pop()
            stack.append(b >= a)
            ip += 1
        else:
            assert False, "Unknown or Unimplemented Operator: %s" % op[0]
    if len(stack) > 0:
        encountered_warn.append(SpecialWarnings.StackNotEmpty(stack, line, col, file))
    for warn in encountered_warn:
        print(warn)
    for err in encountered_err:
        print(err)
    if len(encountered_err) > 0:
        exit(1)


if __name__ == "__main__":
    import sys

    argv = sys.argv
    if len(argv) < 2:
        help_msg()
    elif len(argv) == 2:
        if argv[1] in ("help", "h", "--help", "-h"):
            help_msg()
        elif argv[1] in ["--version", "-v"]:
            print(f"İstandil Version {__version__} released at {__release_date__}")
    elif len(argv) == 3:
        if argv[1] in ("run", "r"):
            run_from_source(argv[2])
        elif argv[1] in ("transpile", "tpl"):
            byt_from_source(argv[2])
        elif argv[1] in ("help", "h", "--help", "-h"):
            help_msg(argv[2])
