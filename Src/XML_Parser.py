# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import path
import re
class xml_parser:
    def __init__(self,data_path,output_path):
        #input and output directory name
        self.data_path=data_path
        self.output_path=output_path
        self.cur_file=""
        if self.data_path[-1] is not '/':
            self.data_path+="/"
        if self.output_path[-1] is not '/':
            self.output_path+="/"


    def GenerateMeta(self,root,out_file):
        texts= root[0].text.splitlines()
        tags=  root[1]

        tag_list=[]
        #sort the tags by the start attribute. Because annotation may different from
        #the order *pro* appear in the text
        for tag in tags :
            tag_list.append(tag)
        sorted(tag_list,key=lambda x:x.attrib["start"])

        out_buf=[]
        tags_index=0
        tags_len=len(tag_list);
        for i in range(len(texts)):
            if "suid=" in texts[i]:
                suid,speaker=texts[i].split(" ")
                continue
            if "*pro*" in texts[i] and tags_index<tags_len:
                pro_num=[m.start() for m in re.finditer('\*pro\*', texts[i])]
                texts[i]=texts[i].replace("*pro* ",""); #remove *pro*+" "
                for j in pro_num:#if multiple *pro* apprear in the line
                    pro=tag_list[tags_index].attrib["id"][:-1]
                    start=tag_list[tags_index].attrib["start"]
                    entry=self.cur_file+"\t"+pro+"\t"+start+"\t"+str(j)+"\t"+texts[i]+"\t"+suid[5:]+"\t"+speaker[12:]
                    out_buf.append(entry)
                    tags_index+=1
            else:
                pro="NONE"
                start="-1"
                if len(texts[i])>0:
                    entry=self.cur_file+"\t"+pro+"\t"+start+"\t"+str(-1)+"\t"+texts[i]+"\t"+suid[5:]+"\t"+speaker[12:]
                    out_buf.append(entry)
                    
        self.write_file(out_file,out_buf)

        

    def multi_task(self):
        #parse all file ended with xml in input directory
        #Generate meta data for producing feature files
        files=[x for x in os.listdir(self.data_path)]
        for file_name in files:
            if ".xml" in file_name:
                self.cur_file=file_name
                self.parse_xml(file_name,file_name.replace(".xml",".meta"),self.GenerateMeta)
        

    def parse_xml(self,file_name,out_file,func):
        #parse a single xml file, generate one .meta file a time
        #remove *pro* from the text
        file_name=self.data_path+file_name
        out_file=self.output_path+out_file
        
        if ".xml" not in file_name:
            print file_name," is not xml file"
            return
        tree=ET.parse(file_name);
        root=tree.getroot();
        func(root,out_file)
                
    def write_file(self,file_name,content):
        #write to file
        with open(file_name,'w') as outfile:
            for line in content:
                outfile.writelines(line.encode("utf-8")+"\n")


if __name__=="__main__":
    xp= xml_parser("../Data/XMLData","../Data/MetaData");
    xp.multi_task()
    print "Finished"
    
