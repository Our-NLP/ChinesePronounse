import subprocess
if __name__=="__main__":
    with open("./sample-data/numeric/alltest.csv") as input_file, open("./test/alltest.meta",'w') as  output_file:
        i=0
        for line in input_file:
            label,f1,f2=line.split(',')
            f2=f2[:-2]
            #output_file.write(label+" "+f1+" "+f2+"\n")
            #output_file.write(label+" "+f1+":"+f1+" "+f2+":"+f2+"\n")
            output_file.write(label+" "+"f1:"+f1+" f2:"+f2+"\n")
            #output_file.write(str(i)+","+label+","+"f1="+f1+","+"f2="+f2+"\n")
            i+=1
###### Import Data######
    #subprocess.call(["./bin/csv2vectors","--input","./test/alltest.meta","--output","./test/alltest.mallet"])
    subprocess.call(["./bin/mallet","import-svmlight","--input","./test/alltest.meta","--output","./test/alltest.mallet"])
###### Check Data######
    #subprocess.call(["./bin/vectors2info","--input","./test/alltest.mallet","--print-matrix"]);
###### Classify ######
    subprocess.call(["./bin/mallet","train-classifier","--input","./test/alltest.mallet","--trainer","MaxEnt","--training-portion","0.9"]);


