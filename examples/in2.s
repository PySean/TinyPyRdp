#Compiled by Sean Soderman
             .globl main
             main:	move $s7, $ra
             la  $s1, M
             #I print my name
             la	$a0, Name
             li	$v0, 4
             syscall
             l.d $f2, 8($s1)
             s.d $f2, 184($s1)
             l.d $f2, 0($s1)
             s.d $f2, 224($s1)
             li $v0, 7
             syscall
             s.d $f0, 176($s1)
        loop0:
             l.d  $f2, 184($s1)
             l.d  $f4, 176($s1)
             sub.d  $f6, $f2, $f4
             s.d  $f6, 304($s1)
             l.d $f2, 304($s1)
             l.d $f4, 0($s1)
             c.eq.d $f2, $f4
             bc1t   end0
             l.d  $f2, 8($s1)
             l.d  $f4, 184($s1)
             div.d  $f6, $f2, $f4
             s.d  $f6, 320($s1)
             l.d  $f2, 224($s1)
             l.d  $f4, 320($s1)
             add.d  $f6, $f2, $f4
             s.d  $f6, 336($s1)
             l.d $f2, 336($s1)
             s.d $f2, 224($s1)
             li $v0, 3
             l.d $f12, 184($s1)
             syscall
             li $v0, 4
             la $a0, Tab
             syscall
             li $v0, 3
             l.d $f12, 224($s1)
             syscall
             li $v0, 4
             la $a0, NewL
             syscall
             l.d  $f2, 184($s1)
             l.d  $f4, 8($s1)
             add.d  $f6, $f2, $f4
             s.d  $f6, 424($s1)
             l.d $f2, 424($s1)
             s.d $f2, 184($s1)
             j loop0
        end0:
             move	$ra, $s7
             jr $ra
             pow:
             # truncate $f4
             trunc.w.d $f4, $f4
             cvt.d.w $f4, $f4
             l.d     $f6, 8($s1)
             # check if $f4 == 0
             l.d     $f8, 0($s1)
             c.eq.d  $f4, $f8
             bc1t    end
              # check if $f4 > 0
             l.d     $f8, 0($s1)
             c.lt.d  $f8, $f4
              bc1t  next
             l.d     $f8, 8($s1)
             div.d   $f2, $f8, $f2
              neg.d   $f4, $f4
             # loop as long as $f4 == 0
             next:   l.d  $f8, 0($s1)
              c.eq.d  $f4, $f8
             bc1t  end
             mul.d $f6, $f6, $f2
             l.d  $f8, 8($s1)
             sub.d $f4, $f4, $f8
             b next
             end:    jr    $ra
             	.data
             .align 3
             M:	.double 0.,1.,2.,3.,4.,5.
             .double 6.,7.,8.,9. #cons, car, cdr, whatever
             .space	208 #a to z, as doubles!
             .space	1000 #125 temps
             Blank:	.asciiz " "
             NewL:	.asciiz "\n"
             Tab:	.asciiz "\t"
             Name:	.asciiz "Executed by Sean Soderman\n"
