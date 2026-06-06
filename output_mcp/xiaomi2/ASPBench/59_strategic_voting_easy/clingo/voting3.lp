% Voters and candidates
voter(v1). voter(v2). voter(v3). voter(v4).
candidate(a). candidate(b). candidate(c).

% True preferences: prefer(V, C1, C2) means V prefers C1 over C2
prefer(v1, a, b). prefer(v1, a, c). prefer(v1, b, c).
prefer(v2, a, c). prefer(v2, a, b). prefer(v2, c, b).
prefer(v3, b, c). prefer(v3, b, a). prefer(v3, c, a).
prefer(v4, c, b). prefer(v4, c, a). prefer(v4, b, a).

% Current truthful votes
current_vote(v1, a).
current_vote(v2, a).
current_vote(v3, b).
current_vote(v4, c).

% Current winner is A (most votes: A=2, B=1, C=1)
current_winner(a).

% Each voter chooses exactly one new vote
{ new_vote(V, C) : candidate(C) } = 1 :- voter(V).

% A voter is changed if their new vote differs from current
changed(V) :- voter(V), new_vote(V, C), current_vote(V, C2), C != C2.

% Coalition size
coalition_size(N) :- N = #count { V : changed(V) }.

% Compute new vote counts
new_count(C, N) :- candidate(C), N = #count { V : voter(V), new_vote(V, C) }.

% Find maximum vote count
max_count(M) :- M = #max { N : new_count(_, N) }.

% New winner: candidate with the maximum count
new_winner(C) :- new_count(C, N), max_count(M), N = M.

% Constraint: new winner must be different from current winner (A)
:- new_winner(a).

% Constraint: every changed voter must prefer new winner over current winner (A)
:- changed(V), new_winner(W), not prefer(V, W, a).

% Minimize coalition size
#minimize { 1, V : changed(V) }.

% Show results
#show current_winner/1.
#show new_winner/1.
#show changed/1.
#show new_vote/2.
#show coalition_size/1.