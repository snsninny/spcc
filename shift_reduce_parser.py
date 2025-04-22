from tabulate import tabulate
import re

class ShiftReduceParser:
    def __init__(self, grammar, start_symbol):
        self.grammar = grammar  # Grammar rules
        self.start_symbol = start_symbol  # Start symbol for validation
        self.stack = ['$']  # Stack initialization with $

    def reduce_stack(self):
        while True:
            for lhs, rhs_list in self.grammar.items():
                for rhs in rhs_list:
                    if len(self.stack) >= len(rhs) and self.stack[-len(rhs):] == rhs:
                        self.stack = self.stack[:-len(rhs)] + [lhs]
                        return f"Reduce by {lhs} → {' '.join(rhs)}"
            return None

    def parse(self, input_tokens):
        if not input_tokens:
            print("Error: No tokens to parse. Check input format.")
            return
        
        input_tokens.append('$')  # End symbol
        table = [[" ".join(self.stack), " ".join(input_tokens), "Initial"]]

        while True:
            if input_tokens:
                token = input_tokens.pop(0)
                self.stack.append(token)
                table.append([" ".join(self.stack), " ".join(input_tokens), "Shift"])
            
            while True:
                action = self.reduce_stack()
                if action:
                    table.append([" ".join(self.stack), " ".join(input_tokens), action])
                else:
                    break
            
            if self.stack == ['$', self.start_symbol] and input_tokens == ['$']:
                table.append([" ".join(self.stack), " ".join(input_tokens), "Accept"])
                print(tabulate(table, headers=["Stack", "Input", "Action"], tablefmt="grid"))
                return
            
            if not input_tokens:
                print("Error: Parsing failed. Stack did not reach valid state.")
                print(tabulate(table, headers=["Stack", "Input", "Action"], tablefmt="grid"))
                return

if __name__ == "__main__":
    grammar = {}
    num_rules = int(input("Enter number of production rules: "))
    print("Enter production rules in format: LHS -> RHS (use spaces between symbols)")
    start_symbol = None
    
    for _ in range(num_rules):
        rule = input().strip()
        lhs, rhs = rule.split("->")
        lhs = lhs.strip()
        rhs = [part.strip() for part in rhs.split()]
        if lhs in grammar:
            grammar[lhs].append(rhs)
        else:
            grammar[lhs] = [rhs]
        if start_symbol is None:
            start_symbol = lhs  # Set the first LHS as start symbol
    
    input_string = input("Enter input string: ")  # User-provided input
    tokens = re.findall(r"id\d+|[A-Za-z]+'?|\+|\*|\(|\)|\$", input_string)  # Proper tokenization
    
    if not tokens:
        print("Error: No valid tokens found in input string.")
    else:
        print("Tokens Identified:", tokens)
        parser = ShiftReduceParser(grammar, start_symbol)
        parser.parse(tokens)
