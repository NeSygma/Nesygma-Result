fof(music_piece_symphony9, axiom, music_piece(symphony9)).
fof(composers_write, axiom, ! [X] : (composer(X) => ? [Y] : (music_piece(Y) & writes(X, Y)))).
fof(beethoven_wrote, axiom, writes(beethoven, symphony9)).
fof(premiered, axiom, premiered(vienna_music_society, symphony9)).
fof(orchestra_vms, axiom, orchestra(vienna_music_society)).
fof(beethoven_leads, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [X, Y] : (leads(X, Y) & orchestra(Y) => conductor(X))).
fof(beethoven_is_composer, axiom, ! [X, Y] : (writes(X, Y) & music_piece(Y) => composer(X))).
fof(goal, conjecture, conductor(beethoven)).