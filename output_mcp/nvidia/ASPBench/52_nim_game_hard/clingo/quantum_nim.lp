size(0,6). size(1,7). size(2,10). size(3,13).
move(standard, 0, 6, 0, 7, 10, 13).
move(standard, 1, 6, 1, 6, 10, 13).
move(standard, 3, 2, 6, 7, 10, 11).
1 { move(standard, I, K, P1, P2, P3, P4) } 1.
#show move/6
analysis('Optimal moves: remove 6 from pile 0 -> [0,7,10,13]; remove 6 from pile 1 -> [1,6,10,13]; remove 2 from pile 3 -> [6,7,10,11].')
#show analysis/1