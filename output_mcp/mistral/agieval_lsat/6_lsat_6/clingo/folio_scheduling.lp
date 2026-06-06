% Define the domain
student(george). student(helen). student(irving). student(kyle). student(lenore). student(nina). student(olivia). student(robert).
day(monday). day(tuesday). day(wednesday).
time(morning). time(afternoon).

% Olivia and Robert do not give any reports
:- report(olivia, D, T).
:- report(robert, D, T).

% Exactly 6 students give reports (Olivia and Robert do not)
1 { report(S, D, T) : day(D), time(T) } 1 :- student(S), S != olivia, S != robert.

% Exactly 2 reports per day
:- day(D), #count { S, T : report(S, D, T) } != 2.

% Tuesday is the only day George can give a report
:- report(george, D, T), D != tuesday.

% Given condition: Helen, Kyle, and Lenore give the three morning reports
% Define the set of morning reporters
morning_reporter(helen).
morning_reporter(kyle).
morning_reporter(lenore).

% For each day, exactly one of {helen, kyle, lenore} gives a morning report
:- day(D), #count { S : report(S, D, morning), morning_reporter(S) } != 1.

% Each of helen, kyle, lenore must give exactly one report (morning)
1 { report(helen, D, T) : day(D), time(T) } 1.
1 { report(kyle, D, T) : day(D), time(T) } 1.
1 { report(lenore, D, T) : day(D), time(T) } 1.

% If Nina gives a report, then on the next day Helen and Irving must both give reports, unless Nina's report is on Wednesday
:- report(nina, D, T), D != wednesday, not report(helen, ND, _), not report(irving, ND, _), next(D, ND).

% Helper to define next day
next(monday, tuesday).
next(tuesday, wednesday).
next(wednesday, wednesday).

% Map the correct answer to option/1
% Option A: Helen gives a report on Monday
option(a) :- report(helen, monday, morning).

% Option B: Irving gives a report on Monday
option(b) :- report(irving, monday, morning).

% Option C: Irving gives a report on Wednesday
option(c) :- report(irving, wednesday, morning).

% Option D: Kyle gives a report on Tuesday
option(d) :- report(kyle, tuesday, morning).

% Option E: Kyle gives a report on Wednesday
option(e) :- report(kyle, wednesday, morning).

#show option/1.