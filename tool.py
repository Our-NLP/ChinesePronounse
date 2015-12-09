# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
from os import path
import re
class xml_parser:
    def __init__(self,data_path):
        #input and output directory name
        self.data_path=data_path
        self.cur_file=""
        if self.data_path[-1] is not '/':
            self.data_path+="/"

    def GenerateMeta(self,root):
        texts= root[0].text.splitlines()
        tags=  root[1]

        tag_list=[]
        #sort the tags by the start attribute. Because annotation may different from
        #the order *pro* appear in the text
        for tag in tags :
            tag_list.append(tag)
        tag_list=sorted(tag_list,key=lambda x:int(x.attrib["start"]))

        out_buf=[]
        tags_index=0
        tags_len=len(tag_list);
        for i in range(len(texts)):
            #print texts[i]
            if "suid=" in texts[i] or "msgid=" in texts[i]:
                suid,speaker=texts[i].split(" ")
                print suid,speaker
                continue
            while "*pro*" in texts[i] and tags_index<tags_len:
                pro=tag_list[tags_index].attrib["id"][:-1]
                texts[i]=texts[i].replace('*pro*','*'+pro+'*',1)
                tags_index+=1
            print texts[i]
                
    def multi_task(self):
        #parse all file ended with xml in input directory
        #Generate meta data for producing feature files
        files=[x for x in os.listdir(self.data_path)]
        for file_name in files:
            if ".xml" in file_name:
                print file_name
                self.cur_file=file_name
                self.parse_xml(file_name,self.GenerateMeta)
        

    def parse_xml(self,file_name,func):
        #parse a single xml file, generate one .meta file a time
        #remove *pro* from the text
        file_name=self.data_path+file_name
        
        if ".xml" not in file_name:
            print file_name," is not xml file"
            return
        tree=ET.parse(file_name);
        root=tree.getroot();
        func(root)

if __name__=="__main__":
    xp= xml_parser("./Data/XMLData");
    xp.multi_task()
    print "Finished"
