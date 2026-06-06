% Words and lengths
word(code). word(data). word(tech). word(chip). word(byte). word(net).
word_len(code,4). word_len(data,4). word_len(tech,4). word_len(chip,4). word_len(byte,4). word_len(net,3).
% Letters (index starting at 0)
word_letter(code,0,"C"). word_letter(code,1,"O"). word_letter(code,2,"D"). word_letter(code,3,"E").
word_letter(data,0,"D"). word_letter(data,1,"A"). word_letter(data,2,"T"). word_letter(data,3,"A").
word_letter(tech,0,"T"). word_letter(tech,1,"E"). word_letter(tech,2,"C"). word_letter(tech,3,"H").
word_letter(chip,0,"C"). word_letter(chip,1,"H"). word_letter(chip,2,"I"). word_letter(chip,3,"P").
word_letter(byte,0,"B"). word_letter(byte,1,"Y"). word_letter(byte,2,"T"). word_letter(byte,3,"E").
word_letter(net,0,"N"). word_letter(net,1,"E"). word_letter(net,2,"T").
% Grid dimensions
row(0..4). col(0..4).
% Possible start positions for each word and direction
start(W,R,C,horiz) :- word(W), word_len(W,Len), row(R), col(C), C+Len <= 5.
start(W,R,C,vert) :- word(W), word_len(W,Len), row(R), col(C), R+Len <= 5.
% Exactly one placement per word
1 { placed(W,R,C,Dir) : start(W,R,C,Dir) } 1 :- word(W).
% Derive cells occupied by placed words
cell(W,R,C,L) :- placed(W,R0,C0,horiz), word_letter(W,Idx,L), R = R0, C = C0 + Idx, row(R), col(C).
cell(W,R,C,L) :- placed(W,R0,C0,vert), word_letter(W,Idx,L), R = R0 + Idx, C = C0, row(R), col(C).
% Conflict constraint: overlapping cells must have same letter
:- cell(W1,R,C,L1), cell(W2,R,C,L2), W1 != W2, L1 != L2.
% Show placements and resulting grid cells
#show placed/4.
#show cell/3.