fof(popular_stranger_things, axiom, (netflix_show(stranger_things) & popular(stranger_things))).
fof(popular_implies_binge, axiom, ! [S] : ((netflix_show(S) & popular(S)) => binge_watches(karen, S))).
fof(binge_iff_download, axiom, ! [S] : (binge_watches(karen, S) <=> downloads(karen, S))).
fof(karen_does_not_download_black_mirror, axiom, ~downloads(karen, black_mirror)).
fof(black_mirror_is_netflix, axiom, netflix_show(black_mirror)).
fof(binge_implies_share, axiom, ! [S] : ((netflix_show(S) & binge_watches(karen, S)) => shares_with(karen, lisa, S))).
fof(goal_negation, conjecture, ~shares_with(karen, lisa, black_mirror)).