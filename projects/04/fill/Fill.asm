// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// KBD > 0 set n = 8192

(START)
  @KBD
  D=M
  @key
  M=D

  @WHITE
  D;JEQ
  @BLACK
  D;JGT

  (WHITE)
  @color
  M=0 // color = 0
  @NEXT
  0;JMP

  (BLACK)
  @color
  M=-1 // color = -1
  @NEXT
  0;JMP
  
  (NEXT)
  @8191
  D=A
  @n
  M=D // n = 8192

  @i
  M=0 // i = 0

  @SCREEN
  D=A
  @address
  M=D // address = 16384 (base address of the hack screen)

(LOOP)
   @i
   D=M
   @n
   D=D-M
   @END
   D;JGT // if i > n goto END

   @color
   D=M
   @address
   A=M
   M=D // RAM[address] = -1 (16 pixels)

   @i
   M=M+1 // i = i + 1
   @1
   D=A
   @address
   M=M+D // address = address + 1
   @LOOP
   0;JMP // goto LOOP

(END)
   @KBD
   D=M
   @key
   D=M-D
   @END
   D;JEQ
   @START
   0;JMP

