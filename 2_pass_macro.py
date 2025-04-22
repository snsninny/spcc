class MacroExpansion:
    # Macro Definition Table (MDT) and Macro Name Table (MNT)
    macro_table = {}

    @staticmethod
    def define_macro(lines):
        """Pass 1: Store macro definitions in the Macro Table"""
        macro_name = ""
        macro_body = []
        is_macro = False

        for line in lines:
            parts = line.split()
            
            # Identify the start of a macro definition
            if parts[0].upper() == "MACRO":
                is_macro = True
                continue
            
            # Handle macro body lines
            if is_macro:
                if parts[0].upper() == "MEND":
                    # End of the macro definition
                    MacroExpansion.macro_table[macro_name] = macro_body.copy()
                    macro_body.clear()
                    is_macro = False
                elif not macro_name:
                    # The first line after "MACRO" defines the macro name
                    macro_name = parts[0]
                else:
                    # Add remaining lines to the macro body
                    macro_body.append(line)

    @staticmethod
    def expand_macro(lines):
        """Pass 2: Expand macro invocations"""
        for line in lines:
            parts = line.split()
            
            # Skip MACRO and MEND directives in expansion phase
            if parts[0].upper() in ["MACRO", "MEND"]:
                continue
                
            # If the line is a macro invocation, expand it
            if parts[0] in MacroExpansion.macro_table:
                # Macro invocation found; expand it
                macro_body = MacroExpansion.macro_table[parts[0]]
                print(f"; Expanding macro: {parts[0]}")
                for macro_line in macro_body:
                    print(macro_line)
            else:
                # Normal instruction
                print(line)

def main():
    # Sample input program with macro definitions and invocations
    program = [
        "MACRO",
        "INCREMENT",
        "LOAD A",
        "ADD #1",
        "STORE A",
        "MEND",
        "START",
        "LOAD B",
        "INCREMENT",  # Macro invocation
        "STORE B",
        "HALT"
    ]

    print("Pass 1: Defining Macros")
    MacroExpansion.define_macro(program)
    print("Macro Table:", MacroExpansion.macro_table)
    
    print("\nPass 2: Expanding Macros")
    MacroExpansion.expand_macro(program)

if __name__ == "__main__":
    main()