fof(is_netflix_show_st, axiom, is_netflix_show(stranger_things)).
fof(is_popular_st, axiom, is_popular(stranger_things)).
fof(rule_binge, axiom, ! [X] : ((is_netflix_show(X) & is_popular(X)) => binge_watches(karen, X))).
fof(rule_download, axiom, ! [X] : (is_netflix_show(X) => (binge_watches(karen, X) <=> downloads(karen, X)))).
fof(not_download_bm, axiom, ~downloads(karen, black_mirror)).
fof(is_netflix_show_bm, axiom, is_netflix_show(black_mirror)).
fof(rule_share, axiom, ! [X] : ((is_netflix_show(X) & binge_watches(karen, X)) => shares_with_lisa(karen, X))).
fof(goal, conjecture, shares_with_lisa(karen, stranger_things)).