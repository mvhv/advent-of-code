class IntMachine():
    def __init__(self, code, cin, cout):
        self.pointer = 0
        self.read_head = 0
        self.write_head = 0
        self.code = code
        self.cin = cin
        self.cout = cout
        self.opcodes = {
            1: self.addition,
            2: self.multiplication,
            3: self.take,
            4: self.give,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            99: self.end
        }

    def get(self, mode, param):
        if mode == 0: # position mode
            return self.code[param]
        elif mode == 1: # immediate mode
            return param

    def parse(self, opcode):
        op = opcode % 100
        mode1 = opcode // 100 % 10
        mode2 = opcode // 1000 % 10
        mode3 = opcode // 10000 % 10
        return (op, (mode1, mode2, mode3))

    def run(self):
        while True:
            (op, modes) = self.parse(self.code[self.pointer])
            self.opcodes[op](modes, self.pointer)
            if op == 99: break # halt program, but end func runs first

    def addition(self, modes, ptr):
        (m1, m2, m3) = modes
        a = self.get(m1, self.code[ptr+1])
        b = self.get(m2, self.code[ptr+2])
        c = self.code[ptr+3]
        self.code[c] = a + b
        self.pointer += 4

    def multiplication(self, modes, ptr):
        (m1, m2, m3) = modes
        a = self.get(m1, self.code[ptr+1])
        b = self.get(m2, self.code[ptr+2])
        c = self.code[ptr+3]
        self.code[c] = a * b
        self.pointer += 4

    def take(self, modes, ptr):
        (m1, m2, m3) = modes
        a = self.code[ptr+1]
        self.code[a] = self.cin[self.read_head]
        self.read_head += 1
        self.pointer += 2

    def give(self, modes, ptr):
        (m1, m2, m3) = modes
        a = self.get(m1, self.code[ptr+1])
        self.cout.append(a)
        self.write_head += 1
        self.pointer += 2

    def jump_if_true(self, modes, ptr):
        (m1, m2, m3) = modes
        a = self.get(m1, self.code[ptr+1])
        b = self.get(m2, self.code[ptr+2])
        if a == 0:
            self.pointer += 3
        else:
            self.pointer = b

    def jump_if_false(self, modes, ptr):
        (m1, m2, m3) = modes
        a = self.get(m1, self.code[ptr+1])
        b = self.get(m2, self.code[ptr+2])
        if a == 0:
            self.pointer = b
        else:
            self.pointer += 3

    def less_than(self, modes, ptr):
        (m1, m2, m3) = modes
        a = self.get(m1, self.code[ptr+1])
        b = self.get(m2, self.code[ptr+2])
        c = self.code[ptr+3]
        if a < b:
            self.code[c] = 1
        else:
            self.code[c] = 0
        self.pointer += 4

    def equals(self, modes, ptr):
        (m1, m2, m3) = modes
        a = self.get(m1, self.code[ptr+1])
        b = self.get(m2, self.code[ptr+2])
        c = self.code[ptr+3]
        if a == b:
            self.code[c] = 1
        else:
            self.code[c] = 0
        self.pointer += 4

    def end(self, modes, ptr):
        print(f"Program halted at: {ptr} with diagnostic code: {self.cout[-1]}")


if __name__ == "__main__":
    data = "3,225,1,225,6,6,1100,1,238,225,104,0,1102,88,66,225,101,8,125,224,101,-88,224,224,4,224,1002,223,8,223,101,2,224,224,1,224,223,223,1101,87,23,225,1102,17,10,224,101,-170,224,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1101,9,65,225,1101,57,74,225,1101,66,73,225,1101,22,37,224,101,-59,224,224,4,224,102,8,223,223,1001,224,1,224,1,223,224,223,1102,79,64,225,1001,130,82,224,101,-113,224,224,4,224,102,8,223,223,1001,224,7,224,1,223,224,223,1102,80,17,225,1101,32,31,225,1,65,40,224,1001,224,-32,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,2,99,69,224,1001,224,-4503,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1002,14,92,224,1001,224,-6072,224,4,224,102,8,223,223,101,5,224,224,1,223,224,223,102,33,74,224,1001,224,-2409,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,107,677,677,224,1002,223,2,223,1006,224,329,101,1,223,223,108,677,677,224,1002,223,2,223,1005,224,344,101,1,223,223,1007,677,677,224,1002,223,2,223,1006,224,359,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,374,1001,223,1,223,8,677,226,224,1002,223,2,223,1006,224,389,101,1,223,223,1108,677,677,224,1002,223,2,223,1005,224,404,1001,223,1,223,7,226,226,224,1002,223,2,223,1006,224,419,101,1,223,223,1107,677,677,224,1002,223,2,223,1005,224,434,101,1,223,223,107,226,226,224,102,2,223,223,1005,224,449,101,1,223,223,107,677,226,224,1002,223,2,223,1006,224,464,1001,223,1,223,8,226,677,224,102,2,223,223,1006,224,479,1001,223,1,223,108,677,226,224,102,2,223,223,1005,224,494,1001,223,1,223,1108,677,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,524,101,1,223,223,1008,226,226,224,1002,223,2,223,1006,224,539,101,1,223,223,1008,226,677,224,1002,223,2,223,1005,224,554,1001,223,1,223,7,226,677,224,1002,223,2,223,1005,224,569,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,584,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,1007,226,226,224,102,2,223,223,1006,224,614,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,629,101,1,223,223,108,226,226,224,102,2,223,223,1006,224,644,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,659,101,1,223,223,8,226,226,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226"
    code = [int(x) for x in data.split(",")]
    cin = [5]
    cout = []
    machine = IntMachine(code, cin, cout)
    machine.run()
    print(cout)