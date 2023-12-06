import sys
import csv

#Settings================================================================================================================================================================================
#TO EDIT: files 
filename = "PLACEHOLDER FILENAME WITHOUT .dat SUFFIX - WILL BE INCLUDED IN FILEPATH AND RESULTSPATH"
filepath = "PLACEHOLDER FILEPATH" + filename + ".dat"
resultspath = "PLACEHOLDER PATH RESULTS" + filename + "_RESULTS.txt"

#TO EDIT: chains and residues available in the dataset that shall be analyzed 
chains = ["A", "B"]
resnums = [1,2,3]

#TO EDIT: allowed difference in frameNumbers to still be considered a continuous contact
allowedDifference = 1


#Start of Analysis========================================================================================================================================================================
all_contacts = []

with open(filepath) as file:
    tsv_file = csv.reader(file, delimiter="\t")    
    for line in tsv_file:
        all_contacts.append(" ".join(line[0].split()).split(" "))

all_partners = []
for contact in all_contacts: 
    if not contact[6] in all_partners:
        if not contact[6] == "LigandFragment":
            all_partners.append(contact[6])

for currentPartner in all_partners:
    for currentChain in chains: 
        for currentRes in resnums: 
            all_contacts.append(['2000000000000000000',str(currentRes),currentChain,'XXX','XXX','XXX',currentPartner,'0'])

to_save = []
for currentPartner in all_partners:
    for currentChain in chains:
        for currentRes in resnums:
            lastFrameFound = 2000000000000000000
            lastLigandAtom = ""
            counterFramesSameLigand = 0
            allDurationsForResidue = []
            
            for contact in all_contacts:
                if (not ((contact[1] == str(currentRes)) and (contact[2] == currentChain) and (contact[6] == currentPartner))):
                    continue
                
                if ((contact[6] == lastLigandAtom) and (int(contact[0]) - lastFrameFound <= allowedDifference)): 
                    counterFramesSameLigand = counterFramesSameLigand + (int(contact[0]) - lastFrameFound)
                    lastFrameFound = int(contact[0])
                    continue
                
                if not (counterFramesSameLigand == 0): 
                    allDurationsForResidue.append(counterFramesSameLigand)
                
                lastFrameFound = int(contact[0])
                lastLigandAtom = contact[6]
                counterFramesSameLigand = 1
            
            for dur in allDurationsForResidue:
                to_save.append(str(currentRes)+","+currentChain+","+str(dur)) 


#Save Data================================================================================================================================================================================
with open(resultspath, "w") as file:
    file.write("res,chain,duration"+ "\n");
    
    for line in to_save:
        file.write(line + "\n")

print("Analysis succesfull!")
