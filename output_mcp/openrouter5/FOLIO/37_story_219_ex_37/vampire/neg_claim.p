% Negative claim: Beethoven is not a composer.
fof(premise_1, axiom, music_piece(symphony_no_9)).
fof(premise_2, axiom, ! [X, Y] : (composes(X, Y) => composer(X))).
fof(premise_3, axiom, composes(beethoven, symphony_no_9)).
fof(premise_4, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(premise_5, axiom, orchestra(vienna_music_society)).
fof(premise_6, axiom, leads(beethoven, vienna_music_society)).
fof(premise_7, axiom, ! [X] : (orchestra(X) => ? [Y] : (leads(Y, X) & conductor(Y)))).
fof(distinct, axiom, (beethoven != symphony_no_9 & beethoven != vienna_music_society & symphony_no_9 != vienna_music_society)).
fof(goal, conjecture, ~composer(beethoven)).