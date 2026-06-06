% Domains
student(george). student(helen). student(irving). student(kyle). student(lenore). student(nina). student(olivia). student(robert).
day(mon). day(tue). day(wed).
period(morning). period(afternoon).

% Next day relation
next_day(mon, tue).
next_day(tue, wed).

% Option schedule identifiers
option_schedule(a).
option_schedule(b).
option_schedule(c).
option_schedule(d).
option_schedule(e).

% Assignments for each option
% Option A
assigned(helen, mon, morning) :- option_schedule(a).
assigned(robert, mon, afternoon) :- option_schedule(a).
assigned(olivia, tue, morning) :- option_schedule(a).
assigned(irving, tue, afternoon) :- option_schedule(a).
assigned(lenore, wed, morning) :- option_schedule(a).
assigned(kyle, wed, afternoon) :- option_schedule(a).

% Option B
assigned(irving, mon, morning) :- option_schedule(b).
assigned(olivia, mon, afternoon) :- option_schedule(b).
assigned(helen, tue, morning) :- option_schedule(b).
assigned(kyle, tue, afternoon) :- option_schedule(b).
assigned(nina, wed, morning) :- option_schedule(b).
assigned(lenore, wed, afternoon) :- option_schedule(b).

% Option C
assigned(lenore, mon, morning) :- option_schedule(c).
assigned(helen, mon, afternoon) :- option_schedule(c).
assigned(george, tue, morning) :- option_schedule(c).
assigned(kyle, tue, afternoon) :- option_schedule(c).
assigned(robert, wed, morning) :- option_schedule(c).
assigned(irving, wed, afternoon) :- option_schedule(c).

% Option D
assigned(nina, mon, morning) :- option_schedule(d).
assigned(helen, mon, afternoon) :- option_schedule(d).
assigned(robert, tue, morning) :- option_schedule(d).
assigned(irving, tue, afternoon) :- option_schedule(d).
assigned(olivia, wed, morning) :- option_schedule(d).
assigned(lenore, wed, afternoon) :- option_schedule(d).

% Option E
assigned(olivia, mon, morning) :- option_schedule(e).
assigned(nina, mon, afternoon) :- option_schedule(e).
assigned(irving, tue, morning) :- option_schedule(e).
assigned(helen, tue, afternoon) :- option_schedule(e).
assigned(kyle, wed, morning) :- option_schedule(e).
assigned(george, wed, afternoon) :- option_schedule(e).

% Helper predicates for constraint 3
assigned_helen_on(O, D) :- assigned(helen, D, P), option_schedule(O).
assigned_irving_on(O, D) :- assigned(irving, D, P), option_schedule(O).

% Constraint 1: George only on Tuesday
constraint_violated(O) :- option_schedule(O), assigned(george, D, P), D != tue.

% Constraint 2: Olivia and Robert not afternoon
constraint_violated(O) :- option_schedule(O), assigned(olivia, D, afternoon).
constraint_violated(O) :- option_schedule(O), assigned(robert, D, afternoon).

% Constraint 3: If Nina on Monday or Tuesday, then Helen and Irving on next day
constraint_violated(O) :- option_schedule(O), assigned(nina, D, P), next_day(D, D2), not assigned_helen_on(O, D2).
constraint_violated(O) :- option_schedule(O), assigned(nina, D, P), next_day(D, D2), not assigned_irving_on(O, D2).

% Additional: No duplicate student assignments (should be satisfied by given options)
constraint_violated(O) :- option_schedule(O), assigned(S, D1, P1), assigned(S, D2, P2), D1 != D2.
constraint_violated(O) :- option_schedule(O), assigned(S, D, P1), assigned(S, D, P2), P1 != P2.

% Valid schedule if no constraints violated
valid_schedule(O) :- option_schedule(O), not constraint_violated(O).

% Map to answer options
option(a) :- valid_schedule(a).
option(b) :- valid_schedule(b).
option(c) :- valid_schedule(c).
option(d) :- valid_schedule(d).
option(e) :- valid_schedule(e).

#show option/1.