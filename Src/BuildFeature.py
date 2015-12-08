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
        self.feature_func.append(self.at_head)
        self.feature_func.append(self.followed_verb)
        #self.feature_func.append(self.pre_noun_followed_verb)
        #self.feature_func.append(self.at_head_followed_verb)
        #self.feature_func.append(self.followed_noun)
        #self.feature_func.append(self.is_pre_noun)
        #self.feature_func.append(self.is_pre_pre_noun)
        #self.feature_func.append(self.is_pre_pre_pre_noun)
        #self.feature_func.append(self.followed_verb)
        #self.feature_func.append(self.is_next_next_verb)
        #self.feature_func.append(self.is_next_next_next_verb)
        #self.feature_func.append(self.unigram_followed_cirtical_words)
        #self.feature_func.append(self.HaoXiangShiAtHead)
        #self.feature_func.append(self.YeJiuFeature)
        #self.feature_func.append(self.LenSmaller4)
        #self.feature_func.append(self.DanShiFeature)
        #self.feature_func.append(self.GenFeature)
        ##self.feature_func.append(self.HaoXiangFeature)
        #self.feature_func.append(self.without_pro_in_sentence)
        #self.feature_func.append(self.RuGuoYouFeature)
        #self.feature_func.append(self.ShiDeFeature)
        #self.feature_func.append(self.ZhenHaoFeature)
        #self.feature_func.append(self.ZhiDaoFeature)
        #self.feature_func.append(self.DuiLeFeature)
        #self.feature_func.append(self.HaoDeFeature)
        #self.feature_func.append(self.XieXieFeature)
        #self.feature_func.append(self.NaJiuFeature)
        #self.feature_func.append(self.ZaiMaFeature)


        ##self.feature_func.append(self.god_mod) #testing only!
        ##self.feature_func.append(self.get_suid)
        ##self.feature_func.append(self.get_protype)


        #self.feature_func.append(self.first_sent)
        #self.feature_func.append(self.same_speaker)

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
        self.pre_sent=[]
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
                if self.pre_sent==[]:
                    self.pre_sent.append(items)
                else:
                    pre=self.pre_sent[-1]
                    if pre[4] != items[4]:
                        self.pre_sent.append(items)
                count=0
                #print items[4]
                #print self.loclist
                #for key in self.loc2tag:
                #    print key,self.loc2tag[key]
                self.loc2tag={}
                self.loclist=[]
                sentence=items[4].decode('utf8')
                sentence=u' '+sentence+u' '
                
                for loc in range(0,len(sentence)):
                    print loc,sentence[loc],len(sentence.strip())
                    if loc!=0 and sentence[loc]!=' ' and loc!=len(sentence):
                        continue
                    #build loc->postag
                    if loc<len(sentence)-1:
                        self.loc2tag[loc]=items[7].split(' ')[count]
                    count+=1
                    self.loclist.append(loc)
                for loc in range(0,len(sentence)):
                    if loc!=0 and sentence[loc]!=' ' and loc!=len(sentence):
                        continue
                    output_file.write(str(self.get_label(items,loc)))
                    feature=''
                    for fuc in self.feature_func:
                        feature+=' '+fuc.__name__+":"+fuc(items,loc)
                    output_file.write(feature)
                    output_file.write("\n")


##### 你我其他feature #####
    def NaJiuFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        pre_tag=self.get_pre_N(item,loc,1)
        if pre_tag=='index error' or next_tag=='index error':
            return '0'
        else:
            next_word=self.get_word_from_tag(next_tag)
            pre_word=self.get_word_from_tag(pre_tag)
            if pre_word == '那' and next_word=='就':
                return '1'
            else:
                return '0'
    def ZaiMaFeature(self,item,loc):
        if loc!=0:
            return '0'
        else:
            next_tag=self.get_next_N(item,loc,1)
            next_next_tag=self.get_next_N(item,loc,2)
            if next_tag=='index error':
                return '0'
            else:
                if self.get_word_from_tag(next_tag)=='在' and next_next_tag!='index error':
                    next_next_word=self.get_word_from_tag(next_next_tag)
                    if next_next_word=='吗'or next_next_word=='?':
                        #print item[1],item[4]
                        return '1'
                    else:
                        return '0'
                else:
                    return '0'
                

                
    def first_sent(self,item,loc):
        if len(self.pre_sent)==1:
            return '1'
        else:
            return '0'
    def same_speaker(self,item,loc):
        if len(self.pre_sent)>1 and self.pre_sent[-2][6]==item[6]:
            return '1'
        else:
            return '0'
            
##### general feature #####
    def at_head(self,item,loc):
        if self.is_head(item,loc):
            return '1'
        else:
            return '0'

    '''def at_head_followed_verb(self,item,loc):
        if self.is_head(item,loc): 
            return self.followed_verb(item,loc)'''

    def followed_noun(self,item,loc):
        if self.is_noun(self.loc2tag[loc]): 
            return '1'
        else:
            return '0'

    def followed_verb(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        #print 'loc',loc,' next',next_tag
        if next_tag=='index error':
            return '0'
        elif self.is_verb(next_tag): 
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
    def LenSmaller4(self,item,loc):
        last_loc=self.loclist[-1]
        last_tag= self.loc2tag[last_loc]
        last_word=self.get_pos_from_tag(last_tag)
        if len(self.loclist)<=6 and (last_tag=="SP" or last_tag=='PU'):
            return "1"
        else:
            return "0"
    def DanShiFeature(self,item,loc):
        pre_tag=self.get_pre_N(item,loc,1)
        next_tag=self.get_next_N(item,loc,1)
        if pre_tag=='index error':
            pre_word= self.get_word_from_tag(pre_tag)
            if pre_word!='但是':
                return '0'
        if next_tag=='index error':
            return '0'
        next_pos=self.get_pos_from_tag(next_tag)
        if 'N' in next_pos:
            return '0'
        return '1'

    def YeJiuFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1);
        next_next_tag=self.get_next_N(item,loc,2);
        if next_tag == 'index error' or next_next_tag=='index error':
            return "0"
        next_word=self.get_word_from_tag(next_tag)
        next_next_word=self.get_word_from_tag(next_next_tag)

        pre_tag=self.get_pre_N(item,loc,1)
        pre_pre_tag=self.get_pre_N(item,loc,2)
        if pre_tag== 'index error' or  pre_pre_tag== 'index error':
            return "0";
        pre_pos=self.get_pos_from_tag(pre_tag)
        pre_pre_pos=self.get_pos_from_tag(pre_pre_tag)
        
        if pre_pos=='NN' or pre_pos=='PN':
            return "0";     
        if next_word== '也' and next_next_word=='就':
            return "1";
        return "0";
    def GenFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        next3tag=self.get_next_N(item,loc,3)

        pre_tag=self.get_pre_N(item,loc,1)

        if next_tag!='index error':
                next_word=self.get_word_from_tag(next_tag)
                next_pos=self.get_pos_from_tag(next_tag)
                if next_word=='跟':
                    pre_pos=self.get_word_from_tag(pre_tag)
                    if pre_tag!='index error':
                        if 'N' not in pre_pos:
                            return '10'
                elif next2tag!='index error':
                        next2word=self.get_word_from_tag(next2tag)
                        next2pos=self.get_pos_from_tag(next2tag)
                        if next2tag=='跟':
                            pre_pos=self.get_word_from_tag(pre_tag)
                            if pre_tag!='index error':
                                if 'N' not in pre_pos and 'N' not in next_pos:
                                    return '10' 
        return '0'
    def RuGuoYouFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        pre_tag=self.get_pre_N(item,loc,1)
        if next_tag=='index error':
            return '0'
        else:
            next_word=self.get_word_from_tag(next_tag)
            if next_word=='如果' and next2tag!='index error':
                next2word=self.get_word_from_tag(next2tag)
                if next2word=='有':
                    return "1"
            elif next_word=='有' and pre_tag!='index error':
               pre_word=self.get_word_from_tag(pre_tag)
               if pre_word=='如果':
                   return '1'
        return '0'
    def ShiDeFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        if next_tag!='index error' and next2tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            next2word=self.get_word_from_tag(next2tag)
            if next_word=='是' and next2word=='的':
                return '1'
        return '0'

    def ZhenHaoFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        if next_tag!='index error' and next2tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            next2word=self.get_word_from_tag(next2tag)
            if next_word=='真' and next2word=='好':
                return '1'
        return '0'
    def BuKeQiFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        if next_tag!='index error' and next2tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            next2word=self.get_word_from_tag(next2tag)
            if next_word=='不' and next2word=='客气':
                return '1'
        return '0'
    def ZhiDaoFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        next3tag=self.get_next_N(item,loc,3)
        pre_tag=self.get_pre_N(item,loc,1)
        if pre_tag!='index error':
            pre_pos=self.get_pos_from_tag(pre_tag)
            if pre_pos=='PN':
                return '0'
        if next_tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            if next_word=='知道':
                return '1'
            if next2tag!='index error':
                next2word=self.get_word_from_tag(next2tag)
                if next2word=='知道':
                    return '1'
            if next3tag!='index error':
                next3word=self.get_word_from_tag(next2tag)
                if next3word=='知道':
                    return '1'
        return '0'
    def DuiLeFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        if next_tag!='index error' and next2tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            next2word=self.get_word_from_tag(next2tag)
            if next_word=='对' and next2word=='了':
                return '1'
        return '0'
    def HaoDeFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        if next_tag!='index error' and next2tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            next2word=self.get_word_from_tag(next2tag)
            if next_word=='好' and next2word=='的':
                return '1'
        return '0'
    def XieXieFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        if next_tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            if next_word=='谢谢' :
                return '1'
        return '0'


        

        

        
        

        
        ##### helper function ####
    def get_next_N(self,item,loc,n):
        index=self.loclist.index(loc)
        if index+n-1>=len(self.loclist)-1:
            #print self.loclist
            #print index,len(self.loclist),n
            return 'index error'
        else:
            index=index+n-1
            print self.loclist
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
            if '我' in item[1] and '我们' not in item[1]:
                return '我'
            elif '你' in item[1] and '你们' not in item[1]:
                return '你'
            else:
                return '其他'
        else:
            return 'none'
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
            return True
        elif self.is_sign(self.get_pre_tag(item,loc)):
            #print self.get_pre_tag(item,loc)
            return True
        else:
            return False




if __name__=="__main__":
    bf=BuildFeature()
    bf.run()
