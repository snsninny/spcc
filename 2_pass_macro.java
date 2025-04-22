# Define the structure to store Macro Definition Table (MDT) entries
class MDT:
    def __init__(self, label, opcode, operand):
        self.lab = label
        self.opc = opcode
        self.oper = operand

def main():
    label = ""
    opcode = ""
    operand = ""
    macroname = ""
    lines = 0
    d = []

    # Open the input and output files with proper file paths using raw strings
    with open(r"C:\Users\Administrator\Desktop\MACIN.txt", "r") as f1, \
         open(r"C:\Users\Administrator\Desktop\MACOUT.txt", "w") as f2, \
         open(r"C:\Users\Administrator\Desktop\MDT.txt", "w") as f3:

        # Read the first line
        line = f1.readline()
        if not line:
            print("Input file is empty.")
            return

        label, opcode, operand = line.strip().split()

        while opcode != "END":
            if opcode == "MACRO":
                macroname = label
                label, opcode, operand = f1.readline().strip().split()
                lines = 0

                # Start reading the macro body until we encounter MEND
                while opcode != "MEND":
                    f3.write(f"{label}\t{opcode}\t{operand}\n")
                    d.append(MDT(label, opcode, operand))
                    label, opcode, operand = f1.readline().strip().split()
                    lines += 1
            elif opcode == macroname:
                print(f"Macro call detected. Expanding {macroname} ({lines} lines):")
                for i in range(lines):
                    f2.write(f"{d[i].lab}\t{d[i].opc}\t{d[i].oper}\n")
                    print(f"DLAB={d[i].lab}, DOPC={d[i].opc}, DOPER={d[i].oper}")
            else:
                f2.write(f"{label}\t{opcode}\t{operand}\n")

            # Read the next line
            line = f1.readline()
            if not line:
                break
            label, opcode, operand = line.strip().split()

        # Finally write the last line
        f2.write(f"{label}\t{opcode}\t{operand}\n")
        print("FINISHED")

if __name__ == "__main__":
    main()


I/P
MACIN.txt

CALC START 1000
SUM MACRO **
** LDA #5
** ADD #10
** sTA 2000
** MEND **
** LDA LENGTH
** COMP ZERO
** JEQ LOOP
** SUM **
LENGTH WORD S
ZERO WORD S
LOOP SUM **
** END **
    
O/P
Macro call detected. Expanding SUM (3 lines):
DLAB=**, DOPC=LDA, DOPER=#5
DLAB=**, DOPC=ADD, DOPER=#10
DLAB=**, DOPC=sTA, DOPER=2000
Macro call detected. Expanding SUM (3 lines):
DLAB=**, DOPC=LDA, DOPER=#5
DLAB=**, DOPC=ADD, DOPER=#10
DLAB=**, DOPC=sTA, DOPER=2000
FINISHED

    
MDT.TXT
**	LDA	#5
**	ADD	#10
**	sTA	2000

MACOUT.TXT

CALC	START	1000
**	LDA	LENGTH
**	COMP	ZERO
**	JEQ	LOOP
**	LDA	#5
**	ADD	#10
**	sTA	2000
LENGTH	WORD	S
ZERO	WORD	S
**	LDA	#5
**	ADD	#10
**	sTA	2000
**	END	**
