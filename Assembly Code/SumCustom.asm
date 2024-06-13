. Based on example assembly code from pg. 111
. Exercise 2 in Chapter 2
. Tests our custom opcodes: TIXW and XOS
SUMCUS     START       4000
FIRST   LDX         ZERO
        LDA         ONE
LOOP1   MUL         COUNT
        STA         TABLE,X
        TIXW        COUNT
        JLT         LOOP1
        LDX         ZERO
        LDA         ZERO
LOOP2   ADD         TABLE,X
        TIXW        COUNT
        JLT         LOOP2
        STA         TOTAL
        XOS
TABLE   RESW        2000
COUNT   WORD        3
ZERO    WORD        0
ONE     WORD        1
TOTAL   RESW        1
        END         FIRST