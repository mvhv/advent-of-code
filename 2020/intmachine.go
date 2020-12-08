package main

import "fmt"

// IntMachine is a virtual machine that runs an intcode
type IntMachine struct {
	programCounter int
	memory         []int
	inputChannel   chan int
	outputChannel  chan int
}

func (machine *IntMachine) getInstruction() int {
	return machine.memory[machine.programCounter]
}

func (machine *IntMachine) getPointer(mode, pointer int) int {
	switch mode {
	case 0:
		return machine.memory[pointer] // parameter mode
	case 1:
		return pointer // immediate mode
	default:
		return -1
	}
}

func parseInstruction(opcode int) (int, int, int, int) {
	op := opcode % 100
	mode1 := opcode / 100 % 10
	mode2 := opcode / 1000 % 10
	mode3 := opcode / 10000 % 10
	return op, mode1, mode2, mode3
}

func (machine *IntMachine) addition(mode1, mode2, mode3 int) {
	pc := machine.programCounter
	aPtr := machine.getPointer(mode1, pc+1)
	bPtr := machine.getPointer(mode2, pc+2)
	writePtr := machine.getPointer(mode3, pc+3)
	machine.memory[writePtr] = machine.memory[aPtr] + machine.memory[bPtr]
	machine.programCounter += 4
}

func (machine *IntMachine) multiplication(mode1, mode2, mode3 int) {
	pc := machine.programCounter
	aPtr := machine.getPointer(mode1, pc+1)
	bPtr := machine.getPointer(mode2, pc+2)
	writePtr := machine.getPointer(mode3, pc+3)
	machine.memory[writePtr] = machine.memory[aPtr] * machine.memory[bPtr]
	machine.programCounter += 4
}

func (machine *IntMachine) input(mode1, mode2, mode3 int) {
	pc := machine.programCounter
	writePtr := machine.getPointer(mode1, pc+1)
	machine.memory[writePtr] = <-machine.inputChannel
	machine.programCounter += 2
}

func (machine *IntMachine) output(mode1, mode2, mode3 int) {
	pc := machine.programCounter
	readPtr := machine.getPointer(mode1, pc+1)
	machine.outputChannel <- machine.memory[readPtr]
	machine.programCounter += 2
}

func (machine *IntMachine) jumpIfTrue(mode1, mode2, mode3 int) {
	pc := machine.programCounter
	boolPtr := machine.getPointer(mode1, pc+1)
	jumpPtr := machine.getPointer(mode2, pc+2)
	if machine.memory[boolPtr] == 0 {
		machine.programCounter += 3
	} else {
		machine.programCounter = machine.memory[jumpPtr]
	}
}

func (machine *IntMachine) jumpIfFalse(mode1, mode2, mode3 int) {
	pc := machine.programCounter
	boolPtr := machine.getPointer(mode1, pc+1)
	jumpPtr := machine.getPointer(mode2, pc+2)
	if machine.memory[boolPtr] == 0 {
		machine.programCounter = machine.memory[jumpPtr]
	} else {
		machine.programCounter += 3
	}
}

func (machine *IntMachine) lessThan(mode1, mode2, mode3 int) {
	pc := machine.programCounter
	lowPtr := machine.getPointer(mode1, pc+1)
	highPtr := machine.getPointer(mode2, pc+2)
	writePtr := machine.getPointer(mode3, pc+3)
	if machine.memory[lowPtr] < machine.memory[highPtr] {
		machine.memory[writePtr] = 1
	} else {
		machine.memory[writePtr] = 0
	}
	machine.programCounter += 4
}

func (machine *IntMachine) equals(mode1, mode2, mode3 int) {
	pc := machine.programCounter
	aPtr := machine.getPointer(mode1, pc+1)
	bPtr := machine.getPointer(mode2, pc+2)
	writePtr := machine.getPointer(mode3, pc+3)
	if machine.memory[aPtr] == machine.memory[bPtr] {
		machine.memory[writePtr] = 1
	} else {
		machine.memory[writePtr] = 0
	}
	machine.programCounter += 4
}

func (machine *IntMachine) halt(mode1, mode2, mode3 int) {
	pc := machine.programCounter
	fmt.Printf("Program halted at: %d with exit code: %d\n", pc, 1)
}

var opcodes = map[int]func(*IntMachine, int, int, int){
	1:  (*IntMachine).addition,
	2:  (*IntMachine).multiplication,
	3:  (*IntMachine).input,
	4:  (*IntMachine).output,
	5:  (*IntMachine).jumpIfTrue,
	6:  (*IntMachine).jumpIfFalse,
	7:  (*IntMachine).lessThan,
	8:  (*IntMachine).equals,
	99: (*IntMachine).halt}

func (machine *IntMachine) run() {
	for {
		op, mode1, mode2, mode3 := parseInstruction(machine.getInstruction())
		opcodes[op](machine, mode1, mode2, mode3)
		if op == 99 {
			break // halt program
		}
	}
}

func memClone(a []int) []int {
	b := make([]int, len(a))
	copy(b, a)
	return b
}

func machineLoop(code []int, number int) []IntMachine {
	machines := make([]IntMachine, number)

	// create machines
	for i := 0; i < number; i++ {
		machine := IntMachine{0, memClone(code), nil, nil}
		machines = append(machines, machine)
	}

	// link machines
	for i := 0; i < number; i++ {
		ch := make(chan int)
		machines[i].outputChannel = ch
		machines[i+1%number].inputChannel = ch
	}
	return machines
}

func permutations(arr []int) [][]int {
	res := [][]int{}
	permute(arr, len(arr))
	return res
}

func permute(arr []int, n int) {
	if n == 1 {
		tmp := make([]int, len(arr))
		copy(tmp, arr)
		res := append(res, tmp)
	} else {
		for i := 0; i < n; i++ {
			permute(arr, n-1)
			if n%2 == 1 {
				tmp := arr[i]
				arr[i] = arr[n-1]
				arr[n-1] = tmp
			} else {
				tmp := arr[0]
				arr[0] = arr[n-1]
				arr[n-1] = tmp
			}
		}
	}
}

func main() {
	data := []int{3, 8, 1001, 8, 10, 8, 105, 1, 0, 0, 21, 42, 55, 76, 89, 114, 195, 276, 357, 438, 99999, 3, 9, 1001, 9, 3, 9, 1002, 9, 3, 9, 1001, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 101, 5, 9, 9, 4, 9, 99, 3, 9, 102, 3, 9, 9, 101, 5, 9, 9, 1002, 9, 2, 9, 101, 4, 9, 9, 4, 9, 99, 3, 9, 102, 5, 9, 9, 1001, 9, 3, 9, 4, 9, 99, 3, 9, 1001, 9, 4, 9, 102, 5, 9, 9, 1001, 9, 5, 9, 1002, 9, 2, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 99, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 99, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1001, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 99, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 101, 1, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 3, 9, 1001, 9, 1, 9, 4, 9, 3, 9, 1002, 9, 2, 9, 4, 9, 3, 9, 102, 2, 9, 9, 4, 9, 3, 9, 101, 2, 9, 9, 4, 9, 99}
	machines := machineLoop(data, 5)

}
