fof(axiom_1, axiom, music_piece(symphony9)).
fof(axiom_2, axiom, orchestra(viennamusicsociety)).
fof(axiom_3, axiom, premiered(viennamusicsociety, symphony9)).
fof(conjecture, conjecture, ~ ? [O] : (orchestra(O) & ? [P] : (premiered(O, P) & music_piece(P))) ).