from collections import defaultdict
# int       = 0
# float     = 1
# string    = 2
# bool      = 3
# +         = 0
# -         = 1
# *         = 2
# /         = 3
# %         = 4


semanticCube = {}
semanticCube = defaultdict(lambda: -1, semanticCube)

# int _ int = _
# float _ float = _
# int _ float = _
# float _ int = _
for i in range(0,3):
    semanticCube[0,i,0] = 0
    semanticCube[1,i,1] = 1
    semanticCube[0,i,1] = 1
    semanticCube[1,i,0] = 1

# % is always integer
semanticCube[0,4,0] = 0
semanticCube[1,4,1] = 0
semanticCube[0,4,1] = 0
semanticCube[1,4,0] = 0

# "string1" + "string2" = "string1string2"
semanticCube[2,0,2] = 2