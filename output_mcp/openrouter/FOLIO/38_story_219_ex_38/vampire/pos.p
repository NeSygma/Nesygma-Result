% Positive version
fof(premise1, axiom, music_piece(symphony_no_9)).
fof(premise2, axiom, ![X] : (composer(X) => ?[Y] : (music_piece(Y) & writes(X,Y)))).
fof(premise3, axiom, wrote(beethoven, symphony_no_9)).
fof(premise4, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(premise5, axiom, orchestra(vienna_music_society)).
fof(premise6, axiom, leads(beethoven, vienna_music_society)).
fof(premise7, axiom, ![O] : (orchestra(O) => ?[C] : (conductor(C) & leads(C,O)))).
fof(distinct, axiom, (beethoven != vienna_music_society & beethoven != symphony_no_9 & vienna_music_society != symphony_no_9)).
fof(goal, conjecture, ?[O,M] : (orchestra(O) & music_piece(M) & premiered(O,M))).