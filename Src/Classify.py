import subprocess
if __name__=="__main__":
    mallet_bin="../mallet-2.0.8RC2/bin/"
    train_data="../TrainData/train.dat"
    mallet_data="../TrainData/train.mallet"

#Import Data
    subprocess.call([mallet_bin+"mallet","import-svmlight","--input",train_data,"--output",mallet_data])
#Check Data
    #subprocess.call([mallet_bin+"vectors2info","--input",mallet_data,"--print-matrix"]);
#Classify 
    subprocess.call([mallet_bin+"mallet","train-classifier","--input",mallet_data,"--trainer","MaxEnt","--training-portion","0.9"]);

