fof(netflix_stranger_things, axiom, netflix_show(stranger_things)).
fof(popular_stranger_things, axiom, popular(stranger_things)).
fof(popular_implies_binge, axiom, ! [S] : (netflix_show(S) & popular(S) => binge_watches(karen, S))).
fof(binge_download_iff, axiom, ! [S] : (netflix_show(S) => (binge_watches(karen, S) <=> downloads(karen, S)))).
fof(not_download_black_mirror, axiom, ~downloads(karen, black_mirror)).
fof(netflix_black_mirror, axiom, netflix_show(black_mirror)).
fof(binge_share, axiom, ! [S] : (netflix_show(S) & binge_watches(karen, S) => shares(karen, lisa, S))).
fof(goal_negation, conjecture, ~popular(black_mirror)).