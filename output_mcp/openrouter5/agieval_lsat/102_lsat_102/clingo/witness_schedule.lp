% Domain
witness(franco; garcia; hong; iturbe; jackson).
day(monday; tuesday; wednesday).

% Each witness testifies on exactly one day
1 { testifies(W, D) : day(D) } 1 :- witness(W).

% Franco does not testify on the same day as Garcia
:- testifies(franco, D), testifies(garcia, D).

% Iturbe testifies on Wednesday
testifies(iturbe, wednesday).

% Exactly two witnesses testify on Tuesday
:- #count { W : testifies(W, tuesday) } != 2.

% Hong does not testify on Monday
:- testifies(hong, monday).

% At least one witness testifies on Monday
:- #count { W : testifies(W, monday) } < 1.

% Additional condition: Franco is scheduled to testify on the same day as Hong
:- testifies(franco, D1), testifies(hong, D2), D1 != D2.

% Now evaluate each option

% (A) Franco is scheduled to testify on Wednesday.
% This must be true in ALL valid schedules.
% So we check if there exists a valid schedule where Franco is NOT on Wednesday.
% If not, then A must be true.
possible_not_a :- testifies(franco, D), D != wednesday.

% (B) Garcia is scheduled to testify on Monday.
possible_not_b :- testifies(garcia, D), D != monday.

% (C) Garcia is scheduled to testify on Wednesday.
possible_not_c :- testifies(garcia, D), D != wednesday.

% (D) Hong is scheduled to testify on Tuesday.
possible_not_d :- testifies(hong, D), D != tuesday.

% (E) Iturbe is the only witness scheduled to testify on Wednesday.
% Iturbe is on Wednesday. For E to be false, some other witness is also on Wednesday.
possible_not_e :- testifies(W, wednesday), W != iturbe.

% An option is "must be true" if its negation is impossible (unsatisfiable).
% We derive which options are forced.
forced(a) :- not possible_not_a.
forced(b) :- not possible_not_b.
forced(c) :- not possible_not_c.
forced(d) :- not possible_not_d.
forced(e) :- not possible_not_e.

% Map to answer
option(a) :- forced(a).
option(b) :- forced(b).
option(c) :- forced(c).
option(d) :- forced(d).
option(e) :- forced(e).

#show testifies/2.
#show option/1.