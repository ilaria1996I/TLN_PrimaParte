
import math

#funzione principale di questo file py. Questa funzione svolgera tutta la fase di learning.
def fase_di_learning(path):
    tag_che_precede_tag, tag_della_parola = contatore_di_tag_e_parole(path) 
    #da questo punto in poi si calcola le probabilità usando i contatori precedenti (tag_che_precede_tag, tag_della_parola)
    
    #calcoliamo P(ti | ti-1) usando "tag_che_precede_tag"
    prob_che_un_tag_precedi_un_altro_tag = dict()
    for tag_precedente in tag_che_precede_tag:
        
        for tag_corrente in tag_che_precede_tag[tag_precedente]:
            if tag_precedente not in prob_che_un_tag_precedi_un_altro_tag:
                prob_che_un_tag_precedi_un_altro_tag[tag_precedente] = dict()  
            
            numeratore = tag_che_precede_tag[tag_precedente][tag_corrente]
            denominatore = contaOccorrenze(tag_che_precede_tag[tag_precedente])
            prob_che_un_tag_precedi_un_altro_tag[tag_precedente][tag_corrente] = calcoloLogaritmo(numeratore,denominatore)

            
    #calcoliamo P(wi | ti) usando "tag_della_parola"
    prob_parola_con_tag = dict()
    for parola in tag_della_parola:
        for tag_corrente in tag_della_parola[parola]:
            if parola not in prob_parola_con_tag:prob_parola_con_tag[parola] = dict()  
            
            numeratore = tag_della_parola[parola][tag_corrente]
            denominatore = contaOccorrenze(tag_che_precede_tag[tag_corrente]) 
            prob_parola_con_tag[parola][tag_corrente] = calcoloLogaritmo(numeratore,denominatore)
            
    return tag_che_precede_tag, tag_della_parola, prob_parola_con_tag , prob_che_un_tag_precedi_un_altro_tag


def riempi_dict_quando_non_è_una_riga_vuota(tag_precedente,numero_di_riga,parola,tag,tag_della_parola,tag_che_precede_tag):
    if numero_di_riga == 0: #se è la prima parola della frase!
        tag_precedente = tag
        if tag in tag_che_precede_tag['FIRST']:tag_che_precede_tag['FIRST'][tag] += 1
        else:tag_che_precede_tag['FIRST'][tag] = 1

            
    #C(ti, wi) -----> mi permetterà di fare il conteggio quando la parola W viene dato tag T 
    if parola not in tag_della_parola:tag_della_parola[parola] = dict()
    if tag in tag_della_parola[parola]:tag_della_parola[parola][tag] += 1
    else:tag_della_parola[parola][tag] = 1
    

    #C(ti-1, ti)-----> mi permette di fare il conteggio quando la parola T-1 precede il tag T 
    if numero_di_riga > 0:
        if tag_precedente not in tag_che_precede_tag:tag_che_precede_tag[tag_precedente] = dict() 
        if tag in tag_che_precede_tag[tag_precedente]:tag_che_precede_tag[tag_precedente][tag] += 1
        else:tag_che_precede_tag[tag_precedente][tag] = 1
    tag_precedente = tag
    return tag_della_parola,tag_che_precede_tag,tag_precedente

def contatore_di_tag_e_parole(path):
    tag=''
    tag_precedente = ''
    tag_della_parola = dict()
    tag_che_precede_tag = dict()
    tag_che_precede_tag['FIRST'] = dict()

    with open(path, 'r', encoding='utf-8') as testo:
        for i, line in enumerate(testo):    
            
            if(line == '\n'): # se è una riga vuota è finita la frase
                if "LAST" not in tag_che_precede_tag[tag]:tag_che_precede_tag[tag]['LAST'] = 1
                else:tag_che_precede_tag[tag]['LAST'] += 1
                       
            elif (line.split('\t')[0].isdigit()): #se il primo numero è un digit allora
                splitLine = line.split('\t')
                numero_di_riga = int(splitLine[0])  
                parola = splitLine[1]    
                tag = splitLine[2]      
                tag_della_parola,tag_che_precede_tag,tag_precedente = riempi_dict_quando_non_è_una_riga_vuota(tag_precedente,numero_di_riga,parola,tag,tag_della_parola,tag_che_precede_tag)
                
    
    return tag_che_precede_tag, tag_della_parola

def calcoloLogaritmo(v1,v2):
    c = math.log(v1/v2)
    return c

def contaOccorrenze(dictValue):
    conta = 0
    for correnteE in dictValue:
        conta += dictValue[correnteE]
        #print(dictValue[elem])
    return conta  

