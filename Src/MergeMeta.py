import os

class MergeMeta:
    def __init__(self,data_path,output_path):
        #input and output directory name
        self.data_path=data_path
        self.output_path=output_path
        self.cur_file=""
        if self.data_path[-1] is not '/':
            self.data_path+="/"
        if self.output_path[-1] is not '/':
            self.output_path+="/"
    
    def merge(self,fname):
        last_sent=''
        global_loc=[]
        relative_loc=[]
        pro_type=[]
        file_name=''
        postag=''
        speaker=''
        sid=''
        with open(self.data_path+fname) as fin, open(self.output_path+fname,'w') as fout:
            for line in fin:
                tokens=line.split('\t')
                if (tokens[4]!=last_sent or tokens[5]!=sid) and last_sent!='' and sid!='':
                    out_buf=file_name+'\t'+','.join(pro_type)+'\t'+','.join(global_loc)+'\t'+','.join(relative_loc)+'\t'+last_sent+'\t'+sid+'\t'+speaker+'\t'+postag
                    fout.write(out_buf)
                    last_sent=''
                    global_loc=[]
                    relative_loc=[]
                    pro_type=[]
                    file_name=''
                    postag=''
                    speaker=''
                    sid=''
                
                file_name=tokens[0]
                pro_type.append(tokens[1])
                global_loc.append(tokens[2])
                relative_loc.append(tokens[3])
                last_sent=tokens[4]
                sid=tokens[5]
                speaker=tokens[6]
                postag=tokens[7]

                    
                    
                
    
    def Multi_task(self):
        for f in os.listdir(self.data_path):
            if not f.endswith('.meta'):
                continue
            else:
                self.merge(f)


if __name__=="__main__":
    xp= MergeMeta("../Data/MetaData","../Data/MergedMetaData")
    #xp.merge('CHT_CMN_20101230.0004.su.meta')
    xp.Multi_task()
