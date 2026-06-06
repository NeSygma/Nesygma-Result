% Witnesses
witness(f).
witness(g).
witness(h).
witness(i).
witness(j).

% Days
day(monday).
day(tuesday).
day(wednesday).

% Each witness assigned to exactly one day
1 { assigned(W, D) : day(D) } 1 :- witness(W).

% Constraints
% Franco not same day as Garcia
:- assigned(f, D), assigned(g, D).

% Iturbe on Wednesday
assigned(i, wednesday).

% Exactly two witnesses on Tuesday
2 { assigned(W, tuesday) : witness(W) } 2.

% Hong not on Monday
:- assigned(h, monday).

% At least one witness on Monday
1 { assigned(W, monday) : witness(W) } 1.

% Jackson on Wednesday
assigned(j, wednesday).

% Ensure Monday has exactly one witness
:- #count{W : assigned(W, monday)} != 1.

% Option mapping
option(a) :- assigned(f, monday), not assigned(f, monday).
option(b) :- assigned(g, monday), not assigned(g, monday).
option(c) :- #count{W : assigned(W, monday)} = 1.
option(d) :- #count{W : assigned(W, monday)} = 2.
option(e) :- assigned(g, D), assigned(h, D).

% Ensure exactly one option is true
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.