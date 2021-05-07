// Notes I tried to be efficient as possiable i didn't use i for counting the
// number of iterations instead i decided to increase screenval by 1 each time
// and stop filling the screen when it reached to 24576 (means 8192 iterations)
// moreover if the screen is already filled with the relevant color due to
// keyboard state, the program won't do nothing and go to ISKEY (listen to the
// keyboard)



@24576 // 512 * 16 is 8192 so we'll do 8192 iterations (16384 + 8192 = 24576)
D=A
@n // stop value - n (24576) so when starting from 16384 we'll execute 8192
   // iterations
M=D
@color // 0 means white -1 means black
M=0
@KBD // reset the keyboard value
M=0

(ISKEY) // listen to the keyboard
    @i // reset the counter
    M=0
    @SCREEN
    D=A
    @screenval // set the screen location to be top left
    M=D
    @KBD
    D=M
    @BLACK // fill the screen with black if key pressed
    D;JNE
    @WHITE // clear the screen if keyboard value is zero
    D;JEQ

(FILL) // if color = -1 fill the screen with black else fill with white
    @screenval
    D=M
    @n
    D=D-M
    @ISKEY
    D;JGE // if screenval >= n (8192) go to ISKEY (listen to the keyboard)
    @color
    D=M
    @screenval
    A=M
    M=D // draw 16 Pixels (-1 is 16 in binary)
    @screenval
    M=M+1
    @FILL
    0;JMP

(WHITE) // clear the screen
    @color // if color already white (0) jump to ISKEY (increase efficiency)
    D=M
    @ISKEY
    D;JEQ
    @color // set the color to be white (0)
    M=0
    @FILL // jump to FILL
    0;JMP


(BLACK) // fill the screen with black
    @color // if color already black (-1) jump to ISKEY (increase efficiency)
    D=M
    @ISKEY
    D;JNE
    @color // set to color to be black (-1)
    M=-1
    @FILL // jump to FILL
    0;JMP






