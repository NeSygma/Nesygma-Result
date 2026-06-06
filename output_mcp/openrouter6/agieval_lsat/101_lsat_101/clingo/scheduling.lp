% Witnesses and days
witness(franco).
witness(garcia).
witness(hong).
witness(iturbe).
witness(jackson).

day(monday).
day(tuesday).
day(wednesday).

% Each witness testifies exactly one day
1 { testifies(W, D) : day(D) } 1 :- witness(W).

% Iturbe testifies on Wednesday
testifies(iturbe, wednesday).

% Hong does not testify on Monday
:- testifies(hong, monday).

% Exactly two witnesses testify on Tuesday
2 { testifies(W, tuesday) : witness(W) } 2.

% At least one witness testifies on Monday
1 { testifies(W, monday) : witness(W) }.

% Franco and Garcia not on same day
:- testifies(franco, D), testifies(garcia, D).

% Jackson is the only witness on Monday
testifies(jackson, monday).
:- testifies(W, monday), W != jackson.

% Additional constraint: Hong cannot be on Wednesday (derived from logic)
:- testifies(hong, wednesday).

% Define the answer choices
option(a) :- testifies(franco, wednesday).
option(b) :- testifies(hong, tuesday).
option(c) :- testifies(garcia, tuesday).
option(d) :- testifies(franco, D), testifies(hong, D).
option(e) :- testifies(garcia, D), testifies(hong, D).

#show option/1.