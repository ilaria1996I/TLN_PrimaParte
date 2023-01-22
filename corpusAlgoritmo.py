import operator
import math

#algoritmo di viterbi
def viterbi(frase:list, trans_prob:dict, emission_prob:dict, smoothed:dict ):
    vit = dict()
    path = dict()
    posPath = dict()
    maxTag='_'
    for state in trans_prob.keys():
        if(state != 'FIRST'):
            vit[state] = list()
            path[state] = list()
            if  frase[0] in smoothed:
                if state in smoothed[frase[0]] and state in trans_prob['FIRST']:
                    vit[state].append(  trans_prob['FIRST'][state] +  smoothed[frase[0]][state])
                else:
                    vit[state].append(-9999)
            else:
                if state in emission_prob[frase[0]] and state in trans_prob['FIRST']:
                    vit[state].append(  trans_prob['FIRST'][state] +  emission_prob[frase[0]][state])
                else:
                    vit[state].append(-9999)
            path[state].append(maxTag)
    for i in range(len(frase)):
        if(i>0):
            mVit = -9999
            for state in trans_prob.keys():
                if(state != 'FIRST'):
                    mVit, mPath,  maxTag = maximum(vit, frase[i], i-1, maxTag,state, trans_prob, emission_prob, smoothed)
                    path[state].append(round(mPath,2))
                    vit[state].append(round(mVit,2))
            posPath[frase[i-1]] = maxTag

    mPath = -9999
    temp = 0
    lastTag = ''
    for s in trans_prob.keys():
        if s != 'FIRST':
            if( 'LAST' in trans_prob[s]):
                temp = vit[s][i]+ trans_prob[s]['LAST']
                if temp > mPath:
                    mPath = temp
                    lastTag = s 
    vit['END'] = mPath
    posPath[frase[i]] = lastTag

    return posPath, vit

#algoritmo di Baseline
def baseline(frase, tag_della_parola):
    res = dict()
    
    for parola in frase:
        if parola in tag_della_parola:
            res[parola] = max(tag_della_parola[parola].items(), key=operator.itemgetter(1))[0]
            
        else:
            res[parola] = 'MISC'
    return res

#La funzione che preleva il massimo (viene utilizzata nell'algoritmo di viterbi)
def maximum(vit, parola, i, maxTag, state,trans_prob, emission_prob, smoothed):
    mVit = -9999
    mPath = -9999
    temp1 = 0
    temp2 = 0

    for s in trans_prob.keys():
        if s != 'FIRST':
            if parola in smoothed:
                if state in smoothed[parola] and state in trans_prob[s]:
                    temp1 = vit[s][i] + trans_prob[s][state]+   smoothed[parola][state]
                    if temp1 > mVit:
                        mVit = temp1
                    
                    temp2 = vit[s][i]+ trans_prob[s][state]
                    if temp2 > mPath:
                        mPath = temp2
                        maxTag = s
            else:
                if (parola in emission_prob and s in trans_prob):
                    if(state in emission_prob[parola] and state in trans_prob[s]):
                        temp1 = vit[s][i] + trans_prob[s][state]+   emission_prob[parola][state]
                        if temp1 > mVit:
                            mVit = temp1
                        
                        temp2 = vit[s][i]+ trans_prob[s][state]
                        if temp2 > mPath:
                            mPath = temp2
                            maxTag = s
    
    return mVit, mPath, maxTag


def decoding(pathTest, tag_della_parola, prob_che_un_tag_precedi_un_altro_tag, prob_parola_con_tag,smoothing1, smoothing2, smoothing3, smoothing4,condizione):
    frase = list()
    tag_suggerito_dal_file = list()
    
    paroleCorretteBaseline = 0
    paroleCorretteSmoothing1 = 0
    paroleCorretteSmoothing2 = 0
    paroleCorretteSmoothing3 = 0
    paroleCorretteSmoothing4 = 0

    num_totale_parole = 0
    i = 0
    with open(pathTest, 'r', encoding='utf-8') as test:
            for line in test:
                if line.split('\t')[0].isdigit():
                    splitline = line.split('\t')
                    frase.append(splitline[1])
                    if condizione == True:
                        print("Word: ")
                        print(splitline[1])
                    tag_suggerito_dal_file.append(splitline[2])
                    num_totale_parole += 1
                if line == '\n':
                    res_base = baseline(frase, tag_della_parola )
                    sm1 = viterbi(frase, prob_che_un_tag_precedi_un_altro_tag, prob_parola_con_tag, smoothing1)[0]
                    sm2 = viterbi(frase, prob_che_un_tag_precedi_un_altro_tag, prob_parola_con_tag, smoothing2)[0]
                    sm3 = viterbi(frase, prob_che_un_tag_precedi_un_altro_tag, prob_parola_con_tag, smoothing3)[0]
                    sm4 = viterbi(frase, prob_che_un_tag_precedi_un_altro_tag, prob_parola_con_tag, smoothing4)[0]
                    
                    
                    for i, parola in enumerate(frase):
                        if (condizione == True):
                            print(parola)
                            print("smothing1 -->", sm1[parola])
                            print("smothing2 -->", sm2[parola])
                            print("smothing3 -->", sm3[parola])
                            print("smothing4 -->", sm4[parola])
                            print("baseline -->", res_base[parola] )

                        if sm1[parola] == tag_suggerito_dal_file[i]:
                            paroleCorretteSmoothing1 += 1
                        if sm2[parola] == tag_suggerito_dal_file[i]:
                            paroleCorretteSmoothing2 += 1
                        if sm3[parola] == tag_suggerito_dal_file[i]:
                            paroleCorretteSmoothing3 += 1
                        if sm4[parola] == tag_suggerito_dal_file[i]:
                            paroleCorretteSmoothing4 += 1
                        if res_base[parola] == tag_suggerito_dal_file[i]:
                            paroleCorretteBaseline += 1
                        
                    tag_suggerito_dal_file = list()
                    frase = list()
            
            s1 = round((paroleCorretteSmoothing1 *100) /num_totale_parole ,2)
            s2 = round((paroleCorretteSmoothing2 *100) /num_totale_parole, 2)
            s3 = round((paroleCorretteSmoothing3 *100) /num_totale_parole, 2)
            s4 = round((paroleCorretteSmoothing4 *100) /num_totale_parole, 2)
            cont = (int(s1)+int(s2)+int(s3)+int(s4))/4
            
            print("smoothing1: "+str(s1) +" %")
            print("smoothing2: "+str(s2)+" %")
            print("smoothing3: "+str(s3)+" %")
            print("smoothing4: "+str(s4)+" %")
            print("smooth baseline: "+str(round((paroleCorretteBaseline *100) / num_totale_parole, 2))+"%")
