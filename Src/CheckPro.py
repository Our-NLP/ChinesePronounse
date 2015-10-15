from XML_Parser import xml_parser
import os
import re
class CheckPro(xml_parser):
    def __init__(self,data_path,output_path):
        xml_parser.__init__(self,data_path,output_path);
        
    def Check(self,root,out_file):
        texts= root[0].text.splitlines()
        tags=  root[1]
        label_pro=[]

        for tag in tags:
            label_pro.append(tag.attrib["start"])
        label_pro=sorted(label_pro,key=lambda x: int(x))
        print label_pro
        pros_in_text=[m.start()+1 for m in re.finditer('\*pro\*',root[0].text)]

        pro_count=0
        for text in texts:
            pro_num_this_line=len([m.start()+1 for m in re.finditer('\*pro\*',text)])
            for i in range(pro_num_this_line):
                if pros_in_text[pro_count]!=int(label_pro[pro_count]):
                    print text,pros_in_text[pro_count],label_pro[pro_count]
                pro_count+=1

                
          
    def multi_task(self):
        files=[x for x in os.listdir(self.data_path)]
        for file_name in files:
            if ".xml" in file_name:
                self.parse_xml(file_name,file_name.replace(".xml",".meta"),self.Check)

if __name__=="__main__":
    ck=CheckPro("../XMLData","../CheckPro");
    ck.multi_task()
    print "Finish"

