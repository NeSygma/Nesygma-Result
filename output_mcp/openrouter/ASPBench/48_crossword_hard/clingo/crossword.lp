% Domains
row(0..5).
col(0..5).

% Black squares
black(0,0). black(0,5). black(5,0). black(5,5).

% Words
word(cat). word(ace). word(tea). word(ear). word(ate). word(rat). word(car). word(tar).

% Letters of each word (position 0,1,2)
letter(cat,0,"C"). letter(cat,1,"A"). letter(cat,2,"T").
letter(ace,0,"A"). letter(ace,1,"C"). letter(ace,2,"E").
letter(tea,0,"T"). letter(tea,1,"E"). letter(tea,2,"A").
letter(ear,0,"E"). letter(ear,1,"A"). letter(ear,2,"R").
letter(ate,0,"A"). letter(ate,1,"T"). letter(ate,2,"E").
letter(rat,0,"R"). letter(rat,1,"A"). letter(rat,2,"T").
letter(car,0,"C"). letter(car,1,"A"). letter(car,2,"R").
letter(tar,0,"T"). letter(tar,1,"A"). letter(tar,2,"R").

% Possible start positions for each word and direction (respecting bounds)
% Horizontal: need col <= 3
start(W,R,C,h) :- word(W), row(R), col(C), C <= 3,
    not black(R,C), not black(R,C+1), not black(R,C+2).
% Vertical: need row <= 3
start(W,R,C,v) :- word(W), row(R), col(C), R <= 3,
    not black(R,C), not black(R+1,C), not black(R+2,C).

% Choose exactly one placement per word
1 { place(W,R,C,Dir) : start(W,R,C,Dir) } 1 :- word(W).

% Derive occupied cells from placements
% Horizontal placement
occupied(R, C, L) :- place(W,R0,C0,h), letter(W,P,L), R = R0, C = C0 + P.
% Vertical placement
occupied(R, C, L) :- place(W,R0,C0,v), letter(W,P,L), R = R0 + P, C = C0.

% No two different letters in same cell
:- occupied(R,C,L1), occupied(R,C,L2), L1 != L2.

% No occupied black squares (safety)
:- occupied(R,C,_), black(R,C).

% Identify horizontal and vertical occupied cells
hcell(R,C) :- place(W,R0,C0,h), letter(W,P,_), R = R0, C = C0 + P.
vcell(R,C) :- place(W,R0,C0,v), letter(W,P,_), R = R0 + P, C = C0.

% Intersections where both hcell and vcell exist
intersect(R,C) :- hcell(R,C), vcell(R,C).
% Require at least 3 intersections
:- #count { R,C : intersect(R,C) } < 3.

% Connectivity: pick a root occupied cell
1 { root(R,C) : occupied(R,C,_) } 1.

% Adjacent predicate (Manhattan distance 1)
adjacent(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2), R2 = R1+1, C2 = C1.
adjacent(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2), R2 = R1-1, C2 = C1.
adjacent(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2), C2 = C1+1, R2 = R1.
adjacent(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2), C2 = C1-1, R2 = R1.

% Reachability
reachable(R,C) :- root(R,C).
reachable(R2,C2) :- reachable(R1,C1), occupied(R2,C2,_), adjacent(R1,C1,R2,C2).
% All occupied cells must be reachable
:- occupied(R,C,_), not reachable(R,C).

#show place/4.