symbolDict = {
        "R0":"0",   
        "R1":"1",       
        "R2":"2",   
        "R3":"3",   
        "R4":"4",   
        "R5":"5",   
        "R6":"6",   
        "R7":"7",   
        "R8":"8",   
        "R9":"9",
        "R10":"10",
        "R11":"11",
        "R12":"12",
        "R13":"13",
        "R14":"14",
        "R15":"15",
        "SCREEN":"16384",
        "KBD":"24576",
        "SP":"0",
        "LCL":"1",
        "ARG":"2",
        "THIS":"3",
        "THAT":"4"
        }

destDict = { 
        "null":"000",
        "M":"001",
        "D":"010",
        "MD":"011",
        "A":"100",
        "AM":"101",
        "AD":"110",
        "AMD":"111"
        }

jumpDict = {
        "null":"000",
        "JGT":"001",
        "JEQ":"010",
        "JGE":"011",
        "JLT":"100",
        "JNE":"101",
        "JLE":"110",
        "JMP":"111"
        }

compDict = {
        "0":"0101010",
        "1":"0111111",
        "-1":"0111010",
        "D":"0001100",
        "A":"0110000",
        "!D":"0001101",
        "!A":"0110001",
        "-D":"0001111",
        "-A":"0110011",
        "D+1":"0011111",
        "A+1":"0110111",
        "D-1":"0001110",
        "A-1":"0110010",
        "D+A":"0000010",
        "D-A":"0010011",
        "A-D":"0000111",
        "D&A":"0000000",
        "D|A":"0010101", 
        "M":"1110000",
        "!M":"1110001",
        "-M":"1110011",
        "M+1":"1110111",
        "M-1":"1110010",
        "D+M":"1000010",
        "D-M":"1010011",
        "M-D":"1000111",
        "D&M":"1000000",
        "D|M":"1010101",
        }

file_name = input("Enter the name of the source file: ")

with open(file_name, 'r') as source_file:
    source_code = source_file.read()

last_used_addr = 16 
ass_instructions = []

n=0
# first pass. (handling of jump labels and getting rid of blank spaces and comments)
for line in source_code.splitlines():
    
    if not line.strip() or (len(line.strip()) > 1 and line.strip()[0:2] == "//"):
        continue

    if len(line.split()) > 1 and line.split()[1][0:2] != "//":
        raise Exception("multiple commands in one line:", line )
    
    # gets the actual instruction—or label—after having removed all the garbage
    inst = line.split()[0]
    
    # stores labels as symbols
    if inst[0] == "(" and inst[-1] == ")":
        label = inst[1:-1]
        symbolDict[label] = n
        continue

    ass_instructions.append(inst) 
    n += 1

bin_instructions = []

# second pass. (symbols and binary instructions translation)
for inst in ass_instructions:

    if inst[0] == "@":
        # A instruction
        a_value = inst[1:]
        if not a_value.isdigit():
            try:
                rep_value = symbolDict[a_value]
            except KeyError:
                symbolDict[a_value] = rep_value = last_used_addr
                last_used_addr += 1
            a_value = rep_value  
        bin_value = bin(int(a_value))[2:]    
        binary_instruction = "0" + bin_value.zfill(15)

    else:  
        # C instruction 
        dest = jump = "null"
        if "=" in inst:
            dest, comp = inst.split("=")
        elif ";" in inst:
            comp, jump = inst.split(";")

        # *Kronk*: Oh yeah.. It's all comming together ( ͡° ͜ʖ ͡°). 
        try:
            binary_instruction = "111" + compDict[comp] + destDict[dest] + jumpDict[jump]
        except:
            print("something went wrong (maybe invalid syntax¿?):", line)
    
    bin_instructions.append(binary_instruction)

# new name
if "/" in file_name:
    file_name = file_name.split("/")[-1]
new_filename = file_name.split(".")[0] + ".hack"

binary_code = "\n".join(bin_instructions)

# outputs the new file containing the binary instructions with the same name and different .hack extension 
with open(new_filename, "w") as binary_file:
    binary_file.write(binary_code)

# we might as well let them now right?
print("Done.") 
