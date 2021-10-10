from warnerr import colorama, IstandilWarning
from colorama import Fore, Style

colorama.init(autoreset=True)

class StackNotEmpty(IstandilWarning):
    def __init__(self, stack, line, col, file):
        self.stack = stack
        super(StackNotEmpty, self).__init__("StackNotEmpty", "Stack is not empty by the end of program", line, col, file)
    def __str__(self):
        return f"""{Style.BRIGHT+Fore.YELLOW}[WARNING]{Fore.RESET} on Line %s, Column %d  in {repr(self.file)}
    %s:{Style.RESET_ALL} %s
    %u variable(s) left in the stack: %s""" % (
                self.line, self.column, self.type, self.cont, len(self.stack), self.stack
                )

