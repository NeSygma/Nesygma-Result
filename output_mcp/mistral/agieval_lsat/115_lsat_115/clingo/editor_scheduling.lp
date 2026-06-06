% Base facts
article(g; h; j; q; r; s; y).
position(1..7).

% Article topics
finance(g; h; j).
nutrition(q; r; s).
wildlife(y).

% Topic assignment
topic(A, finance) :- finance(A).
topic(A, nutrition) :- nutrition(A).
topic(A, wildlife) :- wildlife(A).

% Choice rule: assign each article to a unique position
1 { assigned(A, P) : position(P) } 1 :- article(A).
% Ensure each position has exactly one article
1 { assigned(A, P) : article(A) } 1 :- position(P).

% Derive the sequence: article at each position
seq(P, A) :- assigned(A, P).

% Constraint 1: Consecutive articles cannot cover the same topic
:- seq(P, A1), seq(P+1, A2), topic(A1, T), topic(A2, T), P < 7.

% Constraint 2: S can be earlier than Q only if Q is third
% This means: if S is before Q, then Q must be at position 3
% Equivalently: if Q is not at position 3, then Q must be before S
:- seq(Q_pos, q), Q_pos != 3, seq(S_pos, s), S_pos > Q_pos.

% Constraint 3: S must be earlier than Y
:- seq(S_pos, s), seq(Y_pos, y), S_pos >= Y_pos.

% Constraint 4: J must be earlier than G, and G must be earlier than R
:- seq(J_pos, j), seq(G_pos, g), J_pos >= G_pos.
:- seq(G_pos, g), seq(R_pos, r), G_pos >= R_pos.

% Additional constraints to ensure proper ordering
% From constraint 4: J < G < R
:- seq(J_pos, j), seq(G_pos, g), J_pos >= G_pos.
:- seq(G_pos, g), seq(R_pos, r), G_pos >= R_pos.

% Map the multiple choice options to conditions
% Option A: H is fourth
option(a) :- seq(4, h).

% Option B: H is sixth
option(b) :- seq(6, h).

% Option C: R is fourth
option(c) :- seq(4, r).

% Option D: R is seventh
option(d) :- seq(7, r).

% Option E: Y is fifth
option(e) :- seq(5, y).

% Show the answer
#show option/1.