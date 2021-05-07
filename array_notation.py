"""
A tool for exploring interval ratios in microtonal music,
this program takes a given fraction and decomposes it into its
prime factors, returning it in array notation - as a list of
powers of successive prime numbers.
For example, since 3/2 is equal to 2^-1 * 3^1,
    its array notation is [-1, 1].
For example, since 7/8 is equal to 2^-3 * 7^1,
    its array notation is [-3, 0, 0, 1]
This program searches for prime factors only up to 53.
"""

primes_list = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53]

def factor_array(number, input_array = [0 for x in range(16)]):
    """
    A helper function for array_notation().
    Decompose number into its prime factors and return as a list.
    """
    output_array = [x for x in input_array]
    # check if number is divisible by a factor contained in primes_list
    for factor in range(0, 16):
        # if number is divisible, update input_array, call factor_array() again
        if number % primes_list[factor] == 0:
            output_array[factor] += 1
            return factor_array(number / primes_list[factor], output_array)
    
    # if number cannot be further divided, return output_array
    return output_array
    
def array_notation(num = 1, denom = 1, strip_trailing_zeroes = True):
    """
    Return a given fraction in array notation.
    """
    output_array = [0 for x in range(16)]
    # decompose numerator and denominator using factor_array()
    num_array, denom_array = factor_array(num), factor_array(denom)
    
    # represent factors of the numerator as positive integers and factors of the denominator as negative integers.
    for factor in range(0, 16):
        output_array[factor] += num_array[factor]
        output_array[factor] -= denom_array[factor]
    
    # if necessary, trim output_array to only include up to the largest prime factor
    if strip_trailing_zeroes:
        while output_array[-1] == 0:
            output_array.pop()
    
    return output_array