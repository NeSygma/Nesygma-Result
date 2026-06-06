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
1 { testifies_on(W, D) : day(D) } 1 :- witness(W).

% Each day has at least one witness (Monday constraint)
:- day(D), D = monday, not witness_on_day(D).
witness_on_day(D) :- testifies_on(_, D).

% Exactly two witnesses testify on Tuesday
:- { testifies_on(W, tuesday) } != 2.

% Iturbe testifies on Wednesday
:- testifies_on(iturbe, D), D != wednesday.

% Franco does not testify on the same day as Garcia
:- testifies_on(franco, D), testifies_on(garcia, D).

% Hong does not testify on Monday
:- testifies_on(hong, monday).

% Additional constraint: Jackson is scheduled to testify on Wednesday
:- testifies_on(jackson, D), D != wednesday.

% Helper predicates for answer mapping
franco_on_monday :- testifies_on(franco, monday).
garcia_on_monday :- testifies_on(garcia, monday).
hong_on_monday :- testifies_on(hong, monday).

% Count witnesses on Monday
witness_count_monday(N) :- N = #count { W : testifies_on(W, monday) }.

% Define answer options based on the constraints
% (A) Franco is scheduled to testify on Monday.
option(a) :- franco_on_monday.

% (B) Garcia is scheduled to testify on Monday.
option(b) :- garcia_on_monday.

% (C) Exactly one witness is scheduled to testify on Monday.
option(c) :- witness_count_monday(1).

% (D) Exactly two witnesses are scheduled to testify on Monday.
option(d) :- witness_count_monday(2).

% (E) Garcia is scheduled to testify on the same day as Hong.
% This is not necessarily true, so we do not derive option(e).
% option(e) :- testifies_on(garcia, D), testifies_on(hong, D).

#show option/1.