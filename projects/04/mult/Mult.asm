// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

// input: the values store in the R0 and R1
// the program is to multiplies R0 and R1 then stores the result in R2
// Output R2

// while R0 > 0:
// 	R2 = R1 + R2
//	R0--

// set R2 = 0
@R2
M=0

(LOOP)

// if R0 == 0 End the loop
@R0
D=M
@END
D;JEQ

// R2 = R2 + R1
@R1
D=M
@R2
M=M+D

// R0 = R0 - 1
@R0
D=M-1
M=D

// goto LOOP
@LOOP
0;JMP

(END)
@END
0;JMP
