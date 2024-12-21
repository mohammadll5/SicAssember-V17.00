from PASS_1 import DIRECTIVES, SYMTAB, OPTAB, ERRCTR, PRGLTH, ADDSTA
INTMDT = open("OUTPUT/intmdte_file.mdt", "r")
OBJFILE = open("OUTPUT/output_file.obj", "w+")
LISTFILE = open("OUTPUT/listing_file.lst", "w+")
ERRORS = open("OUTPUT/errors_file.txt", "w+")
LISTARR = [] 
ADDARR = [] 




if ERRCTR == 0:
    while True:
        line = INTMDT.readline()  
        if not line:  
            break

        currentLine = line

        ADDRESS, LABEL, MNEMONIC, OPERAND = (currentLine[i:j].strip() for i, j in [(0, 8), (9, 17), (18, 25), (25, 34)])



        if MNEMONIC != "START":  
            ADDARR.append(ADDRESS)
            

        if MNEMONIC == "START":


            OBJFILE.write("H^" + LABEL + "^00" + currentLine[0:5].strip().upper() + "^00" + PRGLTH.upper())
            LISTFILE.write(currentLine.strip() +  "\n") 

            ADDARR.append(currentLine[0:6].strip())
            LISTARR.append("")      
            

        elif MNEMONIC == "END":
            LISTARR.append("")  
            LISTFILE.write(" " * 19 + currentLine.strip() +  "\n") 
            

        else:  

            if MNEMONIC in DIRECTIVES or MNEMONIC in OPTAB.keys():
                if MNEMONIC == "RSUB":
                    objCode = OPTAB[MNEMONIC] + "0000" 

                    LISTARR.append(objCode)
                    LISTFILE.write(currentLine.strip()  + " " * (17 - len(str(OPERAND))) + objCode + "\n")  

                elif MNEMONIC not in DIRECTIVES and ",X" not in OPERAND:  
                    if OPERAND in SYMTAB.keys():
                        LISTFILE.write(currentLine.strip() + " " * (14 - len(str(OPERAND))) +  OPTAB[MNEMONIC] + SYMTAB[OPERAND] + "\n")  
                        LISTARR.append(OPTAB[MNEMONIC] + SYMTAB[OPERAND])

                elif OPERAND[-2:] == ",X":  
                    if OPERAND[:-2] in SYMTAB.keys(): 
                        hexCode = hex(int(bin(1)[-1:] + "00" + bin(int(SYMTAB[OPERAND[:-2]][0:1]))[2:]))[-1:]
                        objCode = OPTAB[MNEMONIC[0:]] + hexCode + (SYMTAB[OPERAND[:-2]][1] 
                        +SYMTAB[OPERAND[:-2]][2] + SYMTAB[OPERAND[:-2]][3])

                        LISTFILE.write(currentLine.strip() + " " * (14 - len(str(OPERAND))) + objCode + "\n")
                        LISTARR.append(objCode)

                elif MNEMONIC == "RESW" or MNEMONIC == "RESB":
                    LISTARR.append("")   # No the object code!
                    LISTFILE.write(currentLine.strip() +  "\n") 

                elif MNEMONIC == "WORD":  
                    objCode= hex(((int(OPERAND)) + (1 << 24)) % (1 << 24))[2:]

                    if len(objCode) < 6: 
                        for i in range(6 - len(objCode)):
                            objCode = "0" + objCode

                    LISTFILE.write(currentLine.strip() + " " * (14 - len(str(OPERAND))) + objCode + "\n")
                    LISTARR.append(objCode)

                elif MNEMONIC == "BYTE" :  
                    temp = OPERAND[2:len(OPERAND) - 1] 
                    objCode = ""
                 
                    if "X'" in OPERAND:  
                        LISTFILE.write(currentLine.strip() + " " * (14 - len(str(OPERAND))) + temp + "\n") 
                        LISTARR.append(temp)
               
                    elif "C'" in OPERAND: 
                        LISTFILE.write(currentLine.strip() +  " " * (14 - len(str(OPERAND))))
                        for i in temp:  
                            ascii = ord(i)
                            hexCode = hex(ascii)[2:]  
                            LISTFILE.write( str(hexCode)) 
                            objCode += hexCode 
                            
                        LISTFILE.write("\n")
                        LISTARR.append(objCode)     
            else:
                LISTARR.append("")

else:
    ERRORS.write("Cannot execute pass 2. The input file has errors!")
    print("Cannot execute pass 2. The input file has errors!")
    


currentListing = 1

while currentListing < len(LISTARR):  

    currentAddress = ADDARR[currentListing]
    lngth = 0  

    if LISTARR[currentListing] != "":
        
        OBJFILE.write("\nT^00" + currentAddress.upper() + "^")
        pointer = OBJFILE.tell()   
        OBJFILE.write("  ")
        j = currentListing
        while j < len(LISTARR) and LISTARR[j] != "" and lngth <= 9:
            OBJFILE.write("^" + LISTARR[j].upper())
            lngth += 1
            j += 1

        currentListing = j - 1

        OBJFILE.seek(pointer)  
        tempAdd = hex(int(str(int(ADDARR[currentListing], 16) - int(currentAddress, 16) + int(3))))[2:4]

        if len(tempAdd) == 1:
            tempAdd = "0" + tempAdd 

        if tempAdd == "03":
            tempAdd = "01"

        OBJFILE.write(tempAdd.upper())
        OBJFILE.seek(0, 2) 

    currentListing += 1

OBJFILE.write("\n" + "E" + "^00" + str(hex(ADDSTA))[2:])



OBJFILE.close()
INTMDT.close()
LISTFILE.close()






