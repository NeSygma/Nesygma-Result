% Domains
student(george). student(helen). student(irving). student(kyle). student(lenore). student(nina). student(olivia). student(robert).
day(mon). day(tue). day(wed).
period(morning). period(afternoon).

% Next day relation
next_day(mon, tue).
next_day(tue, wed).

% Option A schedule
a_sched(helen, mon, morning).
a_sched(robert, mon, afternoon).
a_sched(olivia, tue, morning).
a_sched(irving, tue, afternoon).
a_sched(lenore, wed, morning).
a_sched(kyle, wed, afternoon).

% Option B schedule
b_sched(irving, mon, morning).
b_sched(olivia, mon, afternoon).
b_sched(helen, tue, morning).
b_sched(kyle, tue, afternoon).
b_sched(nina, wed, morning).
b_sched(lenore, wed, afternoon).

% Option C schedule
c_sched(lenore, mon, morning).
c_sched(helen, mon, afternoon).
c_sched(george, tue, morning).
c_sched(kyle, tue, afternoon).
c_sched(robert, wed, morning).
c_sched(irving, wed, afternoon).

% Option D schedule
d_sched(nina, mon, morning).
d_sched(helen, mon, afternoon).
d_sched(robert, tue, morning).
d_sched(irving, tue, afternoon).
d_sched(olivia, wed, morning).
d_sched(lenore, wed, afternoon).

% Option E schedule
e_sched(olivia, mon, morning).
e_sched(nina, mon, afternoon).
e_sched(irving, tue, morning).
e_sched(helen, tue, afternoon).
e_sched(kyle, wed, morning).
e_sched(george, wed, afternoon).

% Check constraints for each option

% Constraint 1: George only on Tuesday
george_violation(O) :- O = a, a_sched(george, D, P), D != tue.
george_violation(O) :- O = b, b_sched(george, D, P), D != tue.
george_violation(O) :- O = c, c_sched(george, D, P), D != tue.
george_violation(O) :- O = d, d_sched(george, D, P), D != tue.
george_violation(O) :- O = e, e_sched(george, D, P), D != tue.

% Constraint 2: Olivia and Robert not afternoon
olivia_afternoon(O) :- O = a, a_sched(olivia, D, afternoon).
olivia_afternoon(O) :- O = b, b_sched(olivia, D, afternoon).
olivia_afternoon(O) :- O = c, c_sched(olivia, D, afternoon).
olivia_afternoon(O) :- O = d, d_sched(olivia, D, afternoon).
olivia_afternoon(O) :- O = e, e_sched(olivia, D, afternoon).

robert_afternoon(O) :- O = a, a_sched(robert, D, afternoon).
robert_afternoon(O) :- O = b, b_sched(robert, D, afternoon).
robert_afternoon(O) :- O = c, c_sched(robert, D, afternoon).
robert_afternoon(O) :- O = d, d_sched(robert, D, afternoon).
robert_afternoon(O) :- O = e, e_sched(robert, D, afternoon).

% Constraint 3: If Nina on Mon or Tue, Helen and Irving on next day
% For option A: Nina not scheduled, so no violation possible
nina_on_day(O, D) :- O = a, a_sched(nina, D, P).
nina_on_day(O, D) :- O = b, b_sched(nina, D, P).
nina_on_day(O, D) :- O = c, c_sched(nina, D, P).
nina_on_day(O, D) :- O = d, d_sched(nina, D, P).
nina_on_day(O, D) :- O = e, e_sched(nina, D, P).

helen_on_day(O, D) :- O = a, a_sched(helen, D, P).
helen_on_day(O, D) :- O = b, b_sched(helen, D, P).
helen_on_day(O, D) :- O = c, c_sched(helen, D, P).
helen_on_day(O, D) :- O = d, d_sched(helen, D, P).
helen_on_day(O, D) :- O = e, e_sched(helen, D, P).

irving_on_day(O, D) :- O = a, a_sched(irving, D, P).
irving_on_day(O, D) :- O = b, b_sched(irving, D, P).
irving_on_day(O, D) :- O = c, c_sched(irving, D, P).
irving_on_day(O, D) :- O = d, d_sched(irving, D, P).
irving_on_day(O, D) :- O = e, e_sched(irving, D, P).

% Nina on Mon or Tue triggers constraint
nina_triggers(O) :- nina_on_day(O, mon).
nina_triggers(O) :- nina_on_day(O, tue).

% Next day after Nina's day
nina_next(O, D2) :- nina_on_day(O, mon), next_day(mon, D2).
nina_next(O, D2) :- nina_on_day(O, tue), next_day(tue, D2).

% Violation if Nina triggers but Helen or Irving missing on next day
nina_violation(O) :- nina_triggers(O), nina_next(O, D2), not helen_on_day(O, D2).
nina_violation(O) :- nina_triggers(O), nina_next(O, D2), not irving_on_day(O, D2).

% Any violation makes option invalid
any_violation(O) :- george_violation(O).
any_violation(O) :- olivia_afternoon(O).
any_violation(O) :- robert_afternoon(O).
any_violation(O) :- nina_violation(O).

% Valid option if no violations
valid(O) :- O = a, not any_violation(a).
valid(O) :- O = b, not any_violation(b).
valid(O) :- O = c, not any_violation(c).
valid(O) :- O = d, not any_violation(d).
valid(O) :- O = e, not any_violation(e).

% Map to answer options
option(a) :- valid(a).
option(b) :- valid(b).
option(c) :- valid(c).
option(d) :- valid(d).
option(e) :- valid(e).

#show option/1.
#show any_violation/1.
#show george_violation/1.
#show olivia_afternoon/1.
#show robert_afternoon/1.
#show nina_violation/1.
#show nina_triggers/1.
#show nina_next/2.
#show helen_on_day/2.
#show irving_on_day/2.