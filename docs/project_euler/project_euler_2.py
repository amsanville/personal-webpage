'''
Calculates the sum of all even Fibonacci numbers below 4 million.
'''
def main():
    # Initialize
    fib0 = 0;
    fib1 = 1;
    total = 0;

    # Loop while under 4 million
    while(fib1 < 4*(10**6)):
        # Check if the current Fibonacci number is even
        if(fib1 % 2 == 0):
            total += fib1

        # Calculate the next Fibonacci number
        temp = fib1
        fib1 += fib0
        fib0 = temp

    # Print the result
    print("Total: " + str(total))

if __name__=='__main__':
    main()