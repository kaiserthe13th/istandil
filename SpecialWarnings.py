from warnerr import colorama, IstandilWarning
from colorama import Fore, Style

colorama.init(autoreset=True)

class StackNotEmpty(IstandilWarning):
    def __init__(self, stack):
        self.stack = stack
        super(StackNotEmpty, self).__init__("StackNotEmpty", "Stack is not empty by the end of program")
    def __str__(self):
        return f"{Style.BRIGHT+Fore.YELLOW}[WARNING]{Fore.RESET} %s:{Style.RESET_ALL} %s\n%u variable(s) left in the stack: %s" % (
                self.type, self.cont, len(self.stack), self.stack
                )

