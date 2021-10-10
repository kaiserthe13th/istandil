from ops import Operators
from warnerr import IstandilError
import re

def lex(file, prog):
    def fit_ident_standarts(ch, first=False):
        if not first and re.match(r'[a-zA-Z0-9_]', ch):
            return True
        elif first and re.match(r'[a-zA-Z_]', ch):
            return True
        return False
    def peek(n: int = 0):
        return prog[cr+n]
    rl = []
    cr: int = 0
    proglen = len(prog)
    enc_err, enc_warn = [], []
    line = 1
    col = 1
    while proglen > cr:
        if peek() in ("'", '"'):
            tmpi = 1
            try:
                while peek(tmpi) != peek():
                    tmpi += 1
            except IndexError:
                enc_err.append(
                    IstandilError("SyntaxError",
                        f"String literal({peek()}) not finished", line, col, file
                    ))
            rl.append([file, [Operators.String, prog[cr+1:cr+tmpi]], line, col])
            cr = cr+tmpi+1
            col += 1
        elif peek() == '-' and peek(1) == '*':
            tmpi = 2
            try:
                while peek(tmpi) != '*' and peek(tmpi+1) != '-':
                    tmpi += 1
            except IndexError:
                enc_err.append(IstandilError("SyntaxError", "Comment not finished", line, col, file))
            cr = cr+tmpi+2
            col += 1
        elif peek() == '\n':
            line += 1
            col = 1
            cr += 1
        elif peek().isnumeric():
            tmpi = 0
            dot_used = False
            dot_errd = False
            while cr+tmpi+1 < proglen and (peek(tmpi).isnumeric() or peek(tmpi) in ('.', '_')):
                if peek(tmpi) == '.':
                    if dot_used:
                        dot_errd = True
                        enc_err.append(
                            IstandilError("SyntaxError",
                                "Extra dot detected in Float", line, col, file
                            ))
                    dot_used = True
                tmpi += 1
            if dot_used and not dot_errd:
                rl.append([file, [Operators.Float, float(prog[cr:cr+tmpi])], line, col])
            elif dot_errd: rl.append([file, [Operators.Float, 0.0], line, col])
            else: rl.append([file, [Operators.Int, int(prog[cr:cr+tmpi])], line, col])
            cr += tmpi + 1
        elif peek() == "+":
            rl.append([file, [Operators.Plus], line, col])
            cr += 1
        elif peek() == "-":
            rl.append([file, [Operators.Minus], line, col])
            cr += 1
        elif peek() == "*":
            rl.append([file, [Operators.Multiply], line, col])
            cr += 1
        elif peek() == "/":
            rl.append([file, [Operators.Division], line, col])
            cr += 1
        elif peek() == "=":
            rl.append([file, [Operators.Equals], line, col])
            cr += 1
        elif peek() == "<":
            rl.append([file, [Operators.Lesser], line, col])
            cr += 1
        elif peek() == ">":
            rl.append([file, [Operators.Greater], line, col])
            cr += 1
        elif peek() == "!" and peek(1) == "=":
            rl.append([file, [Operators.NotEqual], line, col])
            cr += 2
        elif peek().isspace():
            cr += 1
            col += 1
        else:
            tmpi = 0
            try:
                while fit_ident_standarts(peek(tmpi)):
                    tmpi += 1
            except IndexError: pass
            tmps = prog[cr:cr+tmpi]
            if tmps == "print": rl.append([file, [Operators.Print], line, col])
            elif tmps == "dump": rl.append([file, [Operators.Dump], line, col])
            elif tmps == "while": rl.append([file, [Operators.While], line, col])
            elif tmps == "break": rl.append([file, [Operators.Break], line, col])
            elif tmps == "if": rl.append([file, [Operators.If], line, col])
            elif tmps == "else": rl.append([file, [Operators.Else], line, col])
            elif tmps == "match": rl.append([file, [Operators.Match], line, col])
            elif tmps == "enum": rl.append([file, [Operators.Enum], line, col])
            elif tmps == "end": rl.append([file, [Operators.End], line, col])
            elif tmps == "len": rl.append([file, [Operators.Length], line, col])
            elif tmps == "dup": rl.append([file, [Operators.Duplicate], line, col])
            elif tmps == "do": rl.append([file, [Operators.Do], line, col])
            elif tmps == "enum": rl.append([file, [Operators.Enum], line, col])
            elif tmps == "stacklen": rl.append([file, [Operators.StackLength], line, col])
            else: rl.append([file, [Operators.Identifier, tmps], line, col])
            cr += tmpi
    return {
        "l":rl,
        "errs": enc_err,
        "warns": enc_warn
        }