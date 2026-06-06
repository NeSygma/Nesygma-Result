fof(axiom1, axiom, (netflix_show(stranger_things) & popular(stranger_things))).
fof(axiom2, axiom, ! [X] : ((netflix_show(X) & popular(X)) => binge_watch(X))).
fof(axiom3, axiom, ! [X] : (netflix_show(X) => (binge_watch(X) <=> download(X)))).
fof(axiom4, axiom, ~download(black_mirror)).
fof(axiom5, axiom, netflix_show(black_mirror)).
fof(axiom6, axiom, ! [X] : (binge_watch(X) => share_with_lisa(X))).
fof(distinct, axiom, stranger_things != black_mirror).
fof(conjecture, conjecture, share_with_lisa(stranger_things)).