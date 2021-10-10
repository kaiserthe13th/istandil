import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class IstandilError:
    def __init__(self, wtyp, wcnt, line, column, file):
        self.type = wtyp
        self.cont = wcnt
        self.line = line
        self.column = column
        self.file = file

    def __repr__(self): return "Error(%s, %s)" % (repr(self.type), repr(self.cont))
    def __str__(self): return f"{Style.BRIGHT+Fore.RED}[ERROR]{Fore.RESET} on Line %d, Column %d in {repr(self.file)}\n    %s:{Style.RESET_ALL} %s" % (self.line, self.column, self.type, self.cont)

class IstandilWarning:
    def __init__(self, wtyp, wcnt, line, column, file):
        self.type = wtyp
        self.cont = wcnt
        self.line = line
        self.column = column
        self.file = file

    def __repr__(self): return "Warning(%s, %s)" % (repr(self.type), repr(self.cont))
    def __str__(self): return f"{Style.BRIGHT+Fore.YELLOW}[WARNING]{Fore.RESET} on Line %d, Column %d in {repr(self.file)}\n    %s:{Style.RESET_ALL} %s" % (self.line, self.column, self.type, self.cont)

import SpecialWarnings
