import os


class BuildFeature:
    def __init__(self):
        """ multiple input,single output"""
        
        self.data_dir=os.path.realpath(os.path.dirname(os.path.realpath("__file__"))+"/../Data")
        self.meta_dir=self.data_dir+"/MetaData/"
        self.feature_dir=self.data_dir+"/Features/"

        self.feature_file=self.feature_dir+"features.fb"
        self.feature_func=[]

        self.loc2tag={}
        self.loclist=[]
        
    def run(self):
        #self.feature_func.append(self.get_filename)
        #self.feature_func.append(self.cur_loc)
        #self.feature_func.append(self.get_participant) too big value!
        self.feature_func.append(self.is_head)
        #self.feature_func.append(self.followed_verb)
        self.feature_func.append(self.pre_noun_followed_verb)
        self.feature_func.append(self.at_head_followed_verb)
        self.feature_func.append(self.followed_noun)
        self.feature_func.append(self.is_pre_noun)
        self.feature_func.append(self.is_pre_pre_noun)
        self.feature_func.append(self.is_pre_pre_pre_noun)
        self.feature_func.append(self.followed_verb)
        self.feature_func.append(self.is_next_next_verb)
        self.feature_func.append(self.is_next_next_next_verb)
        #self.feature_func.append(self.god_mod) #testing only!
        #self.feature_func.append(self.get_suid)
        #self.feature_func.append(self.get_protype)
        self.multi_task()

    def multi_task(self):
        files=os.listdir(self.meta_dir)
        with open(self.feature_file,'w') as out:
            for f_name in files:
                if f_name.endswith(".meta"):
                    #print f_name
                    self.extract_feature(f_name,out)
            
    def extract_feature(self,in_file,output_file):
        in_path=self.meta_dir+in_file
        with open(in_path) as input_file:
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
                count=0
                self.loc2tag={}
                self.loclist=[]
                for loc in range(0,len(items[4])):
                    if loc!=0 and items[4][loc]!=' ' and loc!=len(items[4]):
                        continue
                    #build loc->postag
                    self.loc2tag[loc]=items[7].split(' ')[count]
                    count+=1
                    self.loclist.append(loc)

                    output_file.write(str(self.get_label(items,loc)))
                    feature=''
                    for fuc in self.feature_func:
                        feature+=' '+fuc.__name__+":"+fuc(items,loc)
                    output_file.write(feature)
                    output_file.write("\n")
                
##### feature #####
    def at_head_followed_verb(self,item,loc):
        if self.is_head(item,loc) and self.followed_verb(item,loc):
            return '1'
        else:
            return '0'
    def followed_noun(self,item,loc):
        if self.is_noun(self.loc2tag[loc]): 
            return '1'
        else:
            return '1'

    def followed_verb(self,item,loc):
        #print  "follow:",self.loc2tag[loc],loc
        if self.is_verb(self.loc2tag[loc]): 
            return '1'
        else:
            return '0'
        
        
    def is_pre_noun(self,item,loc):
        if loc==0:
            return '0'
        pre_tag=self.get_pre_tag(item,loc)
        if self.is_noun(pre_tag):
            return '1'
        else:
            return '0'
    def is_pre_pre_noun(self,item,loc):
        pre_tag=self.get_pre_N(item,loc,2)
        if pre_tag=="index error":
            return '0'
        elif self.is_noun(pre_tag):
            return '1'
        else:
            return '0'
    def is_pre_pre_pre_noun(self,item,loc):
        pre_tag=self.get_pre_N(item,loc,3)
        if pre_tag=="index error":
            return '0'
        elif self.is_noun(pre_tag):
            return '1'
        else:
            return '0'
    def is_next_next_verb(self,item,loc):
        next_tag=self.get_next_N(item,loc,2)
        if next_tag=='index error':
            return '0'
        elif self.is_verb(next_tag):
            return '1'
        else:
            return '0'
    def is_next_next_next_verb(self,item,loc):
        next_tag=self.get_next_N(item,loc,3)
        if next_tag=='index error':
            return '0'
        elif self.is_verb(next_tag):
            return '1'
        else:
            return '0'        

    def pre_noun_followed_verb(self,item,loc):
        #print item[7]
        #pre_bool= self.is_pre_noun(item,loc)=='1'
        #next_bool=self.followed_verb(item,loc)=='1'
        if  self.is_pre_noun(item,loc)=='1' and self.followed_verb(item,loc)=='1':
            return '1'
        else:
            return '0'
##### helper function ####
    def get_next_N(self,item,loc,n):
        index=self.loclist.index(loc)
        if index+n-1>=len(self.loclist):
            return 'index error'
        else:
            print self.loclist
            print index,len(self.loclist),n
            index=index+n-1
            next_loc=self.loclist[index]
            next_tag= self.loc2tag[pre_loc]
            return next_tag

            
    def get_pre_N(self,item,loc,n):
        index=self.loclist.index(loc)
        if index<n:
            return "index error"
        else:
            index=index-n
            pre_loc=self.loclist[index]
            pre_tag= self.loc2tag[pre_loc]
            return pre_tag


    def get_pre_tag(self,item,loc):
        #index=self.loclist.index(loc)-1
        #pre_loc=self.loclist[index]
        #pre_tag= self.loc2tag[pre_loc]
        #print "pre:",pre_tag
        #return pre_tag
        return self.get_pre_N(item,loc,1)

    def get_pos_from_tag(self,tag):
        return tag.split("#")[1]

    def is_sign(self,tag):
        pos=self.get_pos_from_tag(tag)
        if pos=='PU':
            return True
        else:
            return False

    def is_verb(self,tag):
        pos=self.get_pos_from_tag(tag)
        if 'V' in pos or pos=='BA' or pos=='P':
            return True
        else:
            return False
    def is_noun(self,tag):
        pos=self.get_pos_from_tag(tag)
        if pos=='NN' or pos=='PN' or pos=='NR':
            return True
        else:
            return False
    def get_label(self,item,loc):
        #if loc can be the place to hide pro
        if loc == int(item[3]):
            return 1
        else:
            return 0
    def get_filename(self,item,loc):
        return item[0]
    def get_protype(self,item,loc):
        return item[1]
    def get_relative_loc(self,item,loc):
        return item[3]
    def cur_loc(self,item,loc):
        return str(loc)
    def get_suid(self,item,loc):
        return item[5]
    def get_participant(self,item,loc):
        return item[6]
    def god_mod(self,item,loc):
        if int(item[3])==loc:
            return str(100)
        else:
            return str(0)
    def is_head(self,item,loc):
        '''if current is at the beginning of sentence'''
        if loc==0:
            return '1'
        elif self.is_sign(self.get_pre_tag(item,loc)):
            return '1'
        else:
            return '0'




if __name__=="__main__":
    bf=BuildFeature()
    bf.run()
