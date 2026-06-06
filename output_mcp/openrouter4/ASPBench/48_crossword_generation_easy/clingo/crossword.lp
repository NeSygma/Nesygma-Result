% --- Domain ---
row(0..4). col(0..4).

% --- Word Data ---
word("code"). word("data"). word("tech"). word("chip"). word("byte"). word("net").
word_len("code",4). word_len("data",4). word_len("tech",4). word_len("chip",4). word_len("byte",4). word_len("net",3).

% Letters of each word
letter("code",0,"c"). letter("code",1,"o"). letter("code",2,"d"). letter("code",3,"e").
letter("data",0,"d"). letter("data",1,"a"). letter("data",2,"t"). letter("data",3,"a").
letter("tech",0,"t"). letter("tech",1,"e"). letter("tech",2,"c"). letter("tech",3,"h").
letter("chip",0,"c"). letter("chip",1,"h"). letter("chip",2,"i"). letter("chip",3,"p").
letter("byte",0,"b"). letter("byte",1,"y"). letter("byte",2,"t"). letter("byte",3,"e").
letter("net",0,"n"). letter("net",1,"e"). letter("net",2,"t").

% --- Choice: direction and start position for each word ---
1 { direction(W, "h"); direction(W, "v") } 1 :- word(W).
{ start(W, R, C) : row(R), col(C) } 1 :- word(W).

% --- Bounds Constraints ---
:- start(W, R, C), direction(W, "h"), word_len(W, L), C + L - 1 > 4.
:- start(W, R, C), direction(W, "v"), word_len(W, L), R + L - 1 > 4.

% --- Position index within each word ---
pos(W,P) :- word(W), word_len(W, L), P = 0..L-1.

% --- Derive cell coordinates for each word ---
cell_of(W, R, C, P) :- start(W, R0, C0), direction(W, "h"), pos(W,P), R = R0, C = C0 + P.
cell_of(W, R, C, P) :- start(W, R0, C0), direction(W, "v"), pos(W,P), R = R0 + P, C = C0.

% Occupied cells and letters
occupied(W, R, C) :- cell_of(W, R, C, _).
cell_letter(W, R, C, L) :- cell_of(W, R, C, P), letter(W, P, L).

% --- Conflict Constraints ---
% If two different words occupy the same cell, their letters must match
:- cell_letter(W1, R, C, L1), cell_letter(W2, R, C, L2), W1 < W2, L1 != L2.

% --- Intersection Requirement ---
% At least one intersection (cell with two different words)
intersection(R,C) :- occupied(W1, R, C), occupied(W2, R, C), W1 < W2.
:- not intersection(_, _).

% --- Derive output grid ---
grid(R, C, L) :- cell_letter(W, R, C, L).

% --- Output predicates ---
word_placement(W, R, C, D) :- start(W, R, C), direction(W, D).
intersection_info(R, C, W1, W2) :- cell_letter(W1, R, C, _), cell_letter(W2, R, C, _), W1 < W2.

#show grid/3.
#show word_placement/4.
#show intersection_info/4.