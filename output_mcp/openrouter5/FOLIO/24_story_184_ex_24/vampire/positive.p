% Positive version: original claim as conjecture
% Premises:
% 1. "Stranger Things" is a popular Netflix show.
fof(premise1, axiom, popular_netflix_show(stranger_things)).
% 2. If a Netflix show is popular, Karen will binge-watch it.
fof(premise2, axiom, ! [X] : (netflix_show(X) & popular(X) => binge_watch(karen, X))).
% 3. If and only if Karen binge-watches a Netflix show, she will download it.
fof(premise3, axiom, ! [X] : (netflix_show(X) => (download(karen, X) <=> binge_watch(karen, X)))).
% 4. Karen does not download "Black Mirror."
fof(premise4, axiom, ~download(karen, black_mirror)).
% 5. "Black Mirror" is a Netflix show.
fof(premise5, axiom, netflix_show(black_mirror)).
% 6. If Karen binge-watches a Netflix show, she will share it with Lisa.
fof(premise6, axiom, ! [X] : (netflix_show(X) & binge_watch(karen, X) => share_with(karen, X, lisa))).

% Conclusion: Karen will share "Black Mirror" with Lisa.
fof(goal, conjecture, share_with(karen, black_mirror, lisa)).