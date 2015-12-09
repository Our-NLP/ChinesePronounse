import os
if __name__=='__main__':
    dir='./Data/MetaData'
    f_list=os.listdir(dir)
    for fname in f_list:
        with open(dir+'/'+fname) as fin:
            for line in fin:
                print line
