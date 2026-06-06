fof(netflix_show_stranger_things, axiom, is_netflix_show(stranger_things)).
fof(popular_stranger_things, axiom, is_popular(stranger_things)).
fof(rule_binge, axiom, ! [X] : ((is_netflix_show(X) & is_popular(X)) => binge_watches(karen, X))).
fof(rule_download, axiom, ! [X] : (is_netflix_show(X) => (binge_watches(karen, X) <=> downloads(karen, X)))).
fof(not_download_black_mirror, axiom, ~downloads(karen, black_mirror)).
fof(is_netflix_black_mirror, axiom, is_netflix_show(black_mirror)).
fof(rule_share, axiom, ! [X] : (is_netflix_show(X) => (binge_watches(karen, X) => shares_with_lisa(karen, X)))).
fof(distinct, axiom, (stranger_things != black_mirror)).

fof(goal, conjecture, is_popular(black_mirror)).