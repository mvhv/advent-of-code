def in_range(num, low, high):
    return num >= low and num <= high

def six_digits(num):
    return len(str(num)) == 6

def two_adjacent(num):
    chars = str(num)
    for i in range(len(chars) - 1):
        if chars[i] == chars[i+1]:
            return True
    return False

def non_decreasing(num):
    chars = str(num)
    for i in range(len(chars) - 1):
        if int(chars[i]) > int(chars[i+1]):
            return False
    return True

def main(data):
    data = data.split("-")
    low = int(data[0])
    high = int(data[1])
    valid = 0
    for i in range(low, high+1):
        if six_digits(i) and two_adjacent(i) and non_decreasing(i):
            valid += 1
    return valid

data = "359282-820401"

print(main(data))