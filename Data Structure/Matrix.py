import random
class Array2D :   # No need to touch this class.
    # Creates a 2-D array of size numRows x numCols.
    def __init__( self, numRows, numCols ):
        # Create a 1-D array to store an array reference for each row.
        self._theRows = [None] * numRows

        # Create the 1-D arrays for each row of the 2-D array.
        for i in range( numRows ) :
            self._theRows[i] = [None] * numCols

    # Returns the number of rows in the 2-D array.
    def numRows( self ):
        return len( self._theRows )

    # Returns the number of columns in the 2-D array.
    def numCols( self ):
         return len( self._theRows[0] )

    # Clears the array by setting every element to the given value.
    def clear( self, value ):
        for row in range( self.numRows() ):
            for col in range(self.numCols()):
                self[row, col] = value
                
    # Gets the contents of the element at position [i, j]
    def __getitem__( self, ndxTuple ):
        assert len(ndxTuple) == 2, "Invalid number of array subscripts."
        row = ndxTuple[0]
        col = ndxTuple[1]
        assert row >= 0 and row < self.numRows() \
        and col >= 0 and col < self.numCols(), \
        "Array subscript out of range."
        the1dArray = self._theRows[row]
        return the1dArray[col]

    # Sets the contents of the element at position [i,j] to value.
    def __setitem__( self, ndxTuple, value ):
        assert len(ndxTuple) == 2, "Invalid number of array subscripts."
        row = ndxTuple[0]
        col = ndxTuple[1]
        assert row >= 0 and row < self.numRows() \
        and col >= 0 and col < self.numCols(), \
        "Array subscript out of range."
        the1dArray = self._theRows[row]
        the1dArray[col] = value


class Matrix :
    #Creates a matrix of size numRows x numCols initialized to 0.
    def __init__( self, numRows, numCols ):
        self._theGrid = Array2D( numRows, numCols )
        self._theGrid.clear( 0 )

    # Returns the number of rows in the matrix.
    def numRows( self ):
        return self._theGrid.numRows()

    # Returns the number of columns in the matrix.
    def numCols( self ):
        return self._theGrid.numCols()

    # Returns the value of element (i, j): x[i,j]
    def __getitem__( self, ndxTuple ):
        return self._theGrid[ ndxTuple[0], ndxTuple[1] ]

    # Sets the value of element (i,j) to the value s: x[i,j] = s
    def __setitem__( self, ndxTuple, scalar ):
        self._theGrid[ ndxTuple[0], ndxTuple[1] ] = scalar


    # Returns the maximum value within this(self) matrix
    def max_value(self):
        # To do ......
        max_can=[]
        for row in self._theGrid._theRows:
            max_can.append(max(row))
        return max(max_can)

    # Scales the matrix by the given scalar.
    def scaleBy( self, scalar ):
        # To do ......
        for i in range(self.numRows()):
            for j in range(self.numCols()):
                self._theGrid[i,j]*=scalar

    # Creates and returns a new matrix that is the transpose of this matrix.
    def transpose( self ):
        # To do ......
        tran=Matrix(self._theGrid.numCols(),self._theGrid.numRows())
        for i in range(self.numRows()):
            for j in range(self.numCols()):
                tran._theGrid[j,i]=self._theGrid[i,j]
        return tran

    # Creates and returns a new matrix that results from matrix addition.
    def __add__( self, rhsMatrix ):
        # To do ......
        result=Matrix(self.numRows(),self.numCols())
        for i in range(self.numRows()):
            for j in range(self.numCols()):
                result._theGrid.__setitem__((i,j),self._theGrid.__getitem__((i,j))+rhsMatrix.__getitem__((i,j)))
        return result

    # Creates and returns a new matrix that results from matrix subtraction.
    def __sub__( self, rhsMatrix ):
        # To do ......
        result = Matrix(self.numRows(), self.numCols())
        for i in range(self.numRows()):
            for j in range(self.numCols()):
                result._theGrid.__setitem__((i, j), self._theGrid.__getitem__((i, j)) - rhsMatrix.__getitem__((i, j)))
        return result


    # Creates and returns a new matrix resulting from matrix multiplication.
    def __mul__( self, rhsMatrix ):
        # To do ......
        result=Matrix(self.numRows(),rhsMatrix.numCols())
        for i in range(self.numRows()):
            for j in range(rhsMatrix.numCols()):
                entry=0
                for k in range(self.numCols()):
                    entry+=self._theGrid[i,k]*rhsMatrix._theGrid[k,j]
                result._theGrid.__setitem__((i,j),entry)
        return result

    def __str__(self):
        answer = []  # Use list for efficiency
        for row in range(self.numRows()):
            for col in range(self.numCols()):
                answer.append(str(self[row, col]) + '\t')
            answer.append('\n')
        return ''.join(answer)


def main():
    #########Test codes#########
    m1 = Matrix(3,2)
    m2 = Matrix(2,3)
    m3 = Matrix(3,2)

    # Fill m1，m2, m3 with random values
    for row in range(m1.numRows()):
        for col in range(m1.numCols()):
            m1[row, col] = random.randint(-9,9)

    for row in range(m2.numRows()):
        for col in range(m2.numCols()):
            m2[row, col] = random.randint(-9,9)

    for row in range(m3.numRows()):
        for col in range(m3.numCols()):
            m3[row, col] = random.randint(-9,9)


    # Comment them out if you are submitting on gradescope!
    print("matrix 1 is: \n", m1, sep = "")
    print("matrix 2 is: \n", m2, sep = "")
    print("matrix 3 is: \n", m3, sep = "")
    print("------------------------------------------------------")
    print("Maximum value of matrix 1 is", m1.max_value())
    print("------------------------------------------------------")
    print("Transpose of matrix 1:\n", m1.transpose(), sep = "")
    print("Transpose of matrix 2:\n", m2.transpose(), sep = "")
    print("Transpose of matrix 3:\n", m3.transpose(), sep = "")
    print("------------------------------------------------------")
    print("matrix 1 add matrix 3:\n", m1 + m3, sep = "")
    print("matrix 1 subtract matrix 3:\n", m1 - m3, sep = "")
    print("matrix 1 multiply matrix 2:\n", m1 * m2, sep = "")
    print("------------------------------------------------------")
    m1.scaleBy(-4)
    print("Scale matrix m1 -4 times: \n", m1, sep = "")


if __name__ == '__main__':
    main()



