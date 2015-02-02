"tinyparse.py", by Sean Soderman
################################

A recursive descent parser I wrote for a programming languages course that compiles
a subset of the Tiny (tm) programming language.

In the examples directory are files containing both Tiny(tm) code and their MIPS equivalents.
You can compile this code with SPIM. Also, one thing to note is that you can't have single instructions with
more than 125 operands due to the amount of space that needs to be allocated for temporary variables. 

The Tiny(tm) code files end with a ".t" extension, whereas the MIPS ends with ".s".

Eventually I may extend this to accomodate a grammar supporting function calls and for loops, among other
common programming language constructs.

It was quite a lot of fun to implement this so it is definitely possible, given enough free time.
