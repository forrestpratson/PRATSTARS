# PRATSTARS
Event Visualization Tool for High Energy Particle Physics. Current version works with DAOD and LHE files

### LHE Event Display:
Arguments

    --file - specify the full path to the LHE file you wish to analyze

    --event - specify the specific event within the file you wish to analyze
        Contrary to the DAOD display, the LHE display labels the events sequentially as they appear in the file. 
        Therefore, if there are 100 events in your file. the possible values for event number are 1,2,3...100.

    --output - the full path to the folder where you would like to save out the generated figure. 
    
    Example:
    <User-Computer>$ pratstar_LHE.py --file=file.lhe --event=10 --output=/Path/To/Folder/Outputs
The above example code will open "file.lhe" and generate a figure for the 10th event in the file, then save said figure in a folder called "Outputs"
 
 ### DAOD Event Display
 Arguments
 
    --file - specify the full path to the LHE file you wish to analyze

    --event - specify the specific event within the file you wish to analyze
        Contrary to the DAOD display, the LHE display labels the events sequentially as they appear in the file. 
        Therefore, if there are 100 events in your file. the possible values for event number are 1,2,3...100.

    --output - the full path to the folder where you would like to save out the generated figure.
    
 
    Example:
    <User-Computer>$ pratstar_DAOD.py --file=file.root.1 --event=1234567 --output=/Path/Outputs --view=Transverse --show=True --thresh=10 --lables=1
The above example code will open the file "file.root.1", and generate a transverse plane display for the event numbered 1234567. It will only show the vectors of particles of transverse momentum greater than 10MeV, and label the top 5 tracks with the highest transverse momentum. The program will also open the image after it is generated
