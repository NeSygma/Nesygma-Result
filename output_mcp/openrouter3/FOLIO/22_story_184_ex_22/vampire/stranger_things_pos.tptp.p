% Positive version: Karen will share "Stranger Things" with Lisa
fof(popular_stranger_things, axiom, popular(netflix_show_stranger_things)).
fof(karen_binges_popular, axiom, ! [S] : (popular(S) => binge_watches(karen, S))).
fof(binge_download_equiv, axiom, ! [S] : (binge_watches(karen, S) <=> downloads(karen, S))).
fof(not_download_black_mirror, axiom, ~downloads(karen, netflix_show_black_mirror)).
fof(black_mirror_is_netflix, axiom, netflix_show(netflix_show_black_mirror)).
fof(binge_shares, axiom, ! [S] : (binge_watches(karen, S) => shares(karen, S, lisa))).
fof(goal, conjecture, shares(karen, netflix_show_stranger_things, lisa)).