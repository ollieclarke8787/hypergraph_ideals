# Hypergraph Ideals
Python module for working with polynomials, hypergraph ideals and S-polynomials.
This code is written for Python version 3.8


## Notes on running the code

### Results

After runnning the code, the output has been collected in the output.txt file.
In particular, the main result is that the number of exceptions is zero.
The code took around 11 hours to run on a Intel i5-8350U CPU @ 1.70GHz with 8GB of physical memory


### What does the code calculate?

Running polynomial.py from the command line will perform the following very specific calculation:

0) We consider the 6x6 matrix X of variables with rows {0,...,5} and cols {0,...,5}
1) For each pair of minors m1 = [R1 | C1] and m2 = [R2 | C2] where R1 and C1 are 4-subsets of {0,...,5} and R2 and C2 are 3-subsets of {0,...,5}
2) If the leading diagonal terms of m1 and m2 are coprime then the program outputs that the reduction of the S-polynomial 'trivially holds'
3) Otherwise construct a list G of all of the following polynomials:
- All 4-minors of X
- All 3 minors of X on columns spanned by C2, e.g. if C2 = {0,2,3} then we take all 3-minors on columns {0,1,2,3} since 1 is contained in the span of {0,2,3}
4) Let S = S(m1, m2) be the S-polynomial of m1 and m2
5) Define the lexicographic term order 'lex' for all polynomials where x_(1,1) < x_(1,2) < .. < x_(1,6) < x_(2,1) < .. < x_(6,6)
6) Apply the dividion algorithm to S dividing by the polynomials G with respect to the term order lex *
7) If the result of the division algorithm is zero then we output 'True'
8) If the result of the division algorithm is non-zero we output 'False' and record m1 and m2 as exceptions
9) After completing all 90,000 cases for m1 and m2, we print the number of excpetions

(*) Note that the division algorithm is this module performs a division if and only if the leading term of the current remainder is divisible by the leading term of some polynomial in G. This means that if G is a Groebner basis, this algorithm does not return the normal form of the polynonial with respect to that Groebner basis. However this algorithm is sufficient for Buchberger's criterion since a polynomial reduces to zero with this algorithm if and only if it reduces to zero using the conventional division algorithm.

If the code is also supplied the command line argument '-v' then all commands will be verbose. This means that the program will print out the division algorithm process. This is not recommended since the output will become very long!

## Contents of the module

The polynomial.py module introduces the following objects:
- Monomial
- Polynomial
- VarMatrix
- SPolyCheck

And the following functions:
- div_alg
- s_poly

Detailed documentation will be added later.



