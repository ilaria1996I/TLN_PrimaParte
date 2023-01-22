import operator
import math
from time import sleep


def takeWordAndTag(line):
    if line.split('\t')[0].isdigit():
        splitline = line.split('\t')
        parola = splitline[1]
        tag = splitline[2]
        return parola,tag
    return False, False

def smoothingFour(parola_count,tag_count,tag_count_by_parola,ipotesiDiSmothing4,pathVal,pathTest,prob_word_given_tag, tags):
    
    n_parole = 0
    for tag in tags:
            tag_count[tag] = 0
    with open(pathVal, 'r', encoding='utf-8')  as val:
        for line in val:
            parola, tag = takeWordAndTag(line)
            if parola!=False and tag!=False:
                if parola not in parola_count:                  
                    parola_count[parola] = 1 
                    tag_count_by_parola[parola] = dict()              
                    tag_count_by_parola[parola][tag] = 1
                else:
                    parola_count[parola] += 1
                    if tag not in tag_count_by_parola[parola]:
                        tag_count_by_parola[parola][tag] =1
                    else:
                        tag_count_by_parola[parola][tag] +=1
        
        for parola in parola_count.keys():
            for tag in tag_count_by_parola[parola].keys():
                if parola_count[parola] == 1:
                    tag_count[tag] += tag_count_by_parola[parola][tag]
            if parola_count[parola] == 1:
                n_parole += 1
                    
    with open(pathTest, 'r', encoding='utf-8')  as test:
        for line in test:
            if line.split('\t')[0].isdigit():
                splitline = line.split('\t')
                parola = splitline[1]
                if parola not in prob_word_given_tag:
                    ipotesiDiSmothing4[parola] = dict()
                    for tag in tags:
                        if tag != 'LAST':
                            if(tag_count[tag] > 0):
                                ipotesiDiSmothing4[parola][tag] = math.log(
                                tag_count[tag]/n_parole)
    return ipotesiDiSmothing4   

def paroleSconosciute(ipotesiDiSmothing1,ipotesiDiSmothing2,ipotesiDiSmothing3,pathTest,emission, tags,pathVal,prob_word_given_tag, tag_che_precede_tag):
    with open(pathTest, 'r', encoding='utf-8') as test:
        for line in test:
            if line.split('\t')[0].isdigit():
                splitline = line.split('\t')
                word = splitline[1]
                if word not in emission:
                    ipotesiDiSmothing1[word], ipotesiDiSmothing2[word], ipotesiDiSmothing3[word]= dict(), dict(), dict()

                    #P(unk|O) = 1
                    ipotesiDiSmothing1[word]['O'] = math.log(1)

                    #P(unk|O)=P(unk|B-MISC)=0.5
                    ipotesiDiSmothing2[word]['O'] = math.log(0.5)
                    ipotesiDiSmothing2[word]['B-MISC'] = math.log(0.5)
                    
                    #P(unk|ti) = 1/#(PoS_TAGs)
                    for tag in tags:
                        if tag != 'LAST':
                            ipotesiDiSmothing3[word][tag] =  math.log(1/(len(tags)-1)) 

    ipotesiDiSmothing4 = smoothingFour(dict(),dict(),dict(),dict(),pathVal,pathTest,prob_word_given_tag, tag_che_precede_tag.keys())
    return ipotesiDiSmothing1,ipotesiDiSmothing2,ipotesiDiSmothing3,ipotesiDiSmothing4
    