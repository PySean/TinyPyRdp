"""
"mipstrs.py", by Sean Soderman
Contains functions pertinent to file I/O and MIPS instruction construction.
"""
import os
import sys
from hdrftr import preamble, epilogue

#File handler for opened MIPS file.
mipc = None

"""
Spit out the appropriate storage instruction for the assignment statement.
"""
def store(src, dest):
    str = "\
             l.d $f2, {0}($s1)\n\
             s.d $f2, {1}($s1)\n".format(src, dest)
    write_mips(str)
"""
Spit out appropriate MIPS code according to the passed in expression.
"""
def arith(operator, op1, op2, count):
    ins = {'*' : 'mul.d', '+' : 'add.d', '-' : 'sub.d', '/' : 'div.d'}
    str = "\
             l.d  $f2, {0}($s1)\n\
             l.d  $f4, {1}($s1)\n\
             {2}  $f6, $f2, $f4\n\
             s.d  $f6, {3}($s1)\n".format(op1, op2, ins[operator], count)
    write_mips(str)
"""
Spit out appropriate MIPS code for the special division and modulo operators.
"""
def sdiv_arith(operator, op1, op2, count):
    remstr = "mul.d $f6, $f6, $f4\n\
              sub.d $f6, $f2, $f6\n"
    ins = {'%': remstr}
    str = "\
            l.d $f2, {0}($s1)\n\
            l.d $f4, {1}($s1)\n\
            div.d $f6, $f2, $f4\n\
            trunc.w.d $f6, $f6\n\
            cvt.d.w $f6, $f6\n{2}\
            s.d $f6, {3}($s1)\n".format(op1, op2, ins.get(operator, ""), count)
    write_mips(str)
"""
Spit out MIPS code to negate a value.
"""
def negate(op, count):
    str = "\
            l.d $f2, {0}($s1)\n\
            neg.d $f2, $f2\n\
            s.d $f2, {1}($s1)\n".format(op,count)
    write_mips(str)
"""
Invoke the exponentiation function on the proper value. Note: may be wrong.
"""
def exp(base, exp, count):
    str = "\
            l.d $f2, {0}($s1)\n\
            l.d $f4, {1}($s1)\n\
            jal pow\n\
            s.d $f6, {2}($s1)\n".format(base, exp, count)
    write_mips(str)
"""
Spit out the simple address loading & value printing code 
for doubles or strings in a terse, obfuscated fashion.
"""
def printit(addr):
    ins = ""
    spaces = {'N' : 'NewL', 'B': 'Blank', 'T': 'Tab'}
    bob = str(addr)
    bob = spaces.get(addr, bob)
    ins ="l.d" if bob not in spaces.values() else "la"
    sysnum = int('3') + str(bob).isalpha()  #3 is for doubles, 4 is for strings!
    bob = bob + '($s1)' if bob.isdigit() else bob
    sysreg = '$f12' if sysnum == 3 else '$a0'
    #Let's dance.
    string = "\
             li $v0, {0}\n\
             {1} {2}, {3}\n\
             syscall\n".format(sysnum, ins, sysreg, bob)
    write_mips(string)

"""
Spit out code relevant to taking stdin from the user.
"""
def insert(reg):
    string = "\
             li $v0, 7\n\
             syscall\n\
             s.d $f0, {}($s1)\n".format(reg)
    write_mips(string)
"""
Spit out preamble to conditional block.
testval: The value I am testing against zero
count: This is the count-th if statement I have fashioned.
"""
def condcheck(testval, name, count):
    string = "\
             l.d $f2, {0}($s1)\n\
             l.d $f4, 0($s1)\n\
             c.eq.d $f2, $f4\n\
             bc1t   {1}{2}\n".format(testval, name, count)
    write_mips(string)
"""
Print out the label...nicely.
"""
def condend(label, count, jump=False):
    if jump == True:
        string = "\
             j {0}{1}\n".format(label, count)
    else:
        string = "\
        {0}{1}:\n".format(label, count)
    write_mips(string)
"""
Open up a file to write MIPS to.
Will _always_ truncate and write to a file. This file will have the same name
as the cmd line argument except with a .s extension rather than a .t.
Will also write out the preamble. May as well.
"""
def open_mips(fname):
    global mipc
    try:
        mipc = os.open(fname[:-2] + '.s', os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
        mipc = os.fdopen(mipc, "w")
    except FileNotFoundError:
        sys.stderr.write("File not found!")
        mipc.close()
        sys.exit(1)
    write_mips(preamble)

    
def close_mips():
    global mipc
    mipc.close()

#A general purpose function for file output.
def write_mips(string):
    global mipc
    if mipc.write(string) == 0:
        sys.stderr.write("Error: problem writing to file")
        sys.exit(1)
