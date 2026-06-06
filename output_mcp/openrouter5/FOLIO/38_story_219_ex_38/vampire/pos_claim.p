% Positive claim: Some orchestras premiered music pieces.
fof(premise_1, axiom, music_piece(symphony_no_9)).
fof(premise_2, axiom, ! [X] : (composer(X) => ! [Y] : (music_piece(Y) => writes(X, Y)))).
fof(premise_3, axiom, wrote(beethoven, symphony_no_9)).
fof(premise_4, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(premise_5, axiom, orchestra(vienna_music_society)).
fof(premise_6, axiom, leads(beethoven, vienna_music_society)).
fof(premise_7, axiom, ! [X] : (orchestra(X) => ? [Y] : (conductor(Y) & leads(Y, X)))).

fof(goal, conjecture, ? [O, P] : (orchestra(O) & music_piece(P) & premiered(O, P))).