student(franz). student(greene). student(hidalgo). student(isaacs).
type(oil). type(watercolor).
wall(1). wall(2). wall(3). wall(4).
position(upper). position(lower).

painting(S,T) :- student(S), type(T).
slot(W,P) :- wall(W), position(P).

% Each painting assigned to exactly one slot
1 { assign(S,T,W,P) : slot(W,P) } 1 :- painting(S,T).

% Each slot gets at most one painting (and exactly one by counting)
:- assign(S1,T1,W,P), assign(S2,T2,W,P), (S1,T1) != (S2,T2).

% Given facts:
assign(isaacs, oil, 4, lower).
assign(greene, watercolor, 3, upper).
% Franz's oil on wall 3, but position unknown. We'll add a constraint that it must be on wall 3.
:- assign(franz, oil, W, _), W != 3.
% Isaacs's watercolor on wall 2, position unknown.
:- assign(isaacs, watercolor, W, _), W != 2.

% Condition 1: No wall has only watercolors.
has_oil(W) :- assign(_, oil, W, _).
:- wall(W), not has_oil(W).

% Condition 2: No wall has the work of only one student.
:- assign(S,_,W,_), assign(S,_,W,_).  % This forbids the same student having two paintings on the same wall.

% Condition 3: No wall has both Franz and Isaacs.
:- assign(franz,_,W,_), assign(isaacs,_,W,_).

% Condition 4: Already enforced by the fact assign(greene, watercolor, 3, upper) and the constraint that Franz's oil is on wall 3.

% Now we add the options:
option(a) :- assign(franz, watercolor, 1, _).
option(b) :- assign(greene, oil, 1, _).
option(c) :- assign(greene, watercolor, 1, _).
option(d) :- assign(hidalgo, oil, 1, _).
option(e) :- assign(hidalgo, watercolor, 1, _).

#show option/1.