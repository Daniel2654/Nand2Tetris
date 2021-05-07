// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)



// set variables r0 and r1 to be R0 and R1 

@R0
D=M
@r0
M=D
@R1
D=M
@r1
M=D


// if r1 > r0 switch between them (it might add some commands to the
// program but it increase the efficiency a lot)


@r0
D=M
@r1
D=D-M
@SWITCH
D;JLT
@RESET
0;JMP


// Switch between r0 and r1
(SWITCH)
    @r0
    D=M
    @R2
    M=D
    @r1
    D=M
    @r0
    M=D
    @R2
    D=M
    @r1
    M=D


(RESET) // reset the arguments (counter and product)
    @i // set i (counter) to be 1
    M=1 // i=1
    @R2 // initialize the product to be 0
    M=0
(LOOP) // each iteration add r1 to the product the program will do it R0 times
    @i
    D=M // D=i
    @r1
    D=D-M // D=i-r1
    @END
    D;JGT // If (i-r1)>0 goto END
    @r0
    D=M
    @R2 // add r1 to the product
    M=D+M
    @i
    M=M+1 // i=i+1
    @LOOP
    0;JMP // Goto LOOP
(END)
    @END


