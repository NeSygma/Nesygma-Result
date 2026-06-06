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

% Tie-breaking order: alphabetical (a > b > c)
tie_break(a, b). tie_break(a, c). tie_break(b, c).

% Each voter chooses exactly one new vote (could be same as current)
{ new_vote(V, C) : candidate(C) } = 1 :- voter(V).

% A voter is considered changed if their new vote differs from current
changed(V) :- voter(V), new_vote(V, C), current_vote(V, C2), C != C2.

% Compute current vote counts - ground C first
current_count(C, N) :- candidate(C), N = #count { V : voter(V), current_vote(V, C) }.

% Find maximum current count
current_max_count(N) :- N = #max { M : current_count(_, M) }.

% Current winner candidates (before tie-breaking)
current_winner_candidate(C) :- current_count(C, N), current_max_count(N).

% Determine if one candidate beats another in tie-breaking
beaten_by(C1, C2) :- current_winner_candidate(C1), current_winner_candidate(C2), 
                     tie_break(C2, C1), C1 != C2.

% Unique current winner after tie-breaking
current_winner(C) :- current_winner_candidate(C), 
                     not beaten_by(C, _) : current_winner_candidate(_).

% Compute new vote counts based on new votes - ground C first
new_count(C, N) :- candidate(C), N = #count { V : voter(V), new_vote(V, C) }.

% Find maximum new count
new_max_count(N) :- N = #max { M : new_count(_, M) }.

% New winner candidates (before tie-breaking)
new_winner_candidate(C) :- new_count(C, N), new_max_count(N).

% Determine if one candidate beats another in tie-breaking for new outcome
beaten_by_new(C1, C2) :- new_winner_candidate(C1), new_winner_candidate(C2),
                         tie_break(C2, C1), C1 != C2.

% Unique new winner after tie-breaking
new_winner(C) :- new_winner_candidate(C),
                 not beaten_by_new(C, _) : new_winner_candidate(_).

% Constraint: Every changed voter must prefer the new winner over the current winner
:- changed(V), current_winner(CW), new_winner(NW), not prefer(V, NW, CW).

% The new winner must differ from the current winner
:- current_winner(CW), new_winner(CW).

% Minimize the number of changed voters
#minimize { 1, V : changed(V) }.

% Show relevant information
#show current_winner/1.
#show new_winner/1.
#show changed/1.
#show new_vote/2.