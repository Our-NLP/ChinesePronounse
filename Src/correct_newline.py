# -*- coding: utf-8 -*-
import os
class Correct:
    def __init__(self):
        self.data_dir=os.path.realpath(os.path.dirname(os.path.realpath("__file__"))+"/../Data")
        self.meta_dir=self.data_dir+"/MetaData/"
        self.output_dir=self.data_dir+"/new_Data/"
        
    def multi_task(self):
        for file in os.listdir(self.meta_dir):
            if not file.endswith('meta'):
                continue
            with open(self.meta_dir+file) as fin,open(self.output_dir+file,'w') as out:
                for line in fin:
                    tokens=line.split('\t')
                    tag= tokens[7].split(' ')
                    pos=tag[-1].split('#')[1]
                    word=tag[-1].split('#')[0]
                    if len(pos)>10:
                        for i,ch in enumerate(pos):
                            if (pos[i] =='C' and pos[i+1]=='H') or (pos[i]=='S' and pos[i+1]=='M'):
                                new_pos=word+"#"+pos[:i]
                                rest=tokens[8:]
                                rest.insert(0,file.replace('meta','xml'))
                        tag[-1]=new_pos
                        tag_str=' '.join(tag)
                        line='\t'.join(tokens[:7])
                        line+='\t'+tag_str+'\n'
                        print line
                        #out.write()
                        print '\t'.join(rest)
                        out.write(line)
                        out.write('\t'.join(rest))
                    else:
                        out.write(line)
                        

if __name__=="__main__":
    ct=Correct()
    #print ct.postaged_dir
    ct.multi_task()
