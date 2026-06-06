% Base facts: articles and their topics
article(g). article(h). article(j). article(q). article(r). article(s). article(y).

% Topics:
% Finance: g, h, j
% Nutrition: q, r, s
% Wildlife: y

% Topic assignments (facts)
topic(g, finance). topic(h, finance). topic(j, finance).
topic(q, nutrition). topic(r, nutrition). topic(s, nutrition).
topic(y, wildlife).

% Time horizon: 7 steps (1 to 7)
time(1..7).

% Assign each article to a unique time slot
1 { assigned(A, T) : time(T) } 1 :- article(A).
:- time(T), article(A1), article(A2), A1 != A2, assigned(A1, T), assigned(A2, T).

% G is fourth (given condition)
:- not assigned(g, 4).

% Constraints:
% 1. Consecutive articles cannot cover the same topic
:- time(T), time(T+1), assigned(A1, T), assigned(A2, T+1), topic(A1, Topic), topic(A2, Topic).

% 2. S can be earlier than Q only if Q is third
:- assigned(s, T1), assigned(q, T2), T1 < T2, T2 != 3.

% 3. S must be earlier than Y
:- assigned(s, T1), assigned(y, T2), T1 >= T2.

% 4. J must be earlier than G, and G must be earlier than R
:- assigned(j, T1), assigned(g, T2), T1 >= T2.
:- assigned(g, T1), assigned(r, T2), T1 >= T2.

% Additional constraint: G is fourth (already enforced above)

% Define the position of each article for convenience
position(A, T) :- assigned(A, T).

% Map the answer choices to conditions
% (A) H is fifth
option(a) :- position(h, 5).

% (B) J is first
option(b) :- position(j, 1).

% (C) Q is second
option(c) :- position(q, 2).

% (D) S is fifth
option(d) :- position(s, 5).

% (E) Y is sixth
option(e) :- position(y, 6).

#show option/1.