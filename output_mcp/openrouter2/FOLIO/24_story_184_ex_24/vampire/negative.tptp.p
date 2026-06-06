fof(distinct, axiom, (karen != lisa & karen != black_mirror & lisa != black_mirror)).
fof(netflix_show_stranger, axiom, netflix_show(stranger_things)).
fof(popular_stranger, axiom, popular(stranger_things)).
fof(netflix_show_black, axiom, netflix_show(black_mirror)).
fof(not_download_black, axiom, ~download(karen, black_mirror)).
fof(binge_implies_popular, axiom, ![S] : ((netflix_show(S) & popular(S)) => binge_watch(karen, S))).
fof(binge_download_equiv, axiom, ![S] : ((netflix_show(S) => (binge_watch(karen, S) <=> download(karen, S))))).
fof(binge_shares, axiom, ![S] : ((binge_watch(karen, S) & netflix_show(S)) => share_with(karen, S, lisa))).
fof(goal, conjecture, ~share_with(karen, black_mirror, lisa)).