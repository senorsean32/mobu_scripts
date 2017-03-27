from pyfbsdk import FBApplication, FBComponentList, FBFindObjectsByName,FBFindModelByLabelName

# Create an empty Componenet List to populated with the effector models
compList = FBComponentList()
# Get refernce to current character
currChar = FBApplication().CurrentCharacter

# If Char Controls is active run through the Control Rig joint models
# Else apply the calculation to the Skel Hips joint
if currChar.ActiveInput:
    # Find all Effectors, select them, turn down Reach Values, unselect them
    FBFindObjectsByName("*Effector", compList, False, False)
    for comp in compList:
        comp.Selected = True
        comp.PropertyList.Find("IK Blend T").Data = 0
        comp.PropertyList.Find("IK Blend R").Data = 0
        comp.PropertyList.Find("IK Pull").Data = 0
        comp.Selected = False
    
    # Get the Hips Effector, select it and set Translation Reach to 100    
    hips = FBFindModelByLabelName("Character_Ctrl:HipsEffector")
    hips.Selected = True
    hips.PropertyList.Find("IK Blend T").Data = 100
else:
    # Find the hips skel joint
    hips = FBFindModelByLabelName("Hips")
    hips.Selected = True

# Get the Translation nodes of the component
hipsTransNodes = hips.Translation.GetAnimationNode().Nodes
# Subtract the X & Z first keyframe value from 
# the current X & Z positions to zero out their translations
for node in hipsTransNodes:
    if node.Name == "X" or node.Name == "Z":
        keyOffset = node.FCurve.Keys[0].Value
        for key in node.FCurve.Keys:
            key.Value = key.Value - keyOffset
            
# Clean up
del FBApplication, FBComponentList, FBFindObjectsByName,FBFindModelByLabelName