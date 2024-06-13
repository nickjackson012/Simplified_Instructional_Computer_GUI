. Example assembly code from pg. 17
. Figure 1.5A in Chapter 1
. Modified to be a assembly program
XLOOP   START       7F00
        LDA         ZERO            INITIALIZE INDEX REGISTER TO 0
        STA         INDEX
ADDLP   LDX         INDEX           LOAD INDEX VALUE INTO REGISTER X
        LDA         ALPHA,X         LOAD WORD FROM ALPHA INTO REGISTER A
        ADD         BETA,X          ADD WORD FROM BETA
        STA         GAMMA,X         STORE THE RESULT IN A WORD IN GAMMA
        LDA         INDEX           ADD 3 TO INDEX VALUE
        ADD         THREE
        STA         INDEX
        COMP        K300            COMPARE NEW INDEX VALUE TO 300
        JLT         ADDLP           LOOP IF INDEX IS LESS THAN 300
        XOS                         END PROGRAM AND EXIT TO THE OS
        .
        .
        .
INDEX   RESW        1               ONE-WORD VARIABLE FOR INDEX VALUE
.
ALPHA   WORD        24
        WORD        -54
BETA    WORD        82
        WORD        53
GAMMA   RESW        10
.
ZERO    WORD        0               ONE-WORD CONSTANT
K300    WORD        6               ONE-WORD CONSTANT
THREE   WORD        3               ONE-WORD CONSTANT
        END