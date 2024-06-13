. Example assembly code from pg. 16
. Figure 1.4A in Chapter 1
. Modified to be a assembly program
LOOP    START       7F00
        LDX         ZERO            INTIALIZE INDEX REGISTER TO 0
MOVECH  LDCH        STR1,X          LOAD CHARACTER FROM STR1 INTO REG A
        STCH        STR2,X          STORE CHARACTER INTO STR2
        TIX         ELEVEN          ADD 1 TO INDEX, COMPARE RESULT TO 11
        JLT         MOVECH          LOOP IF INDEX IS LESS THAN 11
        XOS                         END PROGRAM AND EXIT TO THE OS
        .
        .
        .
STR1    BYTE        C'TEST STRING'  11-BYTE STRING CONSTANT
STR2    RESB        11              11-BYTE VARIABLE
.
ZERO    WORD        0               ONE-WORD CONSTANT
ELEVEN  WORD        11              ONE-WORD VARIABLE
        END