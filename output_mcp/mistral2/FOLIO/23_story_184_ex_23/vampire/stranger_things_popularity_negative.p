fof(netflix_show_stranger_things, axiom, netflix_show(stranger_things)).
fof(popular_stranger_things, axiom, popular(stranger_things)).
fof(popular_netflix_show_implies_binge, axiom,
    ! [S] : (netflix_show(S) & popular(S) => binge_watches(karen, S))).
fof(binge_watches_iff_downloads, axiom,
    ! [S] : (binge_watches(karen, S) <=> downloads(karen, S))).
fof(not_downloads_black_mirror, axiom, ~downloads(karen, black_mirror)).
fof(netflix_show_black_mirror, axiom, netflix_show(black_mirror)).
fof(binge_watches_implies_shares, axiom,
    ! [S] : (binge_watches(karen, S) => shares_with(karen, S, lisa))).

fof(conclusion_not_popular_black_mirror, conjecture, ~popular(black_mirror)).