% Coalition Manipulation in Plurality Election
% Voters: 1..6, Candidates: A, B, C, D

% Domains
voter(1..6).
candidate("A"; "B"; "C"; "D").
rank_value("A",1). rank_value("B",2). rank_value("C",3). rank_value("D",4).

% Original votes
original_vote(1, "A").
original_vote(2, "B").
original_vote(3, "B").
original_vote(4, "B").
original_vote(5, "A").
original_vote(6, "A").

% Dissatisfied voters (prefer B but currently vote A)
dissatisfied(5).
dissatisfied(6).

% Preferences (strict ordering)
% V1: A > B > C > D
prefers(1, "A", "B"). prefers(1, "A", "C"). prefers(1, "A", "D").
prefers(1, "B", "C"). prefers(1, "B", "D").
prefers(1, "C", "D").
% V2: A > C > B > D
prefers(2, "A", "C"). prefers(2, "A", "B"). prefers(2, "A", "D").
prefers(2, "C", "B"). prefers(2, "C", "D").
prefers(2, "B", "D").
% V3: A > D > B > C
prefers(3, "A", "D"). prefers(3, "A", "B"). prefers(3, "A", "C").
prefers(3, "D", "B"). prefers(3, "D", "C").
prefers(3, "B", "C").
% V4: B > C > D > A
prefers(4, "B", "C"). prefers(4, "B", "D"). prefers(4, "B", "A").
prefers(4, "C", "D"). prefers(4, "C", "A").
prefers(4, "D", "A").
% V5: B > A > D > C
prefers(5, "B", "A"). prefers(5, "B", "D"). prefers(5, "B", "C").
prefers(5, "A", "D"). prefers(5, "A", "C").
prefers(5, "D", "C").
% V6: B > D > A > C
prefers(6, "B", "D"). prefers(6, "B", "A"). prefers(6, "B", "C").
prefers(6, "D", "A"). prefers(6, "D", "C").
prefers(6, "A", "C").

% Coalition formation: choose a subset of dissatisfied voters
{coalition_member(V) : dissatisfied(V)}.

% Strategic vote: coalition members vote for B (Condorcet winner)
strategic_vote(V, "B") :- coalition_member(V).

% Actual votes in manipulated election
actual_vote(V, C) :- original_vote(V, C), not coalition_member(V).
actual_vote(V, C) :- coalition_member(V), strategic_vote(V, C).

% Vote counts
vote_count(C, N) :- candidate(C), N = #count{V : actual_vote(V, C)}.
original_vote_count(C, N) :- candidate(C), N = #count{V : original_vote(V, C)}.

% Original winner (plurality with alphabetical tie-break)
max_original_count(Max) :- Max = #max{N : original_vote_count(_, N)}.
% Helper: candidate with max count and smallest rank
is_original_winner(C) :- candidate(C), original_vote_count(C, Max), max_original_count(Max),
    not (candidate(D), original_vote_count(D, Max), rank_value(D, RD), rank_value(C, RC), RD < RC).
original_winner(C) :- is_original_winner(C).

% Manipulated winner
max_manipulated_count(Max) :- Max = #max{N : vote_count(_, N)}.
is_manipulated_winner(C) :- candidate(C), vote_count(C, Max), max_manipulated_count(Max),
    not (candidate(D), vote_count(D, Max), rank_value(D, RD), rank_value(C, RC), RD < RC).
manipulated_winner(C) :- is_manipulated_winner(C).

% Condorcet winner computation
beats(X, Y) :- candidate(X), candidate(Y), X != Y,
    N1 = #count{V : prefers(V, X, Y)},
    N2 = #count{V : prefers(V, Y, X)},
    N1 > N2.
condorcet_winner(C) :- candidate(C), not (candidate(D), D != C, not beats(C, D)).

% Individual rationality: no coalition member is worse off
not_worse_off(V) :- coalition_member(V), manipulated_winner(New), original_winner(Old),
    (prefers(V, New, Old) or New == Old).

% Coalition improved (all members not worse off)
coalition_improved :- not (coalition_member(V), not not_worse_off(V)).
no_member_worse_off :- coalition_improved.

% Condorcet winner elected
condorcet_winner_elected :- manipulated_winner("B").

% Manipulation successful (winner changed)
manipulation_successful :- original_winner(A), manipulated_winner(B), A != B.

% Minimize coalition size
#minimize {1, V : coalition_member(V)}.

% Output predicates
coalition_size(N) :- N = #count{V : coalition_member(V)}.
manipulation_type("strategic").

% Show directives
#show coalition_member/1.
#show coalition_size/1.
#show manipulation_type/1.
#show strategic_votes/2.
#show original_winner/1.
#show original_vote_count/2.
#show manipulated_winner/1.
#show manipulated_vote_count/2.
#show manipulation_successful/0.
#show coalition_improved/0.
#show no_member_worse_off/0.
#show condorcet_winner_elected/0.