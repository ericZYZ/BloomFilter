# BloomFilter
An implementation of both non-scalable and scalable bloom filter.

## Prerequisites
Please make sure you have bitarray and mmh3 installed prior to running the examples.

To install bitarray:

	pip install bitarray
To install mmh3:

	pip install mmh3

## Components

This folder contains 4 python files. 
	
	bloomfilter.py:			Implementation of the bloom filter(non-scalable).
	scalable_bloomfilter:	Implementation of the scalable bloom filter following: http://gsd.di.uminho.pt/members/cbm/ps/dbloom.pdf
	bloomfilter_test.py:	An example of running the non-scalabe bloom filter on two set of data.
	scalable_bloomfilter_test.py:	An example of running the scalabe bloom filter on two set of data.
 
This folder contains 2 text files. 

	presentfile.txt:	Contains the data to be added to the bloom filter. Integers from 0 to 999.
	absentfile.txt:		Contains the data which are not added to the bloom filter at the beginning, and is used to test the false positive rate.
						Integers from 1000 to 2999.
	
You can change the content of these two text files to test on different data. Or you can use two different files directly and remember to specify 
the name of the new files when running the examples. All data files need to be stored in the same folder as the python files.
	
## Run examples

**To run the non-scalabe bloom filter example using bloomfilter_test.py:

	usage: python bloomfilter_test.py [--h] [--capacity CAPACITY] [--error ERROR] [--present-file-name FILENAME1] [--absent-file-name FILENAME2]
	
	optional arguments:
	-h, --help            show this help message and exit
	--capacity N          input bloom filter capacity (default: 3000)
	--error N             input error rate (default: 0.01)
	--present-file-name N
                        file containing the elements to be added (default:
                        presentfile.txt)
	--absent-file-name N  file containing the elements that are not in the set
                        and to be tested (default: absentfile.txt)

	Example:
		python bloomfilter_test.py --capacity 3000 --error 0.01 --present-file-name presentfile.txt --absent-file-name absentfile.txt
		
**To run the scalable bloom filter example using scalable_bloomfilter_test.py:

	usage: python scalable_bloomfilter_test.py [--h] [--initial-capacity CAPACITY] [--error ERROR] [--present-file-name FILENAME1] [--absent-file-name FILENAME2]
	
	optional arguments:
	-h, --help            show this help message and exit
	--initial-capacity N  input initial bloom filter capacity (default: 100)
	--error N             input error rate (default: 0.01)
	--present-file-name N
                        file containing the elements to be added (default:
                        presentfile.txt)
	--absent-file-name N  file containing the elements that are not in the set
                        and to be tested (default: absentfile.txt)
					
	Example:
		python scalable_bloomfilter_test.py --initial-capacity 100 --error 0.01 --present-file-name presentfile.txt --absent-file-name absentfile.txt
	
## Analysis

The implementations of both the simple non-scalabe bloom filter and the scalable bloom filter follow the paper: http://gsd.di.uminho.pt/members/cbm/ps/dbloom.pdf
Note that for the non-scalabe version, the bit array is diveded into k slices and each hash function output an index to one slice. This is a variant to the 
traditional non-scalabe bloom filter but the equations used to derive the number of bits m in the filter and the number of hash functions k given the maximum 
false positive rate p and number of elements to be inserted n are the same:

	m = (n|ln(p)|)/(ln(2)**2)
	
	k = -log2(p)
	
The scalable version follows the implementation stated in the paper with the default s set to 2 and r set to 0.9. Since it can scale automatically, the initial 
capacity of the scalable bloom filter can be set much smaller than the non-scalabe version given the same number of data.

For the non-scalabe version, the time complexity is O(k) for both insertion and search no matter how big the dataset is. The space complexity is O(m) which can 
be much smaller than an error-free hashing methods.
For the scalabe version, the time and space complexity is a bit complicated. As the paper points out, the space complexity is related to the value of r and s with
s to be 2 or 4, and r between 0.8-0.9 giving the smallerest space growth. The time complexity is approximately O(k0) + O(log(n)) = O(log(n)). 



