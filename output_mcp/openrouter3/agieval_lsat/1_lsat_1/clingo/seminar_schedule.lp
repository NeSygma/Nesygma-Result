% Students
student(george). student(helen). student(irving). student(kyle).
student(lenore). student(nina). student(olivia). student(robert).

% Days and times
day(monday). day(tuesday). day(wednesday).
time(morning). time(afternoon).

% Exactly 6 students give reports
1 { gives_report(S) : student(S) } 6 :- true.

% Schedule assignment: exactly one student per slot
1 { schedule(D, T, S) : student(S) } 1 :- day(D), time(T).

% A student can only give a report if they are scheduled
gives_report(S) :- schedule(_, _, S).

% Constraint 1: Tuesday is the only day George can give a report
% George cannot give reports on Monday or Wednesday
:- schedule(monday, _, george).
:- schedule(wednesday, _, george).
% George must give a report on Tuesday (if he gives any)
gives_report(george) :- schedule(tuesday, _, george).

% Constraint 2: Neither Olivia nor Robert can give an afternoon report
:- schedule(_, afternoon, olivia).
:- schedule(_, afternoon, robert).

% Constraint 3: If Nina gives a report, then on the next day Helen and Irving must both give reports,
% unless Nina's report is on Wednesday
% Define next day relationship
next_day(monday, tuesday).
next_day(tuesday, wednesday).

% If Nina gives a report on Monday or Tuesday, then next day both Helen and Irving must give reports
:- schedule(monday, _, nina), not gives_report(helen), not gives_report(irving).
:- schedule(tuesday, _, nina), not gives_report(helen), not gives_report(irving).

% Helper: Check if a student gives a report on a specific day
gives_on_day(S, D) :- schedule(D, _, S).

% For the constraint: if Nina gives on Monday, then Tuesday must have both Helen and Irving
:- gives_on_day(nina, monday), not gives_on_day(helen, tuesday), not gives_on_day(irving, tuesday).
% If Nina gives on Tuesday, then Wednesday must have both Helen and Irving
:- gives_on_day(nina, tuesday), not gives_on_day(helen, wednesday), not gives_on_day(irving, wednesday).

% Define the answer choices as schedules
% Choice A
choice_a_schedule(monday, morning, helen).
choice_a_schedule(monday, afternoon, robert).
choice_a_schedule(tuesday, morning, olivia).
choice_a_schedule(tuesday, afternoon, irving).
choice_a_schedule(wednesday, morning, lenore).
choice_a_schedule(wednesday, afternoon, kyle).

% Choice B
choice_b_schedule(monday, morning, irving).
choice_b_schedule(monday, afternoon, olivia).
choice_b_schedule(tuesday, morning, helen).
choice_b_schedule(tuesday, afternoon, kyle).
choice_b_schedule(wednesday, morning, nina).
choice_b_schedule(wednesday, afternoon, lenore).

% Choice C
choice_c_schedule(monday, morning, lenore).
choice_c_schedule(monday, afternoon, helen).
choice_c_schedule(tuesday, morning, george).
choice_c_schedule(tuesday, afternoon, kyle).
choice_c_schedule(wednesday, morning, robert).
choice_c_schedule(wednesday, afternoon, irving).

% Choice D
choice_d_schedule(monday, morning, nina).
choice_d_schedule(monday, afternoon, helen).
choice_d_schedule(tuesday, morning, robert).
choice_d_schedule(tuesday, afternoon, irving).
choice_d_schedule(wednesday, morning, olivia).
choice_d_schedule(wednesday, afternoon, lenore).

% Choice E
choice_e_schedule(monday, morning, olivia).
choice_e_schedule(monday, afternoon, nina).
choice_e_schedule(tuesday, morning, irving).
choice_e_schedule(tuesday, afternoon, helen).
choice_e_schedule(wednesday, morning, kyle).
choice_e_schedule(wednesday, afternoon, george).

% Helper: Count students in a choice
count_students_a(N) :- N = #count{S : choice_a_schedule(_, _, S)}.
count_students_b(N) :- N = #count{S : choice_b_schedule(_, _, S)}.
count_students_c(N) :- N = #count{S : choice_c_schedule(_, _, S)}.
count_students_d(N) :- N = #count{S : choice_d_schedule(_, _, S)}.
count_students_e(N) :- N = #count{S : choice_e_schedule(_, _, S)}.

% Check each choice against constraints
% Choice A validation
valid_a :- count_students_a(6),
           not choice_a_schedule(monday, _, george),
           not choice_a_schedule(wednesday, _, george),
           choice_a_schedule(tuesday, _, george),
           not choice_a_schedule(_, afternoon, olivia),
           not choice_a_schedule(_, afternoon, robert).

% Additional constraint for Nina in choice A
valid_a :- count_students_a(6),
           not choice_a_schedule(monday, _, george),
           not choice_a_schedule(wednesday, _, george),
           choice_a_schedule(tuesday, _, george),
           not choice_a_schedule(_, afternoon, olivia),
           not choice_a_schedule(_, afternoon, robert),
           choice_a_schedule(monday, _, nina),
           choice_a_schedule(tuesday, morning, helen),
           choice_a_schedule(tuesday, afternoon, irving).

valid_a :- count_students_a(6),
           not choice_a_schedule(monday, _, george),
           not choice_a_schedule(wednesday, _, george),
           choice_a_schedule(tuesday, _, george),
           not choice_a_schedule(_, afternoon, olivia),
           not choice_a_schedule(_, afternoon, robert),
           choice_a_schedule(monday, _, nina),
           choice_a_schedule(tuesday, morning, irving),
           choice_a_schedule(tuesday, afternoon, helen).

valid_a :- count_students_a(6),
           not choice_a_schedule(monday, _, george),
           not choice_a_schedule(wednesday, _, george),
           choice_a_schedule(tuesday, _, george),
           not choice_a_schedule(_, afternoon, olivia),
           not choice_a_schedule(_, afternoon, robert),
           choice_a_schedule(tuesday, _, nina),
           choice_a_schedule(wednesday, morning, helen),
           choice_a_schedule(wednesday, afternoon, irving).

valid_a :- count_students_a(6),
           not choice_a_schedule(monday, _, george),
           not choice_a_schedule(wednesday, _, george),
           choice_a_schedule(tuesday, _, george),
           not choice_a_schedule(_, afternoon, olivia),
           not choice_a_schedule(_, afternoon, robert),
           choice_a_schedule(tuesday, _, nina),
           choice_a_schedule(wednesday, morning, irving),
           choice_a_schedule(wednesday, afternoon, helen).

% Choice B validation
valid_b :- count_students_b(6),
           not choice_b_schedule(monday, _, george),
           not choice_b_schedule(wednesday, _, george),
           choice_b_schedule(tuesday, _, george),
           not choice_b_schedule(_, afternoon, olivia),
           not choice_b_schedule(_, afternoon, robert).

valid_b :- count_students_b(6),
           not choice_b_schedule(monday, _, george),
           not choice_b_schedule(wednesday, _, george),
           choice_b_schedule(tuesday, _, george),
           not choice_b_schedule(_, afternoon, olivia),
           not choice_b_schedule(_, afternoon, robert),
           choice_b_schedule(monday, _, nina),
           choice_b_schedule(tuesday, morning, helen),
           choice_b_schedule(tuesday, afternoon, irving).

valid_b :- count_students_b(6),
           not choice_b_schedule(monday, _, george),
           not choice_b_schedule(wednesday, _, george),
           choice_b_schedule(tuesday, _, george),
           not choice_b_schedule(_, afternoon, olivia),
           not choice_b_schedule(_, afternoon, robert),
           choice_b_schedule(monday, _, nina),
           choice_b_schedule(tuesday, morning, irving),
           choice_b_schedule(tuesday, afternoon, helen).

valid_b :- count_students_b(6),
           not choice_b_schedule(monday, _, george),
           not choice_b_schedule(wednesday, _, george),
           choice_b_schedule(tuesday, _, george),
           not choice_b_schedule(_, afternoon, olivia),
           not choice_b_schedule(_, afternoon, robert),
           choice_b_schedule(tuesday, _, nina),
           choice_b_schedule(wednesday, morning, helen),
           choice_b_schedule(wednesday, afternoon, irving).

valid_b :- count_students_b(6),
           not choice_b_schedule(monday, _, george),
           not choice_b_schedule(wednesday, _, george),
           choice_b_schedule(tuesday, _, george),
           not choice_b_schedule(_, afternoon, olivia),
           not choice_b_schedule(_, afternoon, robert),
           choice_b_schedule(tuesday, _, nina),
           choice_b_schedule(wednesday, morning, irving),
           choice_b_schedule(wednesday, afternoon, helen).

% Choice C validation
valid_c :- count_students_c(6),
           not choice_c_schedule(monday, _, george),
           not choice_c_schedule(wednesday, _, george),
           choice_c_schedule(tuesday, _, george),
           not choice_c_schedule(_, afternoon, olivia),
           not choice_c_schedule(_, afternoon, robert).

valid_c :- count_students_c(6),
           not choice_c_schedule(monday, _, george),
           not choice_c_schedule(wednesday, _, george),
           choice_c_schedule(tuesday, _, george),
           not choice_c_schedule(_, afternoon, olivia),
           not choice_c_schedule(_, afternoon, robert),
           choice_c_schedule(monday, _, nina),
           choice_c_schedule(tuesday, morning, helen),
           choice_c_schedule(tuesday, afternoon, irving).

valid_c :- count_students_c(6),
           not choice_c_schedule(monday, _, george),
           not choice_c_schedule(wednesday, _, george),
           choice_c_schedule(tuesday, _, george),
           not choice_c_schedule(_, afternoon, olivia),
           not choice_c_schedule(_, afternoon, robert),
           choice_c_schedule(monday, _, nina),
           choice_c_schedule(tuesday, morning, irving),
           choice_c_schedule(tuesday, afternoon, helen).

valid_c :- count_students_c(6),
           not choice_c_schedule(monday, _, george),
           not choice_c_schedule(wednesday, _, george),
           choice_c_schedule(tuesday, _, george),
           not choice_c_schedule(_, afternoon, olivia),
           not choice_c_schedule(_, afternoon, robert),
           choice_c_schedule(tuesday, _, nina),
           choice_c_schedule(wednesday, morning, helen),
           choice_c_schedule(wednesday, afternoon, irving).

valid_c :- count_students_c(6),
           not choice_c_schedule(monday, _, george),
           not choice_c_schedule(wednesday, _, george),
           choice_c_schedule(tuesday, _, george),
           not choice_c_schedule(_, afternoon, olivia),
           not choice_c_schedule(_, afternoon, robert),
           choice_c_schedule(tuesday, _, nina),
           choice_c_schedule(wednesday, morning, irving),
           choice_c_schedule(wednesday, afternoon, helen).

% Choice D validation
valid_d :- count_students_d(6),
           not choice_d_schedule(monday, _, george),
           not choice_d_schedule(wednesday, _, george),
           choice_d_schedule(tuesday, _, george),
           not choice_d_schedule(_, afternoon, olivia),
           not choice_d_schedule(_, afternoon, robert).

valid_d :- count_students_d(6),
           not choice_d_schedule(monday, _, george),
           not choice_d_schedule(wednesday, _, george),
           choice_d_schedule(tuesday, _, george),
           not choice_d_schedule(_, afternoon, olivia),
           not choice_d_schedule(_, afternoon, robert),
           choice_d_schedule(monday, _, nina),
           choice_d_schedule(tuesday, morning, helen),
           choice_d_schedule(tuesday, afternoon, irving).

valid_d :- count_students_d(6),
           not choice_d_schedule(monday, _, george),
           not choice_d_schedule(wednesday, _, george),
           choice_d_schedule(tuesday, _, george),
           not choice_d_schedule(_, afternoon, olivia),
           not choice_d_schedule(_, afternoon, robert),
           choice_d_schedule(monday, _, nina),
           choice_d_schedule(tuesday, morning, irving),
           choice_d_schedule(tuesday, afternoon, helen).

valid_d :- count_students_d(6),
           not choice_d_schedule(monday, _, george),
           not choice_d_schedule(wednesday, _, george),
           choice_d_schedule(tuesday, _, george),
           not choice_d_schedule(_, afternoon, olivia),
           not choice_d_schedule(_, afternoon, robert),
           choice_d_schedule(tuesday, _, nina),
           choice_d_schedule(wednesday, morning, helen),
           choice_d_schedule(wednesday, afternoon, irving).

valid_d :- count_students_d(6),
           not choice_d_schedule(monday, _, george),
           not choice_d_schedule(wednesday, _, george),
           choice_d_schedule(tuesday, _, george),
           not choice_d_schedule(_, afternoon, olivia),
           not choice_d_schedule(_, afternoon, robert),
           choice_d_schedule(tuesday, _, nina),
           choice_d_schedule(wednesday, morning, irving),
           choice_d_schedule(wednesday, afternoon, helen).

% Choice E validation
valid_e :- count_students_e(6),
           not choice_e_schedule(monday, _, george),
           not choice_e_schedule(wednesday, _, george),
           choice_e_schedule(tuesday, _, george),
           not choice_e_schedule(_, afternoon, olivia),
           not choice_e_schedule(_, afternoon, robert).

valid_e :- count_students_e(6),
           not choice_e_schedule(monday, _, george),
           not choice_e_schedule(wednesday, _, george),
           choice_e_schedule(tuesday, _, george),
           not choice_e_schedule(_, afternoon, olivia),
           not choice_e_schedule(_, afternoon, robert),
           choice_e_schedule(monday, _, nina),
           choice_e_schedule(tuesday, morning, helen),
           choice_e_schedule(tuesday, afternoon, irving).

valid_e :- count_students_e(6),
           not choice_e_schedule(monday, _, george),
           not choice_e_schedule(wednesday, _, george),
           choice_e_schedule(tuesday, _, george),
           not choice_e_schedule(_, afternoon, olivia),
           not choice_e_schedule(_, afternoon, robert),
           choice_e_schedule(monday, _, nina),
           choice_e_schedule(tuesday, morning, irving),
           choice_e_schedule(tuesday, afternoon, helen).

valid_e :- count_students_e(6),
           not choice_e_schedule(monday, _, george),
           not choice_e_schedule(wednesday, _, george),
           choice_e_schedule(tuesday, _, george),
           not choice_e_schedule(_, afternoon, olivia),
           not choice_e_schedule(_, afternoon, robert),
           choice_e_schedule(tuesday, _, nina),
           choice_e_schedule(wednesday, morning, helen),
           choice_e_schedule(wednesday, afternoon, irving).

valid_e :- count_students_e(6),
           not choice_e_schedule(monday, _, george),
           not choice_e_schedule(wednesday, _, george),
           choice_e_schedule(tuesday, _, george),
           not choice_e_schedule(_, afternoon, olivia),
           not choice_e_schedule(_, afternoon, robert),
           choice_e_schedule(tuesday, _, nina),
           choice_e_schedule(wednesday, morning, irving),
           choice_e_schedule(wednesday, afternoon, helen).

% Map the correct answer to option/1
option(a) :- valid_a.
option(b) :- valid_b.
option(c) :- valid_c.
option(d) :- valid_d.
option(e) :- valid_e.

#show option/1.