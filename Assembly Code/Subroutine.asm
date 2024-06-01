. Example assembly code from pg. 20
. Figure 1.7A in Chapter 1
. Modified to be a assembly program
SUBRT   START       7F00
        JSUB        READ        CALL READ SUBROUTINE
        XOS                     END PROGRAM AND EXIT TO THE OS
        .
        .
        .
.                               SUBROUTINE TO READ 3-BYTE RECORD
READ    LDX         ZERO        INITIALIZE INDEX REGISTER TO 0
RLOOP   TD          INDEV       TEST INPUT DEVICE
        JEQ         RLOOP       LOOP IF DEVICE IS BUSY
        RD          INDEV       READ ONE BYTE INTO REGISTER A
        STCH        RECORD,X    STORE DATA BYTE INTO RECORD
        TIX         K3          ADD 1 TO INDEX AND COMPARE TO 3
        JLT         RLOOP       LOOP IF INDEX IS LESS THAN K3
        RSUB                    EXIT FROM SUBROUTINE
        .
        .
        .
INDEV   BYTE        X'F1'       INPUT DEVICE NUMBER
RECORD  RESB        100         100 BYTE BUFFER FOR INPUT RECORD
.                               ONE-WORD CONSTANTS
ZERO    WORD        0
K3      WORD        3
        END