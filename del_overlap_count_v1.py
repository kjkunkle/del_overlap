# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 11:36:11 2016

@author: kevinkunkle

The goal of this code is to find the longest deletion in each of the YBs
and compare its precense throughout the rest of the YBs
"""

import sys
import fileinput
from intervaltree import Interval, IntervalTree 
import xlwt


# number of chromosomes on the genome 
numChroms = 12
# number of YB files we are looking at
numYBs = 26 # nipponbare + YB1-YB8
# minimum length of a deletion to be considered
min_length = 200
# top n number of longest deletions to be looked at
numLong = 50
# threshold for overlap percentage, ex: 98%
overlap_thres = .98

"""
DelObj is used to store a deletion event.
It has many variables and conveinence functions
"""
def getOverlap(a, b):
     return max(0, min(a[1], b[1]) - max(a[0], b[0]))

class DelObj:
    def __init__(self, query_name, YB_number, chromosome, start, end):
        self.query_name = query_name
        self.YB_number = YB_number
        self.chromosome = chromosome
        self.start = start
        self.end = end
        self.length = end - start
        self.overlap_list = [0 for i in range(numYBs)]
    
    def addOverlap(self, YB_number):
        self.overlap_list[YB_number - 1] = 1
    
    def hasOverlap(self):
        for i in range(len(self.overlap_list)):
            if(self.overlap_list[i] == 1 and i != self.YB_number - 1):
                return True
        return False
    
    def allOverlapped(self):
        if((self.overlap_list[0] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[1] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[2] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[3] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[4] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[5] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[6] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[7] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[8] == 0) and ((i+1) != self.YB_number)):
            return False
        return True
        
    def notYB1butYB2thruYB8(self):
        if(self.overlap_list[0] == 1):
            return False
        if(self.YB_number == 1):
            return False
        if((self.overlap_list[1] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[2] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[3] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[4] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[5] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[6] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[7] == 0) and ((i+1) != self.YB_number)):
            return False
        if((self.overlap_list[8] == 0) and ((i+1) != self.YB_number)):
            return False
        return True
        
    def toString(self):
        return_str = 'YB' + str(self.YB_number) + '\t' + self.query_name + '\tChr' + str(self.chromosome) + '\t' + str(self.start) + '\t' + str(self.end) + '\tOverlap: '
        for i in range(len(self.overlap_list) - 1):
            if(self.overlap_list[i] == 1):
                return_str += 'YB' + str(i+1) + ', '
        if(self.overlap_list[8] == 1):
            return_str += 'NIPPONBARE'
        return return_str

"""
The expected file input is 8 YB files in a format that results from a workflow
that Dr. Chun-Yuan Huang developed and implemented.
Huang's workflow is availible at: https://github.com/huangc/WGvarINDEL

The code can easily be modified to support other file formats such as .psl and .bed
"""

if(len(sys.argv) < numYBs):
    print "Expected input with " + str(numYBs) + " args: python <program_name>.py <file1> <file2> ... <file" + str(numYBs) +">"
else:
    
    
    chrom_list = [IntervalTree() for i in range(numChroms)];
    del_obj_list = []    
    
    yb1 = 0
    yb2 = 0
    yb3 = 0
    yb4 = 0
    yb5 = 0
    yb6 = 0
    yb7 = 0
    yb8 = 0
    nipponbare = 0
    
    # for each YB file input
    for i in range(numYBs):
        # for each line of .bed file
        for line in fileinput.input(sys.argv[i+1]):
            parsed_line = line.split()
            #chromosome deletion occurs on
            chrom = int(parsed_line[1][6:])
            #starting base of deletion
            start = int(parsed_line[12])
            #ending base of deletion
            end = int(parsed_line[13])
            del_obj = DelObj(parsed_line[0], i+1, chrom, start, end)
            if(end - start >= min_length):
                #print del_obj.query_name
                #print del_obj.YB_number
                #print chrom
                chrom_list[chrom - 1][start:end] = del_obj
                del_obj_list.append(del_obj)
                if(del_obj.YB_number == 1):
                    yb1 += 1
                elif(del_obj.YB_number == 2):
                    yb2 += 1
                elif(del_obj.YB_number == 3):
                    yb3 += 1    
                elif(del_obj.YB_number == 4):
                    yb4 += 1   
                elif(del_obj.YB_number == 5):
                    yb5 += 1   
                elif(del_obj.YB_number == 6):
                    yb6 += 1   
                elif(del_obj.YB_number == 7):
                    yb7 += 1   
                elif(del_obj.YB_number == 8):
                    yb8 += 1   
                elif(del_obj.YB_number == 9):
                    nipponbare += 1  
                
    #sorts the deletions by length
    del_obj_list.sort(key=lambda x: x.length, reverse=True)
    
    phy_scores = [[0 for y in range(numYBs)] for x in range(numYBs)]
    length_scores = [[0 for y in range(numYBs+1)] for x in range(numYBs)]
    number_overlap = [[0 for y in range(numYBs)] for x in range(numYBs)]
    score_count = 500
    
    
    excel_file = 'phy_chart_del_cx140.xls'
    book = xlwt.Workbook(encoding="utf-8")

    sheet1 = book.add_sheet("Sheet 1")

    count = 1
    x = 1
    for i in range(1000):
        sheet1.write(count,0, str(x) + " longest del query#")
        sheet1.write(count+1,0, "length")
        sheet1.write(count+2,0, "Start")
        sheet1.write(count+3,0, "End")
        sheet1.write(count+4,0, "Overlap")  
        x += 1
        count +=5
    
    for yb in range(numYBs):
        count = 1
        i = 0
        for del_obj in del_obj_list:
            if(yb+1 == del_obj.YB_number):
                if(score_count - i > 0):
                    length_scores[yb][numYBs] += del_obj.length
                
                sheet1.write(count,yb+1, del_obj.query_name)
                sheet1.write(count+1,yb+1, del_obj.length)
                sheet1.write(count+2,yb+1, del_obj.start)
                sheet1.write(count+3,yb+1, del_obj.end)
                
                overlap_string = ""
                for x in sorted(chrom_list[del_obj.chromosome - 1][del_obj.start:del_obj.end]):
                    overlap_string += "Overlap: YB" + str(x[2].YB_number) + " query: " + str(x[2].query_name) + " start: " + str(x[2].start) + " end: " + str(x[2].end) + " length: " + str(x[2].end - x[2].start) + "\n"
                    if(score_count - i > 0):
                        phy_scores[yb][x[2].YB_number-1] += score_count - i
                        
                        
                        tar = [del_obj.start, del_obj.end]
                        query = [x[2].start, x[2].end]
                        
                        if(getOverlap(tar, query) > 0):
                            length_scores[yb][x[2].YB_number-1] += getOverlap(tar, query)
                            
                        if(del_obj.start <= x[2].start):
                            norm_start = del_obj.start
                        else:
                            norm_start = x[2].start
                            
                        if(del_obj.end >= x[2].end):
                            norm_end = del_obj.end
                        else:
                            norm_end = x[2].end
                        
                        normalize_length = norm_end - norm_start
                        
                        if(getOverlap(tar, query)/float(normalize_length) > overlap_thres):
                            number_overlap[yb][x[2].YB_number-1] += 1
                                
                sheet1.write(count+4,yb+1, overlap_string)
                count += 5    
                i += 1
     
    
    for del_obj in del_obj_list:
        for x in sorted(chrom_list[del_obj.chromosome - 1][del_obj.start:del_obj.end]):
            if(x[2] != del_obj):            
                del_obj.addOverlap(x[2].YB_number)
                #print x[2]
    
    for i in range(numYBs):
        print "YB" + str(i+1)
        print phy_scores[i]
    for i in range(numYBs):   
        print "YB" + str(i+1)
        print length_scores[i]
    for i in range(numYBs):   
        print "YB" + str(i+1)
        print number_overlap[i]
    
    for i in range(numYBs):
        for j in range(numYBs):
            length_scores[i][j] = length_scores[i][j]/float(length_scores[i][numYBs])
    
    sheet2 = book.add_sheet("Total Overlap Percentage")
    
    for i in range(numYBs):
        sheet2.write(i+1,0, "YB" + str(i+1))
        sheet2.write(0, i+1, "YB" + str(i+1))
    
    
    for i in range(numYBs):   
        print "YB" + str(i+1)
        print length_scores[i]
        for j in range(numYBs+1):
            sheet2.write(i+1, j+1, length_scores[i][j])
    
    sheet3 = book.add_sheet("Overlap of " + str(overlap_thres) + " Count")
    
    for i in range(numYBs):
        sheet3.write(i+1,0, "YB" + str(i+1))
        sheet3.write(0, i+1, "YB" + str(i+1))
    
    for i in range(numYBs):   
        print "YB" + str(i+1)
        print length_scores[i]
        for j in range(numYBs):
            sheet3.write(i+1, j+1, number_overlap[i][j])
        
    book.save(excel_file) 