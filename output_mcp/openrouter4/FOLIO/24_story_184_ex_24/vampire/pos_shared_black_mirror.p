% Positive file: conjecture is Karen will share Black Mirror with Lisa
fof(premise1, axiom,
    (netflix_show(stranger_things) & popular(stranger_things))).
fof(premise2, axiom,
    ! [X] : ((netflix_show(X) & popular(X)) => binge_watch(X))).
fof(premise3, axiom,
    ! [X] : (netflix_show(X) => (binge_watch(X) <=> download(X)))).
fof(premise4, axiom,
    ~download(black_mirror)).
fof(premise5, axiom,
    netflix_show(black_mirror)).
fof(premise6, axiom,
    ! [X] : ((netflix_show(X) & binge_watch(X)) => share_with_lisa(X))).
fof(distinct, axiom,
    stranger_things != black_mirror).
fof(goal, conjecture,
    share_with_lisa(black_mirror)).