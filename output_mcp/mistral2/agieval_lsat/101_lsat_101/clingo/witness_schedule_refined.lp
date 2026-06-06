% Base facts: witnesses and days
witness(franco).
witness(garcia).
witness(hong).
witness(iturbe).
witness(jackson).

day(monday).
day(tuesday).
day(wednesday).

% Each witness testifies on exactly one day
1 { testifies(W, D) : day(D) } 1 :- witness(W).

% Franco does not testify on the same day as Garcia
:- testifies(franco, D), testifies(garcia, D).

% Iturbe testifies on Wednesday
:- not testifies(iturbe, wednesday).

% Exactly two witnesses testify on Tuesday
:- not 2 { testifies(W, tuesday) : witness(W) } 2.

% Hong does not testify on Monday
:- testifies(hong, monday).

% Jackson is the only witness scheduled to testify on Monday
:- testifies(W, monday), W != jackson.
:- not testifies(jackson, monday).

% At least one witness testifies on Monday (already ensured by Jackson being the only witness on Monday)

% Map the correct answer to option/1
% (A) Franco is scheduled to testify on Wednesday.
option(a) :- testifies(franco, wednesday).

% (B) Hong is scheduled to testify on Tuesday.
option(b) :- testifies(hong, tuesday).

% (C) Garcia is scheduled to testify on Tuesday.
option(c) :- testifies(garcia, tuesday).

% (D) Franco is scheduled to testify on the same day as Hong.
option(d) :- testifies(franco, D), testifies(hong, D).

% (E) Garcia is scheduled to testify on the same day as Hong.
option(e) :- testifies(garcia, D), testifies(hong, D).

#show option/1.