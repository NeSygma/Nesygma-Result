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

% Nina condition
:- assigned(nina, monday, _), not assigned(helen, tuesday, _).
:- assigned(nina, monday, _), not assigned(irving, tuesday, _).
:- assigned(nina, tuesday, _), not assigned(helen, wednesday, _).
:- assigned(nina, tuesday, _), not assigned(irving, wednesday, _).

% Given: Helen, Kyle, Lenore give the three morning reports
1 { assigned(helen, D, morning) : day(D) } 1.
1 { assigned(kyle, D, morning) : day(D) } 1.
1 { assigned(lenore, D, morning) : day(D) } 1.

:- assigned(S, _, morning), S != helen, S != kyle, S != lenore.

% Now let's check each option by seeing if it can be false.
% We'll use a "test" approach: for each option, add a constraint that it's false,
% and see if the problem is still satisfiable. If not, it must be true.

% Option A: Helen gives a report on Monday.
% Option B: Irving gives a report on Monday.
% Option C: Irving gives a report on Wednesday.
% Option D: Kyle gives a report on Tuesday.
% Option E: Kyle gives a report on Wednesday.

% Let's just enumerate all models and see what's common.
% We already saw some models. Let's get more.

#show assigned/3.