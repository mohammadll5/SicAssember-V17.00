from INPUT.DEFININGS import *
INPUT = open("INPUT/cource_file.asm", "r")
OUTPUT = open("OUTPUT/intmdte_file.mdt", "w+")
ERRORS = open("OUTPUT/errors_file.txt", "w+")

#data structure
LOCCTR = 0      
PRGLTH = 0       
SYMTAB = {}                              #key_value_dic
PRGNAME = ""     
ADDSTA = 0       
ERRCTR = 0       



  
  





line = INPUT.readline()

if line:
    if line[9:15].strip() == "START": # checks if the line starts with the word "START" at position 9 and ends at position 15
        PRGNAME = line[0:8].strip()   # get program name
        ADDSTA = int(line[16:35].strip(), 16)  # get the starting address and convert to int
        LOCCTR = ADDSTA
        OUTPUT.write(hex(LOCCTR)[2:] + " " * (10 - len(str(LOCCTR))) + line)  # write first line in outputFile

        # Continue reading
        while True:
            line = INPUT.readline()
            if not line:  # Check if there's no lines to read
                break
            operation = line[9:15].strip()

            if operation != "END" and ("." not in line):  # if not endOfFile and the line is not a comment
    
                OUTPUT.write(hex(LOCCTR)[2:] + " " * (10 - len(str(LOCCTR))) + line)  # write line to outputFile

                label = line[0:8].strip()  # get the label

                if label != "":  # Check if there's a label]
                    if label in SYMTAB:  # if the label already exist then log an error
                        ERRORS.write(ERRORLIST[2])
                        print(ERRORLIST[2])
                        ERRCTR += 1

                    else:  # if there's no errors add to the SYMTAB
                        SYMTAB[label] = hex(LOCCTR)[2:]

                if operation not in OPTAB:
                    operand = 0

                # check if operation exist in OPTAB
                if operation in OPTAB:
                    LOCCTR += 3

                elif operation == "WORD":
                    LOCCTR += 3

                elif operation == "RESB":
                    operand = line[16:35].strip()
                    LOCCTR += int(operand)

                elif operation == "BYTE":
                    operand = line[16:35].strip()

                    if operand[0] == 'X':
                        LOCCTR += int((len(operand) - 3) / 2)

                    elif operand[0] == 'C':
                        LOCCTR += int((len(operand) - 3))

                elif operation == "RESW":
                    operand = line[16:35].strip()
                    LOCCTR += 3 * int(operand)

                else:
                    ERRORS.write(ERRORLIST[3])
                    print(ERRORLIST[3])
                    ERRCTR += 1

        

            if operation == "END":
                OUTPUT.write(" " * 10 + line)

    else:
        ERRORS.write(ERRORLIST[1]) 
        print(ERRORLIST[1])

else:
    ERRORS.write(ERRORLIST[0])
    print(ERRORLIST[0])


length = int(LOCCTR) - int(ADDSTA)  # program length ( current location counter - start address)
PRGLTH = hex(int(length))[2:].format(int(length))  # program length in hexadecimal
loc = hex(int(LOCCTR))[2:].format(int(LOCCTR))  # location counter in hexadecimal



INPUT.close()
OUTPUT.close()
ERRORS.close()


# Print output of pass 1 SYMBOL TABLE
print(" PROGRAM NAME: " +  PRGNAME )
print(" PROGRAM LENGTH: " + str(PRGLTH).upper())
print(" LOCATION COUNTER: " + str(loc).upper())
print(" NUMBER OF ERRORS: " + str(ERRCTR) + "\n")


print(" SYMBOL TABLE ")
for label, address in SYMTAB.items():
    print(f" {label:<9}  {address.upper():^9} ")









