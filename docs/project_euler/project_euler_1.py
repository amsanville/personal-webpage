'''
Calculates the sum of all integers divisible by 3 or 5 below 1000 using a for loop and modular arithemetic. Prints the result to the console when finished.
'''
def main():
    total = 0
    for i in range(1, 1001):
        if (i % 3 == 0 or i % 5 == 0):
            total += i
    print("The sum of all integers divisible by 3 or 5 below 1000: " + str(total))

if __name__ == "__main__":
    main()