##################################################################################
############### PROGRAM TO APPLY ENTROPY BASED DISCRETIZATION  ###################
########################## BY LIONEL NGOBESING ALANGEH ###########################
##################################################################################
from math import log,log2
import csv

#################################################################################
## Iterate through table for different combinations and separate ages into those
## who satisfy response combinations and those who dont
def answer_combinations():
    #generate different answer combinations (EEE,EEH,EHE,EHH,HEE,HEH,HHE,HHH)
    combo = ['EEE','EEH','EHE','EHH','HEE','HEH','HHE','HHH']
    yes = 0
    no = 0
    info_l = 0
    info_g = 0
    temporal_list = []

    for i in combo:
        best_I_G = 0
        best_age = 0
        IG_list = []
        for split_age in range(9, 96):
            Dataset = []
            split_age_greater = []
            split_age_greater_count = 0
            split_age_lesser = []
            split_age_lesser_count = 0
            entries = 0
            yes = 0
            temporal_list = []
            temporal_list_string = ''

            with open("dataset_ebd.csv", 'r') as file:
                reader = csv.reader(file, delimiter=';')
                for line in reader:
                    Entries_arr = []
                    entries += 1
                    for word in line:
                        Entries_arr.append(word)

                    if int(Entries_arr[1]) >= split_age:
                        split_age_greater.append(Entries_arr)
                        split_age_greater_count += 1
                    elif int(Entries_arr[1]) < split_age:
                        split_age_lesser.append(Entries_arr)
                        split_age_lesser_count += 1
                    Dataset.append(Entries_arr)

            #print("------------ For ages < split age-------------")
            result = answer_combinations_lesser(combo,yes,no,i,split_age_lesser,split_age_greater_count)
            a = result[0]
            b = split_age_lesser_count - a
            info_l = info_split_calc(split_age_lesser_count, entries, a, b)

            #print("---------- For ages > or = split age----------")
            result = answer_combinations_greater(combo,yes,no,i,split_age_greater,split_age_greater_count)
            a = result[0]
            b = split_age_greater_count - a
            info_g = info_split_calc(split_age_greater_count, entries, a, b)

            # Return total entropy of iteration
            E = calc_entropy(split_age_lesser_count,split_age_greater_count,entries)
            I = info_split(info_l,info_g)
            I_G = E-I
            new_I_G = float(format(I_G,".5f"))
            IG_list.append(new_I_G)
            if new_I_G > best_I_G:
                best_age = split_age
                best_I_G = new_I_G

        big = max(IG_list)
        print("==============================================")
        print("********* I(G)'s for ", i," ******************")
        print(IG_list)
        print("----------------------------------------------")
        print("Best I(G) for ", i, "is at age ", best_age)
        print("==> I(G) = E(X) - I(E) = %f" % (best_I_G))
        print("**********************************************")
        print("==============================================")

    return split_age_lesser,split_age_lesser_count, split_age_greater, split_age_greater_count
################################################################################


################################################################################
## Function for less than split age combination
def answer_combinations_lesser(combo,yes,no,i,split_age_lesser,split_age_lesser_count):
    for answer in split_age_lesser:
        #take 2nd, 3rd and 4th items in list and convert to string (or. 'H' 'E' 'E' = HEE)
        temporal_list = []
        temporal_list.append(answer[2])
        temporal_list.append(answer[3])
        temporal_list.append(answer[4])
        temporal_list_string = ''.join(temporal_list)
        if temporal_list_string == i:
            yes = yes + 1

    return yes, no
#################################################################################


#################################################################################
## Function for greater than split age combinations
def answer_combinations_greater(combo,yes,no,i,split_age_greater,split_age_greater_count):
    for answer in split_age_greater:
        # take 2nd, 3rd and 4th items in list and convert to string (or. 'H' 'E' 'E' = HEE)
        temporal_list = []
        temporal_list.append(answer[2])
        temporal_list.append(answer[3])
        temporal_list.append(answer[4])
        temporal_list_string = ''.join(temporal_list)
        if temporal_list_string == i:
            yes = yes + 1

    return yes, no
###############################################################################


################################################################################
## Function to calculate information of the split
def info_split_calc(l, m, y, n):
    p_yes = y / l
    p_no = n / l
    entropy_of_yes = -(p_yes * log2(p_yes))
    entropy_of_no = -(p_no * log2(p_no))
    info1 = ((l/m) * (entropy_of_yes + entropy_of_no))
    info = format(info1, ".5f")
    #print ("information(E) = ", info)
    return info
##############################################################################


##############################################################################
## Function to calculate information split of iteration.
def info_split(info_l, info_g):
    info_s = float(info_l) + float(info_g)
    #print ("I(E) = %F" %(info_s))
    return info_s
##############################################################################


##############################################################################
## function to find iteration entropy using formula Entropy=-∑(p)log2(p)
def calc_entropy(split_age_lesser_count,split_age_greater_count,entries):
    p = split_age_lesser_count / entries
    n = split_age_greater_count / entries
    entropy = -(p) * log2(p) - (n) * log2(n)
    return entropy
################################################################################

#-------------------------RUN PROGRAM--------------------------------------
answer_combinations()