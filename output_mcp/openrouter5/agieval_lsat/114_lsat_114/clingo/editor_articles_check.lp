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
:- assigned(P_s, s), assigned(P_q, q), P_s < P_q, P_q != 3.

% S must be earlier than Y
:- assigned(P_s, s), assigned(P_y, y), P_s >= P_y.

% J must be earlier than G
:- assigned(P_j, j), assigned(P_g, g), P_j >= P_g.

% G must be earlier than R
:- assigned(P_g, g), assigned(P_r, r), P_g >= P_r.

% For each position, check if S can be there
% We'll use a choice rule to test each position individually
% and see which ones are possible.

% Let's use a different approach: compute all possible positions for S
% by collecting them across all answer sets.

% First, let's just enumerate all models and see which positions S can take.
% We'll use a trick: for each position P, try to force S at P and see if SAT.

% Actually, let's just check each position systematically.

% Position 1: can S be first?
% We'll test by adding a constraint that S is at position 1 and see if SAT.
% Let's do this in one program by checking each position.

% For each position P, define a scenario where we force S at P
% and check if it's satisfiable.

% We'll use a helper: possible(P) means there exists a valid assignment with S at P.
% We can't directly compute this in one shot, so let's use a different method.

% Let's just compute all possible positions for S by looking at all models.
% We'll use #show to see all s_possible facts.

% Actually, let's just run multiple queries.

% First, let's see all models with S at position 1
% by adding a constraint that forces S at 1.
#show assigned/2.