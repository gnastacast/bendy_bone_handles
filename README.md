# bendy_bone_handles
Blender add-on to add a new bendy bone object with handles. Several these have been made, most don't work with 2.8 any more. This one does. It adds a bendy bone as a new object in the same way you would add an armature. Support coming soon for being able to add handled bendy bones into existing armatures in edit mode. For now just arrange them and join them in as you go. Tested with 2.80 and 2.81.

[Here is an example of how to install an add on](https://www.youtube.com/watch?v=14G_YIVdBd0)

Once installed the tool is available in object mode. Simply click Add -> Armature -> Bendy Bone

It's suggested to create a mesh that will serve to visualize the handles. The default cube does nicely. Once the bendy bone is created, you can manipulate the handles on each end of the bendy bone to change the pose of the bone. You can also scale the handles in the bones X and Y component to make the bendy bone thick or thin and scale in the Y component to change the weight of that handle on the curve.

One issue you may encounter is that when you press "Apply pose" your bone goes crazy. This is because you have to reset the "Stretch to" constraint on the bendy bone.

New Media Supply has kindly made a [youtube tutorial](https://www.youtube.com/watch?v=iwzNSpx1umw&t=73s) showing off some of the addon's capabilities
