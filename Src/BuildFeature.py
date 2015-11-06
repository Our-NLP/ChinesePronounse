# -*- coding: utf-8 -*-
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
        self.feature_func.append(self.unigram_followed_cirtical_words)
        self.feature_func.append(self.HaoXiangShiAtHead)
        #self.feature_func.append(self.HaoXiangFeature)
        self.feature_func.append(self.without_pro_in_sentence)

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

                for loc in range(0,len(items[4])):
                    if loc!=0 and items[4][loc]!=' ' and loc!=len(items[4]):
                        continue
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
    ## version 2##
    def unigram_followed_cirtical_words(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        if next_tag=='index error':
            return '0'
        else:
            next_word=self.get_word_from_tag(next_tag)
            if next_word=='对' or next_word=='也' or next_word=='能' or next_word=='应该' or next_word=='谢谢':
                return '1'
            else:
                return '0'

    def HaoXiangShiAtHead(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next_next_tag=self.get_next_N(item,loc,2)
        pre_tag=self.get_pre_N(item,loc,1)
        if next_tag=='index error' or next_next_tag=="index error":
            return '0'
        else:
            next_word=self.get_word_from_tag(next_tag)
            next_next_word=self.get_word_from_tag(next_next_tag)
            if(next_word!='好像' or next_next_word!='是'):
                return '0'
            if pre_tag=='index error':
                return '10'
            else:
                pre_pos=self.get_pos_from_tag(pre_tag)
                if pre_pos=='PU':
                    return '10'
        return '0'




    def HaoXiangFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next_next_tag=self.get_next_N(item,loc,2)
        pre_tag=self.get_pre_N(item,loc,1)
        pre_pre_tag=self.get_pre_N(item,loc,2)
        if next_tag=='index error':
            return '0'
        next_word=self.get_word_from_tag(next_tag)
        if next_word!='好像':
            return '0'

        if pre_tag!='index error':
            pre_word=self.get_word_from_tag(pre_tag)
            pre_pos=self.get_pos_from_tag(pre_tag)
            #if 'N' in pre_pos or pre_word=='就' or pre_pos=='DEG' or pre_pos=='DT':
            #    return '0'
            #if pre_word=='这些' or pre_word=='那边' or pre_word=='现在' or pre_word=='就' or pre_word=='那个' or pre_pos=='NN':
            #    return '0'
            if pre_pos=='NN' or pre_pos=='NP':
                return '0'
        if next_next_tag == 'index error':
            return '0'
        next_next_word=self.get_word_from_tag(next_next_tag)
        next_next_pos=self.get_pos_from_tag(next_next_tag)
        if next_next_pos=='NN' or next_next_pos=="NP":
            return '0'
        ##Check the pre_pre
        return '1'
    def without_pro_in_sentence(self,item,loc):
        i=1;
        while(self.get_pre_N(item,loc,i)!='index error'):
            pre_tag=self.get_pre_N(item,loc,i)
            pre_pos=self.get_pos_from_tag(pre_tag)
            if pre_pos=='PU':
                break
            elif pre_pos=='PN':
                return '0'
            i+=1
        i=1
        while(self.get_next_N(item,loc,i)!='index error'):
            next_tag=self.get_next_N(item,loc,i)
            next_pos=self.get_pos_from_tag(next_tag)
            if next_pos=='PN':
                return '0'
            i+=1
        return '1'

            




        ##### helper function ####
    def get_next_N(self,item,loc,n):
        index=self.loclist.index(loc)
        if index+n-1>=len(self.loclist):
            #print self.loclist
            #print index,len(self.loclist),n
            return 'index error'
        else:
            index=index+n-1
            next_loc=self.loclist[index]
            next_tag= self.loc2tag[next_loc]
            return next_tag


    def get_pre_N(self,item,loc,n):
        #print loc,self.loclist
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
    def get_word_from_tag(self,tag):
        return tag.split("#")[0]

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
