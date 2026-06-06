% Negative version (negated claim)
fof(distinct_shows, axiom, (stranger_things != black_mirror)).
fof(netflix_stranger, axiom, netflix_show(stranger_things)).
fof(popular_stranger, axiom, popular(stranger_things)).
fof(netflix_black, axiom, netflix_show(black_mirror)).
fof(not_download_black, axiom, ~download(black_mirror)).
fof(rule_popular_binge, axiom, ![X] : ((netflix_show(X) & popular(X)) => binge(X))).
fof(rule_binge_download, axiom, ![X] : (binge(X) <=> download(X))).
fof(rule_binge_share, axiom, ![X] : ((netflix_show(X) & binge(X)) => share(X))).
fof(goal_neg, conjecture, ~share(stranger_things)).