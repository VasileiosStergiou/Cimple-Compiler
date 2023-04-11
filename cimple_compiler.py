#Petridis Efstathios ΑΜ:4157 cs04157
#Stergiou Vasileios ΑΜ:4300 cs04300
#Το πρόγραμμα πρέπει να δοθεί σαν input(μόνο αρχεία *.ci)
import sys
class ActivityGraph:
	"""docstring for QUAD"""
	def __init__(self,scope,bathos,tempVar,localVar,usedVar,pars,retVal,arguments,retAdd ):
		self.scope=scope
		self.bathos=bathos
		self.tempVar = tempVar
		self.localVar = localVar
		self.usedVar= usedVar
		self.pars = pars#[in/inout]
		self.retVal = retVal
		self.arguments =arguments
		self.retAdd =retAdd #ret quad
		
class Token:
	"""docstring for Toke"""
	def __init__(self, tokenType,tokenString,LineNo):
		self.tokenType = tokenType
		self.tokenString = tokenString
		self.LineNo = LineNo		
class Quad:
	"""docstring for QUAD"""
	def __init__(self,tag,op,arg1,arg2,arg3):
		self.tag=tag
		self.op = op
		self.arg1 = arg1
		self.arg2 = arg2
		self.arg3 = arg3
program_name = sys.argv[1]
ending = program_name.split('.')[1]
finalDict={}
labelTag=1
if (not(ending == 'ci')):
	print(program_name,"is invalid, .ci expected but",'.'+ending,"was found instead")
	sys.exit()

file = open(program_name)

funcFlag =0
activityGraphList=[]
#the lines of the program
lines = []
bathos=0
#Here is the 'legal' characters that our language supports
me=0#kathe fora poy jekinao na grafo mia synarthsh sto assemblyFile tha anavenei kata ena etsi oste na einai to index moy stis lsites activityGraphList,declerationsList
Capitals = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

Lowers = [x.lower() for x in Capitals]

numbers =['0','1','2','3','4','5','6','7','8','9']

arithemeticOperators =['+','-','*','/']
funcInUse=''
relationalOperators = ['<','>','=','<=','>=','<>']
declerationList=[]
assignment = ':='
addressCounter=12
delimeters = ['[',']','(',')','{','}',',',';','.']

Keywords = ['program','declare','if','else','while','switchcase',
			'forcase','incase','case','default','not','and','or','function',
		    'procedure','call','return','in','inout','input','print']

commentOperator= '#'
programName=''
statementList = ["if","while","switchcase","incase","forcase","call","return","print","input"]
assemblyFile= open("assemblyFile.asm","w")
TokenList=[]
token=Token('','',0)
nextTempNumber =1
lastVarUsedList=[]
lastVarUsed=''
declerationsList = []
functionList=[]#format[bathos,function/procedure,onoma_synarthseis,(,in/inout,parametros,in/inout,parametros,...,)]
tempVariablesList =[]
notInFunc=True
Q_true = []
Q_false = []
retCounter=0
B_true = []
B_false = []
prevTag=1
R_true = []
R_false = []
funcFlag=0
def newtemp():
	global nextTempNumber
	if(nextTempNumber==11):
		nextTempNumber=1
	
	new_temp_variable = 'T_'+ str(nextTempNumber)
	nextTempNumber+=1
	global bathos
	global declerationsList
	global declerationList
	global addressCounter
	global activityGraphList
	if(new_temp_variable not in declerationList):
		declerationList.append(new_temp_variable)
	if len(declerationsList[-1])==1:
			declerationsList[-1].append((new_temp_variable,addressCounter))
			activityGraphList[-1].tempVar.append((new_temp_variable,addressCounter))
			addressCounter+=4
			return new_temp_variable
	if(bathos!=0):	
		for i in range(-1,-(len(declerationsList)+1),-1):	
			for j in declerationsList[i]:
				
				if type(j)==int and j>bathos:
					break
				if type(j)==int:
					continue
				if j[0]!=new_temp_variable and declerationsList[i][-1]==j:
					declerationsList[i].append((new_temp_variable,addressCounter))
					activityGraphList[i].tempVar.append((new_temp_variable,addressCounter))
					addressCounter+=4
					return new_temp_variable
				elif j[0]!=new_temp_variable:
					continue
				elif j[0]==new_temp_variable and j[1]== addressCounter:
					break
				elif j[0]==new_temp_variable and j[1]!= addressCounter:
					declerationsList[i].append((new_temp_variable,addressCounter))
					activityGraphList[i].tempVar.append((new_temp_variable,addressCounter))
					addressCounter+=4
					return new_temp_variable
	else:
		for i in declerationsList[0]:
			
			if type(i)==int:
				continue
			if i[0]!=new_temp_variable and declerationsList[0][-1]==i:
				declerationsList[0].append((new_temp_variable,addressCounter))
				activityGraphList[0].tempVar.append((new_temp_variable,addressCounter))
				addressCounter+=4
				return new_temp_variable
			elif i[0]!=new_temp_variable:
				continue
			elif i[0]==new_temp_variable and i[1]== addressCounter:
				break
			elif i[0]==new_temp_variable and i[1]!= addressCounter:
				declerationsList[0].append((new_temp_variable,addressCounter))
				activityGraphList[0].tempVar.append((new_temp_variable,addressCounter))
				addressCounter+=4
				return new_temp_variable

	return new_temp_variable

def writeActivityGraphIntoFile():
	global activityGraphList
	global program_name

	activityGraphFile = open("ActivityGraph.txt","w+")

	activityGraphFile.write("Symbol Table of program: "+program_name+"\n\n")


	for elements in activityGraphList:
		activityGraphFile.write("Depth: "+str(elements.bathos)+"\n\n\t")
		activityGraphFile.write("Temp Variables: "+str(elements.tempVar)+"\n\n\t")
		activityGraphFile.write("Local Variables: "+str(elements.localVar)+"\n\n\t")
		activityGraphFile.write("Parametres: "+str(elements.pars)+"\n\n\t")
		activityGraphFile.write("Function's Arguments : "+str(elements.arguments)+"\n\n\t")
		activityGraphFile.write("Return addresses: "+str(elements.retAdd)+"\n\n")
		activityGraphFile.write("Variables that are declared in ancestors: "+str(elements.scope)+"\n\n")	

def nextquad():
	global labelTag
	global prevTag
	prevTag=labelTag
	labelTag+=1

	return labelTag
def genquad(op,arg1,arg2,arg3):
	global labelTag
	global prevTag
	''''''
	tempTag= nextquad()
	prevTag=tempTag
	retQuad=Quad(tempTag,op,arg1,arg2,arg3)
	global finalDict
	finalDict.update({tempTag:retQuad})
	return retQuad
def emptyList():
	tagList=list()
	return tagList
def makeList(a):	
	tempquad=Quad("_","_","_","_",a)
	tagList=[tempquad]
	return tagList
def mergeList(list1,list2):
	retList=list1+list2

	return retList
def backpatch(mylist,z):
	counter=0
	global finalDict

	for tag,quad in finalDict.items() :
		for item in mylist:
			if(item.tag==tag and quad.op==item.op and quad.arg1==item.arg1 
				and quad.arg2==item.arg2 ):
				quad.arg3=z	

	return mylist

def subprograms(token):
	while(token.tokenString == "function" or token.tokenString == "procedure"):
		subprogram(token)
		global funcFlag
		funcFlag+=1
		token = TokenList.pop(0)
		
	return token

def block(token,myList):
	token = decleration(token)
	createActivityGraph(myList)
	token = subprograms(token)
	statements(token)
	return
#with this func we find in which function weare currently so that we can seach later in which address we must return
def findFunc(myFunc):
	global functionList
	global bathos
	counter=0
	otherCounter=0

	for i in functionList:
		if len(i)==len(myFunc):
			for j in range(1,len(myFunc)+1):
				if otherCounter==len(myFunc)-1:
					return counter
				elif i[j]==myFunc[j]:
					if i[j]=="in" or i[j]=="inout":
						otherCounter=j+1
					otherCounter+=1
					continue
				elif i[j]!=myFunc[j]:
					break

				

			
		else:
			counter+=1
			continue
		counter+=1

def checkVariableDecleration(entry):

	global functionList

	variableFound = False

	for function in functionList:
		if (entry in function):
			return 2

	for el in activityGraphList:

			for lv in el.localVar:
				if (entry in lv[0]):
					variableFound = True

			for par in el.pars:
				if (entry in el.pars):
					variableFound = True
				
			for tv in el.tempVar:
				if (len(tv)>1):
					if (entry == tv[0]):
						print(tv)
						variableFound = True
			
	if (variableFound == False):
		return 0
	else:
		return 1

def statement(token):
	global notInFunc
	global declerationsList
	global activityGraphList
	global lastVarUsed
	global addressCounter
	global bathos
	if (token.tokenString == 'if'):
		token=TokenList.pop(0)
		token=ifstat(token)
		return token
	elif(token.tokenType=="Identifier"):#check if we have assignment
		entry=token

		if (checkVariableDecleration(entry.tokenString)==0):
			print("Error: ",entry.tokenString,"undeclared")
			sys.exit()
		#
		#
		if(TokenList[0].tokenString==":="):
			#we need old token for the error print so we look ahead without poping
			lastVarUsed=token.tokenString
			i=-1
			while activityGraphList[i].bathos>bathos:
				i-=1
			activityGraphList[i].usedVar.append(lastVarUsed)
			#print("From statement:",lastVarUsed)
			token=TokenList.pop(0)
			token=TokenList.pop(0)

			token,tempExpress=expression(token)			
			genquad(":=",tempExpress,"_",entry.tokenString)
			return token
		else:
			print("Error in line",token.LineNo,": ':=' expected but got",TokenList[0].tokenString,"instead")
			sys.exit()
	elif(token.tokenString=="while"):
		token=TokenList.pop(0)
		token=whileStat(token)
		return token
	elif(token.tokenString=="switchcase"):
		token=switchCaseStat(token)
		return token
	elif(token.tokenString=="forcase"):
		token=forCaseStat(token)
		return token
	elif(token.tokenString=="incase"):
		token=inCaseStat(token)
		return token
	elif(token.tokenString=="return" or token.tokenString=="print"):
		global retCounter
		if(token.tokenString=="return" and notInFunc):
			print("Error return found outside of function")
			sys.exit()
		retCounter+=1
		op=token.tokenString
		token=TokenList.pop(0)
		token,tempExpress=return_printStat(token)
		if(op=="return"):
			genquad("ret",tempExpress,"_","_")
			isPar=False
			for i in range(-1,-(len(declerationsList)+1),-1):
				for j in range(1,len(declerationsList[i])):#"T_6"
				#print()
					if type(tempExpress)== int  :
						activityGraphList[i].retVal.append(str(tempExpress))
						break
					elif tempExpress[0:2]=="T_":
						activityGraphList[i].retVal.append(addressCounter-4)
						break
					elif tempExpress==declerationsList[i][j][0]:
						activityGraphList[i].retVal.append(declerationsList[i][j][1])
						break
					elif i == len(declerationsList[i])-1:
						isPar=True
				if isPar:
					activityGraphList[i].retVal.append(tempExpress)

		else:
			genquad("out",tempExpress,"_","_")
		return token
	elif(token.tokenString=="call"):
		token=TokenList.pop(0)
		token=callStat(token)
		return token
	elif(token.tokenString=="input"):
		token=TokenList.pop(0)
		token,s=inputStat(token)
		genquad("inp",s,"_","_")
		return token

def ifstat(token):
	global labelTag
	if (token.tokenString == '('):
		token = TokenList.pop(0)
		token,B_true,B_false=condition(token)
		if(token.tokenString==')'):
			token = TokenList.pop(0)
			B_true = backpatch(B_true,nextquad())
			labelTag-=1
			statements(token)
			token=TokenList.pop(0)
			ifList = makeList(nextquad())
			labelTag-=1
			tempquad=genquad("jump","_","_","_")
			ifList.append(tempquad)
			B_false = backpatch(B_false,nextquad())
			labelTag-=1
			if(token.tokenString=="else"):
				token=TokenList.pop(0)
				statements(token)
				token=TokenList.pop(0)
				ifList = backpatch(ifList,nextquad())
				labelTag-=1
				return token
			else:
				ifList = backpatch(ifList,nextquad())
				labelTag-=1
				return token
		else:
			print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
			sys.exit()

	else:
		print("Error in line",token.LineNo,": '(' expected but got",token.tokenString,"instead")
		sys.exit()

def whileStat(token):
	global labelTag
	
	BQuad= nextquad()
	labelTag-=1
	if(token.tokenString=='('):
		token=TokenList.pop(0)
		token,B_true,B_false=condition(token)
		if (token.tokenString==')') :
			
			B_true = backpatch(B_true,nextquad())
			labelTag-=1
			token=TokenList.pop(0)
			statements(token)
			genquad("jump",'_','_',BQuad)
			B_false = backpatch(B_false,nextquad())
			labelTag-=1
			token=TokenList.pop(0)
			return token
		else:
			print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
			sys.exit()
	else:
		print("Error in line",token.LineNo,": '(' expected but got",token.tokenString,"instead")
		sys.exit()

def switchCaseStat(token):
	global labelTag
	exitList = emptyList()
	token=TokenList.pop(0)	
	while(token.tokenString=="case"):
		token=TokenList.pop(0)
		if(token.tokenString=='('):
			token=TokenList.pop(0)
			token,B_true,B_false=condition(token)
			if (token.tokenString==')'):
				B_true = backpatch(B_true,nextquad())
				labelTag-=1
				token=TokenList.pop(0)
				statements(token)
				e = makeList(nextquad())
				labelTag-=1
				tempquad=genquad("jump",'_','_','_')
				e.append(tempquad)
				mergeList(exitList,e)
				B_false = backpatch(B_false,nextquad())
				labelTag-=1
				token=TokenList.pop(0)
				continue
			else:
				print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
				sys.exit()
		else:
			print("Error in line",token.LineNo,": '(' expected but got",token.tokenString,"instead")
			sys.exit()				
	if(token.tokenString=="default"):
		token=TokenList.pop(0)
		statements(token)
		exitList = backpatch(exitList,nextquad())
		token=TokenList.pop(0)
		return token
	else:
		print("Error in line",token.LineNo,": default or case expected but got",token.tokenString,"instead")
		sys.exit()
def forCaseStat(token):
	global labelTag
	p1Quad = nextquad()
	labelTag-=1
	
	token=TokenList.pop(0)	
	while(token.tokenString=="case"):

		token=TokenList.pop(0)
		if(token.tokenString=='('):
			token=TokenList.pop(0)
			token,B_true,B_false=condition(token)
			if (token.tokenString==')') :
				
				B_true = backpatch(B_true,nextquad())
				labelTag-=1
				token=TokenList.pop(0)
				statements(token)
				genquad("jump",'_','_',p1Quad)
				B_false = backpatch(B_false,nextquad())
				labelTag-=1
				token=TokenList.pop(0)
				continue
			else:
				print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
				sys.exit()
		else:
			print("Error in line",token.LineNo,": '(' expected but got",token.tokenString,"instead")
			sys.exit()				
	if(token.tokenString=="default"):
		token=TokenList.pop(0)
		statements(token)
		token=TokenList.pop(0)

		return token
	else:
		print("Error in line",token.LineNo,": default or case expected but got",token.tokenString,"instead")
		sys.exit()
def inCaseStat(token):
	global labelTag
	w = newtemp()
	p1Quad = nextquad()
	labelTag-=1
	genquad(":=",1,'_',w)
	token=TokenList.pop(0)	
	while(token.tokenString=="case"):
		token=TokenList.pop(0)
		if(token.tokenString=='('):
			token=TokenList.pop(0)
			token,B_true,B_false=condition(token)
			if (token.tokenString==')') :
				B_true = backpatch(B_true,nextquad())
				labelTag-=1
				genquad(":=",0,'_',w)
				token=TokenList.pop(0)
				statements(token)
				B_false = backpatch(B_false,nextquad())
				labelTag-=1
				token=TokenList.pop(0)
				continue
			else:
				print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
				sys.exit()
		else:
			print("Error in line",token.LineNo,": '(' expected but got",token.tokenString,"instead")
			sys.exit()
	genquad(":=",p1Quad,0,w)
	return token

def return_printStat(token):
	if(token.tokenString=='('):
		token=TokenList.pop(0)
		token,tempExpress=expression(token)
		if(token.tokenString==')'):
			token=TokenList.pop(0)
			return token,tempExpress
		else:
			print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
			sys.exit()
	else:
		print("Error in line",token.LineNo,": '(' expected but got",token.tokenString,"instead")
		sys.exit()

def callStat(token):
	global labelTag
	global functionList
	possibleMatches=[]
	foundMatch=False
	if(token.tokenType=="Identifier"):
		s=token.tokenString
		for i in functionList:
			if(s ==i[2] and i[1]=="function"):
				print("Error:trying to call  a function")
				sys.exit()
			if(s==i[2]):
				possibleMatches.append(i)
		if(len(possibleMatches)==0):
			print("Error:Couldn't find a match for function in line",token.LineNo)
			sys.exit()
		token=TokenList.pop(0)
		if(token.tokenString=='('):
			token=TokenList.pop(0)
			token,useless,tempList=actualParlist(token,"procedure")
			
			for i in possibleMatches:
				if(len(i)==len(tempList)+5):
					
					for j in range(0,len(tempList)+1,2):
						if(j!=len(tempList) and i[j+4]==tempList[j]):
							
							continue
						elif(j==len(tempList)):
							tempInt=findFunc(i)+1
							tempVar=lastVarUsed
							if bathos==0:
								tempAdd=retAddress((tempVar,0))
							else:
								for k in range(-1,-(len(activityGraphList)+1),-1):
									if activityGraphList[k].bathos==bathos:
										
										tempAdd=retAddress((tempVar,k))
										break
							activityGraphList[tempInt].retAdd.append(tempAdd)
							foundMatch=True
							continue
						else:
							
							break
						
						

				else:
					continue
			if(foundMatch==False):
				print("Error:couldn't find a function to match the function in line",token.LineNo)
				sys.exit()
			if(token.tokenString==')'):
				token=TokenList.pop(0)
				genquad("call",s,"_","_")
				labelTag-=1
				return token
			else:
				print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
				sys.exit()
		else:
			print("Error in line",token.LineNo,": '(' expected but got",token.tokenString,"instead")
			sys.exit()
	else:
		print("Error in line",token.LineNo,": Identifier expected but got",token.tokenString,"instead")
		sys.exit()

def inputStat(token):
	if(token.tokenString=='('):
		token=TokenList.pop(0)
		if(token.tokenType=="Identifier"):
			returnValue=token.tokenString
			token=TokenList.pop(0)
			if(token.tokenString==')'):
				token=TokenList.pop(0)
				return token,returnValue
			else:
				print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
				sys.exit()
		else:
			print("Error in line",token.LineNo,": Identifier expected but got",token.tokenString,"instead")
			sys.exit()
	else:
		print("Error in line",token.LineNo,": '(' expected but got",token.tokenString,"instead")
		sys.exit()

def condition(token):
	global labelTag
	checkConditions=0

	

	while(True):
		token,Q_true,Q_false=boolTerm(token)
		B_true=Q_true
		checkConditions+=1

		if(token.tokenString=="or"):
			B_false=Q_false
			B_false = backpatch(B_false,nextquad())
			labelTag-=1
			token=TokenList.pop(0)
			continue
		else:
			B_true = mergeList(B_true,Q_true)
			
			B_false=Q_false
			B_false = backpatch(B_false,nextquad())
			labelTag-=1
			return token,B_true,B_false

def boolTerm(token):
	global labelTag
	checkBoolFactors =0

	while(True):		

		token,R_true,R_false=boolFactor(token)

		checkBoolFactors+=1

		Q_true = R_true
		Q_false = R_false


		if(token.tokenString=="and"):
			Q_true = backpatch(Q_true,nextquad())
			labelTag-=1
			token=TokenList.pop(0)
			continue
		else:
			
			Q_false = mergeList(Q_false,R_false)
			Q_true = backpatch(Q_true,nextquad())
			
			labelTag-=1
			return token,Q_true,Q_false

def boolFactor(token):

	global R_true
	global R_false

	if(token.tokenString=="not"):
		token=TokenList.pop(0)
		if(token.tokenString=='['):
			token=TokenList.pop(0)
			token,B_true,B_false=condition(token)
			
			if(token.tokenString==']'):
				token = TokenList.pop(0)
				R_true = B_false
				R_false = B_true
				return token,R_true,R_false
			else:
				print("Error in line",token.LineNo,": ']' expected but got",token.tokenString,"instead")
				sys.exit()
		else:
			print("Error in line",token.LineNo,": '[' expected but got",token.tokenString,"instead")
			sys.exit()
	elif(token.tokenString=='['):
			token=TokenList.pop(0)
			token,R_true,R_false=condition(token)
			if(token.tokenString==']'):
				token = TokenList.pop(0)
				return token,R_true,R_false
			else:
				print("Error in line",token.LineNo,": ']' expected but got",token.tokenString,"instead")
				sys.exit()
	else:

		leftPart=''
		rightPart=''
		token,leftPart= expression(token)
		if(token.tokenType=="relationalOperator"):
			myTag=nextquad()
			global prevTag
			global labelTag
			R_true = makeList(myTag)
			labelTag-=1
			relOp = token.tokenString
			token=TokenList.pop(0)
			token,rightPart=expression(token)


			tempquad=genquad(relOp,leftPart,rightPart,'_')
			R_true.append(tempquad)
			

			R_false = makeList(nextquad())
			labelTag-=1
			tempquad=genquad("jump",'_','_',"_")
			R_false.append(tempquad)

			
			
			return token,R_true,R_false
		else:
			print("Error in line",token.LineNo,": relationalOperator expected but got",token.tokenString,"instead")
			sys.exit()
	
def expression(token):
	leftPart=''
	op=''
	if (token.tokenString =='+' or token.tokenString =='-' ):
		leftPart+=token.tokenString#holding sign
		token = TokenList.pop(0)
	while(True):
		token,tempLeftTerm=term(token)
		if(op=='+' or op=='-'):
			temp=newtemp()
			genquad(op,leftPart,tempLeftTerm,temp)
			leftPart=temp	
		else:
			leftPart+=tempLeftTerm
		
		if(token.tokenString=='+' or token.tokenString=='-'):
			
			op=token.tokenString
			
			token=TokenList.pop(0)

			continue
		else:
			returnValue=leftPart
			return token,returnValue



def term(token):
	returnValue=''
	op=''
	temp = ''
	while(True):	
		token,tempValue=factor(token)
		
		if(op=='*' or op=='/'):
			temp=newtemp()
			genquad(op,returnValue,tempValue,temp)
			returnValue=temp	
		else:
			returnValue+=tempValue	
		
		if (token.tokenString ==''):
			token=TokenList.pop(0)		
		if (token.tokenString=='*' or token.tokenString=='/'):
			
			op=token.tokenString
			token=TokenList.pop(0)
			continue
		else:
			
			return token,returnValue

def factor(token):
	global labelTag
	global funcInUse

	global functionList

	returnValue=''
	if (token.tokenType == "Integer"):		
		return Token('','',0),token.tokenString
	elif (token.tokenString == '('):
		
		token = TokenList.pop(0)
		token,tempExpress = expression(token)
		returnValue=tempExpress
		if (token.tokenString == ')'):
			return Token('','',0),returnValue
		else:
			print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
			sys.exit()
	elif (token.tokenType == "Identifier"):
		s=token.tokenString


		
		if (checkVariableDecleration(s) == 0):
			print("Error: ",s,"undeclared")


		returnValue=token.tokenString

		token,tempValue = idtail(token)
		if(tempValue):
			returnValue=newtemp()
			genquad("par",returnValue,"RET","_")
			labelTag-=1
			genquad("call",s,"_","_")

			
			labelTag-=1
		
		return token,returnValue
	else:		
		print("Error in line",token.LineNo,": Integer, '(' or Identifier expected but got",token.tokenString,"instead")
		sys.exit()
def retAddress(myVar):
	global declerationsList
	

	myDeclaredList=declerationsList[myVar[1]]
	
	for i in range(1,len(myDeclaredList)):
		if myDeclaredList[i][0]==myVar[0]:
			return myDeclaredList[i][1]

def idtail(token):
	global activityGraphList
	global functionList
	global bathos
	global funcInUse
	global lastVarUsed
	foundMatch=False
	possibleMatches=[]
	tempCounter=0
	idName=token.tokenString
	token = TokenList.pop(0)
	if (token.tokenString == '('):
		funcInUse=idName
		for i in functionList:
			if(idName ==i[2] and i[1]=="procedure"):
				print("Error:trying to assign value to a variable from a procedure")
				sys.exit()
			elif(idName in i):
				possibleMatches.append(i)
				continue
			elif(idName not in i and len(possibleMatches)==0):
				continue
			tempCounter+=1
			if(tempCounter==len(functionList)and len(possibleMatches)==0):
				print("Error:Couldn't find function in functionList")
				sys.exit()


		returnValue=True
		token = TokenList.pop(0)
		
		token,tempValue,tempList = actualParlist(token,"function")
		for i in possibleMatches:
			if(len(i)==len(tempList)+5):	
				
				for j in range(0,len(tempList)+1,2):

					if(j!=len(tempList) and i[j+4]==tempList[j]):
						
						continue
					elif(j==len(tempList)):

						tempInt=findFunc(i)+1
						tempVar=lastVarUsed
						if bathos==0:
							tempAdd=retAddress((tempVar,0))
						else:
							for k in range(-1,-(len(activityGraphList)+1),-1):
								if activityGraphList[k].bathos==bathos:
									
									tempAdd=retAddress((tempVar,k))
									break
								
						activityGraphList[tempInt].retAdd.append(tempAdd)
						foundMatch=True
						continue
					else:
						
						break
					
					

			else:
				continue
		if(foundMatch==False):
			print("Error:couldn't find a function to match the function in line",token.LineNo)
			sys.exit()
		if (token.tokenString == ')'):
			
			return Token('','',0),returnValue
		else:
			print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
			sys.exit()
	else:
		return token,False

#implemented actualParlist with actualParItem grammar



def actualParlist(token,tempStr):	
	global labelTag
	global activityGraphList
	global addressCounter
	global bathos
	global funcInUse
	tempList=[]
	argumentList=[]
	returnValue = ''

	while (token.tokenString == "in" or token.tokenString =="inout"):
		tempList.append(token.tokenString)
		returnValue+=token.tokenString
		if (token.tokenString =="in"):
			token = TokenList.pop(0)
			token,tempExpress=expression(token)
			tempList.append(tempExpress)
			if bathos==0:
				tempAdd=retAddress((tempExpress,0))
			else:
				tempAdd=retAddress((tempExpress,-1))
			argumentList.append(tempExpress)
			genquad("par",tempExpress,"cv","_")
			labelTag-=1
			if (token.tokenString == ','):
				
				token = TokenList.pop(0)
				if (token.tokenString == "in" or token.tokenString =="inout"):
					continue
				else:
					print("Error in line",token.LineNo,": 'in' or 'inout' expected but got",token.tokenString,"instead")
					sys.exit()
			else:
				testList=[bathos,tempStr,funcInUse,'(']+tempList+[')']
				tempInt=findFunc(testList)
				if bathos==0:
					activityGraphList[tempInt+1].arguments.append([0]+argumentList)
				else:
					activityGraphList[tempInt+1].arguments.append([len(activityGraphList)-1]+argumentList)
				return token,returnValue,tempList
		elif (token.tokenString =="inout"):
			token = TokenList.pop(0)
			tempExpress = token.tokenString		
			if (token.tokenType == "Identifier"):
				tempList.append(token.tokenString)
				if bathos==0:
					tempAdd=retAddress((token.tokenString,0))
				else:
					tempAdd=retAddress((token.tokenString,-1))				
				argumentList.append(tempExpress)
				genquad("par",token.tokenString,"ref","_")
				labelTag-=1
				token = TokenList.pop(0)
				if (token.tokenString == ','):
					
					token = TokenList.pop(0)
					if (token.tokenString == "in" or token.tokenString =="inout"):
						continue
					else:
						print("Error in line",token.LineNo,": 'in' or 'inout' expected but got",token.tokenString,"instead")
						sys.exit()
				else:
					testList=[bathos,tempStr,funcInUse,'(']+tempList+[')']
					tempInt=findFunc(testList)
					if bathos==0:
						activityGraphList[tempInt+1].arguments.append([0]+argumentList)
					else:
						activityGraphList[tempInt+1].arguments.append([len(activityGraphList)-1]+argumentList)
					return token,returnValue,tempList
			else:
				print("Error in line",token.LineNo,": Identifier expected but got",token.tokenString,"instead")
				sys.exit()
	if(token.tokenType=="Identifier"):
		print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
		sys.exit()
	testList=[bathos,tempStr,funcInUse,'(']+tempList+[')']
	tempInt=findFunc(testList)
	if bathos==0:
		activityGraphList[tempInt+1].arguments[-1]=[0]+argumentList
	else:
		activityGraphList[tempInt+1].arguments.append([len(activityGraphList)-1]+argumentList)
	return token,returnValue,tempList

def subprogram(token):
	global labelTag
	global bathos
	global notInFunc
	global retCounter
	global functionList
	global addressCounter
	lastNotInFunc=True
	bathos+=1
	oldAdressCounter=addressCounter
	addressCounter=12
	tempList=[bathos]
	token.LineNo = token.LineNo
	if (token.tokenString == "function" or
	    token.tokenString == "procedure"):
		if(token.tokenString == "function"):
			lastNotInFunc=notInFunc
			notInFunc=False
		tempList.append(token.tokenString)
		token = TokenList.pop(0)
		if(token.tokenType=="Identifier"):
			tempList.append(token.tokenString)
			s=token.tokenString
			genquad("begin_subBlock",s,"_","_")
			token = TokenList.pop(0)
			if (token.tokenString == '('):
				tempList.append(token.tokenString)
				token = TokenList.pop(0)				
				token,newTempList = formalParlist(token)
				for i in newTempList:
					tempList.append(i)
				if (token.tokenString == ')'):
					tempList.append(token.tokenString)
					for i in functionList:
						if(len(i)==len(tempList)):
							for j in range(0,len(i)):
								if(i[j]==tempList[j]):
									continue
								else:
									break
								print("Error:same function found in the same level")
								sys.exit()
						else:
							continue
					functionList.append(tempList)
					
					token=TokenList.pop(0)
					
					block(token,newTempList)
					genquad("end_subBlock",s,"_","_")
					
				else:
					print("Error in line",token.LineNo,": ')' expected but got",token.tokenString,"instead")
					sys.exit()
			else:
				print("Error in line",token.LineNo,": '(' expected but got",token.tokenString,"instead")
				sys.exit()
		else:
			print("Error in line",token.LineNo,": Identifier expected but got",token.tokenString,"instead")
			sys.exit()
	else:
		print("Error in line",token.LineNo,": function or procedure expected but got",token.tokenString,"instead")
		sys.exit()
	if(notInFunc==False and retCounter==0):
		print("Error:zero returns where found in a function")
		sys.exit()
	else:
		retCounter=0
	bathos-=1
	addressCounter=oldAdressCounter
	notInFunc=lastNotInFunc

	

#implemented formalParlist with formalParItem grammar
def formalParlist(token):
	tempList=[]
	while (token.tokenString == "in" or token.tokenString =="inout"):
		tempList.append(token.tokenString)
		token = TokenList.pop(0)
		if(token.tokenType == "Identifier"):
			tempList.append(token.tokenString)
			token = TokenList.pop(0)
			if (token.tokenString ==','):
				token = TokenList.pop(0)
				if(token.tokenString == "in" or token.tokenString =="inout"):
					continue
				else:
					print("Error in line",token.LineNo,": in or inout expected but got",token.tokenString,"instead")
					sys.exit()
			else:				
				return token,tempList
		else:
			print("Error in line",token.LineNo,": Identifier expected but got",token.tokenString,"instead")
			sys.exit()
	return token,tempList

def statements(token):
	if(token.tokenString in statementList or token.tokenType=="Identifier"):
		token=statement(token)
		if(token.tokenString==';'):
			return
		else:
			print("Error in line",token.LineNo,": ';' expected but got",token.tokenString,"instead")
			sys.exit()
	elif(token.tokenString=="{"):
		token=TokenList.pop(0)
		while(token.tokenString in statementList or token.tokenType=="Identifier"):						
			token=statement(token)	
			if(token.tokenString==';'):					
					token=TokenList.pop(0)					
					continue
			elif(token.tokenString=='}'):					
					return 
			else:
				print("Error in line",token.LineNo,": ';','}' expected but got",token.tokenString,"instead")
				sys.exit()
			while(token.tokenString in statementList or token.tokenType=="Identifier"):				
				token=statement(token)
				if(token.tokenString==';'):
					token=TokenList.pop(0)
					continue
				elif(token.tokenString=='}'):					
					return
				else:
					print("Error in line",token.LineNo,": ';','}' expected but got",token.tokenString,"instead")
					sys.exit()
		if(token.tokenString==';'):
				token=TokenList.pop(0)
		elif(token.tokenString=='}'):
				return 
		else:
			print("Error in line",token.LineNo,": '}' expected but got",token.tokenString,"instead")
			sys.exit()
	elif(token.tokenString==';'):
		return
	else:
		print("Error in line",token.LineNo,": '{' or statement or ';'expected but got",token.tokenString,"instead")
		sys.exit()	

def commentRemoval():
	token=TokenList[1]
	tokCounter=0
	while(tokCounter<len(TokenList)):
		if(not(token.tokenString=='#')):
			tokCounter+=1			
			if(len(TokenList)<=tokCounter):
				continue
			token=TokenList[tokCounter]			
		else:
			TokenList.pop(tokCounter).tokenString
			if(len(TokenList)<=tokCounter):
				continue
			token=TokenList[tokCounter]

def decleration(token):
	
	global declerationsList
	global declerationList
	global functionList
	global bathos
	global addressCounter
	localList=[bathos]
	while(token.tokenString=="declare"):

		token=TokenList.pop(0)	
		while(not(token.tokenString==';')):
						
			if(token.tokenType=="Identifier"):
				
				if(token.tokenString not in localList  ):
					if bathos !=0 and token.tokenString !=functionList[-1][2]:
						localList.append((token.tokenString,addressCounter))
						declerationList.append(token.tokenString)
						addressCounter+=4
					elif bathos==0:
						localList.append((token.tokenString,addressCounter))
						declerationList.append(token.tokenString)
						addressCounter+=4
				else:
					print("Error:variable was found more than one times in the same level")
					sys.exit()
				token=TokenList.pop(0)				
				if(token.tokenString==',' ):

					token=TokenList.pop(0)					
					continue
				elif(token.tokenString ==';'):

					continue
				else:
					print("Error in line:",token.LineNo,": expected ';' or ',' symbol and got:",token.tokenString)
					sys.exit()
			else:
				print("Error in line:",token.LineNo,": expected Identifier  and got:",token.tokenString)
				sys.exit()
		token=TokenList.pop(0)
	declerationsList.append(localList)
	return token


def program():
	global programName
	token=TokenList.pop(0)
	if(token.tokenString=="program"):
		programLine=token.LineNo
		token=TokenList.pop(0)
		if(token.tokenType=="Identifier" and token.LineNo==programLine):
			programName=token.tokenString
			token=TokenList.pop(0)
			genquad("begin_block",programName,"_","_")
			block(token,[])			
			if(len(TokenList)>=1):
				token=TokenList.pop(0)

			else:
				print("Error: '.' exepcted at the end of the program and got nothing")
				sys.exit()
			if(token.tokenString=='.'):
				genquad("halt","_","_","_")
				genquad("end_block",programName,"_","_")
				return
			else:
				print("Error: '.' exepcted at the end of the program but got that:",token.tokenString,"symbol")
				sys.exit()
		else:
			print("Error:program name expected")
			sys.exit()
	else:
		print("Error:Keyword program exepcted insted of :",token.tokenString)
		sys.exit()
def makeCFile():
	global funcFlag
	global finalDict
	global programName
	global declerationList
	if(funcFlag>=1):
		myFile = open(programName+".int","w+")
	else:
		myFile = open(programName+".c","w+")
		myFile.write("#include <stdio.h>\n\n")
	for tag,quad in finalDict.items():
		dec ="int "
		if(quad.op=="begin_block"):
			myFile.write("int main () {")
			for i in range(len(declerationList)):
				if (i != len(declerationList)-1):
					dec+=declerationList[i]+','
				else:
					dec+=declerationList[i]+';'
			myFile.write("\n\t"+dec+"\n\tL_%s:"%str(tag))
			continue
		if(quad.op in arithemeticOperators):
			myFile.write("\n\tL_%s:%s=%s%s%s;" %(str(tag),quad.arg3,quad.arg1,quad.op,quad.arg2))
			continue
		if(quad.op in relationalOperators):
			if(quad.op=="<>"):
				myFile.write("\n\tL_%s:if(%s!=%s) goto L_%s;" %(str(tag),quad.arg1,quad.arg2,str(quad.arg3)))
				continue
			elif(quad.op=="="):
				myFile.write("\n\tL_%s:if(%s==%s) goto L_%s;" %(str(tag),quad.arg1,quad.arg2,str(quad.arg3)))
				continue
			else:
				
				myFile.write("\n\tL_%s:if(%s%s%s) goto L_%s;" %(str(tag),quad.arg1,quad.op,quad.arg2,str(quad.arg3)))
				continue
		if(quad.op =="begin_subBlock"):
			myFile.write("\nint func_block{")
			continue
		if(quad.op =="end_subBlock"):
			myFile.write("\n}")
			continue
		if(quad.op=="ret"):
			myFile.write("\n\tL_%s:return(%s);" %(str(tag),quad.arg1))
			continue
		if(quad.op=="out"):
			myFile.write("\n\tL_%s:printf(\" %%d \",%s);" %(str(tag),quad.arg1))
			continue
		if(quad.op=="inp"):
			myFile.write("\n\tL_%s:scanf(\" %%d \",&%s);" %(str(tag),quad.arg1))
			continue
		if(quad.op=="jump"and quad.arg3!='_'):
			myFile.write("\n\tL_%s:goto L_%s;" %(str(tag),str(quad.arg3)))
			continue
		if(quad.op==":="):
			myFile.write("\n\tL_%s: %s=%s;" %(str(tag),quad.arg3,quad.arg1))
			continue
		if(quad.op=="end_block"):
			myFile.write("\n}")
			continue
		if(quad.op=="halt"):
			myFile.write("\n\treturn(0);")
			continue


def createActivityGraph(parsList):
	global activityGraphList
	global declerationsList
	global bathos
	scope=[] 
	counter=0
	lastBathosSeen=-1
	myList=declerationsList[-1]
	tempList=[]
	localList=[]

	for i in range(1,len(myList)):
		
		if len(myList[i][0])>2 and myList[i][0][0]=='T' and myList[i][0][1]=='_':
			tempList.append(myList[i])
		else:
			localList.append(myList[i])

	if bathos>1:
		for i in range(-1,-(len(activityGraphList)+1),-1):
			if activityGraphList[i].bathos>=bathos:
				#lastBathosSeen=activityGraphList[i].bathos
				continue
			elif activityGraphList[i].bathos==0:#[main,]
				lastBathosSeen=activityGraphList[i].bathos
				break

			elif activityGraphList[i].bathos<bathos and (counter==0 or activityGraphList[i].bathos<lastBathosSeen):
				lastBathosSeen=activityGraphList[i].bathos
				counter+=1
				scope.append(activityGraphList[i].localVar)

	temp=ActivityGraph(scope,bathos,tempList,localList,[],parsList,[],[],[])
	activityGraphList.append(temp)
def gnvlcode(noneLocalVar):
	global activityGraphList
	global me 
	for i in activityGraphList[me].scope.reverse():
			
		for j in i.reverse():
			if j==i[-1]:
				myLastAdd=j[1]
				offset+=j[1]-12
			if j[0]==noneLocalVar:
				offset+=myLastAdd-j[1]
					
					
				assemblyFile.write("addi $t0,t0$,%d\n"%(-offset))
				return
		for i in activityGraphList[0].localVar.reverse():
			for j in i.reverse():
				if j==i[-1]:
					myLastAdd=j[1]
					offset+=j[1]-12
				if j[0]==noneLocalVar:
					offset+=myLastAdd-j[1]
					
					
					assemblyFile.write("addi $t0,t0$,%d\n"%(-offset))
					return
		print("Error: trying to find Var that hasnt been initialized")
 
def loadvr(v,r):
	global bathos
	global activityGraphList
	global declerationsList
	global assemblyFile
	global me 
	myAddress=0
	if v.isNumeric():
		assemblyFile.write("li %s,%d\n"%(r,v))
		return
			
	for i in declerationsList[0]:
		if type[i]==int:
			continue
		if v ==i[0]:
			myAddress=i[1]
			assemblyFile.write("lw %s,%d($s0)\n"%(r,-myAddress))
			return
	if activityGraphList[me].bathos>0 :#toDo if something goes wrong implement check for temp var
		for i in activityGraphList[me].localVar:
			if v ==i[0] :
				myAddress=i[1]
				declared=True
				break
		if declared and v in activityGraphList[me].pars:
			for i in range(0,len(activityGraphList[me].pars)):
				if activityGraphList[me].pars[i]== "in":
					lastInSeen=True
					lastInoutSeen=False
				elif activityGraphList[me].pars[i]== "inout":
					lastInoutSeen=True
					lastInSeen=False
				elif activityGraphList[me].pars[i]== v and lastInSeen:
					assemblyFile.write("addiu $t0,$sp,0\n")
					assemblyFile.write("subi $t1,t0$,%d\n"%(myAddress))
					assemblyFile.write("sub $sp,$zero,$t1\n"%(r))
					assemblyFile.write("lw %s,0($sp)\n"%(r))
					return
				elif activityGraphList[me].pars[i]== v and lastInoutSeen:
					assemblyFile.write("addiu $t0,$sp,0\n")
					assemblyFile.write("subi $t1,t0$,%d\n"%(myAddress))
					assemblyFile.write("sub $sp,$zero,$t1\n"%(r))
					assemblyFile.write("lw $t0,0($sp)\n")
					assemblyFile.write("lw %s,($t0)\n"%(r))
					return
		elif declared and v in activityGraphList[me].usedVar:
			assemblyFile.write("addiu $t0,$sp,0\n")
			assemblyFile.write("subi $t1,t0$,%d\n"%(myAddress))
			assemblyFile.write("sub $sp,$zero,$t1\n"%(r))
			assemblyFile.write("lw %s,0($sp)\n"%(r))
			return
		elif activityGraphList[me].bathos>1 :
			for i in activityGraphList[me].scope:
				if i[0]==v:
					myAddress=i[1]
					declaredInGrand=True
					break
				
			
			if declaredInGrand and v in activityGraphList[me].pars:
				for i in range(0,len(activityGraphList[me].pars)):
					if activityGraphList[me].pars[i]== "in":
						lastInSeen=True
						lastInoutSeen=False
					elif activityGraphList[me].pars[i]== "inout":
						lastInSeen=False
						lastInoutSeen=True
					elif activityGraphList[me].pars[i]== v and lastInSeen:
						gnvlcode(v)
						assemblyFile.write("lw %s,($t0)\n"%(r))
						return
					elif activityGraphList[me].pars[i]== v and lastInoutSeen:
						gnvlcode(v)
						assemblyFile.write("lw $t0,($t0)\n")
						assemblyFile.write("lw %s,($t0)\n"%(r))
						return

			if v in activityGraphList[me].usedVar and declaredInGrand:
				gnvlcode(v)
				assemblyFile.write("lw %s,($t0)\n"%(r))
				return
#just changed lw to sw where it was needed 
def storerv(v,r):
	global bathos
	global activityGraphList
	global declerationsList
	global assemblyFile
	global me
	myAddress=0
			
	for i in declerationsList[0]:
		if type[i]==int:
			continue
		if v ==i[0]:
			myAddress=i[1]
			assemblyFile.write("sw %s,%d($s0)\n"%(r,-myAddress))
			return
	if activityGraphList[me].bathos>0 :
		for i in activityGraphList[me].localVar:
			if v ==i[0] :
				myAddress=i[1]
				declared=True
				break
		if declared and v in activityGraphList[me].pars:
			for i in range(0,len(activityGraphList[me].pars)):
				if activityGraphList[me].pars[i]== "in":
					lastInSeen=True
					lastInoutSeen=False
				elif activityGraphList[me].pars[i]== "inout":
					lastInoutSeen=True
					lastInSeen=False
				elif activityGraphList[me].pars[i]== v and lastInSeen:
					assemblyFile.write("addiu $t0,$sp,0\n")
					assemblyFile.write("subi $t1,t0$,%d\n"%(myAddress))
					assemblyFile.write("sub $sp,$zero,$t1\n"%(r))
					assemblyFile.write("sw %s,0($sp)\n"%(r))
					return

				elif activityGraphList[me].pars[i]== v and lastInoutSeen:
					assemblyFile.write("addiu $t0,$sp,0\n")
					assemblyFile.write("subi $t1,t0$,%d\n"%(myAddress))
					assemblyFile.write("sub $sp,$zero,$t1\n"%(r))
					assemblyFile.write("lw $t0,0($sp)\n")
					assemblyFile.write("sw %s,($t0)\n"%(r))
					return
		elif declared and v in activityGraphList[me].usedVar:
			assemblyFile.write("addiu $t0,$sp,0\n")
			assemblyFile.write("subi $t1,t0$,%d\n"%(myAddress))
			assemblyFile.write("sub $sp,$zero,$t1\n"%(r))
			assemblyFile.write("sw %s,0($sp)\n"%(r))
			return
		elif activityGraphList[me].bathos>1 :
			for i in activityGraphList[me].scope:
				if i[0]==v:
					myAddress=i[1]
					declaredInGrand=True
					break
				
			
			if declaredInGrand and v in activityGraphList[me].pars:
				for i in range(0,len(activityGraphList[me].pars)):
					if activityGraphList[me].pars[i]== "in":
						lastInSeen=True
						lastInoutSeen=False
					elif activityGraphList[me].pars[i]== "inout":
						lastInSeen=False
						lastInoutSeen=True
					elif activityGraphList[me].pars[i]== v and lastInSeen:
						gnvlcode(v)
						assemblyFile.write("sw %s,($t0)\n"%(r))
						return
					elif activityGraphList[me].pars[i]== v and lastInoutSeen:
						gnvlcode(v)
						assemblyFile.write("lw $t0,($t0)\n")
						assemblyFile.write("sw %s,($t0)\n"%(r))
						return


			if v in activityGraphList[me].usedVar and declaredInGrand:
				gnvlcode(v)
				assemblyFile.write("sw %s,($t0)\n"%(r))
				return





	
	
def syntax():
	lexical()

	commentRemoval()
	program()
	makeCFile()
	writeActivityGraphIntoFile()
def lexical():	
	line =  file.readline()
	while(line):
		lines.append(line)
		line = file.readline()
	#count line shows the line we are cureently on
	count_lines =1
	count_comments=0
	#In each line of the program
	#we need to read each character and see what it is
	for l in lines:
		#the automato forms a sequence of characters while we add characters
		#so we need to check every time if the current sequence is
		#a terminal state (teliki katastasi)

		#sequence resets on each loop so that we can check the characters
		#from the point we stopped
		sequence = ''
		int_sequence = ''
		characters = l.split()
		
		for c in characters:			
			last_symbol =''
			operator_sequence = ''
			first_symbol =''	
			symbolCounter=0
			for symbol in c:
				symbolCounter+=1				
				#holding the first symbol of every word
				#we resete first symbol when we reset sequence
				if(first_symbol==''):
					first_symbol=symbol				
								
				if(first_symbol in numbers and (symbol in Capitals or symbol in Lowers)):
					if(int_sequence==''):
						print("Error in line",count_lines,"Identifiers can start with number",first_symbol+symbol)
						sys.exit()
					else:
						print("Error in line",count_lines,"Identifiers can start with number",int_sequence+last_symbol+symbol)
						sys.exit()
						break						
				#Checking for comments
				if(symbol == '#'and count_comments %2==0):					
					TokenList.append(Token("commentOperator",symbol,count_lines))
					count_comments+=1
					lastCommentOperatorSeen=count_lines
					continue
				#while we have found odd number of '#' we are still inside the comments
				elif(not(symbol=='#')and count_comments %2==1):
					continue
				#when we find 2nd, 4th,6th... comment operator we are out of the comments
				elif(symbol == '#'and count_comments %2==1):				
					TokenList.append(Token("commentOperator",symbol,count_lines))
					count_comments+=1
					print("commentOperator:",symbol)
					print()
					first_symbol=''
					continue

				if (last_symbol == '<' and (symbol=='=' or symbol=='>')):
					operator_sequence = last_symbol + symbol															
					TokenList.append(Token("relationalOperator",operator_sequence,count_lines))
					last_symbol = symbol						
					sequence = ''
					first_symbol=''
					int_sequence=''
					continue
				elif(last_symbol =='<' and (not(symbol=='=') or not(symbol=='>') )):
					TokenList.append(Token("relationalOperator",last_symbol,count_lines))						
					sequence = ''
					int_sequence=''
					first_symbol=symbol
				elif (last_symbol == '>' and symbol=='=' and not (TokenList[-1].tokenString=="<>")):
					operator_sequence = last_symbol + symbol					
					TokenList.append(Token("relationalOperator",operator_sequence,count_lines))
					last_symbol = symbol					
					sequence = ''
					first_symbol=''
					int_sequence=''
					continue
				elif(last_symbol =='>'and not symbol=='=' and not (TokenList[-1].tokenString=="<>")):
					TokenList.append(Token("relationalOperator",last_symbol,count_lines))					
					sequence = ''
					first_symbol=symbol
					int_sequence=''					
				if(first_symbol in Capitals or first_symbol in Lowers ):					
						#check if the sequence is a Keyword
						#we need to check the next symbol on every loop
						#to make sure we have a Keyword
					if(sequence in Keywords and  (symbol in Capitals or symbol in Lowers or symbol in numbers) ):
						TokenList.pop()
					if (not(sequence + symbol in Keywords) ):
							#check if the symbol is a name
							#we need to check the current sequency adding the next symbol
							#each time
						
						if(len(sequence+symbol)<=30):
							if((symbol in delimeters or symbol in arithemeticOperators or symbol in relationalOperators or symbol== ':'or symbol.isspace() )
								and (last_symbol in Capitals or last_symbol in Lowers or last_symbol in numbers ) ):																														 
								TokenList.append(Token("Identifier",sequence,count_lines))
								first_symbol=symbol
								sequence=''
							elif(symbol in Capitals or symbol in Lowers or symbol in numbers ):
								sequence += symbol
								if(len(c)==symbolCounter):
									TokenList.append(Token("Identifier",sequence,count_lines))
									sequence=''													
						else:
							print("Error in line",count_lines,"Identifier length to big.Length of identifiers should be 30 or smaller")
							print()
							sys.exit()
					elif(sequence + symbol in Keywords):						
						TokenList.append(Token("Keyword",sequence+symbol,count_lines))						
						last_symbol = symbol						
						sequence += symbol
						first_symbol=''
						continue
				#when a word starts with a number +/-
				elif(first_symbol in numbers):						
					if (symbol in numbers and last_symbol in numbers ):
						int_sequence+= last_symbol#here we  hold the digits of a number that we have passed
						TokenList.pop(-1)	
						last_symbol = symbol
						if(int(int_sequence)<(-4294967295)or int(int_sequence)>4294967296):
							print("Integer is out of range.(-4294967295,4294967296)", int(int_sequence))
							print()							
							sys.exit()
						TokenList.append(Token("Integer",int_sequence+symbol,count_lines))	
						continue
						#in case we have an intger with only 1 digit
					elif (symbol in numbers and int_sequence == ''):												
						last_symbol=symbol
						TokenList.append(Token("Integer",symbol,count_lines))
						continue																												
				#check if the symbol is a delimeter
				#no need to check other symbols if we find one
				if symbol in delimeters:					
					TokenList.append(Token("Delimeter",symbol,count_lines))
					last_symbol = symbol #we hold the previous symbol to check if we have <>or >=or <=
					sequence = ''
					first_symbol=''
					continue									
				#checking what symbol is comming after ':'
				if (last_symbol == ':'):
					operator_sequence = last_symbol + symbol
					#print("operator sequence",operator_sequence)
					if (operator_sequence == assignment):#when our current symbol is = we have assignment
						TokenList.append(Token("assignmentOperator",operator_sequence,count_lines))
						last_symbol = symbol
						#print("relationalOperator:",symbol)
						sequence = ''
						first_symbol=''
						continue
					else: #when something else comes up we must sent an error report
						print("Error in line",count_lines,"the operator",operator_sequence,"is invalid")
						print()
						sys.exit()
				if (symbol =='='):					
					TokenList.append(Token("relationalOperator",symbol,count_lines))
					last_symbol = symbol						
					sequence = ''
					first_symbol=''
					int_sequence=''
					continue					
				
				#check if the symbol is an arithmetic operator
				#no need to check other symbols if we find one
				if symbol in arithemeticOperators:					
					TokenList.append(Token("arithemeticOperator",symbol,count_lines))
					last_symbol = symbol
					sequence = ''
					first_symbol=''
					int_sequence=''
					continue
				#holding last symbol,adding symbol in sequence
				last_symbol = symbol
				#checking if a symbol the comes up isn't in te language
				if not(	symbol in arithemeticOperators or symbol in numbers or symbol in Lowers 
					or symbol in Capitals or symbol=='#' or symbol==':' 
					or symbol in delimeters or symbol in relationalOperators):
					print("Error in line",count_lines,"Char: ",symbol,"isn't in the language" )
					print()
					sys.exit()			
			sequence = ''
		count_lines+=1
	#In case we have odd number of # when we finish the file we sent error report
	if(count_comments %2==1):
		print("Error: comment Operator missing.Last time commentOperator was used in line, ",lastCommentOperatorSeen)
		sys.exit()
counter=0

syntax()


print("program finsihed")