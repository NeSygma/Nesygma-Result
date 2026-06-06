fof(netflix_stranger, axiom, netflix_show(stranger_things)).
fof(popular_stranger, axiom, popular(stranger_things)).
fof(netflix_black_mirror, axiom, netflix_show(black_mirror)).

% If a Netflix show is popular, Karen will binge-watch it.
fof(popular_implies_binge, axiom,
    ! [X] : ((netflix_show(X) & popular(X)) => binge_watch(karen, X))).

% If and only if Karen binge-watches a Netflix show, she will download it.
fof(binge_iff_download, axiom,
    ! [X] : (netflix_show(X) => (binge_watch(karen, X) <=> download(karen, X)))).

% Karen does not download Black Mirror.
fof(no_download_black_mirror, axiom, ~download(karen, black_mirror)).

% If Karen binge-watches a Netflix show, she will share it with Lisa.
fof(binge_implies_share, axiom,
    ! [X] : ((netflix_show(X) & binge_watch(karen, X)) => share(karen, X, lisa))).

% Negated conclusion: Karen will NOT share Black Mirror with Lisa.
fof(goal, conjecture, ~share(karen, black_mirror, lisa)).