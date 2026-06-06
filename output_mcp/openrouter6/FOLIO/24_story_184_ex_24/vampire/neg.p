fof(premise1a, axiom, popular(stranger_things)).
fof(premise1b, axiom, netflix(stranger_things)).
fof(premise2, axiom, ! [S] : (netflix(S) & popular(S) => binge_watch(karen, S))).
fof(premise3, axiom, ! [S] : (binge_watch(karen, S) <=> download(karen, S))).
fof(premise4, axiom, ~download(karen, black_mirror)).
fof(premise5, axiom, netflix(black_mirror)).
fof(premise6, axiom, ! [S] : (binge_watch(karen, S) => share(karen, lisa, S))).
fof(distinct_shows, axiom, (stranger_things != black_mirror)).
fof(goal, conjecture, ~share(karen, lisa, black_mirror)).