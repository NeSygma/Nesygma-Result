% Domains and basic facts
art_historian(farley).
art_historian(garcia).
art_historian(holden).
art_historian(jiang).

lecture_topic(lithographs).
lecture_topic(oil_paintings).
lecture_topic(sculptures).
lecture_topic(watercolors).

% Time slots (0 = earliest, 3 = latest)
time(0..3).

% Assign each lecture to a unique historian and topic
1 { assignment(H, T, S) : art_historian(H), lecture_topic(T), time(S) } 1.

% Ensure each historian and topic is assigned exactly once
:- art_historian(H), time(S1), time(S2), S1 != S2, assignment(H, _, S1), assignment(H, _, S2).
:- lecture_topic(T), time(S1), time(S2), S1 != S2, assignment(_, T, S1), assignment(_, T, S2).

% Constraints from the problem statement

% 1. The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
oil_earlier_than_lithographs :- assignment(_, oil_paintings, S1), assignment(_, lithographs, S2), S1 < S2.
watercolors_earlier_than_lithographs :- assignment(_, watercolors, S1), assignment(_, lithographs, S2), S1 < S2.
:- not oil_earlier_than_lithographs.
:- not watercolors_earlier_than_lithographs.

% 2. Farley's lecture must be earlier than the oil paintings lecture.
farley_earlier_than_oil :- assignment(farley, _, S1), assignment(_, oil_paintings, S2), S1 < S2.
:- not farley_earlier_than_oil.

% 3. Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
holden_earlier_than_garcia :- assignment(holden, _, S1), assignment(garcia, _, S2), S1 < S2.
holden_earlier_than_jiang :- assignment(holden, _, S1), assignment(jiang, _, S2), S1 < S2.
:- not holden_earlier_than_garcia.
:- not holden_earlier_than_jiang.

% Derive the order of lectures for each historian and topic
lecture_order(H, T, S) :- assignment(H, T, S).

% Define the relative order of lectures for each option

% Option A: Farley's lecture is earlier than the sculptures lecture.
farley_earlier_than_sculptures :- assignment(farley, _, S1), assignment(_, sculptures, S2), S1 < S2.
option(a) :- farley_earlier_than_sculptures.

% Option B: Holden's lecture is earlier than the lithographs lecture.
holden_earlier_than_lithographs :- assignment(holden, _, S1), assignment(_, lithographs, S2), S1 < S2.
option(b) :- holden_earlier_than_lithographs.

% Option C: The sculptures lecture is earlier than Garcia's lecture.
sculptures_earlier_than_garcia :- assignment(_, sculptures, S1), assignment(garcia, _, S2), S1 < S2.
option(c) :- sculptures_earlier_than_garcia.

% Option D: The sculptures lecture is earlier than Jiang's lecture.
sculptures_earlier_than_jiang :- assignment(_, sculptures, S1), assignment(jiang, _, S2), S1 < S2.
option(d) :- sculptures_earlier_than_jiang.

% Option E: The watercolors lecture is earlier than Garcia's lecture.
watercolors_earlier_than_garcia :- assignment(_, watercolors, S1), assignment(garcia, _, S2), S1 < S2.
option(e) :- watercolors_earlier_than_garcia.

#show option/1.