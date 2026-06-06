fof(netflix_stranger, axiom, netflix_show(stranger_things)).
fof(popular_stranger, axiom, popular(stranger_things)).
fof(popular_implies_binge, axiom,
    ! [X] : ((netflix_show(X) & popular(X)) => binge_watch(karen, X))).
fof(binge_iff_download, axiom,
    ! [X] : (netflix_show(X) => (binge_watch(karen, X) <=> download(karen, X)))).
fof(no_download_black_mirror, axiom, ~download(karen, black_mirror)).
fof(netflix_black_mirror, axiom, netflix_show(black_mirror)).
fof(binge_implies_share, axiom,
    ! [X] : ((netflix_show(X) & binge_watch(karen, X)) => share(karen, lisa, X))).
fof(goal, conjecture, ~popular(black_mirror)).