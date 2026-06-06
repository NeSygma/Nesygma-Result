% Negative: negated claim "No orchestras premiered music pieces"
fof(premise_1, axiom, music_piece(symphony_no_9)).
fof(premise_2, axiom, ! [X,Y] : ((composer(X) & music_piece(Y)) => writes(X,Y))).
fof(premise_3, axiom, wrote(beethoven, symphony_no_9)).
fof(premise_4, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(premise_5, axiom, orchestra(vienna_music_society)).
fof(premise_6, axiom, leads(beethoven, vienna_music_society)).
fof(premise_7, axiom, ! [X,Y] : ((orchestra(X) & leads(Y,X)) => conductor(Y))).
fof(goal, conjecture, ~? [X,Y] : (orchestra(X) & music_piece(Y) & premiered(X,Y))).