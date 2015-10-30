import subprocess
if __name__=="__main__":
    mallet_bin="../mallet-2.0.8RC2/bin/"
    train_data="../Data/Features/features.fb"
    mallet_data="../Data/vectors/train.mallet"

#Import Data
    print "Transforming data into vector..."
    subprocess.call([mallet_bin+"mallet","import-svmlight","--input",train_data,"--output",mallet_data])
#Check Data
    #subprocess.call([mallet_bin+"vectors2info","--input",mallet_data,"--print-matrix"]);
#Classify 
    print "Classifying..."
    subprocess.call([mallet_bin+"mallet","train-classifier","--input",mallet_data,"--trainer","MaxEnt","--training-portion","0.9"]);

