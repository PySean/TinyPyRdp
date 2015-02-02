"""
"hdrftr.py", by Sean Soderman
This is just a spot I can place the preamble and epilogue code, since it really gets in the way.
"""
preamble = "#Compiled by Sean Soderman\n\
             .globl main\n\
             main:\tmove $s7, $ra\n\
             la  $s1, M\n\
             #I print my name\n\
             la\t$a0, Name\n\
             li\t$v0, 4\n\
             syscall\n"

epilogue = "\
             move\t$ra, $s7\n\
             jr $ra\n\
             pow:\n\
             # truncate $f4\n\
             trunc.w.d $f4, $f4\n\
             cvt.d.w $f4, $f4\n\
             l.d     $f6, 8($s1)\n\
             # check if $f4 == 0\n\
             l.d     $f8, 0($s1)\n\
             c.eq.d  $f4, $f8\n\
             bc1t    end\n\
              # check if $f4 > 0\n\
             l.d     $f8, 0($s1)\n\
             c.lt.d  $f8, $f4\n\
              bc1t  next\n\
             l.d     $f8, 8($s1)\n\
             div.d   $f2, $f8, $f2\n\
              neg.d   $f4, $f4\n\
             # loop as long as $f4 == 0\n\
             next:   l.d  $f8, 0($s1)\n\
              c.eq.d  $f4, $f8\n\
             bc1t  end\n\
             mul.d $f6, $f6, $f2\n\
             l.d  $f8, 8($s1)\n\
             sub.d $f4, $f4, $f8\n\
             b next\n\
             end:    jr    $ra\n\
             \t.data\n\
             .align 3\n\
             M:\t.double 0.,1.,2.,3.,4.,5.\n\
             .double 6.,7.,8.,9. #cons, car, cdr, whatever\n\
             .space\t208 #a to z, as doubles!\n\
             .space\t1000 #125 temps\n\
             Blank:\t.asciiz \" \"\n\
             NewL:\t.asciiz \"\\n\"\n\
             Tab:\t.asciiz \"\\t\"\n\
             Name:\t.asciiz \"Executed by Sean Soderman\\n\"\n"
