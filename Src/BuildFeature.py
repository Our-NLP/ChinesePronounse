import os


class BuildFeature:
    def __init__(self):
        self.data_dir=os.path.realpath(os.path.dirname(os.path.realpath("__file__"))+"/../Data")
        self.meta_dir=self.data_dir+"/MetaData/"
        self.feature_dir=self.data_dir+"/Features/"


        self.feature_file=self.feature_dir+"features.fb"
        self.feature_func=[]
        
    def run(self):
        self.feature_func.append(self.get_filename)
        self.feature_func.append(self.get_label)
        self.feature_func.append(self.get_participant)
        self.feature_func.append(self.get_suid)
        self.feature_func.append(self.get_protype)



        self.multi_task()

    def multi_task(self):
        files=os.listdir(self.meta_dir)
        for f_name in files:
            if f_name.endswith(".meta"):
                #print f_name
                self.extract_feature(f_name,f_name.replace(".meta",".fb"))
            
    def extract_feature(self,in_file,out_file):
        in_path=self.meta_dir+in_file
        out_path=self.feature_dir+out_file
        with open(in_path) as input_file, open(out_path,'w') as output_file:
            for line in input_file:
                #0:f_name
                #1:pro_type
                #2:pro_loc_global
                #3:pro_loc_relative
                #4:sent
                #5:suid
                #6:speaker
                #7:postags
                items=line.split("\t")
                output_file.write(self.get_label(items))
                for fuc in self.feature_func:
                    output_file.write(' '+fuc.__name__+":"+fuc(items))
                output_file.write("\n")
    def get_filename(self,item):
        return item[0]
    def get_protype(self,item):
        return item[1]
    def get_label(self,item):
        return item[3]
    def get_suid(self,item):
        return item[5]
    def get_participant(self,item):
        return item[6]




if __name__=="__main__":
    bf=BuildFeature()
    bf.run()
