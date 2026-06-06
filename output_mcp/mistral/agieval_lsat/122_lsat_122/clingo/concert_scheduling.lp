% Base facts
slot(1..6).
band(uneasy; vegemite; wellspring; xpert; yardsign; zircon).

% Each band performs in exactly one slot
1 { performs(B, S) : slot(S) } 1 :- band(B).

% Constraint 1: Vegemite performs in an earlier slot than Zircon
:- performs(vegemite, S1), performs(zircon, S2), S1 >= S2.

% Constraint 2: Wellspring and Zircon each perform in an earlier slot than Xpert
:- performs(wellspring, S1), performs(xpert, S2), S1 >= S2.
:- performs(zircon, S1), performs(xpert, S2), S1 >= S2.

% Constraint 3: Uneasy performs in one of the last three slots
:- performs(uneasy, S), S < 4.

% Constraint 4: Yardsign performs in one of the first three slots
:- performs(yardsign, S), S > 3.

% Define each substitution option as a constraint

% Option A: Only Uneasy can perform in a later slot than Xpert
% This means: no non-uneasy band can be after Xpert
% Since wellspring and zircon are not Uneasy, this implies wellspring < xpert and zircon < xpert
option_a_constraint :-
    not (performs(B, S1), performs(xpert, S2), band(B), B != uneasy, S1 > S2).

% Option B: Vegemite performs in an earlier slot than Wellspring, which performs in an earlier slot than Zircon
option_b_constraint :-
    performs(vegemite, S1), performs(wellspring, S2), S1 < S2,
    performs(wellspring, S2), performs(zircon, S3), S2 < S3.

% Option C: Vegemite and Wellspring each perform in an earlier slot than Xpert
option_c_constraint :-
    performs(vegemite, S1), performs(xpert, S2), S1 < S2,
    performs(wellspring, S3), performs(xpert, S4), S3 < S4.

% Option D: Xpert performs either immediately before or immediately after Uneasy
option_d_constraint :-
    performs(xpert, S1), performs(uneasy, S2), (S1 - S2) = 1.
option_d_constraint :-
    performs(xpert, S1), performs(uneasy, S2), (S2 - S1) = 1.

% Option E: Xpert performs in either slot five or slot six
option_e_constraint :-
    performs(xpert, 5).
option_e_constraint :-
    performs(xpert, 6).

% The correct substitution is the one that is logically equivalent to the original constraint
% We want to find which option, when used as a replacement for the original constraint, still satisfies all other constraints

% Ensure only one option is selected
:- option(X), option(Y), X != Y.

% Map the correct answer to option/1
option(a) :- option_a_constraint.
option(b) :- option_b_constraint.
option(c) :- option_c_constraint.
option(d) :- option_d_constraint.
option(e) :- option_e_constraint.

% Define the choice of options
option(a) :- not option(b), not option(c), not option(d), not option(e).
option(b) :- not option(a), not option(c), not option(d), not option(e).
option(c) :- not option(a), not option(b), not option(d), not option(e).
option(d) :- not option(a), not option(b), not option(c), not option(e).
option(e) :- not option(a), not option(b), not option(c), not option(d).

#show option/1.