% Domain
student(george; helen; irving; kyle; lenore; nina; olivia; robert).
day(monday; tuesday; wednesday).
time(morning; afternoon).

% Exactly 6 students give reports, 2 per day (1 morning, 1 afternoon)
% So we have 6 slots: (day, time) pairs
slot(D, T) :- day(D), time(T).

% Each slot gets exactly one student
1 { assigned(S, D, T) : student(S) } 1 :- slot(D, T).

% Each student gives at most one report
:- assigned(S, D1, T1), assigned(S, D2, T2), (D1, T1) != (D2, T2).

% Exactly 6 students give reports (so exactly 2 do not)
% Since there are 6 slots and each slot gets one student, and each student at most once,
% we need exactly 6 students assigned.
% Count distinct students assigned
assigned_student(S) :- assigned(S, _, _).
:- not #count { S : assigned_student(S) } = 6.

% Condition: Tuesday is the only day on which George can give a report.
% So George cannot give a report on Monday or Wednesday.
:- assigned(george, D, _), D != tuesday.

% Condition: Neither Olivia nor Robert can give an afternoon report.
:- assigned(olivia, _, afternoon).
:- assigned(robert, _, afternoon).

% Condition: If Nina gives a report, then on the next day Helen and Irving must both give reports,
% unless Nina's report is given on Wednesday.
% "unless Nina's report is given on Wednesday" means the condition only applies if Nina's report is NOT on Wednesday.
% So: If Nina gives a report on Monday, then on Tuesday Helen and Irving both give reports.
% If Nina gives a report on Tuesday, then on Wednesday Helen and Irving both give reports.
% If Nina gives a report on Wednesday, no constraint.

% Nina gives a report on some day
nina_gives :- assigned(nina, _, _).

% If Nina on Monday -> Helen and Irving on Tuesday
:- assigned(nina, monday, _), not assigned(helen, tuesday, _).
:- assigned(nina, monday, _), not assigned(irving, tuesday, _).

% If Nina on Tuesday -> Helen and Irving on Wednesday
:- assigned(nina, tuesday, _), not assigned(helen, wednesday, _).
:- assigned(nina, tuesday, _), not assigned(irving, wednesday, _).

% If Nina on Wednesday, no constraint (the "unless" clause)

% Given condition: Helen, Kyle, and Lenore give the three morning reports.
% So exactly these three students give morning reports, one per day.
1 { assigned(helen, D, morning) : day(D) } 1.
1 { assigned(kyle, D, morning) : day(D) } 1.
1 { assigned(lenore, D, morning) : day(D) } 1.

% No other student gives a morning report
:- assigned(S, _, morning), S != helen, S != kyle, S != lenore.

% Each day has exactly one morning report (already enforced by slot constraint)

% Now we need to determine which of A-E must be true.
% Let's derive what must hold in ALL possible solutions.

% Option A: Helen gives a report on Monday.
% Option B: Irving gives a report on Monday.
% Option C: Irving gives a report on Wednesday.
% Option D: Kyle gives a report on Tuesday.
% Option E: Kyle gives a report on Wednesday.

% We'll use a "must be true" check: an option is true if it holds in ALL answer sets.
% Since we can't directly check all answer sets in one run, we'll use a different approach:
% We'll add constraints to test if each option can be false while still satisfying all conditions.
% If an option CANNOT be false (i.e., forcing it false leads to unsat), then it must be true.

% We'll use a choice to select which option to test, and see which ones are forced.

% Let's just enumerate all possibilities and see what's forced.
% We'll use #show to see the assignments and deduce.

% Let's also add constraints to ensure we get a unique or representative model.

% Show all assignments
#show assigned/3.