import sys
import math

def fn_seperate_tokens(text):
   
    tokens = []
    for w in text.split():
        if not all(c in '.,!?;:"()[]' for c in w):  #Here I am ignoring only punctuations
            tokens.append(w)
    return tokens

def fn_helper_counting(lines):
    
    my_unigrams = {}
    my_bigrams = {}
    total_unigrams = 0
    total_bigrams = 0
    
    for line in lines:
        tokens = fn_seperate_tokens(line)
        total_unigrams += len(tokens)
        
        
        for token in tokens:
            if token in my_unigrams:
                my_unigrams[token] += 1
            else:
                my_unigrams[token] = 1
      
        for i in range(len(tokens) - 1):
            bigram = (tokens[i], tokens[i + 1])
            if bigram in my_bigrams:
                my_bigrams[bigram] += 1
            else:
                my_bigrams[bigram] = 1
            total_bigrams += 1
            
    return my_unigrams, my_bigrams, total_unigrams, total_bigrams

def fun_for_chi_square(bigram, my_bigrams, my_unigrams, total_unigrams):
    
    word_1, word_2 = bigram
    obs_11 = my_bigrams
    obs_12 = my_unigrams[word_2] - obs_11
    obs_21 = my_unigrams[word_1] - obs_11
    obs_22 = total_unigrams - obs_11 - obs_12 - obs_21

    exp_11 = (my_unigrams[word_1] * my_unigrams[word_2]) / total_unigrams
    exp_12 = (my_unigrams[word_2] * (total_unigrams - my_unigrams[word_1])) / total_unigrams
    exp_21 = (my_unigrams[word_1] * (total_unigrams - my_unigrams[word_2])) / total_unigrams
    exp_22 = ((total_unigrams - my_unigrams[word_1]) * (total_unigrams - my_unigrams[word_2])) / total_unigrams

    
    chi_square = (obs_11 - exp_11) ** 2 / exp_11 + (obs_12 - exp_12) ** 2 / exp_12 + (obs_21 - exp_21) ** 2 / exp_21 + (obs_22 - exp_22) ** 2 / exp_22
    return chi_square

def fun_for_PMI(bigram, my_bigrams, my_unigrams,total_unigrams ,total_bigrams):
    
    word_1, word_2 = bigram
    p_bigram = my_bigrams / total_bigrams
    p_word_1 = my_unigrams[word_1] / total_unigrams
    p_word_2 = my_unigrams[word_2] / total_unigrams
    pmi = math.log2(p_bigram / (p_word_1 * p_word_2)) if p_word_1 * p_word_2 != 0 else 0
    return pmi

def fun_sorting_bigrams(scores):
    
    return sorted(scores.items(), key=lambda y: y[1],reverse=True)[:20]

def main():
    if len(sys.argv) != 3:
        print("Please use <select_measure> here either 'PMI' or chi-square")
        sys.exit(1)

    my_imputdata = sys.argv[1]
    select_measure = sys.argv[2]

    
    with open(my_imputdata, 'r') as f:
        lines = f.readlines()
    #i'm reading it as lines and  because in input data it look like lines

    my_unigrams, my_bigrams, total_unigrams, total_bigrams = fn_helper_counting(lines)
    
    scores = {}
    for bigram, num_each_B in my_bigrams.items():
        if select_measure == 'chi-square':
            score = fun_for_chi_square(bigram, num_each_B, my_unigrams,total_unigrams)
        elif select_measure == 'PMI':
            score = fun_for_PMI(bigram, num_each_B, my_unigrams, total_unigrams,total_bigrams)
        else:
            print("please select any one measure to proceed further")
            sys.exit(1)
        scores[bigram] = score
    

    top_bigrams = fun_sorting_bigrams(scores)
    #print(top_bigrams)
    
    for bigram, score in top_bigrams:
        print(f"{bigram[0]} {bigram[1]}: {score}")

if __name__ == "__main__":
    main()
