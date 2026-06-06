% Domain definitions
day(mon; tue; wed).
time(morning; afternoon).
student(george; helen; irving; kyle; lenore; nina; olivia; robert).

% Option A assignments
assign_a(mon, morning, helen).
assign_a(mon, afternoon, robert).
assign_a(tue, morning, olivia).
assign_a(tue, afternoon, irving).
assign_a(wed, morning, lenore).
assign_a(wed, afternoon, kyle).

% Option B assignments
assign_b(mon, morning, irving).
assign_b(mon, afternoon, olivia).
assign_b(tue, morning, helen).
assign_b(tue, afternoon, kyle).
assign_b(wed, morning, nina).
assign_b(wed, afternoon, lenore).

% Option C assignments
assign_c(mon, morning, lenore).
assign_c(mon, afternoon, helen).
assign_c(tue, morning, george).
assign_c(tue, afternoon, kyle).
assign_c(wed, morning, robert).
assign_c(wed, afternoon, irving).

% Option D assignments
assign_d(mon, morning, nina).
assign_d(mon, afternoon, helen).
assign_d(tue, morning, robert).
assign_d(tue, afternoon, irving).
assign_d(wed, morning, olivia).
assign_d(wed, afternoon, lenore).

% Option E assignments
assign_e(mon, morning, olivia).
assign_e(mon, afternoon, nina).
assign_e(tue, morning, irving).
assign_e(tue, afternoon, helen).
assign_e(wed, morning, kyle).
assign_e(wed, afternoon, george).

% Helper predicates for Option A
has_student_a(D, S) :- assign_a(D, _, S).
george_on_wrong_day_a :- assign_a(D, _, george), D != tue.
olivia_afternoon_a :- assign_a(_, afternoon, olivia).
robert_afternoon_a :- assign_a(_, afternoon, robert).
% Nina condition: if Nina on Monday, then Tuesday must have Helen and Irving
nina_monday_a :- assign_a(mon, _, nina).
helen_tuesday_a :- assign_a(tue, _, helen).
irving_tuesday_a :- assign_a(tue, _, irving).
nina_monday_violation_a :- nina_monday_a, not (helen_tuesday_a and irving_tuesday_a).
% Nina condition: if Nina on Tuesday, then Wednesday must have Helen and Irving
nina_tuesday_a :- assign_a(tue, _, nina).
helen_wednesday_a :- assign_a(wed, _, helen).
irving_wednesday_a :- assign_a(wed, _, irving).
nina_tuesday_violation_a :- nina_tuesday_a, not (helen_wednesday_a and irving_wednesday_a).

% Helper predicates for Option B
has_student_b(D, S) :- assign_b(D, _, S).
george_on_wrong_day_b :- assign_b(D, _, george), D != tue.
olivia_afternoon_b :- assign_b(_, afternoon, olivia).
robert_afternoon_b :- assign_b(_, afternoon, robert).
nina_monday_b :- assign_b(mon, _, nina).
helen_tuesday_b :- assign_b(tue, _, helen).
irving_tuesday_b :- assign_b(tue, _, irving).
nina_monday_violation_b :- nina_monday_b, not (helen_tuesday_b and irving_tuesday_b).
nina_tuesday_b :- assign_b(tue, _, nina).
helen_wednesday_b :- assign_b(wed, _, helen).
irving_wednesday_b :- assign_b(wed, _, irving).
nina_tuesday_violation_b :- nina_tuesday_b, not (helen_wednesday_b and irving_wednesday_b).

% Helper predicates for Option C
has_student_c(D, S) :- assign_c(D, _, S).
george_on_wrong_day_c :- assign_c(D, _, george), D != tue.
olivia_afternoon_c :- assign_c(_, afternoon, olivia).
robert_afternoon_c :- assign_c(_, afternoon, robert).
nina_monday_c :- assign_c(mon, _, nina).
helen_tuesday_c :- assign_c(tue, _, helen).
irving_tuesday_c :- assign_c(tue, _, irving).
nina_monday_violation_c :- nina_monday_c, not (helen_tuesday_c and irving_tuesday_c).
nina_tuesday_c :- assign_c(tue, _, nina).
helen_wednesday_c :- assign_c(wed, _, helen).
irving_wednesday_c :- assign_c(wed, _, irving).
nina_tuesday_violation_c :- nina_tuesday_c, not (helen_wednesday_c and irving_wednesday_c).

% Helper predicates for Option D
has_student_d(D, S) :- assign_d(D, _, S).
george_on_wrong_day_d :- assign_d(D, _, george), D != tue.
olivia_afternoon_d :- assign_d(_, afternoon, olivia).
robert_afternoon_d :- assign_d(_, afternoon, robert).
nina_monday_d :- assign_d(mon, _, nina).
helen_tuesday_d :- assign_d(tue, _, helen).
irving_tuesday_d :- assign_d(tue, _, irving).
nina_monday_violation_d :- nina_monday_d, not (helen_tuesday_d and irving_tuesday_d).
nina_tuesday_d :- assign_d(tue, _, nina).
helen_wednesday_d :- assign_d(wed, _, helen).
irving_wednesday_d :- assign_d(wed, _, irving).
nina_tuesday_violation_d :- nina_tuesday_d, not (helen_wednesday_d and irving_wednesday_d).

% Helper predicates for Option E
has_student_e(D, S) :- assign_e(D, _, S).
george_on_wrong_day_e :- assign_e(D, _, george), D != tue.
olivia_afternoon_e :- assign_e(_, afternoon, olivia).
robert_afternoon_e :- assign_e(_, afternoon, robert).
nina_monday_e :- assign_e(mon, _, nina).
helen_tuesday_e :- assign_e(tue, _, helen).
irving_tuesday_e :- assign_e(tue, _, irving).
nina_monday_violation_e :- nina_monday_e, not (helen_tuesday_e and irving_tuesday_e).
nina_tuesday_e :- assign_e(tue, _, nina).
helen_wednesday_e :- assign_e(wed, _, helen).
irving_wednesday_e :- assign_e(wed, _, irving).
nina_tuesday_violation_e :- nina_tuesday_e, not (helen_wednesday_e and irving_wednesday_e).

% Option A validity: exactly six distinct students and no violations
option(a) :-
    #count{S : assign_a(_, _, S)} = 6,
    not george_on_wrong_day_a,
    not olivia_afternoon_a,
    not robert_afternoon_a,
    not nina_monday_violation_a,
    not nina_tuesday_violation_a.

% Option B validity
option(b) :-
    #count{S : assign_b(_, _, S)} = 6,
    not george_on_wrong_day_b,
    not olivia_afternoon_b,
    not robert_afternoon_b,
    not nina_monday_violation_b,
    not nina_tuesday_violation_b.

% Option C validity
option(c) :-
    #count{S : assign_c(_, _, S)} = 6,
    not george_on_wrong_day_c,
    not olivia_afternoon_c,
    not robert_afternoon_c,
    not nina_monday_violation_c,
    not nina_tuesday_violation_c.

% Option D validity
option(d) :-
    #count{S : assign_d(_, _, S)} = 6,
    not george_on_wrong_day_d,
    not olivia_afternoon_d,
    not robert_afternoon_d,
    not nina_monday_violation_d,
    not nina_tuesday_violation_d.

% Option E validity
option(e) :-
    #count{S : assign_e(_, _, S)} = 6,
    not george_on_wrong_day_e,
    not olivia_afternoon_e,
    not robert_afternoon_e,
    not nina_monday_violation_e,
    not nina_tuesday_violation_e.

#show option/1.