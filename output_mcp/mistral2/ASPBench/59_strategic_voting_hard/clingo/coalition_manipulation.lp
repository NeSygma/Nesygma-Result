% --- Facts ---
dissatisfied(v5).
dissatisfied(v6).

% Preferences (first preference)
prefers(v1,a).
prefers(v2,a).
prefers(v3,a).
prefers(v4,b).
prefers(v5,b).
prefers(v6,b).

% Initial votes
initial_vote(v1,a).
initial_vote(v2,b).
initial_vote(v3,b).
initial_vote(v4,b).
initial_vote(v5,a).
initial_vote(v6,a).

% Known facts
condorcet_winner(b).
original_winner(a).

% --- Choice Rule: Coalition members ---
% Coalition members are a subset of dissatisfied voters
{ coalition_member(V) : dissatisfied(V) }.

% --- Strategic votes ---
% Coalition members vote for B; others vote as initially
strategic_vote(V, b) :- coalition_member(V).
strategic_vote(V, C) :- initial_vote(V, C), not coalition_member(V).

% --- Vote counts ---
% Count votes for each candidate
candidate(a). candidate(b). candidate(c). candidate(d).

vote_count(C, N) :- candidate(C), N = #count{ V : strategic_vote(V, C) }.

% --- Manipulation success ---
% B must have strictly more votes than A
manipulation_successful :- vote_count(b, Nb), vote_count(a, Na), Nb > Na.

% --- Individual rationality ---
% No coalition member is worse off: their preferred candidate (B) is elected
no_member_worse_off :- coalition_member(V), prefers(V, b), manipulation_successful.

% --- Coalition size ---
coalition_size(N) :- N = #count{ V : coalition_member(V) }.

% --- Minimize coalition size ---
#minimize{ N : coalition_size(N) }.

% --- Show directives ---
#show coalition_member/1.
#show coalition_size/1.
#show manipulation_successful/0.
#show no_member_worse_off/0.
#show condorcet_winner/1.
#show original_winner/1.