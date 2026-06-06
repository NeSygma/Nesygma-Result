% Domain: positions 1 through 8
position(1..8).

% Compositions
comp(f). comp(h). comp(l). comp(o). comp(p). comp(r). comp(s). comp(t).

% Helper positions
first(1). fifth(5). eighth(8).

% Each composition appears exactly once at a position
1 { at(C, P) : comp(C) } 1 :- position(P).
1 { at(C, P) : position(P) } 1 :- comp(C).

% Given: P is third, S is sixth
at(p, 3).
at(s, 6).

% Constraint 1: T is performed either immediately before F OR immediately after R
% This is an OR condition, so we need to allow either case
constraint1_option1 :- at(t, TPos), at(f, FPos), TPos = FPos - 1.
constraint1_option2 :- at(t, TPos), at(r, RPos), TPos = RPos + 1.
:- not constraint1_option1, not constraint1_option2.

% Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
% This means: |pos(F) - pos(R)| >= 3 (at least 2 compositions between them)
constraint2_option1 :- at(f, FPos), at(r, RPos), FPos < RPos, RPos - FPos >= 3.
constraint2_option2 :- at(r, RPos), at(f, FPos), RPos < FPos, FPos - RPos >= 3.
:- not constraint2_option1, not constraint2_option2.

% Constraint 3: O is performed either first or fifth
:- at(o, OPos), OPos != 1, OPos != 5.

% Constraint 4: The eighth composition is either L or H
:- position(8), at(C, 8), C != l, C != h.

% Constraint 5: P is performed before S (already satisfied by given: P=3, S=6)
:- at(p, PPos), at(s, SPos), PPos >= SPos.

% Constraint 6: At least one composition is performed either after O and before S, or after S and before O
% This means: |pos(O) - pos(S)| >= 2 (at least one composition between them)
constraint6_option1 :- at(o, OPos), at(s, SPos), OPos < SPos, SPos - OPos >= 2.
constraint6_option2 :- at(s, SPos), at(o, OPos), SPos < OPos, OPos - SPos >= 2.
:- not constraint6_option1, not constraint6_option2.

% Now, we need to find what must be at position 5
fifth_comp(C) :- at(C, 5).

% Evaluate answer choices
% Choice A: F or H
option(a) :- fifth_comp(f); fifth_comp(h).
% Choice B: F or O  
option(b) :- fifth_comp(f); fifth_comp(o).
% Choice C: F or T
option(c) :- fifth_comp(f); fifth_comp(t).
% Choice D: H or L
option(d) :- fifth_comp(h); fifth_comp(l).
% Choice E: O or R
option(e) :- fifth_comp(o); fifth_comp(r).

#show option/1.
#show at/2.
#show fifth_comp/1.