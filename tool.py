import os
files=os.listdir('./Data/MetaData')
for file in files:
    with open('./Data/MetaData/'+file) as f:
        for line in f:
            print line

