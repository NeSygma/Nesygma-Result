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
% If S is before Q, then Q must be third.
% Equivalently: forbid S before Q when Q is not third.
:- assigned(P_s, s), assigned(P_q, q), P_s < P_q, P_q != 3.

% S must be earlier than Y
:- assigned(P_s, s), assigned(P_y, y), P_s >= P_y.

% J must be earlier than G
:- assigned(P_j, j), assigned(P_g, g), P_j >= P_g.

% G must be earlier than R
:- assigned(P_g, g), assigned(P_r, r), P_g >= P_r.

% Determine which positions S can occupy
s_possible(P) :- assigned(P, s).

% The answer is the position among {1,3,4,5,6} that S CANNOT occupy.
% Options: A=first(1), B=third(3), C=fourth(4), D=fifth(5), E=sixth(6)

% We need exactly one option to be true.
% Let's use a different approach: find all models and check.

% Actually, let's just compute which positions are possible for S.
% Since we have multiple models, we need to check across all models.

% Use #show to see all s_possible facts across models
#show s_possible/1.
#show assigned/2.