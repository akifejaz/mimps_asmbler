# MIMPS Assembler (Assembly to Machine Code Converter)
This is simple MIMPs Architecture Assembler that I made as beginner for learning. 

This Python script converts MIPS assembly instructions to machine code. It reads instructions from a file named `test.asm`, converts them to binary machine code, and writes the binary code to `intr_mem.bin`. Additionally, it converts the binary code to hexadecimal format and writes it to `intr_mem.hex`.

## How to Use

1. Ensure you have Python installed on your system.
2. Create or modify the `test.asm` file with your MIPS assembly instructions.
3. Run the Python script using the command `python main.py`.
4. Check the generated `intr_mem.bin` and `intr_mem.hex` files for the corresponding binary and hexadecimal machine code, respectively.

## Instruction Formats Supported

1. **R-Type Instructions**: These include instructions like `add`, `sub`, `and`, `or`, `slt`.
   - Example: `add $1, $2, $3`
   
2. **I-Type Instructions**: Instructions like `lw`, `sw`, `andi`, `addi`.
   - Example: `lw $1, 100($2)`
   
3. **II-Type Instructions**: Instructions like `andi`, `addi`.
   - Example: `andi $s14, $s15, 10`

## Note

- Comments in the assembly file should start with `#`.
- Each instruction should be on a separate line.

Ensure your MIPS assembly instructions are correctly formatted before running the script.
