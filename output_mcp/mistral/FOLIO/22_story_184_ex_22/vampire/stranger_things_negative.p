fof(popular_stranger_things, axiom, popular(stranger_things)).
fof(stranger_things_netflix, axiom, netflix_show(stranger_things)).
fof(popular_netflix_implies_binge, axiom, ! [S] : ((netflix_show(S) & popular(S)) => binge_watches(karen, S))).
fof(binge_iff_download, axiom, ! [S] : (binge_watches(karen, S) <=> downloads(karen, S))).
fof(karen_no_black_mirror_download, axiom, ~downloads(karen, black_mirror)).
fof(black_mirror_netflix, axiom, netflix_show(black_mirror)).
fof(binge_netflix_implies_share, axiom, ! [S] : ((netflix_show(S) & binge_watches(karen, S)) => shares_with(karen, lisa, S))).
fof(conclusion_negation, conjecture, ~shares_with(karen, lisa, stranger_things)).