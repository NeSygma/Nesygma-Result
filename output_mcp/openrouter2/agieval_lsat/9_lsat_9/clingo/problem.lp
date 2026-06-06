% Define all works
all(fn1). all(fn2). all(fn3). all(rn1). all(rn2). all(rn3). all(fp1). all(fp2). all(rp).

% French novels
french_novel(fn1). french_novel(fn2). french_novel(fn3).
% Russian novels
russian_novel(rn1). russian_novel(rn2). russian_novel(rn3).
% French plays
french_play(fp1). french_play(fp2).
% Russian play
russian_play(rp).

% Selected French novels (given)
selected(fn1). selected(fn2). selected(fn3).

% Domain for other works
other(rn1). other(rn2). other(rn3). other(fp1). other(fp2). other(rp).

% Choice rule for other works
{ selected(W) } :- other(W).

% Total selected between 5 and 6
5 { selected(W) : all(W) } 6.

% No more than one French play selected
:- selected(fp1), selected(fp2).

% At most one Russian novel selected (novels 3-4 constraint)
2 { selected(rn1); selected(rn2); selected(rn3) } 1.

% Option rules
option(a) :- selected(fn1), selected(fn2), selected(fn3), 1 { selected(rn1); selected(rn2); selected(rn3) } 1, not selected(fp1), not selected(fp2), not selected(rp).
option(b) :- selected(fn1), selected(fn2), selected(fn3), selected(fp1), selected(fp2), not selected(rn1), not selected(rn2), not selected(rn3), not selected(rp).
option(c) :- selected(fn1), selected(fn2), selected(fn3), 1 { selected(rn1); selected(rn2); selected(rn3) } 1, selected(rp), not selected(fp1), not selected(fp2).
option(d) :- selected(fn1), selected(fn2), selected(fn3), 1 { selected(rn1); selected(rn2); selected(rn3) } 1, selected(fp1), selected(fp2), not selected(rp).
option(e) :- selected(fn1), selected(fn2), selected(fn3), 2 { selected(rn1); selected(rn2); selected(rn3) } 2, selected(fp1), not selected(fp2), not selected(rp).

#show option/1.