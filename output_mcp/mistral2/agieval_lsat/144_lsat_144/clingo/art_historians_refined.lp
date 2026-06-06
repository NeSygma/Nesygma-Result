% Domains and facts
% Art historians
art_historian(farley).
art_historian(garcia).
art_historian(holden).
art_historian(jiang).

% Lecture topics
lecture_topic(lithographs).
lecture_topic(oil_paintings).
lecture_topic(sculptures).
lecture_topic(watercolors).

% Time slots (lectures are ordered from first to fourth)
time(1..4).

% Assignments for each option (facts)
% Option A: Farley: sculptures (1); Holden: lithographs (2); Garcia: oil paintings (3); Jiang: watercolors (4)
assignment(farley, sculptures, 1, a).
assignment(holden, lithographs, 2, a).
assignment(garcia, oil_paintings, 3, a).
assignment(jiang, watercolors, 4, a).

% Option B: Farley: watercolors (1); Jiang: oil paintings (2); Holden: sculptures (3); Garcia: lithographs (4)
assignment(farley, watercolors, 1, b).
assignment(jiang, oil_paintings, 2, b).
assignment(holden, sculptures, 3, b).
assignment(garcia, lithographs, 4, b).

% Option C: Garcia: sculptures (1); Farley: watercolors (2); Holden: oil paintings (3); Jiang: lithographs (4)
assignment(garcia, sculptures, 1, c).
assignment(farley, watercolors, 2, c).
assignment(holden, oil_paintings, 3, c).
assignment(jiang, lithographs, 4, c).

% Option D: Holden: oil paintings (1); Jiang: watercolors (2); Farley: lithographs (3); Garcia: sculptures (4)
assignment(holden, oil_paintings, 1, d).
assignment(jiang, watercolors, 2, d).
assignment(farley, lithographs, 3, d).
assignment(garcia, sculptures, 4, d).

% Option E: Holden: sculptures (1); Farley: watercolors (2); Jiang: oil paintings (3); Garcia: lithographs (4)
assignment(holden, sculptures, 1, e).
assignment(farley, watercolors, 2, e).
assignment(jiang, oil_paintings, 3, e).
assignment(garcia, lithographs, 4, e).

% Constraints from the problem statement

% 1. The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
valid(a) :-
    assignment(_, oil_paintings, S1, a),
    assignment(_, lithographs, S2, a),
    S1 < S2,
    assignment(_, watercolors, S3, a),
    S3 < S2.
valid(b) :-
    assignment(_, oil_paintings, S1, b),
    assignment(_, lithographs, S2, b),
    S1 < S2,
    assignment(_, watercolors, S3, b),
    S3 < S2.
valid(c) :-
    assignment(_, oil_paintings, S1, c),
    assignment(_, lithographs, S2, c),
    S1 < S2,
    assignment(_, watercolors, S3, c),
    S3 < S2.
valid(d) :-
    assignment(_, oil_paintings, S1, d),
    assignment(_, lithographs, S2, d),
    S1 < S2,
    assignment(_, watercolors, S3, d),
    S3 < S2.
valid(e) :-
    assignment(_, oil_paintings, S1, e),
    assignment(_, lithographs, S2, e),
    S1 < S2,
    assignment(_, watercolors, S3, e),
    S3 < S2.

% 2. Farley's lecture must be earlier than the oil paintings lecture.
valid(a) :-
    assignment(farley, _, S1, a),
    assignment(_, oil_paintings, S2, a),
    S1 < S2.
valid(b) :-
    assignment(farley, _, S1, b),
    assignment(_, oil_paintings, S2, b),
    S1 < S2.
valid(c) :-
    assignment(farley, _, S1, c),
    assignment(_, oil_paintings, S2, c),
    S1 < S2.
valid(d) :-
    assignment(farley, _, S1, d),
    assignment(_, oil_paintings, S2, d),
    S1 < S2.
valid(e) :-
    assignment(farley, _, S1, e),
    assignment(_, oil_paintings, S2, e),
    S1 < S2.

% 3. Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
valid(a) :-
    assignment(holden, _, S1, a),
    assignment(garcia, _, S2, a),
    S1 < S2,
    assignment(jiang, _, S3, a),
    S1 < S3.
valid(b) :-
    assignment(holden, _, S1, b),
    assignment(garcia, _, S2, b),
    S1 < S2,
    assignment(jiang, _, S3, b),
    S1 < S3.
valid(c) :-
    assignment(holden, _, S1, c),
    assignment(garcia, _, S2, c),
    S1 < S2,
    assignment(jiang, _, S3, c),
    S1 < S3.
valid(d) :-
    assignment(holden, _, S1, d),
    assignment(garcia, _, S2, d),
    S1 < S2,
    assignment(jiang, _, S3, d),
    S1 < S3.
valid(e) :-
    assignment(holden, _, S1, e),
    assignment(garcia, _, S2, e),
    S1 < S2,
    assignment(jiang, _, S3, e),
    S1 < S3.

% Only the valid option is the correct answer
option(a) :- valid(a), not valid(b), not valid(c), not valid(d), not valid(e).
option(b) :- valid(b), not valid(a), not valid(c), not valid(d), not valid(e).
option(c) :- valid(c), not valid(a), not valid(b), not valid(d), not valid(e).
option(d) :- valid(d), not valid(a), not valid(b), not valid(c), not valid(e).
option(e) :- valid(e), not valid(a), not valid(b), not valid(c), not valid(d).

% Show the selected option
#show option/1.