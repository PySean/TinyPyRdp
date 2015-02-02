#!/usr/bin/python
"""
tinyparse.py(v3), by Sean Soderman
A modified version of the parser from hmwk8 that handles
assignment statements, output statements, arithmetic and constants.
Now supports exponentiation, tabs, and input.
"""
import sys
import os
from mipstrs import *
from hdrftr import *

if len(sys.argv) < 2:
    print("Usage: %s <filename>" % (sys.argv[0]))
    exit(1)
try:
    infile = open(sys.argv[1])
except FileNotFoundError:
    sys.stderr.write("File not found!\n")
    exit(1)
open_mips(sys.argv[1])

next = None
count = 288 #The first temp. address is here.

#The one rule to rule them all
def M():
    sys.stdout.write("\nSource: ")
    scan()
    while next != '$': 
        S()
        reset()
    else:
        sys.stdout.write(", accept.\n")
        write_mips(epilogue)
        
#Rule for statements of any kind
def S():
    if next == '[':
        I() 
    elif next == '{':
        W() 
    elif next.islower():
        A()
    elif next == '<':
        P()
    elif next == '>':
        G()
    else:
        print("Next was: %s" % (next))
        error(1)

#Rule for if-(else) statements
def I():
    count = I.condcount
    scan()
    testval = E()
    condcheck(testval,"if", count)
    I.condcount += 1
    if next == '?':
        scan()
        S() 
        while next != ':' and next != ']': 
            S()
        if next == ':':
            condend("endif", count, jump=True)
            condend("if", count)
            scan()
            while next != ']' and next != '$':
                S()
            condend("endif", count)
        else:
            condend("if", count)
    if next == '$':
        error(5)
    scan()
I.condcount = 0   #Better than a global variable.

#Rule for while loops
def W():
    count = W.whilecount
    W.whilecount += 1
    condend("loop", count)
    scan()
    testval = E()
    condcheck(testval, "end", count) #Testing
    if next == '?':
        scan()
        S()
        while next != '}' and next != '$':
            S()
    if next == '}':
        scan()
        condend("loop", count, jump=True)
        condend("end", count)
    else:
        error(6)
W.whilecount = 0

#Rule for assignment statements
def A():
    dest = getreg(next) 
    scan()
    if next == '=':
        scan()
        src = E()     
        store(src, dest)
    if next == ';':
        scan()
    else:
        error(2)

#Rule for print statements
def P():
    scan()
    pval = E() 
    if next == ';':
        scan()
        printit(pval)
    elif next == 'N':
        printit(next)
        scan()
        if next == ';':
            scan()
        else:
            error(3)
    elif next == 'B':
        printit(next)
        scan()
        if next == ';':
            scan()
        else:
            error(3)
    elif next == 'T':
        printit(next)
        scan()
        if next == ';':
            scan()
        else:
            error(3)
    else:
        error(3)

#Rule for getting input from stdin.
def G():
    scan()
    if next.islower:
        reg = getreg(next)
        scan()
        if next == ';':
            insert(reg)
            scan()
        else:
            error(7)
    else:
        error(7)

#Rule for +- operations
def E():
    min_flag = False
    op1 = T()
    while op1 == '-':
        scan()
        min_flag = not min_flag #Handle stuff like -----a with ease.
        op1 = T()
    while next == '+' or next == '-':
        save = next #Make sure the operator is saved.
        scan()
        op2 = T()   
        arith(save, op1, op2, count)
        op1 = count
    if min_flag == True:
        negate(op1, count) 
        op1 = count
        inc()
    else:
        inc()
    return op1 

#Rule for */%@ operations
def T():
    min_flag = False
    op1 = U()
    while op1 == '-':
        scan()
        min_flag = not min_flag
        op1 = U() #Perhaps get rid of this line...
    ins = ['*', '/', '%', '@']
    while next in ins:
        save = next
        scan()
        op2 = U()
        if save == '%' or save == '@':
            sdiv_arith(save, op1, op2, count)
        else:
            arith(save, op1, op2, count)
        op1 = count
        inc()
    if min_flag == True:
        negate(op1, count)
        op1 = count
        inc()
    else:
        inc()
    return op1

#Rule for exponentiation.
def U():
    op1 = F()
    if next == '^':
        scan()
        op2 = U()
        exp(op1, op2, count)
        return count
    return op1

#Rule for parenthesis/register evaluation.
def F():
    if next.islower(): # lowernum
        save = next
        scan()
        return getreg(save)
    elif next.isdigit():
        save = next
        scan()
        return int(save) * 8
    elif next == '(':
        scan()
        val = E()
        if next == ')':
            scan()
        else:
            error(4)
        return val
    elif next == '-':
        return '-'

def error(n):
    sys.stdout.write("\nError:" +
    str(n) + "\n")
    sys.exit(1)

def getch():
    c = infile.read(1)
    if len(c) > 0:
        #sys.stdout.write(c) # echo input (for debugging purposes only)
        return c
    else:
        return None

def scan():
    global next
    next = getch()
    if next == None:
        sys.exit(1)
    while next.isspace(): # skip whitespace
        next = getch()
#Increment the global address offset by 8 when needed.
def inc():
    global count
    count += 8
#Just reset count after the end of a long statement.
def reset():
    global count
    count = 288

#Get the proper offset to char's spot in memory.
def getreg(char):
    return 80 + ((ord(char) - ord('a')) * 8)
M()
infile.close()
close_mips()
