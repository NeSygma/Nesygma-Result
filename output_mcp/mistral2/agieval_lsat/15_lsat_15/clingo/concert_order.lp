% Base facts: compositions and their labels
composition(f; h; l; o; p; r; s; t).

% Time steps: 1 to 8 (1=first, 8=eighth)
time(1..8).

% Assign each composition to a unique time step
1 { assigned(C, T) : time(T) } 1 :- composition(C).
:- time(T), 2 { assigned(C, T) : composition(C) }.

% T is performed either immediately before F or immediately after R
:- assigned(t, T), assigned(f, T+1), not assigned(r, T-1).
:- assigned(t, T), assigned(r, T-1), not assigned(f, T+1).

% At least two compositions are performed either after F and before R, or after R and before F
% Case 1: F before R
:- assigned(f, TF), assigned(r, TR), TF < TR, TR - TF =< 2.
% Case 2: R before F
:- assigned(r, TR), assigned(f, TF), TR < TF, TF - TR =< 2.

% O is performed either first or fifth
:- assigned(o, T), T != 1, T != 5.

% The eighth composition performed is either L or H
:- assigned(C, 8), C != l, C != h.

% P is performed at some time before S
:- assigned(s, TS), assigned(p, TP), TS =< TP.

% At least one composition is performed either after O and before S, or after S and before O
% Case 1: O before S
:- assigned(o, TO), assigned(s, TS), TO < TS, TS - TO =< 1.
% Case 2: S before O
:- assigned(s, TS), assigned(o, TO), TS < TO, TO - TS =< 1.

% Additional constraint: If O is performed immediately after T, then F must be performed either fourth or sixth
% This is the condition we are testing for the answer
immediately_after(T, C1, C2) :- assigned(C1, T), assigned(C2, T+1).

% Condition: O is performed immediately after T
condition_holds :- immediately_after(T, t, o).

% If condition_holds, then F must be performed either fourth or sixth
:- condition_holds, assigned(f, TF), TF != 4, TF != 6.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- condition_holds, assigned(f, 1).
option(a) :- condition_holds, assigned(f, 2).

option(b) :- condition_holds, assigned(f, 2).
option(b) :- condition_holds, assigned(f, 3).

option(c) :- condition_holds, assigned(f, 4).
option(c) :- condition_holds, assigned(f, 6).

option(d) :- condition_holds, assigned(f, 4).
option(d) :- condition_holds, assigned(f, 7).

option(e) :- condition_holds, assigned(f, 6).
option(e) :- condition_holds, assigned(f, 7).

#show option/1.