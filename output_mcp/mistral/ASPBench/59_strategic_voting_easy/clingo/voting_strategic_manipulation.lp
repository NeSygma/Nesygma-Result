% Domain declarations
voter(v1). voter(v2). voter(v3). voter(v4).
candidate(a). candidate(b). candidate(c).

% True preferences (strict ordering)
% V1: A > B > C
prefers(v1, a, b). prefers(v1, b, c). prefers(v1, a, c).
% V2: A > C > B
prefers(v2, a, c). prefers(v2, c, b). prefers(v2, a, b).
% V3: B > C > A
prefers(v3, b, c). prefers(v3, c, a). prefers(v3, b, a).
% V4: C > B > A
prefers(v4, c, b). prefers(v4, b, a). prefers(v4, c, a).

% Current truthful voting
current_vote(v1, a).
current_vote(v2, a).
current_vote(v3, b).
current_vote(v4, c).

% Calculate current winner
current_vote_count(C, N) :- N = #count{ V : current_vote(V, C) }, candidate(C).
current_winner(W) :- current_vote_count(W, N), #max{ M : current_vote_count(_, M) } = N.

% Strategic voting: each voter can choose any candidate
{ strategic_vote(V, C) : candidate(C) } = 1 :- voter(V).

% Calculate vote counts under strategic voting
strategic_vote_count(C, N) :- N = #count{ V : strategic_vote(V, C) }, candidate(C).

% Determine the maximum vote count
max_votes(N) :- N = #max{ M : strategic_vote_count(_, M) }.

% Possible winners are those with max votes
possible_winner(W) :- strategic_vote_count(W, N), max_votes(N).

% A voter prefers candidate X over Y
prefers_to(V, X, Y) :- voter(V), candidate(X), candidate(Y), X != Y, prefers(V, X, Y).

% Find coalitions that can manipulate
% A coalition of size 1 can manipulate if that voter can make a preferred candidate win
coalition_size_1 :- voter(V),
                    possible_winner(W),
                    current_winner(CW),
                    W != CW,
                    prefers_to(V, W, CW),
                    strategic_vote(V, W).

% A coalition of size 2 can manipulate if both voters can make a preferred candidate win
% and they vote for the same candidate
coalition_size_2 :- voter(V1), voter(V2), V1 != V2,
                    possible_winner(W),
                    current_winner(CW),
                    W != CW,
                    prefers_to(V1, W, CW),
                    prefers_to(V2, W, CW),
                    strategic_vote(V1, W),
                    strategic_vote(V2, W).

% Similarly for sizes 3 and 4
coalition_size_3 :- voter(V1), voter(V2), voter(V3),
                    V1 != V2, V1 != V3, V2 != V3,
                    possible_winner(W),
                    current_winner(CW),
                    W != CW,
                    prefers_to(V1, W, CW),
                    prefers_to(V2, W, CW),
                    prefers_to(V3, W, CW),
                    strategic_vote(V1, W),
                    strategic_vote(V2, W),
                    strategic_vote(V3, W).

coalition_size_4 :- voter(V1), voter(V2), voter(V3), voter(V4),
                    possible_winner(W),
                    current_winner(CW),
                    W != CW,
                    prefers_to(V1, W, CW),
                    prefers_to(V2, W, CW),
                    prefers_to(V3, W, CW),
                    prefers_to(V4, W, CW),
                    strategic_vote(V1, W),
                    strategic_vote(V2, W),
                    strategic_vote(V3, W),
                    strategic_vote(V4, W).

% The minimum coalition size
min_coalition_size(N) :- N = #min{ Size : coalition_size(Size) }.

coalition_size(1) :- coalition_size_1.
coalition_size(2) :- coalition_size_2.
coalition_size(3) :- coalition_size_3.
coalition_size(4) :- coalition_size_4.

% Show relevant atoms
#show current_winner/1.
#show possible_winner/1.
#show min_coalition_size/1.
#show coalition_size/1.