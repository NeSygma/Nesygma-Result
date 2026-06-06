% Negative version
fof(movie_superhero, axiom, superhero_movie(movie_sd)).
fof(named, axiom, named_after(movie_sd, sir_digby)).
fof(good_if_named, axiom, ! [M,C] : (superhero_movie(M) & named_after(M,C) => good_guy(C))).
fof(in_movie_if_named, axiom, ! [M,C] : (superhero_movie(M) & named_after(M,C) => in_movie(C,M))).
fof(good_win_in_superhero, axiom, ! [M,P] : (superhero_movie(M) & good_guy(P) & in_movie(P,M) => wins(P))).
fof(good_fight_bad, axiom, ! [X,Y] : (good_guy(X) & bad_guy(Y) => fight(X,Y))).
fof(bad_fight_good, axiom, ! [X,Y] : (bad_guy(X) & good_guy(Y) => fight(X,Y))).
fof(sir_fights_nemesis, axiom, fight(sir_digby, nemesis_of(sir_digby))).
fof(win_implies_opponent_not_win, axiom, ! [X,Y] : (fight(X,Y) & wins(X) => ~wins(Y))).
fof(goal, conjecture, wins(nemesis_of(sir_digby))).