fof(premise1, axiom, music_piece(symphony9)).
fof(premise2, axiom, ! [X] : (composer(X) => ? [Y] : (music_piece(Y) & writes(X, Y)))).
fof(premise3, axiom, writes(beethoven, symphony9)).
fof(premise4, axiom, premiered(vienna_music_society, symphony9)).
fof(premise5, axiom, orchestra(vienna_music_society)).
fof(premise6, axiom, leads(beethoven, vienna_music_society)).
fof(premise7, axiom, ! [X,Y] : (orchestra(X) & leads(Y, X) => conductor(Y))).
fof(neg_conclusion, conjecture, ~composer(beethoven)).