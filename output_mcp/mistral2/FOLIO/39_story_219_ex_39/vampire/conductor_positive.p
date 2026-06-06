fof(symphony_no_9_is_music_piece, axiom, is_music_piece(symphony_no_9)).
fof(composers_write_music_pieces, axiom, ! [C, M] : (composer(C) & is_music_piece(M) => composes(C, M))).
fof(beethoven_wrote_symphony_no_9, axiom, wrote(beethoven, symphony_no_9)).
fof(premiered_by_vienna_society, axiom, premiered_by(symphony_no_9, vienna_music_society)).
fof(vienna_music_society_is_orchestra, axiom, is_orchestra(vienna_music_society)).
fof(beethoven_leads_vienna_society, axiom, leads(vienna_music_society, beethoven)).
fof(orchestras_led_by_conductors, axiom, ! [O, P] : (is_orchestra(O) & leads(O, P) => is_conductor(P))).
fof(beethoven_is_composer, axiom, composer(beethoven)).
fof(goal, conjecture, ~is_conductor(beethoven)).