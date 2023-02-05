import operator

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
                    res_base = baseline(frase, tag_della_parola,dict() )
                    sm1 = algoritmoDiViterbi(dict(),dict(),dict(),frase, prob_che_un_tag_precedi_un_altro_tag, prob_parola_con_tag, smoothing1)[0]
                    sm2 = algoritmoDiViterbi(dict(),dict(),dict(),frase, prob_che_un_tag_precedi_un_altro_tag, prob_parola_con_tag, smoothing2)[0]
                    sm3 = algoritmoDiViterbi(dict(),dict(),dict(),frase, prob_che_un_tag_precedi_un_altro_tag, prob_parola_con_tag, smoothing3)[0]
                    sm4 = algoritmoDiViterbi(dict(),dict(),dict(),frase, prob_che_un_tag_precedi_un_altro_tag, prob_parola_con_tag, smoothing4)[0]
                    
                    
                    for i, parola in enumerate(frase):
                        if (condizione == True):
                            print(parola)
                            print("smothing1 --> ", sm1[parola])
                            print("smothing2 --> ", sm2[parola])
                            print("smothing3 --> ", sm3[parola])
                            print("smothing4 --> ", sm4[parola])
                            print("baseline -->", res_base[parola] )

                        if sm1[parola] == tag_suggerito_dal_file[i]:paroleCorretteSmoothing1 += 1
                        if sm2[parola] == tag_suggerito_dal_file[i]:paroleCorretteSmoothing2 += 1
                        if sm3[parola] == tag_suggerito_dal_file[i]:paroleCorretteSmoothing3 += 1
                        if sm4[parola] == tag_suggerito_dal_file[i]:paroleCorretteSmoothing4 += 1
                        if res_base[parola] == tag_suggerito_dal_file[i]:paroleCorretteBaseline += 1
                        
                    tag_suggerito_dal_file = list()
                    frase = list()
            
            s1 = round((paroleCorretteSmoothing1 *100) /num_totale_parole ,2)
            s2 = round((paroleCorretteSmoothing2 *100) /num_totale_parole, 2)
            s3 = round((paroleCorretteSmoothing3 *100) /num_totale_parole, 2)
            s4 = round((paroleCorretteSmoothing4 *100) /num_totale_parole, 2)
            cont = (int(s1)+int(s2)+int(s3)+int(s4))/4
            
            print("smoothing1: "+str(s1)+" %")
            print("smoothing2: "+str(s2)+" %")
            print("smoothing3: "+str(s3)+" %")
            print("smoothing4: "+str(s4)+" %")
            print("baseline: "+str(round((paroleCorretteBaseline *100) / num_totale_parole, 2))+"%")

#algoritmo di Baseline 
def baseline(frase, tag_della_parola,dictForBaseLine):
    for parola in frase:
        if parola in tag_della_parola:dictForBaseLine[parola] = max(tag_della_parola[parola].items(), key=operator.itemgetter(1))[0]  
        else:dictForBaseLine[parola] = 'MISC'
    return dictForBaseLine
    
def algoritmoDiViterbi(vit,path,posPath,frase:list, trans_prob:dict, emission_prob:dict, parole_sconosciute:dict ):
    tag='tag_null' #verrà cambiato con quello corretto successivamente
    numParoleDellaFrase = len(frase)
    #1. setto la prima colonna
    for state in trans_prob.keys():
        if(state != 'FIRST'): #perche mi serve la seconda parola dove il tag precedente è FIRST
            vit[state] = list()
            path[state] = list()
            if  frase[0] in parole_sconosciute:
                trans_probAndParole_sconosciute = -100000 #nel caso in cui non entra nel if sotto do un valore "nullo"
                if state in parole_sconosciute[frase[0]] and state in trans_prob['FIRST']:
                    trans_probAndParole_sconosciute = trans_prob['FIRST'][state] + parole_sconosciute[frase[0]][state]
                vit[state].append(trans_probAndParole_sconosciute)
                
            else:
                trans_probAndEmission_prob = -100000 #nel caso in cui non entra nel if sotto do un valore "nullo"
                if state in emission_prob[frase[0]] and state in trans_prob['FIRST']:
                    trans_probAndEmission_prob = trans_prob['FIRST'][state] +  emission_prob[frase[0]][state]
                vit[state].append(trans_probAndEmission_prob)
            
            path[state].append(tag)
    
    #2. setto le colonne successive alla prima
    for i in range(numParoleDellaFrase):
        if(i>0):
            migliorVitCorr = -100000
            for state in trans_prob.keys():
                if(state != 'FIRST'):
                    migliorVitCorr, migliorPathCorr, tag = scegliValoreDiViterbiMiglioreFinoAlloStatoCorrente(-100000,-100000,vit, frase[i], i-1, tag,state, trans_prob, emission_prob, parole_sconosciute)
                    path[state].append(round(migliorPathCorr,2))
                    vit[state].append(round(migliorVitCorr,2))
            posPath[frase[i-1]] = tag

    migliorPathCorr = -100000
    ViterbiCambiato = 0
    lastTag = ''
    for tagPreced in trans_prob.keys():
        if tagPreced != 'FIRST':
            if( 'LAST' in trans_prob[tagPreced]): #se siamo qui è l'ultima parola
                ViterbiCambiato = vit[tagPreced][i]+ trans_prob[tagPreced]['LAST']
                if ViterbiCambiato > migliorPathCorr:
                    migliorPathCorr = ViterbiCambiato
                    lastTag = tagPreced 
    vit['LAST'] = migliorPathCorr
    posPath[frase[i]] = lastTag

    return posPath, vit



#La funzione che preleva il massimo (viene utilizzata nell'algoritmo di viterbi)
def scegliValoreDiViterbiMiglioreFinoAlloStatoCorrente(migliorVitCorr,migliorPathCorr,vit, parola, i, tag, state,trans_prob, emission_prob, parole_sconosciute):
    for tagPreced in trans_prob.keys():
        if tagPreced != 'FIRST':
            if parola in parole_sconosciute:
                if state in parole_sconosciute[parola] and state in trans_prob[tagPreced]:
                    valoreViterbiCambiato = vit[tagPreced][i] + trans_prob[tagPreced][state]+parole_sconosciute[parola][state]
                    if valoreViterbiCambiato > migliorVitCorr:migliorVitCorr = valoreViterbiCambiato
                    pathViterbiCambiato = vit[tagPreced][i]+ trans_prob[tagPreced][state]
                    if pathViterbiCambiato > migliorPathCorr:
                        migliorPathCorr = pathViterbiCambiato
                        tag = tagPreced
            else:
                if (parola in emission_prob and tagPreced in trans_prob):
                    if(state in emission_prob[parola] and state in trans_prob[tagPreced]):
                        valoreViterbiCambiato = vit[tagPreced][i] + trans_prob[tagPreced][state]+emission_prob[parola][state]
                        if valoreViterbiCambiato > migliorVitCorr:migliorVitCorr = valoreViterbiCambiato
                        pathViterbiCambiato = vit[tagPreced][i]+ trans_prob[tagPreced][state]
                        if pathViterbiCambiato > migliorPathCorr:
                            migliorPathCorr = pathViterbiCambiato
                            tag = tagPreced
    
    return migliorVitCorr, migliorPathCorr, tag



