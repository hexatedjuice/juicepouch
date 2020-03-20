# system security
## architecture fundementals
* mnemonic code - translated machine code
  - ex. nasm, masm (microsoft macro asm)
* instruction set architecture (isa) - set of details for an architecture
  (memory, registers, strucs, etc)
  - ex. intelx86/x86\_64
 * registers
  - 32/64 bit refers to width of cpu reg
  - some have specific funx while others for general data
  - general purpose reg (gpr)
    * naming conventions
      - 8 bi - 16bi reg div into 2 pts: low by (L) or high by (H) at end of name
      - 16 bi - combine L and H > X; stack pt, base pt, src reg, and dst reg
        L is removed
      - 32 bi - reg prefix w E (extended)
      - 64bi - E xged for R
      - eip - struct pt which ctrls pgm exec by storing addr of next struct
* prcs mem
  - text - (strct segm) pgm code RO
  - data - init data and uninit data 
    * init - static, global declared vars
    * uninit - block started by symbol (bss); inits vars set to 0 or implicit
      init
  - heap - pgm can request more space during exec via `brk` or `sbrk`, used by
    `malloc`, `realloc`, and `free`
    * grows form low\>hi mem addr
  - stack - LIFO; an array used for saving funx return addr, passin funx args,
    and store local vars
    * esp - id top of stack and chgs w each push or pop
    * grows from hi\>low mem addr
* push - subtracts 4/8 bi(32/64) from esp and srite data to mem addr in esp and
  then updates esp to top of stack 
* pop - retrieves info and adds 4/8 bi (32/64) from esp
  - ex. POP EAX, stores value to eax and increments esp
  - not zeroed until ow
* stakc frames
  - prlg - preps stack to being use
  - epilg - resets stack to prlg settings
  - stack is made up of logical stack frames
    * push - call a funx
    * pop - return a value
  - on call 
    1. stack frame created
    2. assigned current esp location
  - on term
    1. pgm recieves params passed form funx
    2. eip reset to init call location
  - keeps track of each funx and ctrls term
