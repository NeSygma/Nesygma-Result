% Domain: positions 1..8
position(1..8).

% Exactly eight compositions
composition(f; h; l; o; p; r; s; t).

% Each composition is performed exactly once, at exactly one position
1 { perf(C, P) : position(P) } 1 :- composition(C).

% Each position has exactly one composition
1 { perf(C, P) : composition(C) } 1 :- position(P).

% --- Constraints from the problem ---

% T is performed either immediately before F or immediately after R.
% immediately before: T at P, F at P+1
% immediately after: R at P, T at P+1
:- not (
    (perf(t, P), perf(f, P+1), position(P), position(P+1))
    ;
    (perf(r, P), perf(t, P+1), position(P), position(P+1))
).

% At least two compositions are performed either after F and before R, or after R and before F.
% Count compositions between X and Y
% Use helper: between(X,Y,P) means P is between positions of X and Y
between(X,Y,P) :- composition(X), composition(Y), perf(X,Px), perf(Y,Py), perf(_,P), Px < P, P < Py.

% At least 2 between F and R (in either order)
:- perf(f, Pf), perf(r, Pr), Pf < Pr, 
   #count { P : between(f,r,P) } < 2.
:- perf(f, Pf), perf(r, Pr), Pr < Pf,
   #count { P : between(r,f,P) } < 2.

% O is performed either first or fifth.
:- not perf(o, 1), not perf(o, 5).

% The eighth composition performed is either L or H.
:- not perf(l, 8), not perf(h, 8).

% P is performed at some time before S.
:- perf(p, Pp), perf(s, Ps), Pp >= Ps.

% At least one composition is performed either after O and before S, or after S and before O.
:- perf(o, Po), perf(s, Ps),
   not (
       (Po < Ps, #count { P : between(o,s,P) } >= 1)
       ;
       (Ps < Po, #count { P : between(s,o,P) } >= 1)
   ).

% --- Additional condition from the question: O is performed immediately after T ---
% immediately after T means T at P, O at P+1
:- not (perf(t, Pt), perf(o, Pt+1), position(Pt), position(Pt+1)).

% --- Now determine what positions F can be in ---
% We need to find all possible positions for F under these constraints.
% Then map to answer choices.

% Possible positions for F
possible_f_pos(P) :- perf(f, P).

% Answer choices:
% (A) first or second
% (B) second or third
% (C) fourth or sixth
% (D) fourth or seventh
% (E) sixth or seventh

% We need to check which answer choice correctly describes F's possible positions.
% Since there should be exactly one correct answer, we derive which option is correct.

% Option A: F is either first or second (i.e., F's position is in {1,2})
option(a) :- possible_f_pos(1), possible_f_pos(2), 
             not possible_f_pos(3), not possible_f_pos(4), not possible_f_pos(5), not possible_f_pos(6), not possible_f_pos(7), not possible_f_pos(8).

% Option B: F is either second or third
option(b) :- possible_f_pos(2), possible_f_pos(3),
             not possible_f_pos(1), not possible_f_pos(4), not possible_f_pos(5), not possible_f_pos(6), not possible_f_pos(7), not possible_f_pos(8).

% Option C: F is either fourth or sixth
option(c) :- possible_f_pos(4), possible_f_pos(6),
             not possible_f_pos(1), not possible_f_pos(2), not possible_f_pos(3), not possible_f_pos(5), not possible_f_pos(7), not possible_f_pos(8).

% Option D: F is either fourth or seventh
option(d) :- possible_f_pos(4), possible_f_pos(7),
             not possible_f_pos(1), not possible_f_pos(2), not possible_f_pos(3), not possible_f_pos(5), not possible_f_pos(6), not possible_f_pos(8).

% Option E: F is either sixth or seventh
option(e) :- possible_f_pos(6), possible_f_pos(7),
             not possible_f_pos(1), not possible_f_pos(2), not possible_f_pos(3), not possible_f_pos(4), not possible_f_pos(5), not possible_f_pos(8).

#show option/1.
#show perf/2.