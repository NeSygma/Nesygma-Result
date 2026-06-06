fof(netflix_stranger, axiom, netflix_show(stranger_things)).
fof(popular_stranger, axiom, popular(stranger_things)).
fof(netflix_blackmirror, axiom, netflix_show(black_mirror)).
fof(popular_implies_binge, axiom,
    ! [X] : ((netflix_show(X) & popular(X)) => binge_watch(karen, X))).
fof(binge_iff_download, axiom,
    ! [X] : (netflix_show(X) => (binge_watch(karen, X) <=> download(karen, X)))).
fof(no_download_blackmirror, axiom, ~download(karen, black_mirror)).
fof(binge_share, axiom,
    ! [X] : ((netflix_show(X) & binge_watch(karen, X)) => share(karen, lisa, X))).
fof(goal, conjecture, ~share(karen, lisa, stranger_things)).