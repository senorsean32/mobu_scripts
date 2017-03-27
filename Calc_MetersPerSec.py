from pyfbsdk import FBSystem, FBModelList, FBGetSelectedModels, FBMessageBox

def has_keys_check(node):
    for animNode in translationNode.Nodes:
        if animNode.KeyCount == 0:
            return False
    return True

def find_key_avg(kList):
    # Get the average of the value of all the keys in an Axis
    total = 0
    for key in kList:
        total += key.Value
    return total/float(len(kList))
            
    
def key_variance(kList):
    # Calculate the variance between all the keys
    # This will help determine which translation axis is the movement direction of the cycle
    average = find_key_avg(kList)
    variance = 0
    
    for fbkey in kList:
        variance += ((average - fbkey.Value)**2)
        
    total = variance / len(kList)
    return total
    
def find_move_axis(kList):
    # Grab the keys from each translation axis
    xKeys = kList[0].FCurve.Keys
    yKeys = kList[1].FCurve.Keys
    zKeys = kList[2].FCurve.Keys
    
    # Find the variance value
    xVar = key_variance(xKeys)
    yVar = key_variance(yKeys)
    zVar = key_variance(zKeys)
    
    # Return the key list that has the highest variance value
    if max(xVar, yVar, zVar) == xVar:
        return xKeys
    elif max(xVar, yVar, zVar) == yVar:
        return yKeys
    else:
        return zKeys

def get_dist(kList):
    # Get first and last frame in the key list
    start_pos = kList[0].Value
    end_pos = kList[len(kList) - 1].Value
    
    return end_pos - start_pos

def get_frames():
    #  Get the start and end frames of the time slider
    start_frame = float(FBSystem().CurrentTake.LocalTimeSpan.GetStart().GetFrame())
    end_frame = float(FBSystem().CurrentTake.LocalTimeSpan.GetStop().GetFrame())
    
    return end_frame - start_frame
    
def calc(dist, frames):
    # Calculate the distance in 30 frames per second
    sec = float(frames/30)
    m = float(dist / 100)
    
    return abs(float(m/sec))
    

# Grab a reference to the Scene
scene = FBSystem().Scene

# Create a list and populate it with the selected objects
models = FBModelList()
FBGetSelectedModels(models)

# Check if any objects are selected
if len(models) == 0:
    FBMessageBox("Model Selection Error:", "No selected models found\n Select a model and try again!", "Ok")
else:
    
    key_list = []
    # Get access to the X,Y,Z translation node keys
    for model in models:
        translationNode = model.Translation.GetAnimationNode()
        if has_keys_check(translationNode):
            for animNode in translationNode.Nodes:
                key_list.append(animNode)

            # Get the chosen move axis direction key list    
            move_axis_keys = find_move_axis(key_list)    
            
            # Get distance and frames and pump out the result    
            dist = get_dist(move_axis_keys)
            frames = get_frames()
            result = calc(dist,frames)
            
            print result
            # Pop up window for the result
            FBMessageBox("Meters per second", ("%.4f" % result), "Ok")
        else:
            FBMessageBox("Keyframe Data Error:", "Selected model has no translation keys!", "Ok")

# Clean up
del(FBSystem, FBModelList, FBGetSelectedModels, FBMessageBox)


