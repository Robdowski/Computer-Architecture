"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256

    def ram_read(self, arg):
        return self.ram[arg]

    def load(self, filepath):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(f'examples/{filepath}', "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                if set(line[0:7]) in [{'0'}, {'1'}, {'0', '1'}]: 
                    num  = int('0b' + stripped_line[0:8], base=2)
                    self.ram[address] = num
                    address += 1

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        
           


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] * self.reg[reg_b]
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
        running = True

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        while running:
            command = self.ram[self.pc]

            if command == LDI:
                to_write = self.ram[self.pc+2]

                self.reg[self.ram[self.pc+1]] = to_write

                self.pc += 3

            elif command == PRN:
                address = self.ram[self.pc+1]
                print(self.reg[address])

                self.pc += 2

            elif command == MUL:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3

            elif command == HLT:
                running = False
                self.pc += 1