# Skript determining the duration of interactions

After performing Molecular Dynamics simulations with Schrödinger Desmond, interactions between residues or other molecules present in the simulation can be exportet in individual files using e.g. the Simulations-Interactions-Diagramm Tool. Interactions are saved framewise as follows: 

    /# Frame#   Residue#      Chain    ResName   AtomName  LigandFragment      LigandAtom   Distance
         0          1          A        GLU        OE2        L-FRAG_0         Na00001      1.000 
         0          2          A        ASP        OD2        L-FRAG_0         Na00002      1.000 
         0          3          A        ASP        OD2        L-FRAG_0         Na00003      2.512 
    [...]
         1          1          A        GLU        OE2        L-FRAG_0         Na00001      1.000 
         1          2          A        ASP        OD2        L-FRAG_0         Na00002      1.000 
    [...]
         2          1          A        GLU        OE2        L-FRAG_0         Na00001      1.000 
         2          2          A        ASP        OD2        L-FRAG_0         Na00002      1.000
         2          3          A        ASP        OD2        L-FRAG_0         Na00003      2.512

This skript summarizes interactions that are present in consecutive frames. In the dataset above, Residue #1 shows interactions to the same LigandAtom (Na00001) in all three frames (0, 1, 2). Similarly, Residue #2 shows interactions with the same interaction partner over three frames. Residue #3, however, shows no interaction in Frame 1. This skript summarizes these data and produces a .csv-File as output as follows: 

    res,chain,duration      <- Headline
    1,A,3                   <- Residue 1 of chain A showed an interaction that lasted for three frames (Frames: 0, 1, 2)
    2,A,3                   <- Residue 2 of chain A showed an interaction that lasted for three frames (Frames: 0, 1, 2)
    3,A,1                   <- Residue 3 of chain A showed an interaction that lasted for one frame    (Frame: 0)
    3,A,1                   <- Residue 3 of chain A showed an interaction that lasted for one frame    (Frame: 2)
    [...]

In the skript, it is necessary to specify the File Path of the exported data in `filename` and `filepath` variables, as well as a path for the output file in `resultspath`. Moreover, chains and residues of interest need to be specified in arrays `chains` and `resnums`, respectively.  

> [!TIP]
> If desired, interactions can be deemed continuous despite small gaps in which the interaction was not observed. Therefore, edit the value of the `allowedDifference` variable. A value of 1 means that frames must be consecutive, a value of 2 would e.g. allow (multiple) gaps of 1 Frame in an interaction. 

The repository contains a version with detailed comments on how the skript works and an additional uncommented version. 

This code was used to generate interaction analysis with sodium atoms in the following publication:
Staudner T et al. in preparation. 

For questions, contact florian.sure@fau.de
