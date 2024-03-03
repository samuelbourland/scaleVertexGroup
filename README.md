# Scale Vertex Group
Blender Addon for Precision Weighting

This addon is intended to give you more precise control for assigning weights. 
It was written out a desire to quickly and easily have precise control over weights on individual vertices. 
This type of tool was indispensable during my time at Disney and I believe this one could have saved me many hours setting up rigs in Blender.

Like most Blender tools you can right click to cancel the operation. Holding shift will scale the strength allowing for more precision. 
The tool will scale the active vertex group and do it's best to maintain the ratio between the other unlocked vertex groups assigned to the selected vertices. 
I've found the tool ideal for weighting loops and individual vertices.

Upon installation you'll find the tool under Mesh/Weights/Scale Vertex Groups. 
But for the best experience I recommend assigning it to a hotkey.

Warnings: 
The tool cannot scale a vertex group if it is not assigned to the selected vertex. 
Pushing the tool to either extreme can cause weights to weighted to zero in which case the ratio may not be preserved. I recommend right clicking in that scenario unless you prefer the change. 
For deformation groups, the tool was made to work on normalized weights. It will still work, with unnormalized weights but can create confusion when a group cannot be weighted %100. 
The tool does not currently mirror. 

Thanks for checking it out! I sincerely hope it saves you some time.
Any feedback would wonderful. 
I look forward to seeing the characters and stories you'll create!
samuel.bourland@gmail.com
