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
#Storage Variable for all entries from the file 
all_contacts = []

#open the file with the results 
with open(filepath) as file:
    tsv_file = csv.reader(file, delimiter="\t")
    
    for line in tsv_file:
        all_contacts.append(" ".join(line[0].split()).split(" "))


#Identify all unique interaction partners and save them into an array (necessary, because multiple contacts can exist in a frame which would break an easy row-by-row analysis!)
all_partners = []

#Iterate through all contacts
for contact in all_contacts: 

    #if the contact partner (saved in entry 6) was not yet identified 
    if not contact[6] in all_partners:

        #and if the contact partner is not the file header
        if not contact[6] == "LigandFragment":

            #append this interaction partner to the list of all interaction partners 
            all_partners.append(contact[6])



#an empty entry is appended for each residue-partner combination at the end of the array - this ensures that the last entry is saved! 
for currentPartner in all_partners:
    for currentChain in chains: 
        for currentRes in resnums: 
            all_contacts.append(['2000000000000000000',str(currentRes),currentChain,'XXX','XXX','XXX',currentPartner,'0'])



#Array for storing lines that will be saved into the results file
to_save = []

#iterate through all interaction partners
for currentPartner in all_partners:

    #iterate through all chains
    for currentChain in chains:
        
        #iterate through all residues
        for currentRes in resnums:

            #Here, a new partner of Residue and Interaction Partner is considered
            #All Variables aree reset 
            
            #Variable saving the last frame that showed an interaction
            lastFrameFound = 2000000000000000000
            
            #Variable containing the Ligand from the last identified contact to check if it is a continuous binding - is reset here as a new residue was identified
            lastLigandAtom = ""
            
            #Variable counting the number of frames with an interaction with the same residue
            counterFramesSameLigand = 0
            
            #array saving all durations of contacts identified
            allDurationsForResidue = []
            
            #We now iterate through all identified contacts
            for contact in all_contacts:
            
                #Content of individual contact 
                #contact[0]: Frame#
                #contact[1]: Residue#
                #contact[2]: Chain
                #contact[3]: ResName
                #contact[4]: AtomName
                #contact[5]: LigandFragment
                #contact[6]: LigandAtom
                #contact[7]: Distance
                
                #First we check if the current contact belongs to the residue-interaction partner combination we currently evaluate!
                if (not ((contact[1] == str(currentRes)) and (contact[2] == currentChain) and (contact[6] == currentPartner))):

                    #if not - we skip to the next entry!
                    continue
                
                #Now we are sure, that an entry is of our residue of interest 
                
                #We check if the last found interaction is still present in the current frame (+ a possible allowed Difference). This also checks, if the LigandAtom is indeed the same.
                if ((contact[6] == lastLigandAtom) and (int(contact[0]) - lastFrameFound <= allowedDifference)):
                    
                    #counter gets increased by the number of Frames since the last found frame... 
                    counterFramesSameLigand = counterFramesSameLigand + (int(contact[0]) - lastFrameFound)
                    
                    #...we update the frame Number to the current Frame..
                    lastFrameFound = int(contact[0])
                    
                    #...and continue with the next contact in the list 
                    continue
                
                
                #This point is reached only, when a new interaction partner is found! 
                #The previous entry needs to be saved if any interactions were found.... 
                if not (counterFramesSameLigand == 0): 
                    allDurationsForResidue.append(counterFramesSameLigand)
                
                #...and the variables need to be updated/reset to the current residue
                lastFrameFound = int(contact[0])
                lastLigandAtom = contact[6]
                counterFramesSameLigand = 1
            
            #This is reached when a residue is completely analyzed - all durations get saved to the to_save array
            #residuenumber,residuechain,duration
            for dur in allDurationsForResidue:
                to_save.append(str(currentRes)+","+currentChain+","+str(dur)) 


#Save Data================================================================================================================================================================================

with open(resultspath, "w") as file:
    file.write("res,chain,duration"+ "\n");
    
    for line in to_save:
        file.write(line + "\n")

print("Analysis succesfull!")
