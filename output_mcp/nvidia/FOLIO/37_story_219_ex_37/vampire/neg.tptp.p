fof(axiom1, axiom, is_music_piece(symphony9)).
fof(axiom2, axiom, ! [X] : (composer(X) => ? [Y] : writes(X, Y))).
fof(axiom3, axiom, writes(beethoven, symphony9)).
fof(axiom4, axiom, premiered(vienna_music_society, symphony9)).
fof(axiom5, axiom, is_orchestra(vienna_music_society)).
fof(axiom6, axiom, ! [X] : (is_orchestra(X) => ? [Y] : (conductor(Y) & leads(Y, X)))).
fof(axiom7, axiom, leads(beethoven, vienna_music_society)).
fof(axiom8, axiom, (beethoven != vienna_music_society & beethoven != symphony9 & vienna_music_society != symphony9)).
fof(conjecture, conjecture, ~composer(beethoven)).