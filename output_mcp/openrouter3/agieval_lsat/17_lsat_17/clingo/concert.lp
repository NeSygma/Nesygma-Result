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

% Constraint 1: T is performed either immediately before F or immediately after R
% T before F: position(T) = position(F) - 1
% T after R: position(T) = position(R) + 1
:- at(t, TPos), at(f, FPos), TPos != FPos - 1, TPos != FPos + 1.
:- at(t, TPos), at(r, RPos), TPos != RPos + 1, TPos != RPos - 1.

% Actually, let me rephrase constraint 1 more precisely:
% T is performed either immediately before F OR immediately after R
% This means: (T at pos X, F at pos X+1) OR (R at pos X, T at pos X+1)
% So we need to check both possibilities
constraint1_holds :- at(t, TPos), at(f, FPos), TPos = FPos - 1.
constraint1_holds :- at(t, TPos), at(r, RPos), TPos = RPos + 1.
:- not constraint1_holds.

% Constraint 2: At least two compositions are performed either after F and before R, or after R and before F
% This means: |pos(F) - pos(R)| >= 3 (since at least 2 compositions between them)
% Actually: if F before R, then at least 2 compositions between F and R
% if R before F, then at least 2 compositions between R and F
constraint2_holds :- at(f, FPos), at(r, RPos), FPos < RPos, RPos - FPos >= 3.
constraint2_holds :- at(r, RPos), at(f, FPos), RPos < FPos, FPos - RPos >= 3.
:- not constraint2_holds.

% Constraint 3: O is performed either first or fifth
:- at(o, OPos), OPos != 1, OPos != 5.

% Constraint 4: The eighth composition is either L or H
:- at(l, LPos), LPos != 8.
:- at(h, HPos), HPos != 8.
% Actually: eighth position must be L or H
:- position(8), at(C, 8), C != l, C != h.

% Constraint 5: P is performed before S (already given: P=3, S=6, so this holds automatically)
% But let's keep it general
:- at(p, PPos), at(s, SPos), PPos >= SPos.

% Constraint 6: At least one composition is performed either after O and before S, or after S and before O
% This means: |pos(O) - pos(S)| >= 2 (at least one composition between them)
constraint6_holds :- at(o, OPos), at(s, SPos), OPos < SPos, SPos - OPos >= 2.
constraint6_holds :- at(s, SPos), at(o, OPos), SPos < OPos, OPos - SPos >= 2.
:- not constraint6_holds.

% Now, we need to find what must be at position 5
% Let's define what composition is at position 5
fifth_comp(C) :- at(C, 5).

% Now evaluate the answer choices
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