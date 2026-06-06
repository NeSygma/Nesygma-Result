%% Domain declarations
voter(v1). voter(v2). voter(v3). voter(v4). voter(v5). voter(v6).
candidate(a). candidate(b). candidate(c). candidate(d).

%% Preference relations (Voter V prefers C1 over C2)
prefers(v1, a, b). prefers(v1, a, c). prefers(v1, a, d).
prefers(v1, b, c). prefers(v1, b, d).
prefers(v1, c, d).

prefers(v2, a, c). prefers(v2, a, b). prefers(v2, a, d).
prefers(v2, c, b). prefers(v2, c, d).
prefers(v2, b, d).

prefers(v3, a, d). prefers(v3, a, b). prefers(v3, a, c).
prefers(v3, d, b). prefers(v3, d, c).
prefers(v3, b, c).

prefers(v4, b, c). prefers(v4, b, d). prefers(v4, b, a).
prefers(v4, c, d). prefers(v4, c, a).
prefers(v4, d, a).

prefers(v5, b, a). prefers(v5, b, d). prefers(v5, b, c).
prefers(v5, a, d). prefers(v5, a, c).
prefers(v5, d, c).

prefers(v6, b, d). prefers(v6, b, a). prefers(v6, b, c).
prefers(v6, d, a). prefers(v6, d, c).
prefers(v6, a, c).

%% Initial votes
initial_vote(v1, a).
initial_vote(v2, b).
initial_vote(v3, b).
initial_vote(v4, b).
initial_vote(v5, a).
initial_vote(v6, a).

%% Dissatisfied voters (prefer B but vote A)
dissatisfied(v5). dissatisfied(v6).

%% Known facts
original_winner(a).
condorcet_winner(b).

%% Choice rule: Select coalition members (subset of dissatisfied voters)
{ coalition_member(V) : dissatisfied(V) }.

%% Strategic voting rules:
%% - Coalition members vote for B (condorcet winner)
%% - Non-coalition members vote according to their initial vote
strategic_vote(V, b) :- coalition_member(V), voter(V).
strategic_vote(V, C) :- not coalition_member(V), initial_vote(V, C), voter(V).

%% Calculate vote counts in manipulated election
vote_count(C, N) :- candidate(C), N = #count{ V : strategic_vote(V, C) }.

%% Constraint: Total votes must be 6
:- vote_count(_, N), N != 6.

%% Constraint: B must be the unique winner (strictly more votes than any other candidate)
:- vote_count(b, Nb), candidate(C), C != b, vote_count(C, Nc), Nb <= Nc.

%% Individual rationality: Each coalition member must prefer B over their initial vote
prefers_b_over_initial(V) :- coalition_member(V), initial_vote(V, C), prefers(V, b, C).
no_member_worse_off :- #count{ V : prefers_b_over_initial(V) } = #count{ V : coalition_member(V) }.

%% Manipulation is successful if B wins the manipulated election
manipulation_successful :-
    vote_count(b, Nb),
    candidate(C), C != b, vote_count(C, Nc),
    Nb > Nc.

%% Coalition size
coalition_size(N) :- N = #count{ V : coalition_member(V) }.

%% Objective: Minimize coalition size
#minimize{ N : coalition_size(N) }.

%% Final answer mapping
coalition_improved :- manipulation_successful, no_member_worse_off.

answer(coalition_size(N), manipulation_successful, coalition_improved) :-
    coalition_size(N),
    manipulation_successful,
    coalition_improved.

#show coalition_size/1.
#show manipulation_successful/0.
#show coalition_improved/0.
#show strategic_vote/2.