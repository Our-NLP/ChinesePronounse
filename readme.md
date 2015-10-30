#Readme
##Files:
- __Data__
	- __MetaData:__
		- Extracted from raw data for generating feature vectors.
	- __Vectors:__
		- Directly usable data for mallet classification.
	- __XML Data:__
		- Raw data file
- __Src:__
	Python scripts for all purpose processing.
- __mallet:__
	Mallect package with license.
- __stanford-postagger:__
	Standford postagger
##Usage:
- Generate final meta data: 

	Extract data from xml file, and producing meta data following the formate like:
	FileName,ProType,Pro start location in file, Pro start location in line,text, suid,speaker
	The final meta will have postag as the last field.
	- python XML_Parser.py
	- python Postag.py
		
	Data will be in the Data/MetaData dir
- Run Classification

	Compressing feature document into vector, feature document is written in svmlight format.Using stdout to show result.
	- python Classify.py

- Check missing pro
	Check if the annotator missed any pro. Using stdout to show result.
	- python CheckPro.py
##Feature:
- f1: pre is #NN or #PN, next is #V or #P
- f2: current is at head(after , .)
- f3: current is at head, and followed #V or #P
- f4: next is #NN or #PN
- f6: pre is #NN or #PN
- f7: pre pre is #NN or #PN
- f8: pre pre pre is #N or #PN
- f9: next is #V or #P
- f10: next next is #V or #P
- f11: next next next is #V or #P

##recourse
- Postag : http://www.cis.upenn.edu/~chinese/posguide.3rd.ch.pdf


