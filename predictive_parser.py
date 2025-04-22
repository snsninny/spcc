from collections import defaultdict
import pandas as pd
from tabulate import tabulate

def compute_first(symbol, productions, first_sets):
    if symbol in first_sets:
        return first_sets[symbol]
    first = set()
    if not symbol.isupper():  # Terminal
        first.add(symbol)
    else:
        for prod in productions[symbol]:
            if prod == 'ε':  # Epsilon production
                first.add('ε')
            else:
                for char in prod:
                    char_first = compute_first(char, productions, first_sets)
                    first.update(char_first - {'ε'})
                    if 'ε' not in char_first:
                        break
                else:
                    first.add('ε')
    first_sets[symbol] = first
    return first

# Function to compute FOLLOW set
def compute_follow(symbol, productions, first_sets, follow_sets, start_symbol):
    if symbol == start_symbol:
        follow_sets[symbol].add('$')
    for lhs, rhs_list in productions.items():
        for rhs in rhs_list:
            for i, char in enumerate(rhs):
                if char == symbol:
                    follow_substring = rhs[i + 1:]
                    if follow_substring:
                        first_next = set()
                        for next_char in follow_substring:
                            first_next.update(compute_first(next_char, productions, first_sets) - {'ε'})
                            if 'ε' not in compute_first(next_char, productions, first_sets):
                                break
                        else:
                            first_next.update(follow_sets[lhs])
                        follow_sets[symbol].update(first_next)
                    else:
                        follow_sets[symbol].update(follow_sets[lhs])
    return follow_sets

# Function to create LL(1) Parsing Table
def create_parsing_table(productions, first_sets, follow_sets):
    table = defaultdict(dict)
    for lhs, rhs_list in productions.items():
        for rhs in rhs_list:
            first_rhs = set()
            for char in rhs:
                first_rhs.update(compute_first(char, productions, first_sets) - {'ε'})
                if 'ε' not in compute_first(char, productions, first_sets):
                    break
            else:
                first_rhs.add('ε')
                first_rhs.update(follow_sets[lhs])
            for terminal in first_rhs:
                table[lhs][terminal] = f"{lhs}->{rhs}"
    return table

def main():
    productions = defaultdict(list)
    n = int(input("Enter number of productions: "))
    for _ in range(n):
        lhs, rhs = input("Enter production (e.g., S->AB|a): ").split("->")
        productions[lhs.strip()].extend(map(str.strip, rhs.split("|")))
    
    start_symbol = list(productions.keys())[0]
    first_sets = {}
    follow_sets = defaultdict(set)
    
    for non_terminal in productions:
        compute_first(non_terminal, productions, first_sets)
    for non_terminal in productions:
        compute_follow(non_terminal, productions, first_sets, follow_sets, start_symbol)
    
    parsing_table = create_parsing_table(productions, first_sets, follow_sets)
    
    # Display First and Follow sets
    print("\nFIRST and FOLLOW sets:")
    headers = ["Non-Terminal", "FIRST", "FOLLOW"]
    table_data = [(nt, first_sets[nt], follow_sets[nt]) for nt in productions.keys()]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    print("\nLL(1) Parsing Table:") # Display Parsing Table
    terminals = sorted(set(t for row in parsing_table.values() for t in row) | {'$'})  # Ensure '$' is included
    headers = ["Non-Terminal"] + terminals
    table_data = []
    for nt in productions.keys():
        row = [nt] + [parsing_table[nt].get(t, "-") for t in terminals]
        table_data.append(row)
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

if __name__ == "__main__":
    main()
