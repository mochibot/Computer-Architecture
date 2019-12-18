"""CPU functionality."""

import sys, re

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 7 + [0xF4]
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            sys.exit('Please provide input in the format of "ls8.py [filname]"')

        with open(sys.argv[1]) as f:
            for line in f:
                instruction = re.match(r'\d{8}', line)
                if instruction is not None:
                    self.ram[address] = int(instruction.group(), 2)
                    address += 1
                else: 
                    continue

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        flag = True

        while flag:
            ir = self.ram_read(self.pc)

            if ir == HLT:  
                flag = False
                self.pc += 1
            elif ir == LDI:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.raw_write(operand_b, operand_a)
                self.pc += 3        
            elif ir == PRN:
                operand_a = self.ram_read(self.pc + 1)
                print(self.reg[operand_a])
                self.pc += 2
            elif ir == MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3
            elif ir == PUSH:
                # Decrement SP
                # Copy value in register to address pointed to by SP
                operand_a = self.ram_read(self.pc + 1)
                self.reg[SP] -= 1   
                self.ram[self.reg[SP]] = self.reg[operand_a]  
                self.pc += 2  
            elif ir == POP:
                # Copy value from address pointed to by SP to given register
                # Increment SP
                operand_a = self.ram_read(self.pc + 1)
                self.raw_write(self.ram[self.reg[SP]], operand_a)
                self.reg[SP] += 1   
                self.pc += 2    
            else:
                print(f"Unknown instruction at index {self.pc}")
                self.trace()
                sys.exit(1)  

    def ram_read(self, address):
        return self.ram[address]

    def raw_write(self, value, address):
        self.reg[address] = value

