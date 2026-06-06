% Voting Scenario Analysis with Strategic Voting Detection
% 4 voters, 3 candidates, Plurality voting

% ===== DOMAIN DEFINITIONS =====
voter(1..4).
candidate("A"; "B"; "C").

% ===== PREFERENCES =====
% V1: A > B > C
prefers(1, "A", "B").
prefers(1, "A", "C").
prefers(1, "B", "C").

% V2: A > C > B
prefers(2, "A", "C").
prefers(2, "A", "B").
prefers(2, "C", "B").

% V3: B > C > A
prefers(3, "B", "C").
prefers(3, "B", "A").
prefers(3, "C", "A").

% V4: C > B > A
prefers(4, "C", "B").
prefers(4, "C", "A").
prefers(4, "B", "A").

% Helper: V prefers C1 over C2
better(V, C1, C2) :- prefers(V, C1, C2).

% ===== CURRENT VOTES (TRUTHFUL) =====
vote(1, "A").
vote(2, "A").
vote(3, "B").
vote(4, "C").

% ===== CURRENT WINNER DETERMINATION =====
% Count votes for each candidate
count_current(C, N) :- candidate(C), N = #count{V : vote(V, C)}.

% Find maximum vote count
max_votes_current(M) :- M = #max{N : count_current(_, N)}.

% Current winner (unique candidate with max votes)
winner_current(C) :- candidate(C), count_current(C, M), max_votes_current(M),
                     #count{C2 : count_current(C2, M)} = 1.

% ===== STRATEGIC VOTING ANALYSIS =====
% Coalition membership (to be determined)
{ coalition(V) } :- voter(V).

% Alternative votes: coalition members can vote for any candidate
% Non-coalition members must keep their truthful vote
alt_vote(V, C) :- vote(V, C), not coalition(V).
alt_vote(V, C) :- coalition(V), candidate(C).

% Count votes based on alternative votes
count_alt(C, N) :- candidate(C), N = #count{V : alt_vote(V, C)}.

% Find maximum vote count in alternative scenario
max_votes_alt(M) :- M = #max{N : count_alt(_, N)}.

% Alternative winner (unique candidate with max votes)
winner_alt(C) :- candidate(C), count_alt(C, M), max_votes_alt(M),
                 #count{C2 : count_alt(C2, M)} = 1.

% ===== BETTER OUTCOME CHECK =====
% For a voter, alternative winner is better than current winner
better_outcome(V) :- coalition(V), winner_current(Current), winner_alt(Alt),
                     better(V, Alt, Current).

% ===== MANIPULATION SUCCESS =====
% Manipulation is successful if at least one coalition member benefits
manipulation_possible :- better_outcome(_).

% ===== MINIMUM COALITION SIZE =====
% Minimize coalition size
#minimize { 1@1, V : coalition(V) }.

% ===== OUTPUT =====
% Show current winner
#show winner_current/1.

% Show alternative winner if manipulation possible
#show winner_alt/1 : manipulation_possible.

% Show coalition members
#show coalition/1.

% Show better outcome for each coalition member
#show better_outcome/1.

% Show minimum coalition size
#show size/1 : N = #count{V : coalition(V)}, manipulation_possible, size(N).

% Show if manipulation is possible
#show manipulation_possible/0.