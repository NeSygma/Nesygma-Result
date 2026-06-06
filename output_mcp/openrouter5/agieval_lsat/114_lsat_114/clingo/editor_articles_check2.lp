% Define positions 1-7
position(1..7).

% Define articles
article(g; h; j; q; r; s; y).

% Define topics for each article
topic(g, finance). topic(h, finance). topic(j, finance).
topic(q, nutrition). topic(r, nutrition). topic(s, nutrition).
topic(y, wildlife).

% Each position gets exactly one article
1 { assigned(P, A) : article(A) } 1 :- position(P).

% Each article assigned to exactly one position
1 { assigned(P, A) : position(P) } 1 :- article(A).

% Consecutive articles cannot cover the same topic
:- assigned(P, A1), assigned(P+1, A2), topic(A1, T), topic(A2, T), position(P+1).

% S can be earlier than Q only if Q is third.
:- assigned(P_s, s), assigned(P_q, q), P_s < P_q, P_q != 3.

% S must be earlier than Y
:- assigned(P_s, s), assigned(P_y, y), P_s >= P_y.

% J must be earlier than G
:- assigned(P_j, j), assigned(P_g, g), P_j >= P_g.

% G must be earlier than R
:- assigned(P_g, g), assigned(P_r, r), P_g >= P_r.

% Force S at position 1 and see if satisfiable
:- assigned(P, s), P != 1.

#show assigned/2.