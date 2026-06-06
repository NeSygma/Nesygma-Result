% Domain
student(george; helen; irving; kyle; lenore; nina; olivia; robert).
day(monday; tuesday; wednesday).
time(morning; afternoon).

% 6 slots
slot(D, T) :- day(D), time(T).

% Each slot gets exactly one student
1 { assigned(S, D, T) : student(S) } 1 :- slot(D, T).

% Each student gives at most one report
:- assigned(S, D1, T1), assigned(S, D2, T2), (D1, T1) != (D2, T2).

% Exactly 6 students give reports
assigned_student(S) :- assigned(S, _, _).
:- not #count { S : assigned_student(S) } = 6.

% George only on Tuesday
:- assigned(george, D, _), D != tuesday.

% Olivia and Robert no afternoon
:- assigned(olivia, _, afternoon).
:- assigned(robert, _, afternoon).

% Nina condition: If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is given on Wednesday.
:- assigned(nina, monday, _), not assigned(helen, tuesday, _).
:- assigned(nina, monday, _), not assigned(irving, tuesday, _).
:- assigned(nina, tuesday, _), not assigned(helen, wednesday, _).
:- assigned(nina, tuesday, _), not assigned(irving, wednesday, _).

% Given: Helen, Kyle, Lenore give the three morning reports
1 { assigned(helen, D, morning) : day(D) } 1.
1 { assigned(kyle, D, morning) : day(D) } 1.
1 { assigned(lenore, D, morning) : day(D) } 1.

:- assigned(S, _, morning), S != helen, S != kyle, S != lenore.

% Now test each option by checking if its negation leads to UNSAT.
% We'll use a "must_be_true" approach.

% Option A: Helen gives a report on Monday.
% Option B: Irving gives a report on Monday.
% Option C: Irving gives a report on Wednesday.
% Option D: Kyle gives a report on Tuesday.
% Option E: Kyle gives a report on Wednesday.

% Let's check each systematically by adding the negation constraint
% and seeing if the result is UNSAT.

% First, let's just get all models to analyze commonalities
#show assigned/3.