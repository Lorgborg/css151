import re
import sys

reserved = ["integer", "double", ":=", "<<", "output", "if", ";", "=", "+", "string", "float"]
acceptedTypes = ["integer", "string", "float", "double"]
variables = {}

def initialized(line, lineNum):
    pattern = r"cin\s*>>\s*(.*?)(?=\s*;)"
    match = re.search(pattern, line)
    if match:
        variables[match.group(1)]= input("")
        
    pattern = r"([^=]+)(?=\s*=(?!=))"

    # Use re.findall to find all matches
    match = re.search(pattern, line)
    val = re.search(r"(?<!==)\s*=\s*([^;]+)(?=\s*;)", line)
    if match:
        if not "\"" in line:
            variables[match.group(1)] = int(val.group(1))
        else:
            variables[match.group(1)] = val.group(1)
        
def out(line, lineNum):
    pattern = r"cout\s*<<\s*(.*?)(?=\s*;)"
    match = re.search(pattern, line)

    symbols = ['+', '-', '/', '*', '^']
    symUsed = []
    numUsed = []

    if any(symbol in line for symbol in symbols):
        matches = re.findall(r'([+\-/*^])|([^+\-/*^]+)', match.group(1))
        
        for match in matches:
            symbol, word = match
            if symbol:  # If the symbol is not empty, add it to the symbols array
                symUsed.append(symbol)
            if word:  # If the word is not empty, add it to the words array
                match = re.search(r'^[+-]?\d+$', word)
                if match:
                    print("yeah")
                    numUsed.append(int(word))
                else:
                    numUsed.append(variables[word])
        
        final = 0
        result = next(iter(variables.values()))
        for i in range(1, len(numUsed)):
            symbol = symUsed[i - 1]  # Get the symbol between numbers
            num = numUsed[i]  # Get the next number
            
            if symbol == '+':
                result += num
            elif symbol == '-':
                result -= num
            elif symbol == '*':
                result *= num
            elif symbol == '/':
                result /= num  # Be mindful of division by zero
        print(result)
    if "\"" in line:
        match = re.search(r'"([^"]*)"', line)
        if match:
            print(match.group(1))
    else:
        if match:
            print(variables[match.group(1)])
    
with open("./files/" + sys.argv[1]) as file:
    i = 0
    for line in file:
        line = line.replace(" ", "")
        initialized(line, i)
        out(line, i)
        i = i+1

