#coding:gbk
import codecs
import jieba.posseg as pseg
import jieba

names={}
relationships={}
lineNames=[]
jieba.load_userdict("names.txt")
with codecs.open("hlm.txt",'r',"utf-8") as f:
		for line in f.readlines():
			poss=pseg.cut(line)
			lineNames.append([])
			for w in poss:
				if w.flag !='nr' or len(w.word)<2:
					continue
				lineNames[-1].append(w.word)
				if names.get(w.word) is None:
					names[w.word]=0
					relationships[w.word]={}
				names[w.word]+=1
				
for line in lineNames:             # 对于每一段
	for name1 in line:                
		for name2 in line:          # 每段中的任意两个人
			if name1 == name2:   
				continue
			if relationships[name1].get(name2) is None:          
				relationships[name1][name2]= 1
			else:
				relationships[name1][name2] = relationships[name1][name2]+ 1      # 两人共同出现次数加 1

with codecs.open("People_node.txt", "w","utf-8") as f:
    f.write("Id Label Weight\r\n")
    for name, times in names.items():
        f.write(name + " " + name + " " + str(times) + "\r\n")
            
            
                        
with codecs.open("People_edge.txt", "w","utf-8") as f:         
    f.write("Source Target Weight\r\n")
    for name, edges in relationships.items():   
        for v, w in edges.items():      
            if w > 3:         
                f.write(name + " " + v + " " + str(w) + "\r\n")
