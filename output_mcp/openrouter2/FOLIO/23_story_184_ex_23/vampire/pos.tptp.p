fof(distinct_entities, axiom, (stranger_things != black_mirror & stranger_things != karen & stranger_things != lisa & black_mirror != karen & black_mirror != lisa & karen != lisa)).
fof(popular_stranger, axiom, popular(stranger_things)).
fof(netflix_stranger, axiom, netflix_show(stranger_things)).
fof(netflix_black, axiom, netflix_show(black_mirror)).
fof(not_download_black, axiom, ~download(karen, black_mirror)).
fof(binge_if_popular, axiom, ! [X] : ((netflix_show(X) & popular(X)) => binge(karen, X))).
fof(binge_download_equiv, axiom, ! [X] : (binge(karen, X) <=> download(karen, X))).
fof(binge_share, axiom, ! [X] : (binge(karen, X) => share(karen, lisa, X))).
fof(conjecture, conjecture, popular(black_mirror)).