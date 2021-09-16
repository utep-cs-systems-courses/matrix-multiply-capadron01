#!/usr/bin/env python3
import argparse
import numpy as np
import time
import pymp


def genMatrix(size=1024, value=1):
    """
    Generates a 2d square matrix of the specified size with the specified values
    """

    matrix = [[value for col in range(0,size)] for row in range(0,size)]

    return matrix

def genMatrix2(size=1024, value=1):
    """
    Generates a 2d square matrix of the specified size with the specified values
    """

    matrix = np.asarray([ np.asarray([value for col in range(0,size)]) for row in range(0,size)])

    return matrix

def printSubarray(matrix, size=10):
    """
    Prints the upper left subarray of dimensions size x size of
    the matrix
    """

    for row in range(size):
        for col in range(size):
            print(f'{matrix[row][col]} ' , end='')
        print('')


def writeToFile(matrix, fileName):
    """
    Writes a matrix out to a file
    """

    with open(fileName, 'w') as file:
        for row in matrix:
            for col in row:
                file.write(f'{col} ')
            file.write('\n')

def readFromFile(fileName):
    """
    Reads a matrix from a file
    """

    matrix = []

    with open(fileName, 'r') as file:
        for line in file:
            row = [int(val) for val in line.split()]
            matrix.append(row)

    return matrix

def multiplyMatrix(matrix, matrix2):

    """Multiplies given matrices"""
    dimensions = len(matrix)
    newMatrix = genMatrix(dimensions,0)
    for rows in range(dimensions):
        for col in range(dimensions):
            for index in range(dimensions):
                newMatrix[rows][col] += matrix[rows][index]*matrix2[index][rows]
    return newMatrix

def multiplyMatrixParallel(matrix, matrix2):

    """Multiplies given matrices in parallel"""
    dimensions = len(matrix)
    newMatrix = genMatrix(dimensions,0)
    for rows in range(dimensions):
        for col in range(dimensions):
            with pymp as p:
                for index in range(dimensions):
                    newMatrix[rows][col] += matrix[rows][index]*matrix2[index][rows]
    return newMatrix

def multiplyMatrixBLock(matrix, matrix2):

    """Multiplies given matrices using block"""
    tile_size = 16
    dimensions = len(matrix)
    newMatrix = genMatrix(dimensions,0)
    for kk in range(0,dimensions,tile_size):
        for jj in range(0,dimensions,tile_size):
            for i in range(dimensions):
                j_end_val = jj+tile_size
                for j in range(jj, j_end_val):
                    k_end_val = kk + tile_size
                    sum = newMatrix[i][j]
                    for k in range(kk,k_end_val):
                        sum=sum+matrix[i][k]*matrix2[k][j]
                        newMatrix[i][j] = sum
    return newMatrix


def main():
    """
    Used for running as a script
    """

    parser = argparse.ArgumentParser(description=
        'Generate a 2d matrix and save it to  a file.')
    parser.add_argument('-s', '--size', default=1024, type=int,
        help='Size of the 2d matrix to generate')
    parser.add_argument('-v', '--value', default=1, type=int,
        help='The value with which to fill the array with')
    parser.add_argument('-f', '--filename',
        help='The name of the file to save the matrix in (optional)')
    parser.add_argument('-r', '--result',
        help='The name of the result file to save the matrix in (optional)')

    args = parser.parse_args()

    mat = genMatrix(args.size, args.value)

    if args.filename is not None:
        print(f'Writing first matrix to {args.filename}')
        writeToFile(mat, args.filename)
        newMatrix = multiplyMatrixParallel(mat,mat)

        print(f'Writing result matrix to {args.result}')
        writeToFile(newMatrix, args.result)
        print(f'Testing file\n 1st matrix\n')
        printSubarray(readFromFile(args.filename))
        print(f'Resulting matrix')
        printSubarray(readFromFile(args.result))
    else:
        printSubarray(mat)

if __name__ == '__main__':
    # execute only if run as a script
    main()