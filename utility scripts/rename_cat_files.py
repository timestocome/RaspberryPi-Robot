# http://github.com/timestocome

# clean up cat photos for use in training robots to 
# recognize each cat
# 2 cats in household
# 50 photos each, ~25 actual photos of each, ~25 similar looking cats from internet
# crop each to 1000 x 1000 if needed (same size so have random amount of cat and background)
# resize images to a max of 300 if needed, robot camera input is going to be set low
# each cat is in a different dir, relabel files and combine
# name each file with cat name to make labeling easier


import os
from os import rename
from os.path import basename


# get file list
path = os.getcwd()

merlin_files = os.listdir('merlin')
min_files = os.listdir('min')


os.chdir('merlin')
i = 1
for f in merlin_files:
    new_name = 'merlin_%d.jpg' % i
    old_name = f
    print(old_name, new_name)
    os.rename(old_name, new_name)
    i+= 1

os.chdir(path)
os.chdir('min')
i = 1
for f in min_files:
    new_name = 'min_%d.jpg' % i
    old_name = f
    print(old_name, new_name)
    os.rename(old_name, new_name)
    i+=1