import re

class ThreeAddressCodeGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []
        self.operators = {'+', '-', '*', '/', '^'}
    
    def new_temp(self):
        """Generate a new temporary variable"""
        self.temp_count += 1
        return f't{self.temp_count}'
    
    def precedence(self, op):
        """Get operator precedence"""
        if op in {'^'}:
            return 4
        elif op in {'*', '/'}:
            return 3
        elif op in {'+', '-'}:
            return 2
        else:
            return 0
    
    def is_operator(self, c):
        """Check if character is an operator"""
        return c in self.operators
    
    def infix_to_postfix(self, expression):
        """Convert infix expression to postfix notation"""
        stack = []
        postfix = []
        
        i = 0
        while i < len(expression):
            c = expression[i]
            
            # Skip whitespace
            if c == ' ':
                i += 1
                continue
                
            # Handle multi-digit numbers
            if c.isdigit():
                num = c
                while i + 1 < len(expression) and expression[i+1].isdigit():
                    i += 1
                    num += expression[i]
                postfix.append(num)
            
            # Handle parentheses
            elif c == '(':
                stack.append(c)
            elif c == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()  # Remove '(' from stack
            
            # Handle operators
            elif self.is_operator(c):
                # Handle negative numbers (unary minus)
                if c == '-' and (i == 0 or expression[i-1] == '('):
                    # It's a unary minus, treat it differently
                    num = '-'
                    i += 1
                    while i < len(expression) and expression[i].isdigit():
                        num += expression[i]
                        i += 1
                    postfix.append(num)
                    continue
                
                while stack and self.precedence(stack[-1]) >= self.precedence(c):
                    postfix.append(stack.pop())
                stack.append(c)
            
            i += 1
        
        while stack:
            postfix.append(stack.pop())
        
        return postfix
    
    def generate_tac(self, expression):
        """Generate three address code from infix expression"""
        postfix = self.infix_to_postfix(expression)
        stack = []
        self.code = []
        
        for token in postfix:
            if token.replace('-', '').isdigit():  # Handle both positive and negative numbers
                stack.append(token)
            elif self.is_operator(token):
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                
                op2 = stack.pop()
                op1 = stack.pop()
                
                temp = self.new_temp()
                self.code.append(f"{temp} = {op1} {token} {op2}")
                stack.append(temp)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        
        return self.code
    
    def display_tac(self):
        """Display the generated three address code"""
        print("\nThree Address Code:")
        print("------------------")
        for line in self.code:
            print(line)
        print()

if __name__ == "__main__":
    tac_gen = ThreeAddressCodeGenerator()
    
    while True:
        print("\nThree Address Code Generator")
        print("1. Enter expression")
        print("2. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            expression = input("Enter arithmetic expression: ")
            try:
                tac_gen.generate_tac(expression)
                tac_gen.display_tac()
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
