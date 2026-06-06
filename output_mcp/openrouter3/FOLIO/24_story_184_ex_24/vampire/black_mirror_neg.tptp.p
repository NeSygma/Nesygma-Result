% Negative version: Karen does NOT share Black Mirror with Lisa
fof(stranger_things_popular, axiom, popular(stranger_things) & netflix(stranger_things)).
fof(popular_netflix_binge, axiom, ! [S] : ((netflix(S) & popular(S)) => binge_watches(karen, S))).
fof(binge_iff_download, axiom, ! [S] : ((netflix(S) & binge_watches(karen, S)) <=> downloads(karen, S))).
fof(not_download_black_mirror, axiom, ~downloads(karen, black_mirror)).
fof(black_mirror_netflix, axiom, netflix(black_mirror)).
fof(binge_shares, axiom, ! [S] : ((netflix(S) & binge_watches(karen, S)) => shares(karen, S, lisa))).
fof(goal, conjecture, ~shares(karen, black_mirror, lisa)).