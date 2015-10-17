# -*- coding: utf-8 -*-
from nltk.tag import stanford
import os
#This script is used to do postagging of the text part of meta data
#Meta data has fields:
#FileName,ProTyep,Pro loaction in file, pro location in line, text, suid,speaker id
#All fields are seperated by '\t'
stanford_path="../stanford-postagger/"
meta_path="../Data/MetaData/"

class Postag:
    def __init__(self):
        self.st = stanford.POSTagger(stanford_path+"/models/chinese-distsim.tagger",stanford_path+"stanford-postagger.jar",encoding="utf-8")
    

    def multi_task(self):
        files= os.listdir(meta_path)
        for file_name in files:
            if  file_name.endswith(".meta"):
                print file_name
                self.postag(meta_path+file_name)

    def postag(self,file_path):
        file_buf=[]
        with open(file_path) as in_file:
            for line in in_file:
                file_buf.append(line)

        with open(file_path,'w') as out_file:
            for line in file_buf:
                text=line.split("\t")[4]
                tokens=text.split(" ")
                tag_list=self.st.tag(tokens)
                tag_field=""
                for tag in tag_list:
                    tag_field+=tag[1]+' '
                tag_field=tag_field[:-1]
                #entry=line[:-1]+'\t'+tag_field
                out_file.write(line[:-1]+"\t")
                #print tag_field
                out_file.write(tag_field.encode("utf-8")+"\n")
            
        




if __name__=="__main__":
    postag=Postag()
    postag.multi_task()
    print "Finished"
