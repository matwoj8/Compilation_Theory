# assignment operators
# binary operators
# transposition

A = zeros(7);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
C = eye(10);   # create 10x10 matrix filled with ones on diagonal and zeros elsewhere

C = -A;     # assignment with unary expression
C = B' ;    # assignment with matrix transpose
C = A+B ;   # assignment with binary addition
C = A-B ;   # assignment with binary substraction
C = A*B ;   # assignment with binary multiplication
C = A/B ;   # assignment with binary division
C = A.+B ;  # add element-wise A to B
C = A.-B ;  # substract B from A 
C = A.*B ;  # multiply element-wise A with B
C = A./B ;  # divide element-wise A by B

C += B ;  # add B to C 
C -= B ;  # substract B from C 
C *= A ;  # multiply A with C
C /= A ;  # divide A by C



