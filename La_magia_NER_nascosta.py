import corpusAlgoritmo
import faseDiLearning
import faseDiSmoothing

lingua = ""
condizione = True
while(condizione):
    print('In che lingua mi vuoi istruire: (scrivi it o eng)')
    x = input()
    if (x == "it"):
        lingua = "it"
        condizione = False
    elif (x == "eng"):
        lingua = "eng"
        condizione = False
       
pathTrain = "data/"+lingua+"/train.conllu"
pathTest = "data/"+lingua+"/test.conllu"
pathVal = "data/"+lingua+"/val.conllu"
frasiHarryPotter = "data/valutazione_frasiDelProf.conllu"

#LEARNING!!
tag_che_precede_tag, tag_della_parola,prob_word_given_tag, prob_tag_given_pred_tag = faseDiLearning.fase_di_learning(pathTrain)

#parole sconosciute
ipotesiDiSmothing1,ipotesiDiSmothing2,ipotesiDiSmothing3,ipotesiDiSmothing4 = faseDiSmoothing.paroleSconosciute(dict(),dict(),dict(),pathTest,prob_word_given_tag, tag_che_precede_tag.keys(),pathVal,prob_word_given_tag, tag_che_precede_tag)

#fase di decoding
corpusAlgoritmo.decoding(pathTest, tag_della_parola, prob_tag_given_pred_tag, prob_word_given_tag, ipotesiDiSmothing1, ipotesiDiSmothing2, ipotesiDiSmothing3, ipotesiDiSmothing4,False)

condizione = True
while(condizione):
    print('Preferisci testare le tre frasi del prof? ( si o no)')
    x = input()
    if (x == "si"):
        ipotesiDiSmothing1F,ipotesiDiSmothing2F,ipotesiDiSmothing3F,ipotesiDiSmothing4F = faseDiSmoothing.paroleSconosciute(ipotesiDiSmothing1,ipotesiDiSmothing2,ipotesiDiSmothing3,frasiHarryPotter,prob_word_given_tag, tag_che_precede_tag.keys(),pathVal,prob_word_given_tag, tag_che_precede_tag)
        corpusAlgoritmo.decoding(frasiHarryPotter, tag_della_parola, prob_tag_given_pred_tag, prob_word_given_tag, ipotesiDiSmothing1F, ipotesiDiSmothing2F, ipotesiDiSmothing3F, ipotesiDiSmothing4F,False)
        condizione = False
        
    elif (x == "no"):
        condizione = False
