% Domain: Students
student(george; helen; irving; kyle; lenore; nina; olivia; robert).

% Domain: Days
day(monday; tuesday; wednesday).

% Domain: Times
time(morning; afternoon).

% Next day relation
next_day(monday, tuesday).
next_day(tuesday, wednesday).

% Each slot (day, time) gets exactly one student
1 { assigned(S, D, T) : student(S) } 1 :- day(D), time(T).

% Each student gives at most one report
{ assigned(S, D, T) : day(D), time(T) } 1 :- student(S).

% Exactly 6 students give reports
6 { assigned(S, D, T) : student(S), day(D), time(T) } 6.

% George can only give a report on Tuesday
:- assigned(george, D, T), D != tuesday.

% Olivia cannot give an afternoon report
:- assigned(olivia, D, afternoon).

% Robert cannot give an afternoon report
:- assigned(robert, D, afternoon).

% Nina's constraint: if Nina reports on a non-Wednesday day,
% then on the next day both Helen and Irving must give reports
helen_on_day(D) :- assigned(helen, D, _).
irving_on_day(D) :- assigned(irving, D, _).

:- assigned(nina, D, T), D != wednesday, next_day(D, D2), not helen_on_day(D2).
:- assigned(nina, D, T), D != wednesday, next_day(D, D2), not irving_on_day(D2).

% Additional conditions: George, Nina, Robert all give reports
:- not assigned(george, _, _).
:- not assigned(nina, _, _).
:- not assigned(robert, _, _).

% George, Nina, Robert are on different days
:- assigned(george, D, _), assigned(nina, D, _).
:- assigned(george, D, _), assigned(robert, D, _).
:- assigned(nina, D, _), assigned(robert, D, _).

% Check each option
could_a :- assigned(helen, wednesday, _).
could_b :- assigned(nina, monday, _).
could_c :- assigned(nina, tuesday, _).
could_d :- assigned(olivia, monday, _).
could_e :- assigned(robert, wednesday, _).

#show could_a.
#show could_b.
#show could_c.
#show could_d.
#show could_e.