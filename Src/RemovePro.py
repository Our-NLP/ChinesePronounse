# -*- coding: utf-8 -*-
from XML_Parser import xml_parser
import os
class RemovePro(xml_parser):
    def remove(self,file_name):
        content=[]
        with open(self.data_path+file_name,'r') as cur_file:
            for line in cur_file:
                items=line.split('\t')
                sent=items[4]
                tmp=[]
                for token in sent.split(" "):
                    if '*' not in token:
                        tmp.append(token)
                new_str=" ".join(tmp)
                #print new_str
                items[4]=new_str
                #print sent
                tmp=[]
                pos_tag=items[7]
                for token in pos_tag.split(" "):
                    if '*' not in token:
                        tmp.append(token)
                new_str=" ".join(tmp)
                items[7]=new_str
                s="\t".join(items)
                content.append(s)
        with open(self.output_path+file_name,'w') as outfile:
            for line in content:
                outfile.writelines(line)
 

    
    def multi_task(self):
        files=[x for x in os.listdir(self.data_path)]
        for file_name in files:
            if file_name.endswith(".meta"):
                print file_name
                self.cur_file=file_name
                self.remove(file_name)
if __name__=="__main__":
    rp=RemovePro("../Data/MetaData","../Data/MetaData")
    rp.multi_task()
                    
