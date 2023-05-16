#!/usr/bin/env python3

import math
import random
from tests.pokertest import Pokertest

class Testsuite:


    def banner(self):
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


    def run_all_tests(self, randomNumber):
        randomNumberString = str(randomNumber)
        try:
            run = self.run_test(randomNumberString)
        except:
            print("Run Test:                Failed!")
            run = 0
        longrun = self.long_run_test(randomNumberString,5)
        poker = Pokertest.pokerTest(randomNumberString, 4)
        #monobit = self.monobit_test(randomNumberString)
        equaldistribution = self.equal_distribution_test(randomNumberString)
        #disjointness = self.disjointness_test(randomNumberString)
        autocorrelation = self.autocorrelation_test(randomNumberString)
        passed_tests = run + longrun + poker + equaldistribution + autocorrelation
        print("\nTest passed:", passed_tests, "/5")

    '''
    To test a bit sequence for randomness with the Run test, 
    you first need to count the number of runs in the sequence. 
    A "run" is a consecutive group of the same bit value.
    We then calculate the expected number of runs and variance based on the number of bits 
    in the sequence and the probability of 1 bits (pi) in the sequence. 
    We also calculate the Z-score, which represents the ratio of the deviation 
    of the observed number of runs from the expected number of runs to the expected variance. 
    Finally, we compare the Z-score with the critical values (-1.96 and 1.96) 
    and determine whether the bit sequence is random or not.
    '''
    def run_test(self, bit_sequence):
        # Count the number of runs in the bit sequence
        num_runs = 1
        for i in range(len(bit_sequence)-1):
            if bit_sequence[i] != bit_sequence[i+1]:
                num_runs += 1

        # Calculate the expected number of runs and variance
        n = len(bit_sequence)
        pi = sum(int(bit) for bit in bit_sequence) / n
        expected_runs = 1 + 2*pi*(n-1)
        variance = (2*n-1)*(2*pi*(1-pi))
        #print("expected runs = ", expected_runs)
        #print("runs count = ", num_runs)

        # Calculate the Z-score
        z_score = (num_runs - expected_runs) / variance**0.5

        # Compare the Z-score with the critical values
        if z_score < -1.96 or z_score > 1.96:
            #print("z score =",z_score)
            print("Run Test:                Failed!")
            return False
            
        else:
            #print("z score =",z_score)
            print("Run Test:                Passed!")
            return True


    '''
    The Run test is a simple test that 
    checks the proportion of runs of length 1 and 2 (sequences of consecutive 0's or 1's),
    while the Long Run test is a more powerful test 
    that checks the number of consecutive runs (sequences of consecutive 0's or 1's) 
    of a given length k.
    '''
    def long_run_test(self, bit_sequence, k):
        # Count the number of runs of length k in the bit sequence
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

        # Calculate the Z-score
        z_score = (num_runs - expected_runs) / math.sqrt(variance)

        # Compare the Z-score with the critical values
        if z_score < -1.96 or z_score > 1.96:
            print("Long Run Test:           Failed!")
            return False
        else:
            print("Long Run Test:           Passed!")
            return True


    '''
    The function first divides the sequence into blocks 
    of k bits each, and counts the number of occurrences 
    of each possible k-bit pattern in these blocks. 
    It then calculates the test statistic x, using these 
    frequencies and the total number of blocks m. Finally, 
    it calculates the p-value of the test statistic and compares 
    it to a significance level alpha of 0.01, to determine 
    whether to accept or reject the null hypothesis that the 
    sequence is random.
    '''
    '''
    def poker_test(self, bit_sequence):
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
    '''        
    
    '''
    (Same as equal distribution test)
    The Monobit test is a statistical test used to test 
    the randomness of a binary bit sequence. 
    It checks whether the proportion of 1s and 0s 
    in the bit sequence is approximately equal.
    '''
    def monobit_test(self, bit_sequence):
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

    
    '''
    The Disjointness test is a statistical test 
    used to test the independence and randomness of 
    two binary bit sequences. The test checks whether 
    the two sequences are independent of each other, 
    meaning that the values of one sequence do not 
    provide any information about the values of the other sequence.
    '''
    def disjointness_test(self, seq1, seq2):
        # Check that the two sequences have the same length
        if len(seq1) != len(seq2):
            #print("The sequences are not of equal length")
            return

        # Calculate the number of times the sequences disagree
        num_disagreements = 0
        for i in range(len(seq1)):
            if seq1[i] != seq2[i]:
                num_disagreements += 1

        # Calculate the expected number of disagreements
        n = len(seq1)
        p = 0.5
        expected_disagreements = n * p * p

        # Calculate the variance
        variance = n * p * (1-p) * 2

        # Calculate the Z-score
        z_score = (num_disagreements - expected_disagreements) / math.sqrt(variance)

        # Compare the Z-score with the critical values
        if z_score < -1.96 or z_score > 1.96:
            print("Disjointness Test:           Failed!")
            return False
        else:
            print("Disjointness Test:           Passed!")
            return True

    
    '''
    The function first calculates the autocorrelation 
    coefficients of the sequence, up to a maximum lag of k_max, 
    which is half the length of the sequence. 
    It then calculates the test statistic t, 
    using these autocorrelation coefficients and the sum of 
    the bits in the sequence. Finally, it calculates the p-value 
    of the test statistic and compares it to a significance level 
    alpha of 0.01, to determine whether to accept or reject 
    the null hypothesis that the sequence is random.
    '''
    def autocorrelation_test(self, bit_sequence):
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


    def random_bits(self, num_bits):
        bits = []
        for i in range(num_bits):
            bits.append(str(random.choice([0, 1])))
        return ''.join(bits)


    '''
    Asks the user to enter a valid bit sequence and returns it as a string of 0's and 1's.
    '''
    def get_valid_bit_sequence(self):
        
        while True:
            bit_sequence = input("Please enter a bit sequence (a string of 0's and 1's):\n")
            if all(bit in ['0', '1'] for bit in bit_sequence):
                return bit_sequence
            else:
                print("Invalid input! The bit sequence should only contain 0's and 1's.\n")

'''
if __name__ == '__main__':
    
    testsuite = TestSuite()
    testsuite.banner()
    
    #rand1 = testsuite.random_bits(256)
    #rand2 = '1010100000010001000100010001001001110110110010010100000111100100111001101100100000000010010101100011010101010011110111100100001101001111010100000010110110001110100001100001010101111110100000010001010101010100010011010100111111000010010111111110000110101011'

    randInput = testsuite.get_valid_bit_sequence()
   

    print('\n##################################################################################################################\n')

    testsuite.run_all_tests(randInput)

    print('\n##################################################################################################################\n')
'''    
