import re
from enum import Enum

class TokenType(Enum):
    KEYWORD = 1
    IDENTIFIER = 2
    OPERATOR = 3
    LITERAL = 4
    PUNCTUATOR = 5
    COMMENT = 6
    PREPROCESSOR = 7
    WHITESPACE = 8

# C language keywords
KEYWORDS = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
    'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
}

# Operators
OPERATORS = {
    '+', '-', '*', '/', '%', '++', '--', '==', '!=', '>', '<', '>=', '<=', 
    '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '=', '+=', '-=', '*=', 
    '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '->', '.', '?:'
}

# Punctuators
PUNCTUATORS = {
    ',', ';', '(', ')', '{', '}', '[', ']', '#', '\\'
}

# Regular expressions for token patterns
TOKEN_PATTERNS = [
    (TokenType.COMMENT, r'//.*?$|/\*.*?\*/', re.DOTALL),
    (TokenType.PREPROCESSOR, r'^#.*?$', re.MULTILINE),
    (TokenType.LITERAL, r'\d+\.\d+|\d+|".*?"|\'.*?\''),
    (TokenType.OPERATOR, r'[+\-*/%=&|^<>!]+\=?|&&|\|\||<<|>>|->|\.|\?\:'),
    (TokenType.PUNCTUATOR, r'[(),;{}\[\]\\#]'),
    (TokenType.IDENTIFIER, r'[a-zA-Z_]\w*'),
    (TokenType.WHITESPACE, r'\s+')
]

class Token:
    def __init__(self, token_type, value, line, column):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        return f"{self.type.name}({self.value}) at line {self.line}, column {self.column}"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.position = 0
    
    def tokenize(self):
        while self.position < len(self.code):
            matched = False
            
            for token_type, pattern, *flags in TOKEN_PATTERNS:
                regex = re.compile(pattern, *flags)
                match = regex.match(self.code, self.position)
                
                if match:
                    value = match.group(0)
                    
                    # Skip whitespace but track position
                    if token_type == TokenType.WHITESPACE:
                        self.update_position(value)
                        self.position = match.end()
                        matched = True
                        break
                    
                    # Special handling for keywords (they match the identifier pattern)
                    if token_type == TokenType.IDENTIFIER and value in KEYWORDS:
                        token_type = TokenType.KEYWORD
                    
                    # Create token
                    token = Token(token_type, value, self.current_line, self.current_column)
                    self.tokens.append(token)
                    
                    # Update position
                    self.update_position(value)
                    self.position = match.end()
                    matched = True
                    break
            
            if not matched:
                raise ValueError(f"Unexpected character '{self.code[self.position]}' at line {self.current_line}, column {self.current_column}")
        
        return self.tokens
    
    def update_position(self, text):
        lines = text.split('\n')
        if len(lines) > 1:
            self.current_line += len(lines) - 1
            self.current_column = len(lines[-1]) + 1
        else:
            self.current_column += len(text)

def print_tokens(tokens):
    for token in tokens:
        if token.type != TokenType.WHITESPACE:
            print(token)

if __name__ == "__main__":
    # Example C code to tokenize
    c_code = """
    int main() {
        int x = 10 + 5;
        printf("Hello, World!\\n");
        return 0;
    }
    """
    
    lexer = Lexer(c_code)
    tokens = lexer.tokenize()
    print_tokens(tokens)