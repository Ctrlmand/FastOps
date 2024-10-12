# FASTOPS 
Addon for Blender.

---

###### #20241012

### View 3D > Sidebar > FASTOPS
#### * Rename
* __Name__ : Name prefix
* __Suffix__ : Name suffix
* __Start__ : Start number | __Digit__ : Digits long
* __OnlySuffix__ : (When True) { Ignore the __Name prefix__ when renaming }
* __Rename__ : Execute!!!

#### * Find And Replace Name
* __Find__ : String to find
* __Replace__ : String to replace
  
#### * Edit Normal
* __Add__ : Batch add split normal | __Clear__ : Batch claer split normal
* __ClearSharp__ : Batch clear sharp normal
 
#### * Select By Name
* __Select By__ : Select by ... 
---
  
### View 3D > Pie Menu
#### Modifier ( Shortcut: F )
* __Mirror__
  * can select 2 obj
* __Array__ : 
  * can generate a empty object as offset object.
* __Shrinkwrap__
  * can select 2 obj
* __Solidify__ : _Nothing different_
* __Bevel__ : _Nothing different_
* __WeightedNormal__ : _Nothing different_
* __Weld__ :  _Nothing different_
* __ClearAll__ : _As you think~_
* __SelectByModifier__ : When 0 object selected, it will search modifier in view layer, you need choose a modifier to select.When 1 object selected, it will search obj has same modifier in view layer.When more than 1 objects selected, it will search obj has same modifier in selected objects.

#### About Material ( Shortcut: Ctrl F )
* __Flood Empty Material__ : Set empty material slot to default material.
* __Select By Material__ : Select object by active material.
* __Rename By Active Material__ : Find object by active material and rename them by material name.
* __Select By Image Texture__ : Find object and material by image name.
---
### Shader Editor > SideBar > FASTOPS
* __SetColorSpace__ : Quick set common color space.
* __Merge RGB And Alpha__ ： Set active texture node as _Alpha_, another as _RGB_, generate a new texture node. 

### Shader Editor > Pie Menu
* __SetColorSpace__ : Quick set common color space.
* __Geometry Node Tree__ : Convert to geometry node tree.