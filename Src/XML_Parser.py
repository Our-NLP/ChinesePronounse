import xml.etree.ElementTree as ET
import os
from os import path
#coding=utf-8 
class xml_parser:
    def __init__(self,data_path,output_path):
        #input and output directory name
        self.data_path=data_path
        self.output_path=output_path
        
        if self.data_path[-1] is not '/':
            self.data_path+="/"
        if self.output_path[-1] is not '/':
            self.output_path+="/"


    def multi_task(self):
        #parse all file ended with xml in input directory
        #Generate meta data for producing feature files
        files=[x for x in os.listdir(self.data_path)]
        for file_name in files:
            if ".xml" in file_name:
                self.parse_xml(file_name,file_name.replace(".xml",".meta"))
        

    def parse_xml(self,file_name,out_file):
        #parse a single xml file, generate one .meta file a time
        #remove *pro* from the text
        file_name=self.data_path+file_name
        out_file=self.output_path+out_file
        
        if ".xml" not in file_name:
            print file_name," is not xml file"
            return
        tree=ET.parse(file_name);
        root=tree.getroot();
        
        texts= root[0].text.splitlines()
        tags=  root[1]
        out_buf=[]
        tags_index=0
        tags_len=len(tags);
        for i in range(len(texts)):
            if "suid=" in texts[i]:
                continue
            if "*pro*" in texts[i] and tags_index<tags_len:
                pro=tags[tags_index].attrib["id"][:-1]
                start=tags[tags_index].attrib["start"]
                tags_index+=1
            else:
                pro="NONE"
                start="-1"
            texts[i]=texts[i].replace("*pro* ",""); #remove *pro*+" "
            if len(texts[i])>0:
                out_buf.append(pro+"\t"+start+"\t"+texts[i])
        self.write_file(out_file,out_buf)

                
    def write_file(self,file_name,content):
        #write to file
        file_name=self.output_path+file_name
        with open(file_name,'w') as outfile:
            for line in content:
                outfile.writelines(line.encode("utf-8")+"\n")


if __name__=="__main__":
    xp= xml_parser("../XMLData","../MetaData");
    xp.multi_task()
    print "Finished"
    
