fof(popular_stranger_things, axiom, popular(stranger_things)).
fof(stranger_things_on_netflix, axiom, is_on_platform(stranger_things, netflix)).
fof(black_mirror_on_netflix, axiom, is_on_platform(black_mirror, netflix)).
fof(popular_netflix_show_implies_binge, axiom,
    ! [Show] : ((is_on_platform(Show, netflix) & popular(Show)) => binge_watches(karen, Show))).
fof(binge_watches_iff_downloads, axiom,
    ! [Show] : (binge_watches(karen, Show) <=> downloads(karen, Show))).
fof(karen_does_not_download_black_mirror, axiom,
    ~downloads(karen, black_mirror)).
fof(binge_watches_implies_shares_with_lisa, axiom,
    ! [Show] : ((is_on_platform(Show, netflix) & binge_watches(karen, Show)) => shares_with(karen, Show, lisa))).

fof(conclusion_negation, conjecture, ~shares_with(karen, stranger_things, lisa)).