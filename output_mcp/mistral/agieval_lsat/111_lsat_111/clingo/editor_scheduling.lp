% Define positions
position(1..7).

% Define articles
article(g; h; j; q; r; s; y).

% Define topics
% Finance: G, H, J
% Nutrition: Q, R, S
% Wildlife: Y
topic(g, finance).
topic(h, finance).
topic(j, finance).
topic(q, nutrition).
topic(r, nutrition).
topic(s, nutrition).
topic(y, wildlife).

% Assignment: each position has exactly one article
1 { assigned(A, P) : article(A) } 1 :- position(P).

% Each article appears exactly once
1 { assigned(A, P) : position(P) } 1 :- article(A).

% Consecutive articles cannot cover the same topic
:- assigned(A1, P), assigned(A2, P+1), topic(A1, T), topic(A2, T), P < 7.

% S can be earlier than Q only if Q is third
% This means: if S is before Q, then Q must be at position 3
% Equivalent to: if Q is not at position 3, then S cannot be before Q
:- assigned(s, P1), assigned(q, P2), P1 < P2, P2 != 3.

% S must be earlier than Y
:- assigned(y, P1), assigned(s, P2), P1 < P2.

% J must be earlier than G
:- assigned(j, P1), assigned(g, P2), P1 > P2.

% G must be earlier than R
:- assigned(g, P1), assigned(r, P2), P1 > P2.

% G is fourth (given in the question)
assigned(g, 4).

% Define the multiple choice options
% (A) H is fifth
option(a) :- assigned(h, 5).

% (B) J is first
option(b) :- assigned(j, 1).

% (C) Q is second
option(c) :- assigned(q, 2).

% (D) S is fifth
option(d) :- assigned(s, 5).

% (E) Y is sixth
option(e) :- assigned(y, 6).

#show option/1.