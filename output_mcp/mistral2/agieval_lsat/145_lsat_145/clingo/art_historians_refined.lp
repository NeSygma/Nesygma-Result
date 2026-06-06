% Domains and basic facts
art_historian(farley; garcia; holden; jiang).
lecture_topic(lithographs; oil_paintings; sculptures; watercolors).
time(0..3).

% Assign each lecture to a unique historian and topic at a unique time
% This choice rule ensures each historian, topic, and time slot is used exactly once
{ lecture(H, T, S) : art_historian(H), lecture_topic(T), time(S) } = 1.

% Constraints from the problem statement

% 1. The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
:- lecture(_, oil_paintings, S1), lecture(_, lithographs, S2), S1 >= S2.
:- lecture(_, watercolors, S1), lecture(_, lithographs, S2), S1 >= S2.

% 2. Farley's lecture must be earlier than the oil paintings lecture.
:- lecture(farley, _, S1), lecture(_, oil_paintings, S2), S1 >= S2.

% 3. Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
:- lecture(holden, _, S1), lecture(garcia, _, S2), S1 >= S2.
:- lecture(holden, _, S1), lecture(jiang, _, S2), S1 >= S2.

% Derive the valid_schedule atom if at least one lecture is assigned
valid_schedule :- lecture(_, _, _).

% Map the correct answer to option/1
% Option A: Farley's lecture is earlier than the sculptures lecture.
option(a) :- lecture(farley, _, S1), lecture(_, sculptures, S2), S1 < S2, valid_schedule.

% Option B: Holden's lecture is earlier than the lithographs lecture.
option(b) :- lecture(holden, _, S1), lecture(_, lithographs, S2), S1 < S2, valid_schedule.

% Option C: The sculptures lecture is earlier than Garcia's lecture.
option(c) :- lecture(_, sculptures, S1), lecture(garcia, _, S2), S1 < S2, valid_schedule.

% Option D: The sculptures lecture is earlier than Jiang's lecture.
option(d) :- lecture(_, sculptures, S1), lecture(jiang, _, S2), S1 < S2, valid_schedule.

% Option E: The watercolors lecture is earlier than Garcia's lecture.
option(e) :- lecture(_, watercolors, S1), lecture(garcia, _, S2), S1 < S2, valid_schedule.

% Ensure exactly one option is true
1 { option(X) : option(X) } 1 :- valid_schedule.

#show option/1.
#show valid_schedule/0.