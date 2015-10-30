# -*- coding: utf-8 -*-
import os
class Correct:
    def __init__(self):
        self.data_dir=os.path.realpath(os.path.dirname(os.path.realpath("__file__"))+"/../Data")
        self.meta_dir=self.data_dir+"/MetaData/"
        self.output_dir=self.data_dir+"/new_Data/"
        self.postaged_dir=self.data_dir+"/postaged/"
        
    def multi_task(self):
        for file in os.listdir(self.postaged_dir):
            with open(self.meta_dir+file) as correct,open(self.postaged_dir+file)  as wrong,open(self.output_dir+file,'w') as out:
                correct_list=[line for line in correct]
                wrong_list=[line for line in wrong]
                if len(correct_list) != len(wrong_list):
                    print file
                for i in range(len(correct_list)):
                    out.write(correct_list[i][:-1]+'\t'+wrong_list[i].split('\t')[-1])
                    

if __name__=="__main__":
    ct=Correct()
    #print ct.postaged_dir
    ct.multi_task()
