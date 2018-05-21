import math
import bitarray
import numpy as np
import mmh3
from bitarray import bitarray

class bloomfilter(object):
    def __init__(self, capacity = 100, error = 0.001):
        """
        capacity: 
            the expected number of elements to be added in the set.
        error: 
            the intended maxmimum false positive rate.
        """
        if error <= 0 or error >= 1:
            raise ValueError("Please use an error rate betwen 0 and 1")
        if capacity < 0:
            raise ValueError("Please use a capacity larger than 0")
        
        self.cap = capacity
        self.error = error
        self.num_slices = self.num_slices(self.error)
        self.slice_size = self.return_slice_size(self.num_slices, self.cap, self.error)
        self.total_size = self.num_slices*self.slice_size
        self.cnt = 0
        self.total_array = bitarray(self.total_size)
        self.total_array.setall(0)
    
    def num_slices(self, error):
        """
        Given the error rate, calculate the expected number of slices/hash functions.
        """
        return int(np.ceil(np.log2(1.0 / error)))
    
    def return_slice_size(self, num_slices, capacity, error):
        """
        Given the number of slices, the expected number of elements and the error rate. 
        Calculate the corresponding size of each slice in the filter.
        """
        return int(np.ceil(0 - (capacity*np.log(error))/(num_slices*np.log(2.)**2)))
    
    def check(self, element):
        """
        Check whether a element already exists in the set. There could be false positive errors.
        """
        element = str(element)
        for i in range(self.num_slices):
            index = mmh3.hash(element,i) % self.slice_size
            if self.total_array[index + self.slice_size*i] == 0:
                return False
        return True
    
    def add(self, element):
        """
        Add a new element to the set. If the element already exists, return False and do nothing.
        Otherwise return True and add it to the set.
        """
        element = str(element)
        # check whether the element already exists
        exist = self.check(element)
        if exist == True:
            print("The element to be added:" +str(element) + " already exists.")
            return False
        elif self.cnt == self.cap:
            raise ValueError("Number of elements exceeds capacity. Please create a new bloom filter with larger capacity.")
        else:
            for i in range(self.num_slices):
                index = mmh3.hash(element,i) % self.slice_size
                self.total_array[index + self.slice_size*i] = True
            self.cnt = self.cnt + 1
            return True
    
    def count(self):
        """
        Return the number of elements that have been added to the set.
        """
        return self.cnt
    
    def capacity(self):
        """
        Return the capacity of the filter.
        """
        return self.cap
    
    def size(self):
        """
        Return the number of bits of the filter.
        """
        return self.total_size