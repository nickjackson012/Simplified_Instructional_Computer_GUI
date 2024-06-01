. Example assembly code from pg. 111
. Exercise 2 in Chapter 2
. Code does not work due to table has no data and TIX indexes bytes not integers(words)
SUM     START       4000
FIRST   LDX         ZERO
        LDA         ZERO
LOOP    ADD         TABLE,X
        TIX         COUNT
        JLT         LOOP
        STA         TOTAL
        RSUB
TABLE   RESW        2000
COUNT   RESW        1
ZERO    WORD        0
TOTAL   RESW        1
        END         FIRST