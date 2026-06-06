% --- Domain Declarations ---
voter(v1). voter(v2). voter(v3). voter(v4).
candidate(a). candidate(b). candidate(c).

% --- True Preferences ---
% prefers(V, C1, C2) means V prefers C1 over C2.
prefers(v1, a, b). prefers(v1, b, c). prefers(v1, a, c).
prefers(v2, a, c). prefers(v2, c, b). prefers(v2, a, b).
prefers(v3, b, c). prefers(v3, c, a). prefers(v3, b, a).
prefers(v4, c, b). prefers(v4, b, a). prefers(v4, c, a).

% --- Current Votes ---
current_vote(v1, a).
current_vote(v2, a).
current_vote(v3, b).
current_vote(v4, c).

% --- Strategic Votes (Choice Rule) ---
{ strategic_vote(V, C) : candidate(C) } 1 :- voter(V).

% --- Vote Counts ---
vote_count(C, N) :- N = #count{ V : strategic_vote(V, C) }, candidate(C).

% --- Winner Determination ---
% The winner is the candidate with the most votes.
% If there is a tie, no winner is declared (manipulation fails).
winner(C) :- vote_count(C, N), N > #max{ M : vote_count(D, M), D != C }.

% --- Benefit Condition ---
% A voter benefits if the new winner is preferred over the current winner (a).
benefits(V, C) :- strategic_vote(V, _), winner(C), prefers(V, C, a).

% --- Manipulation Possible ---
manipulation_possible :- benefits(_, _).

% --- Coalition Size ---
% Define a predicate for voters who are not voting truthfully.
not_truthful(V) :- strategic_vote(V, C), current_vote(V, D), C != D.

% The coalition size is the number of not_truthful voters.
coalition_size(N) :- N = #count{ V : not_truthful(V) }.

% We want to find the minimum coalition_size for which manipulation_possible holds.
#minimize{ N : coalition_size(N), manipulation_possible }.

% --- Show the answer ---
#show coalition_size/1.
#show manipulation_possible/0.
#show winner/1.
#show benefits/2.