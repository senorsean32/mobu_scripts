from pyfbsdk import FBSystem
import re

def DICE_mocap_name_strip(text):
    '''
    Find Imagination Studio substrings in the take name and remove them
    EX: DCE_WRS_07_005_001_Basic_Soldier_Melee_FullBody_Combos_V1_JN_1_Select_1
    '''
    
    # First search for the version type(numbered or starts with 'V')
    if re.findall(r'[V][0-9]{1,2}', text):
        # Find the V version substring, save it to a variable and strip it out
        version = re.findall(r'[V][0-9]{1,2}', text)[0]
        no_version_text = re.sub(r'[V][0-9]{1,2}', "", text)

    elif re.findall(r'[0-9]{2}(?=\_[A-Z]{2})', text):
        # Find the numbered version substring, save it to a variable and strip it out
        version = re.findall(r'[0-9]{2}(?=\_[A-Z]{2})', text)[0]
        no_version_text = re.sub(r'[0-9]{2}(?=\_[A-Z]{2})', "", text)

    else:
    	# If there is no matching version substring dont do shit (more-or-less :P)
        version = ""
        no_version_text = text
        print 'Did not find proper version convention'

    # Remove the word pre fixes ie: "DCE_WRS"
    words_pre = re.sub(r'[A-Z]{3}.',"", no_version_text)
    print words_pre
    
    # Remove the word pre fixes ie: "07_005_001"
    nums_pre = re.sub(r'[0-9]{2,3}.(?![A-Z]{2})', "", words_pre)
    print nums_pre
    
    # After the version number strip out the rest ie: "JN_1_Select_1"
    trim_end = re.sub(r'\_[A-Z]{2}\_[0-9].+|\_[A-Z]{2}\_[A-Z]{2}_[A-Z].+', "", nums_pre)
    print trim_end
    
    # Return the final trimmed version plus the version number
    return trim_end + version
    
for take in FBSystem().Scene.Takes:
    if take.Selected:
        take.Name = DICE_mocap_name_strip(take.Name)

# Clean up
del FBSystem
