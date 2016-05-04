# del_overlap

The goals of this workflow are to use reference genome deletions in order to make inferences about genome similarity and lineage.
This work is part of my undergraduate research under Professor Volker Brendel at Indiana University.

The python code looks to find all deletions containing overlaps of a specified percentage.
We are aiming to find a "sweet spot" set of parameters that are the most useful. 

The expected file input is a set of .perGap files that results from a workflow that Dr. Chun-Yuan Huang developed and implemented.
Huang's workflow is availible at: https://github.com/huangc/WGvarINDEL

The code can easily be modified to support other file formats such as .psl and .bed, if you are interested in finding overlaps of features. 

# Input parameters:
There are several input parameters availible to change at the top of the python code.
Python Input:
- Number of chromosomes on the genome
- Number of inputted .perGap files
- Minimum deletion length
- Top "N" number of longest deletions to be looked at
- Threshold for overlap percentage

The command line input simply requires the filepaths to each of the .perGap files you wish to compare.
Command Line Input:
- file names (at least 2 files are required)

Expected command line input: python program_name.py file1 file2 ... file8
