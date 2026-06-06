fof(stranger_things_is_netflix, axiom, netflix_show(stranger_things)).
fof(stranger_things_is_popular, axiom, popular(stranger_things)).
fof(popular_netflix_binge, axiom,
    ! [X] : ((netflix_show(X) & popular(X)) => binge_watch(karen, X))).
fof(binge_iff_download, axiom,
    ! [X] : (netflix_show(X) => (binge_watch(karen, X) <=> download(karen, X)))).
fof(no_download_black_mirror, axiom, ~download(karen, black_mirror)).
fof(black_mirror_is_netflix, axiom, netflix_show(black_mirror)).
fof(binge_then_share, axiom,
    ! [X] : ((netflix_show(X) & binge_watch(karen, X)) => share(karen, X, lisa))).
fof(distinct_shows, axiom, stranger_things != black_mirror).
fof(goal, conjecture, share(karen, stranger_things, lisa)).