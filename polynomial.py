#polynomials with integer coefficients

from itertools import combinations
import sys


class Monomial:
    def __init__(self, coeff, exp):
        self.exp = exp #dict
        self.coeff = coeff #integer

    def __mul__(self, other):
        #assume the monomials are defined over the same ring
        new_coeff = self.coeff * other.coeff
        new_exp = {}
        for e in self.exp:
            new_exp[e] = self.exp[e] + other.exp[e]
        return Monomial(new_coeff, new_exp)
    
    def __repr__(self):
        if self.coeff == 1:
            s = ""
        elif self.coeff == -1:
            s = "-"
        else:
            s = "{}".format(self.coeff)
        
        for e in self.exp:
            if self.exp[e] == 1:
                s += "{}".format(e)
            elif self.exp[e] != 0:
                s += "{}^{}".format(e, self.exp[e])

        if s == "":
            return "0"
        
        return s

    def __neg__(self):
        new_coeff = self.coeff * (-1)
        new_exp = {}
        for e in self.exp:
            new_exp[e] = self.exp[e]
        return Monomial(new_coeff, new_exp)

    def __add__(self, other):

        new_coeff = self.coeff + other.coeff
        new_exp = self.exp
        return Monomial(new_coeff, new_exp)

    def divides(self, other):
        #quotient other / self
        # if doesn't exist then return False
        quotient_coeff = other.coeff / self.coeff
        quotient_exp = {}
        for e in self.exp:
            if self.exp[e] > other.exp[e]:
                return False
            else:
                quotient_exp[e] = other.exp[e] - self.exp[e]
        return Monomial(quotient_coeff, quotient_exp)

    def gcd(self, other):
        #get gcd monomial with coeff 1
        new_coeff = 1
        new_exp = {}
        for e in self.exp:
            new_exp[e] = min(self.exp[e], other.exp[e])
        return Monomial(new_coeff, new_exp)

    def __eq__(self, other):
        return self.coeff == other.coeff and self.exp == other.exp
    
class Polynomial:

    def __init__(self, monomial_list = []):
        self.monomial_list = monomial_list
        self._clean()

    def __repr__(self):

        if len(self.monomial_list) == 0:
            return "0"
        else:
            s = ""
            for index, m in enumerate(self.monomial_list):
                if m.coeff > 0 and index > 0:
                    s += "+" + m.__repr__()
                else:
                    s += m.__repr__()
            return s
            
    
    def _clean(self):
        #remove duplicate copies of monomials that have the same coeff

        if len(self.monomial_list) == 1:
            #check the coeff is non-zero
            if self.monomial_list[0].coeff == 0:
                self.monomial_list.pop(0)
        elif len(self.monomial_list) >= 2:

            #remove duplicate monomials
            #after collecting duplicate exponents
            #remove any monomials with zero coeff
            
            index_1 = 0
            index_2 = 1

            while index_1 < len(self.monomial_list) - 1:

                m1 = self.monomial_list[index_1]
                m2 = self.monomial_list[index_2]

                if m1.exp == m2.exp:
                    self.monomial_list[index_1] = m1 + m2
                    m1 = self.monomial_list[index_1]
                    
                    self.monomial_list.remove(m2)

                    if index_2 == len(self.monomial_list):
                        if m1.coeff == 0:
                            #remove zero coeff monomials
                            self.monomial_list.remove(m1)
                            index_2 = index_1 + 1
                        else:
                            index_1 += 1
                            index_2 = index_1 + 1
                else:
                    if index_2 == len(self.monomial_list)-1:
                        if m1.coeff == 0:
                            #remove zero coeff monomials
                            self.monomial_list.remove(m1)
                            index_2 = index_1 + 1
                        else:
                            index_1 += 1
                            index_2 = index_1 + 1
                    else:
                        index_2 += 1
    
    def __add__(self, other):

        new_monomial_list = []
        for m in self.monomial_list:
            new_monomial_list.append(m)
        for m in other.monomial_list:
            new_monomial_list.append(m)
        new_poly = Polynomial(new_monomial_list)
        return new_poly

    def __sub__(self, other):
        new_monomial_list = []
        for m in self.monomial_list:
            new_monomial_list.append(m)
        for m in other.monomial_list:
            new_monomial_list.append(-m)
        new_poly = Polynomial(new_monomial_list)
        return new_poly
    
    def __mul__(self, other):
        new_monomial_list = []
        for m1 in self.monomial_list:
            for m2 in other.monomial_list:
                new_monomial_list.append(m1*m2)
        new_poly = Polynomial(new_monomial_list)
        return new_poly

    def _get_lower(self, m1, m2, order):
        for index in order:
            if m1.exp[index] > m2.exp[index]:
                return m1
            elif m2.exp[index] > m1.exp[index]:
                return m2
        #otherwise same exponent
        return m1
    
    def lead_term(self, order):
        #get the lead term wrt lex
        #  order = [x,y,z] means x < y < z
        #  lead term is the smallest term
        if len(self.monomial_list) == 0:
            exp = {}
            for e in order:
                exp[e] = 0
            return Monomial(0, exp)
        
        highest_monomial = self.monomial_list[0]
        for m in self.monomial_list[1:]:
            highest_monomial = self._get_lower(highest_monomial, m, order)
        return highest_monomial

    def __eq__(self, other):
        for m1 in self.monomial_list:
            found = False
            for m2 in other.monomial_list:
                if m1 == m2:
                    found = True
            if not found:
                return False
        for m1 in other.monomial_list:
            found = False
            for m2 in self.monomial_list:
                if m1 == m2:
                    found = True
            if not found:
                return False
        return True
        
    
        
        
    
class VarMatrix:

    def __init__(self, size):
        """
        size = (rows, cols)
        """
        #size of matrix
        self.size = size
        self.rows = size[0]
        self.cols = size[1]

        #indices
        self.indices = {}
        for i in range(self.rows):
            for j in range(self.cols):
                self.indices[(i,j)] = "x_({},{})".format(i,j)

        #monomials
        self.monomials = {}
        for index in self.indices:
            exp = {}
            for e in self.indices:
                exp[self.indices[e]] = 0
            exp[self.indices[index]] = 1
            self.monomials[index] = Polynomial([Monomial(1, exp)])

        #matrix of variables
        self.matrix = []
        for i in range(self.rows):
            r = []
            for j in range(self.cols):
                r.append(self.monomials[(i,j)])
            self.matrix.append(r)

        #order of exponents
        self.order = []
        for i in range(self.rows):
            for j in range(self.cols):
                self.order.append(self.indices[(i,j)])
        
    def __repr__(self):
        return "{}x{} matrix of variables".format(self.rows, self.cols)


    def minor(self, R, C):
        #get minor on rows R and cols C:

        if len(R) == 1:
            r = R[0]
            c = C[0]
            return self.matrix[r][c]
        else:
            #expand determinant along first row
            r = R[0]
            new_R = R[1:]
            determinant = Polynomial([])
            for index, c in enumerate(C):
                new_C = C[:index] + C[index+1:]
                next_minor = self.matrix[r][c]*self.minor(new_R, new_C)
                if index % 2 == 0:
                    determinant +=  next_minor
                else:
                    determinant -= next_minor
            return determinant

    def minors(self, R, C, size):
        #get all minors on rows and cols with fixes size
        
        list_minors = []
        for sub_R in combinations(R, size):
            for sub_C in combinations(C, size):
                list_minors.append(self.minor(sub_R, sub_C))
        return list_minors

def div_alg(poly, division_polys, order, verbose = False):
    #basic division algorithm that only reduces leading terms
    #note this is sufficient for Buchberger's algorithm
    
    remainder = poly
    performed_division = True

    if verbose:
        print("Division algorithm")
        print("{}".format(poly))
    
    while performed_division:
        performed_division = False
        for d in division_polys:
            quotient = d.lead_term(order).divides(remainder.lead_term(order))
            if quotient:
                performed_division = True
                Q = Polynomial([quotient])
                if verbose:
                    print("-({})*({})".format(Q,d))
                remainder -= Q*d
    if verbose:
        print("= {}".format(remainder))
    return remainder

def s_poly(poly1, poly2, order):

    m1 = poly1.lead_term(order)
    m2 = poly2.lead_term(order)
    
    g = m1.gcd(m2)
    q1 = Polynomial([g.divides(m2)])
    q2 = Polynomial([g.divides(m1)])

    return poly1*q1 - poly2*q2
    



class CheckSPoly:
    
    def __init__(self, minor1, minor2):
        #Consider the ideal generated by:
        # > all minors of size minor1
        # > all minors of size minor2 that lie in the span of its columns
        #
        #E.g. if minor2 is on cols 2,4,5 then we include all 3 minors on
        #     columns 2,3,4,5
        #
        #note we take minors from all rows
        
        self.m1_rows = minor1[0]
        self.m1_cols = minor1[1]
        self.m1_size = len(minor1[0])
        
        self.m2_rows = minor2[0]
        self.m2_cols = minor2[1]
        self.m2_size = len(minor2[0])

        var_matrix_rows = max(self.m1_rows + self.m2_rows)+1
        var_matrix_cols = max(self.m1_cols + self.m2_cols)+1
        self.matrix = VarMatrix((var_matrix_rows, var_matrix_cols))

        self.minor1 = self.matrix.minor(self.m1_rows, self.m1_cols)
        self.minor2 = self.matrix.minor(self.m2_rows, self.m2_cols)
        
        self.gens = []
        self.gens += self.matrix.minors(range(var_matrix_rows), range(var_matrix_cols), self.m1_size)
        self.gens += self.matrix.minors(range(var_matrix_rows), range(min(self.m2_cols), max(self.m2_cols)+1), self.m2_size)

        self.s_poly = s_poly(self.minor1, self.minor2, self.matrix.order)

    def reduction_holds(self, verbose = False):
        remainder = div_alg(self.s_poly, self.gens, self.matrix.order, verbose)
        if remainder == Polynomial([]):
            return True
        else:
            return False
    

        
    
if __name__ == "__main__":
    if '-v' in sys.argv:
        verbose = True
    else:
        verbose = False
    
    matrix_rows = 6
    matrix_cols = 6

    exceptions = []
    
    for R1 in combinations(range(matrix_rows),4):
        for C1 in combinations(range(matrix_cols),4):
            minor1 = (R1, C1)
            
            for R2 in combinations(range(matrix_rows),3):
                for C2 in combinations(range(matrix_cols),3):
                    minor2 = (R2, C2)

                    #check there is non-trivial reduction
                    LT1 = []
                    LT2 = []
                    for i in range(4):
                        if i < 3:
                            LT2.append((R2[i], C2[i]))
                        LT1.append((R1[i], C1[i]))
                    
                    has_intersection = False
                    for x in LT2:
                        if x in LT1:
                            has_intersection = True
                            break

                    if not has_intersection:
                        print("{}, {} : trivially holds".format(minor1, minor2))
                    else:
                        checker = CheckSPoly(minor1, minor2)
                        holds = checker.reduction_holds(verbose)
                        print("{}, {} : {}".format(minor1, minor2, holds))
                        if not holds:
                            exceptions.append((minor1, minor2))
    print("")
    print("Number of exptions: {}".format(len(exceptions))
    
                    
    
        
        
