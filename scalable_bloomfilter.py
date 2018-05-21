import math
import hashlib
import bitarray
from bloomfilter import *

class scalable_bloomfilter(object):
    def __init__(self, initial_capacity = 100, error = 0.001, s = 2, r = 0.9):
        """
        initial_capacity: 
            the expected number of elements to be added in the initial bloom filter at stage one. 
            As number of stages increases, the size of the set increases, so is the capacity.
        error: 
            the intended maxmimum false positive rate.
        s:
            the scalable growth ratio. Set to 2 if a small set growth is expected. 
            Otherwise set to 4 for a larger growth. Default is 2.
        r:
            the error probability ratio. A sensible choice would be around 
            0.8 - 0.9. Default is 0.9.
        """
        if error <= 0 or error >= 1:
            raise ValueError("Please use an error rate betwen 0 and 1")
        if initial_capacity < 0:
            raise ValueError("Please use a capacity larger than 0")
        
        self.initial_capacity = initial_capacity
        self.error = error
        self.s = s
        self.r = r
        self.n_filters = 0.
        self.cnt = 0.
        self.total_capacity = initial_capacity
        self.total_size = 0.
        self.filter_list = []
        
    def check(self, element):
        """
        Check whether a element already exists in the set. There could be false positive errors.
        """
        element = str(element)
        if len(self.filter_list) == 0:
            return False
        for i in range(len(self.filter_list)):
            exist = self.filter_list[i].check(element)
            if exist == True:
                return True
        return False
        
    def add(self, element):
        """
        Add a new element to the set. Return False if element is already in the set.
        Otherwise return True and the element is added in the filter.
        """
        element = str(element)
        if len(self.filter_list) == 0:
            # initialize the filter list
            one_filter = bloomfilter(capacity = self.total_capacity, error = self.error*(1. - self.r))
            one_filter.add(element)
            self.filter_list.append(one_filter)
            self.n_filters = self.n_filters + 1
            self.cnt = self.cnt + 1
            self.total_size = self.total_size + one_filter.size()
            return True
        elif self.check(element) == True:
            print("The element to be added:" + str(element) + " already exists.")
            return False
        else:
            num_filters = len(self.filter_list)
            last_filter = self.filter_list[num_filters - 1]
            
            # create a new filter
            if last_filter.count() == last_filter.capacity():
                one_filter = bloomfilter(capacity = last_filter.capacity()*self.s, error = last_filter.error*self.r)
                one_filter.add(element)
                self.filter_list.append(one_filter)
                self.n_filters = self.n_filters + 1
                self.cnt = self.cnt + 1
                self.total_capacity = self.total_capacity + one_filter.capacity()
                self.total_size = self.total_size + one_filter.size()
                return True
            else:
                last_filter.add(element)
                self.cnt = self.cnt + 1
                return True
            
    def num_filters(self):
        """
        Return the current number of filters. 
        """
        return self.n_filters

    def count(self):
        """
        Return the total number of elements that have been added to the set.
        """
        return self.cnt

    def capacity(self):
        """
        Return the total capacity of all the filters.
        """
        return self.total_capacity

    def size(self):
        """
        Return the total number of bits of all the filters.
        """
        return self.total_size