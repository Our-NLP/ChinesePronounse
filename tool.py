import os
files=os.listdir('./Data/XMLData')
for file in files:
    with open('./Data/XMLData/'+file) as f:
        for line in f:
            print line

