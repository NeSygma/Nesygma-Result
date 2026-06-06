% Houses
house(j). house(k). house(l). house(m). house(n). house(o). house(p).

% Slots 1-7
slot(1..7).

% Period definitions
morning(1). morning(2).
afternoon(3). afternoon(4). afternoon(5).
evening(6). evening(7).

% Each house assigned to exactly one slot
1 { assigned(H, S) : slot(S) } 1 :- house(H).

% Each slot has exactly one house
1 { assigned(H, S) : house(H) } 1 :- slot(S).

% Constraint 1: J must be shown in the evening
:- assigned(j, S), not evening(S).

% Constraint 2: K cannot be shown in the morning
:- assigned(k, S), morning(S).

% Constraint 3: L must be after K and before M
% This means: slot(K) < slot(L) < slot(M)
:- assigned(k, Sk), assigned(l, Sl), assigned(m, Sm), Sk >= Sl.
:- assigned(k, Sk), assigned(l, Sl), assigned(m, Sm), Sl >= Sm.

% Constraint 4: P is shown in the afternoon (given condition)
:- assigned(p, S), not afternoon(S).

% Define the options
option_a :- assigned(j, 7).
option_b :- assigned(k, 3).
option_c :- assigned(n, 1).
option_d :- assigned(m, S), afternoon(S).
option_e :- assigned(o, S), morning(S).

% We want to find which option is true in ALL valid assignments
% We'll use a trick: for each option, check if it's false in any assignment
% If an option is false in some assignment, it's not necessarily true

% Define counterexample for each option
counterexample_a :- not option_a.
counterexample_b :- not option_b.
counterexample_c :- not option_c.
counterexample_d :- not option_d.
counterexample_e :- not option_e.

% An option must be true if there's no counterexample
must_be_true_a :- not counterexample_a.
must_be_true_b :- not counterexample_b.
must_be_true_c :- not counterexample_c.
must_be_true_d :- not counterexample_d.
must_be_true_e :- not counterexample_e.

% Output the options that must be true
option(a) :- must_be_true_a.
option(b) :- must_be_true_b.
option(c) :- must_be_true_c.
option(d) :- must_be_true_d.
option(e) :- must_be_true_e.

#show option/1.
#show assigned/2.