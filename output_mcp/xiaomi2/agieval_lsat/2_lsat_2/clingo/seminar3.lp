% Domain: Students
student(george). student(helen). student(irving). student(kyle).
student(lenore). student(nina). student(olivia). student(robert).

% Days and periods
day(monday). day(tuesday). day(wednesday).
period(morning). period(afternoon).

% Slots
slot(D, P) :- day(D), period(P).

% Kyle and Lenore do not give reports (given condition)
% We simply don't allow them to be assigned
:- assigned(kyle, _, _).
:- assigned(lenore, _, _).

% Other students may or may not give reports
{ gives_report(S) } :- student(S), S != kyle, S != lenore.

% Exactly 6 give reports
:- #count{ S : gives_report(S) } != 6.

% Each student who gives a report is assigned to exactly one slot
{ assigned(S, D, P) : slot(D, P) } 1 :- gives_report(S).

% Each slot has exactly one student (from those who give reports)
1 { assigned(S, D, P) : gives_report(S) } 1 :- slot(D, P).

% Constraint 1: George can only give a report on Tuesday
:- assigned(george, D, P), D != tuesday.

% Constraint 2: Olivia and Robert cannot give afternoon reports
:- assigned(olivia, D, afternoon).
:- assigned(robert, D, afternoon).

% Constraint 3: If Nina gives a report, then on the next day Helen and Irving
% must both give reports, unless Nina's report is on Wednesday.
% Nina on Monday -> Helen and Irving on Tuesday
:- assigned(nina, monday, _), not assigned(helen, tuesday, _).
:- assigned(nina, monday, _), not assigned(irving, tuesday, _).

% Nina on Tuesday -> Helen and Irving on Wednesday
:- assigned(nina, tuesday, _), not assigned(helen, wednesday, _).
:- assigned(nina, tuesday, _), not assigned(irving, wednesday, _).

% Nina on Wednesday -> no constraint (waived)

% Now check which answer choice matches
% Morning reports on Monday, Tuesday, Wednesday

% Option A: Helen (Mon-morn), George (Tue-morn), Nina (Wed-morn)
option(a) :- assigned(helen, monday, morning), assigned(george, tuesday, morning), assigned(nina, wednesday, morning).

% Option B: Irving (Mon-morn), Robert (Tue-morn), Helen (Wed-morn)
option(b) :- assigned(irving, monday, morning), assigned(robert, tuesday, morning), assigned(helen, wednesday, morning).

% Option C: Nina (Mon-morn), Helen (Tue-morn), Olivia (Wed-morn)
option(c) :- assigned(nina, monday, morning), assigned(helen, tuesday, morning), assigned(olivia, wednesday, morning).

% Option D: Olivia (Mon-morn), Robert (Tue-morn), Irving (Wed-morn)
option(d) :- assigned(olivia, monday, morning), assigned(robert, tuesday, morning), assigned(irving, wednesday, morning).

% Option E: Robert (Mon-morn), George (Tue-morn), Helen (Wed-morn)
option(e) :- assigned(robert, monday, morning), assigned(george, tuesday, morning), assigned(helen, wednesday, morning).

#show option/1.
#show assigned/3.