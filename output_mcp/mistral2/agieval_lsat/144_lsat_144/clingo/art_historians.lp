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

% Assignments: historian H gives lecture on topic T at time S
% We use a choice rule to allow the solver to assign lectures
{ assignment(H, T, S) : art_historian(H), lecture_topic(T), time(S) } = 1 :- art_historian(H), time(S).
{ assignment(H, T, S) : art_historian(H), lecture_topic(T), time(S) } = 1 :- lecture_topic(T), time(S).
{ assignment(H, T, S) : art_historian(H), lecture_topic(T), time(S) } = 1 :- time(S).

% Ensure each historian gives exactly one lecture
1 { assignment(H, T, S) : lecture_topic(T), time(S) } 1 :- art_historian(H).

% Ensure each topic is covered exactly once
1 { assignment(H, T, S) : art_historian(H), time(S) } 1 :- lecture_topic(T).

% Ensure each time slot has exactly one lecture
1 { assignment(H, T, S) : art_historian(H), lecture_topic(T) } 1 :- time(S).

% Constraints from the problem statement

% 1. The oil paintings lecture and the watercolors lecture must both be earlier than the lithographs lecture.
% For every assignment where the topic is oil_paintings or watercolors, its time must be less than the time of the lithographs lecture.
:- assignment(_, oil_paintings, S1), assignment(_, lithographs, S2), S1 >= S2.
:- assignment(_, watercolors, S1), assignment(_, lithographs, S2), S1 >= S2.

% 2. Farley's lecture must be earlier than the oil paintings lecture.
:- assignment(farley, _, S1), assignment(_, oil_paintings, S2), S1 >= S2.

% 3. Holden's lecture must be earlier than both Garcia's lecture and Jiang's lecture.
:- assignment(holden, _, S1), assignment(garcia, _, S2), S1 >= S2.
:- assignment(holden, _, S1), assignment(jiang, _, S2), S1 >= S2.

% Map the answer choices to conditions
% Each option is a specific assignment of historians to topics and times.
% We will check if the assignment in the option satisfies all constraints.

% Option A: Farley: sculptures; Holden: lithographs; Garcia: oil paintings; Jiang: watercolors
% This implies:
%   assignment(farley, sculptures, 1)
%   assignment(holden, lithographs, 2)
%   assignment(garcia, oil_paintings, 3)
%   assignment(jiang, watercolors, 4)
% We need to check if this assignment satisfies all constraints.

% Define the assignments for each option explicitly
% Option A
option(a) :-
    assignment(farley, sculptures, 1),
    assignment(holden, lithographs, 2),
    assignment(garcia, oil_paintings, 3),
    assignment(jiang, watercolors, 4),
    % Additional constraints to ensure no other assignments exist
    not assignment(_, _, 1, farley, sculptures),
    not assignment(_, _, 2, holden, lithographs),
    not assignment(_, _, 3, garcia, oil_paintings),
    not assignment(_, _, 4, jiang, watercolors).

% Option B: Farley: watercolors; Jiang: oil paintings; Holden: sculptures; Garcia: lithographs
option(b) :-
    assignment(farley, watercolors, 1),
    assignment(jiang, oil_paintings, 2),
    assignment(holden, sculptures, 3),
    assignment(garcia, lithographs, 4),
    not assignment(_, _, 1, farley, watercolors),
    not assignment(_, _, 2, jiang, oil_paintings),
    not assignment(_, _, 3, holden, sculptures),
    not assignment(_, _, 4, garcia, lithographs).

% Option C: Garcia: sculptures; Farley: watercolors; Holden: oil paintings; Jiang: lithographs
option(c) :-
    assignment(garcia, sculptures, 1),
    assignment(farley, watercolors, 2),
    assignment(holden, oil_paintings, 3),
    assignment(jiang, lithographs, 4),
    not assignment(_, _, 1, garcia, sculptures),
    not assignment(_, _, 2, farley, watercolors),
    not assignment(_, _, 3, holden, oil_paintings),
    not assignment(_, _, 4, jiang, lithographs).

% Option D: Holden: oil paintings; Jiang: watercolors; Farley: lithographs; Garcia: sculptures
option(d) :-
    assignment(holden, oil_paintings, 1),
    assignment(jiang, watercolors, 2),
    assignment(farley, lithographs, 3),
    assignment(garcia, sculptures, 4),
    not assignment(_, _, 1, holden, oil_paintings),
    not assignment(_, _, 2, jiang, watercolors),
    not assignment(_, _, 3, farley, lithographs),
    not assignment(_, _, 4, garcia, sculptures).

% Option E: Holden: sculptures; Farley: watercolors; Jiang: oil paintings; Garcia: lithographs
option(e) :-
    assignment(holden, sculptures, 1),
    assignment(farley, watercolors, 2),
    assignment(jiang, oil_paintings, 3),
    assignment(garcia, lithographs, 4),
    not assignment(_, _, 1, holden, sculptures),
    not assignment(_, _, 2, farley, watercolors),
    not assignment(_, _, 3, jiang, oil_paintings),
    not assignment(_, _, 4, garcia, lithographs).

% Show the selected option
#show option/1.