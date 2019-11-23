import re

syllable = ['(1)','(#1)','(2)','(#2)','(3)','(4)','(#4)','(5)',\
            '(#5)','(6)','(#6)','(7)','1','#1','2','#2','3','4',\
            '#4','5','#5','6','#6','7','[1]','[#1]','[2]','[#2]'\
            ,'[3]','[4]','[#4]','[5]','[#5]','[6]','[#6]','[7]']


####################################
#
#预处理，将输入转换成可识别的状态
#
###################################
def Pretreatment(talk):
    #将中文括号转换成英文
    talk = talk.replace('（','(')
    talk = talk.replace('【','[')
    talk = talk.replace('）',')')
    talk = talk.replace('】',']')

    #将错误的括号转成正确的
    index1 = 0
    index2 = 0
    while((talk.find('(',index1) != -1) or (talk.find(')',index2) != -1)):
        index1_temp = talk.find('(',index1)
        index2_temp = talk.find(')',index2)
        #print(index1_temp,index2_temp)
        if index1_temp<index2_temp:#左括号位置比右括号前
            if index1_temp == -1:#如果左括号不存在
                talk = talk[0:index2_temp] + talk[(index2_temp+1):len(talk)]
            else:#一对标准的括号
                index1 = index1_temp + 1
                index2 = index2_temp + 1
        elif index1_temp>index2_temp:
            if index2_temp == -1:#右括号不存在
                talk = talk + ')'
                index2 = len(talk) -1
                index1 = index1 + 1
            else:#右括号在左括号前面
                talk = talk[0:index2_temp] + talk[(index2_temp+1):len(talk)]
                index1 = index1_temp - 1
    while(talk.find('()',0) != -1):
        talk = talk.replace('()','')
    
    #处理中括号
    index1 = 0
    index2 = 0
    while((talk.find('[',index1) != -1) or (talk.find(']',index2) != -1)):
        index1_temp = talk.find('[',index1)
        index2_temp = talk.find(']',index2)
        #print(index1_temp,index2_temp)
        if index1_temp<index2_temp:#左括号位置比右括号前
            if index1_temp == -1:#如果左括号不存在
                talk = talk[0:index2_temp] + talk[(index2_temp+1):len(talk)]
            else:#一对标准的括号
                index1 = index1_temp + 1
                index2 = index2_temp + 1
        elif index1_temp>index2_temp:
            if index2_temp == -1:#右括号不存在
                talk = talk + ']'
                index2 = len(talk) - 1
                index1 = index1 + 1
            else:#右括号在左括号前面
                talk = talk[0:index2_temp] + talk[(index2_temp+1):len(talk)]
                index1 = index1_temp - 1
    while(talk.find('[]',0) != -1):
        talk = talk.replace('[]','')
    #print(talk)
    #return talk


    #将括号放到正确的位置，如'sdfs(  ed(     '变成'sdfs  (ed     ('
    while(re.findall(r"\(\s+|\[\s+|\s+\)|\s+\]",talk) != []):
        b = re.findall(r"\(\s+|\[\s+|\s+\)|\s+\]",talk)
        #print(b)
        index = 0
        for i in b:
            m = len(i)
            #print('长度：',m)
            d = talk.find(i,index)
            talk = talk[0:d] + i[::-1] + talk[d+m:len(talk)]
            #print('位置：',d)


    #对#号的处理：   '   
    while(re.findall(r"\#\s+",talk) != []):
        index = 0
        b = re.findall(r"\#\s+",talk)
        #print(b)
        for i in b:
            m = len(i)
            #print('长度：',m)
            d = talk.find(i,index)
            talk = talk[0:d] + i[::-1] + talk[d+m:len(talk)]
            index = d + m
            #print('位置：',d)


    #去除掉无效的#
    index = 0
    while(talk.find('#',index) != -1):
        b = talk.find('#',index)
        #print(b)
        if talk[b+1] not in ['1','2','3','4','5','6','7']:
            talk = talk[0:b] + talk[b+1:len(talk)]
            index = b 
        else:
            index = b + 1
    #print(talk)
    return talk

########################################
#
#将#和数字结合起来，并转成列表形式
#
########################################
def yuchuli(talk):   
    talk = list(talk)
    #print(talk)
    #print(len(talk))
    for index,item in enumerate(talk):
        if item == '#':
            talk[index] = talk[index] + talk[index+1]
            talk.pop(index+1) 
    #print(talk)
    return talk

##########################################
#
#转调
#
#########################################
def zhuandiao(talk,cha):
    #cha = 2#初始音阶与目标音阶的差级
    targe = talk
    for i,item in enumerate(targe):
        if item in syllable:
            tab = syllable.index(item)
            targe[i] = syllable[tab-cha]
    #print(targe)
    targe = yuchuli(''.join(targe))
    #print('转调后',''.join(targe))
    return targe

#########################################
#
#转调后处理，合并括号等问题
#
#########################################
def Afterturn(targe):
    tu = 0
    T = list(range(len(targe)))
    for index,item in enumerate(targe):
        if item == '(':
            lab = -1
        elif item == ')':
            lab = 1
        elif item == '[':
            lab = 1
        elif item == ']':
            lab = -1
        else:
            lab = 0

        tu = tu + lab
        T[index] = tu
    #print(T)
    #有括号的用*字符表示，以便后面删掉
    for i,item in enumerate(targe):
        if item in ['(',')','[',']']:
            targe[i] = '*'

    for index,item in enumerate(T):
        targe[index] = add_kuohao(item,targe[index])
    #print('加*标记的targe',targe)

    #删掉带有*的
    i = 0
    while(i<len(targe)):
        if '*' in targe[i]:
            targe.pop(i)
            i = i - 1
        i = i + 1
    #print('删掉带有*的targe：',targe)

    #最后一步：合并括号
    #print(targe)
    T = list(range(len(targe)))
    for index,item in enumerate(targe):
        a = -item.count('(')
        b = item.count('[')
        t = a + b#计算targe中每个位置中【和（的个数，并存入T中
        targe[index] = targe[index].strip('(\|)\|[\|]')
        T[index] = t

    #print(targe)
    #将相同括号合并
    #print('括号索引：',T)
    #print("调子",targe)
    i = 0
    while(i<(len(T)-1)):
        if T[i] == T[i+1]:
            targe[i] = targe[i] + targe[i+1]
            targe.pop(i+1)
            T.pop(i+1)
            i = i - 1
        i = i + 1
        
    #print('去括号后的调子',targe)
    for index,item in enumerate(targe):
        targe[index] = add_kuohao(int(T[index]),item)

    #print('最后结果:',''.join(targe))
    return ''.join(targe)
################################################
##
##将括号分出来的函数
##
#################################################
def add_kuohao(num,t):
    s1 = ''
    s2 = ''
    if num < 0:
        for i in range(abs(num)):
            s1 = s1 + '('

        for i in range(abs(num)):
            s2 = s2 + ')'
    if num > 0:
        for i in range(abs(num)):
            s1 = s1 + '['

        for i in range(abs(num)):
            s2 = s2 + ']'       
    t = s1 + t + s2
    return t
    
def dealwith(talk,cha):
    talk = Pretreatment(talk)
    targe = yuchuli(talk)
    targe = zhuandiao(targe,cha)
    targe = Afterturn(targe)
    return targe
    
   

