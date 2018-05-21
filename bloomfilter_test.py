from scalable_bloomfilter import *
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Bloom Filter Example')
    parser.add_argument('--capacity', type=int, default=3000, metavar='N',
                        help='input bloom filter capacity (default: 3000)')
    parser.add_argument('--error', type=float, default=0.01, metavar='N',
                        help='input error rate (default: 0.01)')
    parser.add_argument('--present-file-name', type=str, default="presentfile.txt", metavar='N',
                        help='file containing the elements to be added (default: presentfile.txt)')
    parser.add_argument('--absent-file-name', type=str, default="absentfile.txt", metavar='N',
                        help='file containing the elements that are not in the set and to be tested (default: absentfile.txt)')
    args = parser.parse_args()
    
    capacity = args.capacity
    error = args.error
    present_path = args.present_file_name
    absent_path = args.absent_file_name
    
    b = bloomfilter(capacity=capacity, error=error)

    # add to filter
    file = open(present_path, "r") 
    inputs1 = file.read().split() 
    for i in inputs1:
        b.add(i)

    # check absent elements and return a false positive rate
    exist_list = []
    file = open(absent_path, "r") 
    inputs2 = file.read().split() 
    for i in inputs2:
        if(b.add(i) == False):
            exist_list.append(i)
    print("==================== False positive rate is " + str(float(len(exist_list)) / float(len(inputs2))) + " ====================")
    print("The capacity of the bloom filter is "+str(b.capacity()))
    print("There are "+str(b.count())+" elements successfully added to the filter")
    print("There are "+str(b.size())+" bits in the bloom filter")
