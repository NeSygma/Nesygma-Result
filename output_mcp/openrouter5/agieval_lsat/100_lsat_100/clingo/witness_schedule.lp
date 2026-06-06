%% Problem: Schedule 5 witnesses over 3 days
%% Witnesses: Franco, Garcia, Hong, Iturbe, Jackson
%% Days: Monday, Tuesday, Wednesday

%% Domain facts
witness(franco; garcia; hong; iturbe; jackson).
day(monday; tuesday; wednesday).

%% Each witness testifies on exactly one day
1 { testifies(W, D) : day(D) } 1 :- witness(W).

%% Constraints from problem description

%% 1. Franco does not testify on the same day as Garcia
:- testifies(franco, D), testifies(garcia, D).

%% 2. Iturbe testifies on Wednesday
testifies(iturbe, wednesday).

%% 3. Exactly two witnesses testify on Tuesday
:- #count { W : testifies(W, tuesday) } != 2.

%% 4. Hong does not testify on Monday
:- testifies(hong, monday).

%% 5. At least one witness testifies on Monday
:- #count { W : testifies(W, monday) } < 1.

%% Additional condition: Jackson testifies on Wednesday
testifies(jackson, wednesday).

%% Now evaluate the answer choices

%% (A) Franco is scheduled to testify on Monday.
option(a) :- testifies(franco, monday).

%% (B) Garcia is scheduled to testify on Monday.
option(b) :- testifies(garcia, monday).

%% (C) Exactly one witness is scheduled to testify on Monday.
option(c) :- #count { W : testifies(W, monday) } = 1.

%% (D) Exactly two witnesses are scheduled to testify on Monday.
option(d) :- #count { W : testifies(W, monday) } = 2.

%% (E) Garcia is scheduled to testify on the same day as Hong.
option(e) :- testifies(garcia, D), testifies(hong, D).

#show testifies/2.
#show option/1.