# -*- coding: utf-8 -*-
import os
import sys

class BuildFeature:
    def __init__(self):
        """ multiple input,single output"""


        self.global_count=0
        self.data_dir=os.path.realpath(os.path.dirname(os.path.realpath("__file__"))+"/../Data")
        self.meta_dir=self.data_dir+"/MergedMetaData/"
        self.feature_dir=self.data_dir+"/Features/"

        self.feature_file=self.feature_dir+"features.fb"
        self.feature_func=[]

        self.loc2tag={}
        self.loclist=[]

    def run(self):
        

        #self.feature_func.append(self.god_mod) #testing only!
        self.feature_func.append(self.UnigramsInWindow)
        self.feature_func.append(self.BigramsInWindow)
        self.feature_func.append(self.PosOfUnigramsInWindow)
        self.feature_func.append(self.PosOfBigramsInWindow)

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
        #self.pre_PN={}# user id as key
        with open(in_path) as input_file:
            self.pre_PN={}# user id as key
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
                    #print loc,sentence[loc],len(sentence.strip())
                    if loc!=0 and sentence[loc]!=' ' and loc!=len(sentence):
                        continue
                    #build loc->postag
                    if loc<len(sentence)-1:
                         self.loc2tag[loc]=items[7].split(' ')[count]
                    count+=1
                    self.loclist.append(loc)
                count=0
                for loc in range(0,len(sentence)):
                    if loc!=0 and sentence[loc]!=' ' and loc!=len(sentence):
                        continue
                    output_file.write(str(self.global_count)+' '+str(self.get_label(items,loc)))
                   
                    feature=''
                    for fuc in self.feature_func:
                        #print fuc.__name__
                        #feature+=' '+fuc.__name__+":"+fuc(items,loc)
                        feature+=' '+fuc(items,loc)
                    self.global_count+=1
                    #update pre_PN
                    speaker=items[6]
                    if self.NextIsSomePos(items,loc,'PN')=='1':
                        pro_tag=self.get_next_N(items,loc,1)
                        pro=self.get_word_from_tag(pro_tag)
                        if speaker in self.pre_PN:
                            self.pre_PN[speaker].append(pro)
                        else:
                            self.pre_PN[speaker]=[pro]

                    output_file.write(feature)
                    output_file.write("\n")

    def printState(self,item,loc):
        print ' '
        print item[7],"locs: ",item[3]," labels",item[1]
        print 'cur:',loc
        return '1'
### new features####
    def UnigramsInWindow(self,item,loc):
        res=[]
        pre_tag=self.get_pre_N(item,loc,1)
        pre2_tag=self.get_pre_N(item,loc,2)
        next_tag=self.get_next_N(item,loc,1)
        next2_tag=self.get_next_N(item,loc,2)
            
        if pre2_tag!='index error':
            pre2_word=self.get_word_from_tag(pre2_tag)
            res.append(pre2_word)
        if pre_tag!='index error':
            pre_word=self.get_word_from_tag(pre_tag)
            res.append(pre_word)
        if next_tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            res.append(next_word)
        if next2_tag!='index error':
            next2_word=self.get_word_from_tag(next2_tag)
            res.append(next2_word)
        return ' '.join(res)
    def BigramsInWindow(self,item,loc):
        pre_tag=self.get_pre_N(item,loc,1)
        pre2_tag=self.get_pre_N(item,loc,2)
        next_tag=self.get_next_N(item,loc,1)
        next2_tag=self.get_next_N(item,loc,2)

        pre_bigram=''
        next_bigram=''
        if pre2_tag!='index error' and pre_tag!='index error':
            pre2_word=self.get_word_from_tag(pre2_tag)
            pre_word=self.get_word_from_tag(pre_tag)
            pre_bigram=pre2_word+'_'+pre_word
        if next_tag!='index error' and next2_tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            next2_word=self.get_word_from_tag(next2_tag)
            next_bigram=next_word+'_'+next2_word
        return pre_bigram+" "+next_bigram
    def PosOfUnigramsInWindow(self,item,loc):
        res=[]
        pre_tag=self.get_pre_N(item,loc,1)
        pre2_tag=self.get_pre_N(item,loc,2)
        next_tag=self.get_next_N(item,loc,1)
        next2_tag=self.get_next_N(item,loc,2)

        
        if pre2_tag!='index error':
            pre2_pos=self.get_pos_from_tag(pre2_tag)
            res.append(pre2_pos.strip())
        if pre_tag!='index error':
            pre_pos=self.get_pos_from_tag(pre_tag)
            res.append(pre_pos.strip())
        if next_tag!='index error':
            next_pos=self.get_pos_from_tag(next_tag)
            res.append(next_pos.strip())
        if next2_tag!='index error':
            next2_pos=self.get_pos_from_tag(next2_tag)
            res.append(next2_pos.strip())
        return ' '.join(res)
    def PosOfBigramsInWindow(self,item,loc):
        pre_tag=self.get_pre_N(item,loc,1)
        pre2_tag=self.get_pre_N(item,loc,2)
        next_tag=self.get_next_N(item,loc,1)
        next2_tag=self.get_next_N(item,loc,2)

        pre_bigram=''
        next_bigram=''
        if pre2_tag!='index error' and pre_tag!='index error':
            pre2_pos=self.get_pos_from_tag(pre2_tag)
            pre_pos=self.get_pos_from_tag(pre_tag)
            pre_bigram=pre2_pos+'_'+pre_pos
        if next_tag!='index error' and next2_tag!='index error':
            next_pos=self.get_pos_from_tag(next_tag)
            next2_pos=self.get_pos_from_tag(next2_tag)
            next_bigram=next_pos+'_'+next2_pos
        return pre_bigram+" "+next_bigram





        
        


























##### 你我其他feature #####
    def NextIsSomeWord(self,item,loc,word):
        next_tag=self.get_next_N(item,loc,1)
        if next_tag=='index error':
            return '0'
        else:
            next_word=self.get_word_from_tag(next_tag)
            if next_word==word:
                return '1'
            else:
                return '0'
    def NextIsSomePos(self,item,loc,pos):
        next_tag=self.get_next_N(item,loc,1)
        if next_tag=='index error':
            return '0'
        else:
            next_pos=self.get_pos_from_tag(next_tag)
            if next_pos==pos:
                return '1'
            else:
                return '0'

    def PreIsSomeWord(self,item,loc,word):
        pre_tag=self.get_pre_N(item,loc,1)
        if pre_tag=='index error':
            return '0'
        else:
            pre_word=self.get_word_from_tag(pre_tag)
            if pre_word==word:
                return '1'
            else:
                return '0'
    def PreIsSomePos(self,item,loc,pos):
        pre_tag=self.get_pre_N(item,loc,1)
        if pre_tag=='index error':
            return '0'
        else:
            pre_pos=self.get_pos_from_tag(pre_tag)
            if pre_pos==pos:
                return '1'
            else:
                return '0'
    
    def SomeWordInPre(self,item,loc,word,n=sys.maxint):
        cur_index=self.loclist.index(loc)
        while cur_index>0 and n>0:
            loc=self.loclist[cur_index]
            if self.PreIsSomeWord(item,loc,word)=='1':
                return '1'
            cur_index-=1
            n-=1
        return '0'
    
    def SomePosInPre(self,item,loc,pos,n=sys.maxint):
        cur_index=self.loclist.index(loc)
        while cur_index>0 and n>0:
            loc=self.loclist[cur_index]
            if self.PreIsSomePos(item,loc,pos)=='1':
                return '1'
            cur_index-=1
            n-=1
        return '0'

    def SomeWordInFollow(self,item,loc,word,n=sys.maxint):
        cur_index=self.loclist.index(loc)
        while cur_index < len(self.loclist) and n>0:
            loc=self.loclist[cur_index]
            if self.NextIsSomeWord(item,loc,word)=='1':
                return '1'
            cur_index+=1
            n-=1
        return '0'
    def SomePosInFollow(self,item,loc,pos,n=sys.maxint):
        cur_index=self.loclist.index(loc)
        while cur_index < len(self.loclist) and n>0:
            loc=self.loclist[cur_index]
            if self.NextIsSomePos(item,loc,pos)=='1':
                return '1'
            cur_index+=1
            n-=1
        return '0'

    def NextLoc(self,item,loc):
        index=self.loclist.index(loc)
        if index+1<len(self.loclist):
            return self.loclist[index+1]
        else:
            return loc
    def NoPNFollowingVerb(self,item,loc):
        if self.SomePosInPre(item,loc,'PN')=='0' and self.SomePosInPre(item,loc,'NN')=='0':
            if self.SomePosInFollow(item,loc,'VV',2)=='1' or self.SomePosInFollow(item,loc,'VC',2)=='1' or self.SomePosInFollow(item,loc,'VA',2)=='1':
                return '1'
        return '0'
    
    def SameSpeakerProType(self,item,loc):
        speaker=item[6]
        if speaker in self.pre_PN:
            pro=self.pre_PN[speaker][-1]
            if '我' in pro and '我们' not in pro :
                return '1'
            elif '你' in pro and '你们' not in pro:
                return '2'
            else:
                return '3'
        else:
            return '0'
    
    def OtherSpeakerProType(self,item,loc):
        other= None
        for key in self.pre_PN:
            if key != item[6]:
                other = key
        if other != None:
            pro= self.pre_PN[other][-1]
            if '我' in pro and '我们' not in pro :
                return '1'
            elif '你' in pro and '你们' not in pro:
                return '2'
            else:
                return '3'
        else:
            return '0'
    def PreSentFirst(self,item,loc):
        if self.NextIsSomePos(item,loc,'VV')=='0':
            return '0'
        if len(self.pre_sent) >1:
            last=self.pre_sent[-2][7].split(' ')
            for tag in last:
                pos=self.get_pos_from_tag(tag)
                word=self.get_word_from_tag(tag)
                if pos=='PN':
                    if '我' in word and '我们' not in word:
                        return '1'
                    elif '你' in word and '你们' not in word:
                        return '2'
                    else:
                        return '3'
                elif pos=='NN':
                    return '3'
        return '0'
    def PreSentSecond(self,item,loc):
        if self.NextIsSomePos(item,loc,'VV')=='0':
            return '0'
        count=0
        if len(self.pre_sent)>1:
            last=self.pre_sent[-2][7].split(' ')
            for tag in last:
                pos=self.get_pos_from_tag(tag)
                if pos == 'NN' or 'PN':
                    count+=1
                if count==2:
                    word=self.get_word_from_tag(tag)
                    if pos=='PN':
                        if '我' in word and '我们' not in word:
                            return '1'
                        elif '你' in word and '你们' not in word:
                            return '2'
                        else:
                            return '3'
                    elif pos=='NN':
                        return '3'
        return '0'


    #其他
    def ShiDe(self,item,loc):
        if self.NextIsSomeWord(item,loc,'是')=='1':
            loc=self.NextLoc(item,loc)
            if self.NextIsSomeWord(item,loc,'的')=='1':
                return '1'
        return '0'
    def Dui(self,item,loc):
        if self.SomePosInPre(item,loc,'PN',3)=='0' and self.SomePosInPre(item,loc,'NN',3) == '0':
            return self.NextIsSomeWord(item,loc,'对')
        return '0'
    def ZenMe(self,item,loc):
        words=['怎么','怎么办','怎么样','谢','看看']
        if self.SomePosInPre(item,loc,'PN')=='1':
            return '0'
        for word in words:
            return self.SomeWordInFollow(item,loc,word,3)
        return '0'
            
    def OKFeature(self,item,loc):
        words=['ok','OK','Okay']
        if self.SomePosInPre(item,loc,'PN')=='0':
            for word in words:
                return self.NextIsSomeWord(item,loc,word)
        return '0'
    def GuJiInFrontFeature(self,item,loc):
        if self.PreIsSomeWord(item,loc,'估计')=='1':
            if self.NextIsSomePos(item,loc,'VV')=='1' or self.NextIsSomePos(item,loc,'AD')=='1':
                return '1'
        return '0'
    def Zai(self,item,loc):
        if self.SomePosInPre(item,loc,'PN',3)=='1' or self.SomePosInPre(item,loc,'NN',3)=='1':
            return '0'
        cur_index=self.loclist.index(loc)
        count=3
        while cur_index<len(self.loclist) and count>0:
            if self.NextIsSomeWord(item,loc,'在'):
                return str(count)
            count-=1
        return '0'
    #我
    def LaiZi(self,item,loc):
        if self.NextIsSomeWord(item,loc,'来自')=='1' or self.NextIsSomeWord(item,loc,'晕')=='1':
            return '1'
        return '0'
    
    def GongXiFeature(self,item,loc):
        if self.PreIsSomeWord(item,loc,'恭喜')=='0':
            return self.NextIsSomeWord(item,loc,'恭喜')
        else:
            return '0'
        
    def GuJiFeature(self,item,loc):
        if self.SomePosInPre(item,loc,'PN',2)=='1' or self.SomePosInPre(item,loc,'NN',2):
            return '0'
        else:
            return self.NextIsSomeWord(item,loc,'估计')
            
        
    #你
    def Deng(self,item,loc):
        if self.NextIsSomeWord(item,loc,'等') and self.NextIsSomePos(item,loc,'VV'):
            return self.SomePosInPre(item,loc,'PN')
        elif self.PreIsSomeWord(item,loc,'等') and self.PreIsSomePos(item,loc,'VV'):
            return self.SomePosInFollow(item,loc,'PN')
        else:
            return '0'
        
    def PreProSPInFollow(self,item,loc):
        if self.SomePosInPre(item,loc,'PN')=='0' :
            if self.SomePosInFollow(item,loc,'SP')=='1':
                return '1'
            elif self.SomeWordInFollow(item,loc,'?') or self.SomeWordInFollow(item,loc,'？'):
                return '1'
            elif self.SomeWordInFollow(item,loc,'!') or self.SomeWordInFollow(item,loc,'！'):
                return '1'
        else:
            return '0'
        
    def WanAnFeature(self,item,loc):
        words=['客气','早点','注意','加油','晚安']
        for word in words:
            if self.SomeWordInFollow(item,loc,word,3)=='1' and self.SomePosInPre(item,loc,'PN',3)=='0' and self.SomePosInPre(item,loc,'NN',3)=='0':
                return '1'
        return '0'
    
    def PreVerb(self,item,loc):
        return self.PreIsSomePos(item,loc,'VV')
    
    def FollowingWo(self,item,loc):
        cur_index=self.loclist.index(loc)
        while(cur_index<len(self.loclist)):
            if self.NextIsSomeWord(item,loc,'我')=='1':
                return '1'
            if self.NextIsSomePos(item,loc,'PU')=='1':
                break
            loc=self.loclist[cur_index]
            cur_index+=1
            
        return '0'

    
    def BaoQianFeature(self,item,loc):
        return self.NextIsSomeWord(item,loc,'抱歉')
        
    def NaJiuFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        pre_tag=self.get_pre_N(item,loc,1)
        if pre_tag=='index error' or next_tag=='index error':
            return '0'
        else:
            next_word=self.get_word_from_tag(next_tag)
            pre_word=self.get_word_from_tag(pre_tag)
            next2tag=self.get_next_N(item,loc,2)
            next2word=self.get_word_from_tag(next2tag)
            next3tag=self.get_next_N(item,loc,3)

            '''if (pre_word=='那' and next_word=='就') or (next_word=='那' and next2word=='就'):
                if next3tag=='index error':
                    return '0'
                next3pos=self.get_pos_from_tag(next3tag)
                if next3pos=='VA':
                    return '0'
                else:
                    return '1'
                
            else:
                return '0'''
            if pre_word == '那' and next_word=='就':
                #print ' '
                #print item[7]," ",item[1]," ",item[3]
                #print 'cur:',loc
                #return '1'
                if next2tag=='index error':
                    return '0'
                else:
                    next2pos=self.get_pos_from_tag(next2tag)
                    if next2pos=='VA':
                        return '0'
                    elif next2pos=='VD':
                        return '1'
                    elif next2pos=='VV':
                        return '2'
                    else:
                        return '1'
            else:
                return '0'

    def ZaiMaFeature(self,item,loc):
        '''if loc!=0 or self.NextIsSomeWord(item,loc,'在')=='0':
            return '0'
        if len(self.loclist)<=5:
            #self.printState(item,loc)
            return '1'
        else:
            tag= self.get_next_N(item,loc,4)
            if self.get_pos_from_tag(tag)=='PU':
                #self.printState(item,loc)
                return '1'
        return '0'''

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
                        #self.printState(item,loc)
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
    def FollowPU(self,item,loc):
        return self.NextIsSomePos(item,loc,'PU')
    def at_head(self,item,loc):
        if self.is_head(item,loc):
            return '1'
        else:
            return '0'

    def followed_noun(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        #print 'loc',loc,' next',next_tag
        if next_tag=='index error':
            return '0'
        elif self.is_noun(next_tag): 
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

    def without_pro_in_previous(self,item,loc):
        i=1
        while(self.get_pre_N(item,loc,i)!='index error'):
            pre_tag=self.get_pre_N(item,loc,i)
            pre_pos=self.get_pos_from_tag(pre_tag)
            if pre_pos=='PU':
                break
            elif pre_pos=='PN':
                return '0'
            i+=1
        return '1'
    def without_noun_in_previous(self,item,loc):
        i=1
        while(self.get_pre_N(item,loc,i)!='index error'):
            pre_tag=self.get_pre_N(item,loc,i)
            pre_pos=self.get_pos_from_tag(pre_tag)
            if pre_pos=='PU':
                break
            elif self.is_noun(pre_tag):
                return '0'
            i+=1
        return '1'

    def without_pro_in_following(self,item,loc):
        i=1
        while(self.get_next_N(item,loc,i)!='index error'):
            next_tag=self.get_next_N(item,loc,i)
            next_pos=self.get_pos_from_tag(next_tag)
            if next_pos=='PN':
                return '0'
            elif next_pos=='PU':
                break
            i+=1
        return '1'

    def LenFeature(self,item,loc):
        return str(len(self.loclist))
    def LenLargerThan10(self,item,loc):
        if len(self.loclist)>12 :
            return "1"
        else:
            return "0"

    def LenBetween4_10(self,item,loc):
        if(len(self.loclist)>6 and len(self.loclist)<=12):
            return '1'
        else:
            return '0'
    def LenSmaller4(self,item,loc):
        if len(self.loclist)<=6 :
            return "1"
        else:
            return "0"

    def EndWithSign(self,item,loc):
        last_loc=self.loclist[-2]
        last_tag= self.loc2tag[last_loc]
        last_word=self.get_pos_from_tag(last_tag)
        if last_tag=="SP" or last_tag=='PU':
            return '1'
        else:
            return '0'

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
                            return '1'
                elif next2tag!='index error':
                        next2word=self.get_word_from_tag(next2tag)
                        next2pos=self.get_pos_from_tag(next2tag)
                        if next2tag=='跟':
                            pre_pos=self.get_word_from_tag(pre_tag)
                            if pre_tag!='index error':
                                if 'N' not in pre_pos and 'N' not in next_pos:
                                    return '1' 
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
    #其他
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
    #Mixed feature
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
    #其他
    def DuiLeFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        if next_tag!='index error' and next2tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            next2word=self.get_word_from_tag(next2tag)
            if next_word=='对' and next2word=='了':
                return '1'
        return '0'
    #其他
    def HaoDeFeature(self,item,loc):
        next_tag=self.get_next_N(item,loc,1)
        next2tag=self.get_next_N(item,loc,2)
        pre_tag=self.get_pre_N(item,loc,1)
        if next_tag!='index error' and next2tag!='index error':
            next_word=self.get_word_from_tag(next_tag)
            next2word=self.get_word_from_tag(next2tag)
            if next_word=='好' and next2word=='的':
                if pre_tag=='index error':
                    return '1'
                else:
                    pre_pos=self.get_pos_from_tag(pre_tag)
                    if pre_pos=='VV' or pre_pos=='AD' or pre_pos=='NN':
                        return '0'
                    else:
                        return '1'
        return '0'
    #wo featuer
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
        if pos=='VV' or pos=='VC' or pos=='BA' or pos=='P':
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
        candidate_locs=item[3].split(',')
        candidate_pros=item[1].split(',')
        
        #print item[4]
        #print candidate_locs,candidate_pros
        #print 'cur:',loc," ",
        if str(loc) in candidate_locs:
            pro_index=candidate_locs.index(str(loc))
            pro=candidate_pros[pro_index]
            #print pro,
            if '我' in pro and '我们' not in pro:
                #print '我'
                return '我'
            elif '你' in pro and '你们' not in pro:
                #print '你'
                return '你'
            else:
                #print '其他'
                return '其他'
        else:
            #print  'none'
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
        candidate_locs=item[3].split(',')
        candidate_pros=item[1].split(',')
        if str(loc) in candidate_locs:
            pro_index=candidate_locs.index(str(loc))
            pro=candidate_pros[pro_index]
            if '我' in pro and '我们' not in pro :
                return '我'
            elif '你' in pro and '你们' not in pro:
                return '你'
            else:
                return '其他'
        else:
            return 'none'
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
