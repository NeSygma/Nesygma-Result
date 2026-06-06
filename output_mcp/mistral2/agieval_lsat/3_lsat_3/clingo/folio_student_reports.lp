% Base facts: students, days, and time slots
student(george). student(helen). student(irving). student(kyle).
student(lenore). student(nina). student(olivia). student(robert).

day(monday). day(tuesday). day(wednesday).
time(morning). time(afternoon).

% Exactly six students give reports
{ gives_report(S) : student(S) } = 6.

% Exactly two reports per day: one morning, one afternoon
{ assigned(S, D, T) : student(S) } = 1 :- day(D), time(T).

% Ensure that if a student gives a report, they are assigned to exactly one day and time
:- gives_report(S), not assigned(S, _, _).
:- assigned(S, D, T), not gives_report(S).

% George can only give a report on Tuesday
:- assigned(george, D, _), D != tuesday.

% Olivia and Robert cannot give afternoon reports
:- assigned(olivia, _, afternoon).
:- assigned(robert, _, afternoon).

% If Nina gives a report, then on the next day Helen and Irving must both give reports,
% unless Nina's report is given on Wednesday.
:- assigned(nina, D, _), gives_report(nina), D != wednesday,
   not (assigned(helen, ND, _) , assigned(irving, ND, _)),
   next_day(D, ND).

% Helper to define the next day
next_day(monday, tuesday).
next_day(tuesday, wednesday).

% Ensure that exactly two reports are given each day (one morning, one afternoon)
:- day(D), time(T), not assigned(_, D, T).

% Ensure that no student is assigned to more than one report
:- student(S), assigned(S, D1, _), assigned(S, D2, _), D1 != D2.
:- student(S), assigned(S, _, T1), assigned(S, _, T2), T1 != T2.

% --- Multiple Choice Logic ---
% We need to find a pair of students who, if they give reports on the same day as each other,
% must give reports on Wednesday.

% Define pairs for each option
pair(george, lenore).
pair(helen, nina).
pair(irving, robert).
pair(kyle, nina).
pair(olivia, kyle).

% Check if a pair is assigned to the same day
same_day(S1, S2, D) :- assigned(S1, D, _), assigned(S2, D, _), pair(S1, S2), S1 < S2.

% For a pair to "must" give reports on Wednesday, the following must hold:
% If the pair is assigned to the same day, that day must be Wednesday.
% We enforce this by ensuring that if a pair is assigned to the same day, it is Wednesday.

% Constraint: If a pair is assigned to the same day, it must be Wednesday
:- same_day(S1, S2, D), D != wednesday.

% Now, we need to determine which option's pair satisfies this condition.
% We will map the correct answer to option/1 based on the derived conditions.

% For each option, we check if the pair must be assigned to Wednesday.
% We do this by ensuring that the pair cannot be assigned to any other day.

% Option A: George and Lenore
option(a) :- pair(george, lenore), same_day(george, lenore, wednesday).

% Option B: Helen and Nina
option(b) :- pair(helen, nina), same_day(helen, nina, wednesday).

% Option C: Irving and Robert
option(c) :- pair(irving, robert), same_day(irving, robert, wednesday).

% Option D: Kyle and Nina
option(d) :- pair(kyle, nina), same_day(kyle, nina, wednesday).

% Option E: Olivia and Kyle
option(e) :- pair(olivia, kyle), same_day(olivia, kyle, wednesday).

#show option/1.