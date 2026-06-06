% Students
student(george; helen; irving; kyle; lenore; nina; olivia; robert).

% Days
day(monday; tuesday; wednesday).

% Times
time(morning; afternoon).

% Next day relation
next_day(monday, tuesday).
next_day(tuesday, wednesday).

% Base facts for the given scenario
% Kyle gives the afternoon report on Tuesday
afternoon_report(tuesday, kyle).

% Helen gives the afternoon report on Wednesday
afternoon_report(wednesday, helen).

% Each day has exactly one morning and one afternoon report
1 { report(Day, Time, Student) : student(Student) } 1 :- day(Day), time(Time).

% Exactly 6 distinct students give reports
num_students(N) :- N = #count{ S : report(_, _, S) }.
:- num_students(N), N != 6.

% No student gives more than one report
:- report(Day1, Time1, Student), report(Day2, Time2, Student), (Day1, Time1) != (Day2, Time2).

% Tuesday is the only day George can give a report
:- report(Day, Time, george), Day != tuesday.

% Neither Olivia nor Robert can give afternoon reports
:- report(Day, afternoon, olivia).
:- report(Day, afternoon, robert).

% Nina's report constraint
% If Nina gives a report on day D (not wednesday), then Helen and Irving must both give reports on next_day(D)
nina_reports_on(Day) :- report(Day, _, nina), Day != wednesday.

% If Nina reports on a non-wednesday day, then Helen must report the next day
:- nina_reports_on(Day),
   not report(NextDay, _, helen),
   next_day(Day, NextDay).

% If Nina reports on a non-wednesday day, then Irving must report the next day
:- nina_reports_on(Day),
   not report(NextDay, _, irving),
   next_day(Day, NextDay).

% Helper to extract morning reports for each day
morning_report(Day, Student) :- report(Day, morning, Student).

% Define the answer choices
% A: Irving, Lenore, Nina (monday, tuesday, wednesday morning)
answer_a :- morning_report(monday, irving), morning_report(tuesday, lenore), morning_report(wednesday, nina).

% B: Lenore, George, Irving
answer_b :- morning_report(monday, lenore), morning_report(tuesday, george), morning_report(wednesday, irving).

% C: Nina, Irving, Lenore
answer_c :- morning_report(monday, nina), morning_report(tuesday, irving), morning_report(wednesday, lenore).

% D: Robert, George, Irving
answer_d :- morning_report(monday, robert), morning_report(tuesday, george), morning_report(wednesday, irving).

% E: Robert, Irving, Lenore
answer_e :- morning_report(monday, robert), morning_report(tuesday, irving), morning_report(wednesday, lenore).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- answer_a.
option(b) :- answer_b.
option(c) :- answer_c.
option(d) :- answer_d.
option(e) :- answer_e.

% Sentinel to confirm if any solution exists
solution_exists :- option(_).

#show option/1.
#show solution_exists/0.