from pyfbsdk import FBSystem, FBApplication, FBComponentList, FBVector3d, FBFindObjectsByName, FBFindModelByLabelName, FBPlayerControl

def ZeroTrans(transNodes):
    # Subtract the X & Z first keyframe value from 
    # the current X & Z positions to zero out their translations
    for node in transNodes:
        if node.Name == "X" or node.Name == "Z":
            keyOffset = node.FCurve.Keys[0].Value
            for key in node.FCurve.Keys:
                key.Value = key.Value - keyOffset
    
# Create an empty Componenet List to populated with the effector models
compList = FBComponentList()

# Get reference to current character and grab the namespace, if there is one
currChar = FBApplication().CurrentCharacter
if currChar.LongName.rfind(":") != -1:
    nameSpace = currChar.LongName.split(":")[0]+":"
else:
    nameSpace = ""

# If Char Controls is active run through the Control Rig joint models
# Else apply the calculation to the Skel Hips joint
if currChar.ActiveInput:
    # Find all Effectors, select them, turn down Reach Values, unselect them
    FBFindObjectsByName("*Effector", compList, False, False)
    for comp in compList:
        comp.Selected = True
        if comp.PropertyList.Find("IK Blend T"):
            comp.PropertyList.Find("IK Blend T").Data = 0
        if comp.PropertyList.Find("IK Blend R"):
            comp.PropertyList.Find("IK Blend R").Data = 0
        if comp.PropertyList.Find("IK Pull"):
            comp.PropertyList.Find("IK Pull").Data = 0
        comp.Selected = False
        
    # Disable Trans and Rot pinning on all effectors
    for comp in FBSystem().Scene.Components:
        if comp.ClassName() == 'FBControlSet':
            for prop in comp.PropertyList:
                if prop.Name.endswith('TPin') or prop.Name.endswith('RPin'):
                    prop.Data = False
                        
    # Switch Hand IK effectors to FK so the hands follow the rest of the body
    # DICE/Walrus rig has IK/FK Sliders, otherwise the code does nothing
    sliderList = FBComponentList()
    FBFindObjectsByName("IkFk*", sliderList, False, True)
    if sliderList:
        for slider in sliderList:
            if slider.Name.endswith("Slider"):
                if slider.Translation[1] > 2:
                    slider.Translation = FBVector3d(0,-2.5,0)
        
    # Get the Hips Effector, select it and set Translation Reach to 100    
    hips = FBFindModelByLabelName(nameSpace+"Character_Ctrl:HipsEffector")
    if hips:
        hips.Selected = True
        hips.PropertyList.Find("IK Blend T").Data = 100
else:
    # Find the hips skel joint
    hips = FBFindModelByLabelName(nameSpace+"Hips")
    if hips:
        hips.Selected = True

# Get the Translation nodes of the hips and zero out X and Y
hipsTransNodes = hips.Translation.GetAnimationNode().Nodes
ZeroTrans(hipsTransNodes)

# Get the Translation nodes of the Trajectory and zero out X and Y
# Trajectory is the EA nomenclature for the root joint
trajectory = FBFindModelByLabelName(nameSpace+"Trajectory")
if trajectory:
    trajTransNodes = trajectory.Translation.GetAnimationNode().Nodes
    ZeroTrans(trajTransNodes)

# "Scrub" the timeslider to update the scene
FBPlayerControl().GotoEnd()
FBPlayerControl().GotoStart()
            
# Clean up
del FBSystem, FBApplication, FBComponentList, FBVector3d, FBFindObjectsByName, FBFindModelByLabelName, FBPlayerControl