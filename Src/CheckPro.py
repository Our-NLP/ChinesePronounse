from XML_Parser import xml_parser
import os
import re
class CheckPro(xml_parser):
    def __init__(self,data_path,output_path):
        xml_parser.__init__(self,data_path,output_path);
        self.cur_file
        
    def Check(self,root,out_file):
        texts= root[0].text.splitlines()
        tags=  root[1]
        label_pro=[]

        pro_text_dict={}# pro's start place and the sentence it is in


        #pros in the tag part
        for tag in tags:
            label_pro.append(int(tag.attrib["start"]))
        label_pro=sorted(label_pro,key=lambda x: int(x))
        
        #pros in the text
        pros_in_text=[m.start()+1 for m in re.finditer('\*pro\*',root[0].text)]
        

        #find the difference of this two part
        differences=list(set(pros_in_text)-set(label_pro))
        #if no difference, end this iteration
        if len(differences)==0:
            return
        
        #figure out which sentence the missing pro is in
        count=0
        for text in texts:
            for m in re.finditer('\*pro\*',text):
                pro_text_dict[pros_in_text[count]]=text
                count+=1
        for dif in differences:
            print self.cur_file
            print pro_text_dict[dif]
                          
    def multi_task(self):
        files=[x for x in os.listdir(self.data_path)]
        for file_name in files:
            if ".xml" in file_name:
                self.cur_file=file_name
                self.parse_xml(file_name,file_name.replace(".xml",".meta"),self.Check)

if __name__=="__main__":
    ck=CheckPro("../Data/XMLData"," ");
    ck.multi_task()
    print "Finish"


