size = 15
clean_board = [x[:] for x in [[0]*size]*size]
spiral = []
start = (int(size / 2), int(size / 2))
spiral.append(start)
side_length = 1

while spiral[-1] != (0,0):
    f = 1 if side_length % 2 == 1 else -1
    for i in range(side_length):
        spiral.append((spiral[-1][0]+f, spiral[-1][1]))
    for j in range(side_length):
        spiral.append((spiral[-1][0], spiral[-1][1]+f))
    side_length+=1
for i in range(1, int(size)):
    spiral.append((i, 0))

# reorder the spiral!
modified_spiral = {}
num_processors = 8
for i, action in enumerate(spiral):
    if i % num_processors not in modified_spiral.keys():
        modified_spiral[i % num_processors] = [action]
    else:
        modified_spiral[i % num_processors].append(action)

mod_spiral = []
for key in modified_spiral.keys():
    mod_spiral = mod_spiral + modified_spiral[key]

print mod_spiral[0:27]