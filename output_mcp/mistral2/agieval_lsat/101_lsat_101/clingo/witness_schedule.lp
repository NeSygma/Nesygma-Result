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

% Each day has at least one witness (Monday already has Jackson, so this is partially redundant but ensures correctness)
:- day(D), not 1 { testifies(W, D) : witness(W) } 1.

% Constraints from the problem statement
% Franco does not testify on the same day as Garcia
:- testifies(franco, D), testifies(garcia, D).

% Iturbe testifies on Wednesday
:- not testifies(iturbe, wednesday).

% Exactly two witnesses testify on Tuesday
:- not 2 { testifies(W, tuesday) : witness(W) } 2.

% Hong does not testify on Monday
:- testifies(hong, monday).

% At least one witness testifies on Monday (already ensured by Jackson being the only witness on Monday)

% Additional constraint: Jackson is the only witness scheduled to testify on Monday
:- testifies(W, monday), W != jackson.

% Ensure Jackson testifies on Monday (since he is the only one on Monday)
:- not testifies(jackson, monday).

% Helper to determine the schedule for each day
% Monday: Jackson only
schedule(monday, jackson).

% Tuesday: Exactly two witnesses
schedule(tuesday, W1) :- testifies(W1, tuesday), testifies(W2, tuesday), W1 != W2.

% Wednesday: Iturbe only (since Iturbe must testify on Wednesday and no other constraints)
schedule(wednesday, iturbe).

% Map the correct answer to option/1
% (A) Franco is scheduled to testify on Wednesday.
option(a) :- testifies(franco, wednesday).

% (B) Hong is scheduled to testify on Tuesday.
option(b) :- testifies(hong, tuesday).

% (C) Garcia is scheduled to testify on Tuesday.
option(c) :- testifies(garcia, tuesday).

% (D) Franco is scheduled to testify on the same day as Hong.
option(d) :- testifies(franco, D), testifies(hong, D), D != monday.

% (E) Garcia is scheduled to testify on the same day as Hong.
option(e) :- testifies(garcia, D), testifies(hong, D), D != monday.

#show option/1.