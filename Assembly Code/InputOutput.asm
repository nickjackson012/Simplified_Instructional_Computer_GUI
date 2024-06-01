. Example assembly code from pg. 19
. Figure 1.6A in Chapter 1
. Modified to be a assembly program
INOUT   START       7F00
INLOOP  TD          INDEV       TEST INPUT DEVICE
        JEQ         INLOOP      LOOP UNTIL DEVICE IS READY
        RD          INDEV       READ ONE BYTE INTO REGISTER A
        STCH        DATA        STORE BYTE THAT WAS READ
        .
        .
        .
OUTLP   TD          OUTDEV      TEST OUTPUT DEVICE
        JEQ         OUTLP       LOOP UNTIL DEVICE IS READY
        LDCH        DATA        LOAD DATA BYTE INTO REGISTER A
        WD          OUTDEV      WRITE ONE BYTE TO OUTPUT DEVICE
        XOS                     END PROGRAM AND EXIT TO THE OS
        .
        .
        .
INDEV   BYTE        X'F1'       INPUT DEVICE NUMBER
OUTDEV  BYTE        X'05'       OUTPUT DEVICE NUMBER
DATA    RESB        1           ONE-BYTE VARIABLE
        END