fof(pre_1, axiom, superhero_movie(su_adv).).
fof(pre_2, axiom, named_after(su_adv, sir_digby).).
fof(pre_3, axiom, ! [M,C] : (superhero_movie(M) & named_after(M, C) => good_guy(C)).).
fof(pre_4, axiom, ! [X] : (good_guy(X) => win(X)).).
fof(pre_5, axiom, ! [X,Y] : (fight(X, Y) & win(X) => ~win(Y)).).
fof(pre_6, axiom, fight(sir_digby, nemesis).).
fof(conclusion, conjecture, win(nemesis).).