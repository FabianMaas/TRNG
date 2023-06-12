#!/usr/bin/env python3
"""
This file contains a test suite for evaluating the randomness of bit sequences.
It includes several statistical tests commonly used to assess the quality of random number generators.

Note: This file assumes that the bit sequence is represented as a list of integers, 
where 0 represents a zero bit and 1 represents a one bit.
"""


import math
import random


class TestSuite:
    """
    A class that represents a test suite for evaluating the randomness of bit sequences.

    Methods:
        run_all_tests(bit_arr): Runs all the tests in the test suite on the given bit sequence.
        __banner(): Prints a banner with the title of the test suite.
        __run_test(bit_sequence): Performs the run test to check the randomness of a bit sequence.
        __long_run_test(bit_sequence, k): Performs the long run test to check the randomness of a bit sequence.
        __poker_test(bit_sequence): Performs the poker test to check the randomness of a bit sequence.
        __monobit_test(bit_sequence): Performs the monobit test to to check the randomness of a bit sequence.
        __equal_distribution_test(bit_sequence): Performs the equal distribution test to check the randomness of a bit sequence.
        __autocorrelation_test(bit_sequence): Performs the autocorrelation test to check the randomness of a bit sequence.
        __get_valid_bit_sequence(): Asks the user to enter a valid bit sequence and returns it as a string of 0's and 1's.
    """


    def run_all_tests(self, bit_arr):
        """
        Runs a series of tests on a bit sequence.

        Args:
            bit_arr (list): A list of bits representing the bit sequence.

        Returns:
            bool: True if the sequence passes at least two tests, False otherwise.

        Prints the test bit sequence and performs the following tests on it:
        1. Run Test: Checks if the sequence contains a run of consecutive bits.
        2. Long Run Test: Checks if the sequence contains a long run of consecutive bits.
        3. Poker Test: Checks the distribution of different bit patterns in the sequence.
        4. Equal Distribution Test: Checks if the number of ones and zeros in the sequence is approximately equal.
        5. Autocorrelation Test: Measures the correlation between consecutive bits in the sequence.

        The number of tests passed is calculated by adding the results of each test.
        If the number of passed tests is greater than or equal to 3, the function returns True.
        Otherwise, it returns False.
        """
        bit_sequence = ''.join(bit_arr)
        print("test bit_sequence =",bit_sequence)
        try:
            run = self.run_test(bit_sequence)
        except:
            print("Run Test:                Failed!")
            run = 0
        longrun = self.long_run_test(bit_sequence,  int(len(bit_sequence)/2))
        poker = self.poker_test(bit_sequence)
        #monobit = self.monobit_test(randomNumberString)
        equaldistribution = self.equal_distribution_test(bit_sequence)
        autocorrelation = self.autocorrelation_test(bit_sequence)
        passed_tests = run + longrun + poker + equaldistribution + autocorrelation
        print("\nTest passed:", passed_tests, "/5")
        if (passed_tests >= 3) :
            return True
        else:
            return False
        
        
    def banner(self):
        """
        Prints a banner with a custom design.

        The banner is displayed using ASCII art and includes a custom design.
        It consists of a series of lines containing characters forming the design.
        The banner is printed to the console, followed by a line of hashtags for separation.
        """
        banner = "\n".join([
            '████████ ██████  ███    ██  ██████      ████████ ███████ ███████ ████████     ███████ ██    ██ ██ ████████ ███████',
            '   ██    ██   ██ ████   ██ ██              ██    ██      ██         ██        ██      ██    ██ ██    ██    ██',
            '   ██    ██████  ██ ██  ██ ██   ███        ██    █████   ███████    ██        ███████ ██    ██ ██    ██    █████',
            '   ██    ██   ██ ██  ██ ██ ██    ██        ██    ██           ██    ██             ██ ██    ██ ██    ██    ██',
            '   ██    ██   ██ ██   ████  ██████         ██    ███████ ███████    ██        ███████  ██████  ██    ██    ███████',
            '┌┬┐┌─┐┌┬┐┌─┐  ┌┐ ┬ ┬  ╦ ╦┌─┐┬  ┬┌─┐╔╦╗┌─┐┌─┐┬ ┬',
            '│││├─┤ ││├┤   ├┴┐└┬┘  ║║║├─┤└┐┌┘├┤  ║ ├┤ │  ├─┤',
            '┴ ┴┴ ┴─┴┘└─┘  └─┘ ┴   ╚╩╝┴ ┴ └┘ └─┘ ╩ └─┘└─┘┴ ┴'
        ])
        print()
        print(banner)
        print('\n##################################################################################################################\n')


    def run_test(self, bit_sequence):
        """
        Performs the runs test to check the randomness of a bit sequence.\n
        The run test examines the number of runs and the imbalance of '1' runs in the bit sequence. A run
        is defined as a consecutive sequence of the same bit. The test compares the observed number of runs
        and '1' runs to the expected values based on a random sequence.\n
        Args:
            bit_sequence (str): A sequence of bits represented as a string of '0's and '1's.
        
        Returns:
            bool: True if the sequence passes the runs test for randomness, False otherwise.
        """
        n = len(bit_sequence)

        # Count the total number of runs and the number of runs of '1's
        total_runs = 1
        ones_runs = 0
        for i in range(1, n):
            if bit_sequence[i] != bit_sequence[i - 1]:
                total_runs += 1
                if bit_sequence[i] == '1':
                    ones_runs += 1
    
        # Calculate the expected number of runs and the standard deviation
        expected_runs = (2 * len(bit_sequence) - 1) / 3
        std_deviation = (16 * len(bit_sequence) - 29) / 90 ** 0.5

        # Calculate the Z-score
        z_score = (ones_runs - expected_runs) / std_deviation

        # Check if the Z-score is within the range of -1.96 to 1.96 (95% confidence level)
        if -1.96 <= z_score <= 1.96:
            print("run test passed")
            return True
        else:
            print("run test nooot passed")
            return False


    def long_run_test(self, bit_sequence, k):
        """
        Performs the long run test to check for an excessive number of runs of length k in the bit sequence.\n
        The long run test examines the number of runs of length k in the bit sequence and compares it to the expected
        number of runs. If the observed number of runs falls outside the expected range, the test fails.

        Args:
            bit_sequence (str): A sequence of bits represented as a string of '0's and '1's.
            k (int): The length of runs to be tested.

        Returns:
            bool: True if the number of runs of length k is within the expected range, False otherwise.
        """        
        num_runs = 0
        for i in range(len(bit_sequence)-k+1):
            if bit_sequence[i:i+k] in ['0'*k, '1'*k]:
                num_runs += 1

        # Calculate the expected number of runs
        n = len(bit_sequence)
        p = 1 / (2**k)
        expected_runs = (n - k + 3) * p

        # Calculate the variance
        variance = (n-k+3) * p * (1-p)
        # print(variance)
        if(variance == 0):
            return False
        # Calculate the Z-score
        z_score = (num_runs - expected_runs) / math.sqrt(variance)

        # Compare the Z-score with the critical values
        if z_score < -1.96 or z_score > 1.96:
            print("Long Run Test:           Failed!")
            return False
        else:
            print("Long Run Test:           Passed!")
            return True


    def poker_test(self, bit_sequence):
        """
        Performs the poker test to check for non-randomness in a bit sequence.\n
        The poker test examines the distribution of 4-bit patterns (poker hands) in the bit sequence
        and compares it to the expected distribution. If the distribution significantly deviates from
        the expected distribution, the test fails.\n
        Args:
            bit_sequence (str): A sequence of bits represented as a string of '0's and '1's.

        Returns:
            bool: True if the bit sequence passes the poker test, False otherwise.
        """
        counts = [0] * 16
        for i in range(0, len(bit_sequence), 4):
            bits = bit_sequence[i:i+4]
            index = int(bits, 2)
            counts[index] += 1
        N = len(bit_sequence) / 4
        x2 = 0
        for i in range(16):
            x2 += counts[i]**2
        x2 *= 16 / N
        x2 -= N
        s = math.sqrt(2 * 15 * N / 37)
        t = abs(x2 - 16 * N / 37) / s
        p_value = math.erfc(t / math.sqrt(2))
        if p_value >= 0.01:
            #print("p-value:",p_value)
            print("Poker Test:              Passed!")
            return True
        else:
            #print("p-value:",p_value)
            print("Poker Test:              Failed!")
            return False
            
    
    def monobit_test(self, bit_sequence):
        """
        Performs the monobit test to check for bias in a bit sequence.\n
        The monobit test examines the proportion of '1's in the bit sequence and compares it to the
        expected proportion (0.5). If the proportion significantly deviates from 0.5, the test fails,
        indicating bias in the sequence.

        Args:
            bit_sequence (str): A sequence of bits represented as a string of '0's and '1's.

        Returns:
            bool: True if the bit sequence passes the monobit test, False otherwise.
        """
        # Count the number of 1s in the bit sequence
        num_ones = sum(int(bit) for bit in bit_sequence)

        # Calculate the proportion of 1s in the bit sequence
        n = len(bit_sequence)
        prop_ones = num_ones / n

        # Calculate the test statistic
        s = (prop_ones - 0.5) / math.sqrt(n)

        # Compare the test statistic with the critical values
        if s < -1.96 or s > 1.96:
            print("Monobit Test:            Failed!")
            return False
        else:
            print("Monobit Test:            Passed!")
            return True
    

    def equal_distribution_test(self, bit_sequence):
        """
        Performs the equal distribution test to check for bias in a bit sequence.\n
        The equal distribution test examines the proportion of '1's in the bit sequence and compares it to the
        expected proportion (0.5). If the proportion significantly deviates from 0.5, the test fails,
        indicating bias in the sequence.

        Args:
            bit_sequence (str): A sequence of bits represented as a string of '0's and '1's.

        Returns:
            bool: True if the bit sequence passes the equal distribution test, False otherwise.
        """
        # Count the number of 0s and 1s in the bit sequence
        n0 = bit_sequence.count('0')
        n1 = bit_sequence.count('1')
        #print("0 count = ", n0)
        #print("1 count = ", n1)

        length = len(bit_sequence)

        percentageOfOnes =  n0 / length

        # Random if Percentage deviation is less then 5 %
        #print("percentageOfOnes =",percentageOfOnes)
        if(percentageOfOnes > 0.45 and percentageOfOnes < 0.55):
            print("Equal Distribution Test: Passed!")
            return True
        else:
            print("Equal Distribution Test: Failed!")
            return False


    def autocorrelation_test(self, bit_sequence):
        """
        Performs the autocorrelation test to check for serial dependence in a bit sequence.\n
        The autocorrelation test examines the serial dependence of the bit sequence by calculating
        the autocorrelation coefficients and a test statistic. It then compares the test statistic to
        a critical value to determine whether the sequence is serially independent.
        Args:
            bit_sequence (str): A sequence of bits represented as a string of '0's and '1's.

        Returns:
            bool: True if the bit sequence passes the autocorrelation test, False otherwise.
        """
        n = len(bit_sequence)
        k_max = int(n / 2)
        s = sum([int(bit_sequence[i]) * 2 - 1 for i in range(n)])

        # Calculate the autocorrelation coefficients
        r = [0] * (k_max + 1)
        for k in range(k_max + 1):
            for i in range(n - k):
                r[k] += (int(bit_sequence[i]) * 2 - 1) * (int(bit_sequence[i + k]) * 2 - 1)
            r[k] /= (n - k)

        # Calculate the test statistic
        t = s / ((n / 2) ** 0.5)
        for k in range(1, k_max + 1):
            t += (s / ((n / 2) ** 0.5)) * r[k] * ((1 - k / (k_max + 1)) ** 0.5)

        # Calculate the p-value
        p = math.erfc(abs(t) / (2 ** 0.5))

        # Determine whether to accept or reject the null hypothesis
        alpha = 0.01
        if p >= alpha:
             print("Autocorrelation Test:    Passed!")
             return True
        else:
            print("Autocorrelation Test:    Failed!")
            return False


    def get_valid_bit_sequence(self):
        '''
        Asks the user to enter a valid bit sequence and returns it as a string of 0's and 1's.
        '''
        while True:
            bit_sequence = input("Please enter a bit sequence (a string of 0's and 1's):\n")
            if all(bit in ['0', '1'] for bit in bit_sequence):
                return bit_sequence
            else:
                print("Invalid input! The bit sequence should only contain 0's and 1's.\n")


if __name__ == '__main__':
    
    testsuite = TestSuite()
    testsuite.banner()
    randInput = testsuite.get_valid_bit_sequence()
   
    print('\n##################################################################################################################\n')

    testsuite.run_all_tests(randInput)

    print('\n##################################################################################################################\n')
    