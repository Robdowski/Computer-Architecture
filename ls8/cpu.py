"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.sp = 0xf4
        self.reg[7] = self.sp
        self.equal_flag = 00000000
        self.reg[4] = self.equal_flag
        

    def ram_read(self, arg):
        return self.ram[arg]

    def load(self, filepath):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(f'examples/{filepath}', "r") as a_file:
            for line in a_file:
                stripped_line = line.strip()
                if set(line[0:8]) in [{'0'}, {'1'}, {'0', '1'}]: 
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
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if reg_a == reg_b:
                self.equal_flag = 0b00000001

            elif reg_a < reg_b:
                self.equal_flag = 0b00000100

            elif reg_a > reg_b:
                self.equal_flag = 0b00000010

        elif op == "AND":
            result = reg_a & reg_b
            self.reg[self.ram[self.pc+1]] = result

        elif op == "OR":
            result = reg_a | reg_b
            self.reg[self.ram[self.pc+1]] = result
            

        elif op == "XOR":
            result = reg_a ^ reg_b
            self.reg[self.ram[self.pc+1]] = result

        elif op == "NOT":
            result = ~reg_a
            self.reg[self.ram[self.pc+1]] = result

        elif op == "SHL":
            result = reg_a << reg_b
            self.reg[self.ram[self.pc+1]] = result
        
        elif op == "SHR":
            result = reg_a >> reg_b
            self.reg[self.ram[self.pc+1]] = result

        elif op == "MOD":
            result = reg_a % reg_b
            self.reg[self.ram[self.pc+1]] = result

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
        POP = 0b01000110
        PUSH = 0b01000101
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000

        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        JMP = 0b01010100

        AND = 0b10101000
        OR = 0b10101010
        XOR = 0b10101011
        NOT = 0b01101001
        SHL = 0b10101100
        SHR = 0b10101101
        MOD = 0b10100100
        ADDI = 0b10110000

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

            elif command == POP:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.sp]

                self.reg[reg] = val

                self.sp += 1
                self.pc += 2

            elif command == PUSH:
                reg = self.ram[self.pc + 1]
                reg_val = self.reg[reg]

                self.sp -= 1

                self.ram[self.sp] = reg_val

                self.pc += 2

            elif command == CALL:
                reg_address = self.ram[self.pc + 1]
                new_pc = self.reg[reg_address]
                next_instruction = self.pc+2
                self.sp -= 1
                self.ram[self.sp] = next_instruction

                self.pc = new_pc

            elif command == RET:
                self.pc = self.ram[self.sp]
                self.sp += 1

            elif command == ADD:
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.alu("ADD", reg_a, reg_b)
                self.pc += 3

            elif command == CMP:
                regA = self.reg[self.ram[self.pc+1]]
                regB = self.reg[self.ram[self.pc+2]]
                self.alu("CMP", regA, regB)
                self.pc += 3
            
            elif command == JMP:
                reg_address = self.ram[self.pc +1]
                reg_to_jump = self.reg[reg_address]

                self.pc = reg_to_jump

            elif command == JEQ:
                reg_address = self.ram[self.pc +1]
                reg_to_jump = self.reg[reg_address]

                if self.equal_flag == 1:
                    self.pc = reg_to_jump
                else:
                    self.pc += 2

            elif command == JNE:
                reg_address = self.ram[self.pc +1]
                reg_to_jump = self.reg[reg_address]

                if self.equal_flag != 1:
                    self.pc = reg_to_jump
                else:
                    self.pc += 2

            elif command == AND:
                reg_a = self.reg[self.ram[self.pc+1]]
                reg_b = self.reg[self.ram[self.pc+2]]

                self.alu("AND", reg_a, reg_b)

                self.pc += 3

            elif command == OR:
                reg_a = self.reg[self.ram[self.pc+1]]
                reg_b = self.reg[self.ram[self.pc+2]]

                self.alu("OR", reg_a, reg_b)

                
                self.pc += 3

            elif command == XOR:
                reg_a = self.reg[self.ram[self.pc+1]]
                reg_b = self.reg[self.ram[self.pc+2]]

                self.alu("XOR", reg_a, reg_b)

                
                self.pc += 3

            elif command == NOT:
                reg = self.reg[self.ram[self.pc+1]]

                self.alu("NOT", reg, None)

                self.pc += 2

            elif command == SHL:
                reg_a = self.reg[self.ram[self.pc+1]]
                reg_b = self.reg[self.ram[self.pc+2]]

                self.alu("SHL", reg_a, reg_b)

                
                self.pc += 3
            
            elif command == SHR:
                reg_a = self.reg[self.ram[self.pc+1]]
                reg_b = self.reg[self.ram[self.pc+2]]

                self.alu("SHR", reg_a, reg_b)

                self.pc += 3
            
            elif command == MOD:
                reg_a = self.reg[self.ram[self.pc+1]]
                reg_b = self.reg[self.ram[self.pc+2]]

                if reg_b == 0:
                    print("Cannot divide by 0!")
                    self.pc += 3
                    running=False

                self.alu("MOD", reg_a, reg_b)

                self.pc += 3

            elif command == ADDI:
                value = self.ram[self.pc+1]
                reg = self.reg[self.ram[self.pc+2]]

                self.alu("ADD", value, reg)

                self.pc += 3

            elif command == HLT:
                running = False
                self.pc += 1