fof(symphony_is_music_piece, axiom, music_piece(symphony_no_9)).
fof(composers_write_pieces, axiom, ! [C, M] : (composer(C) & music_piece(M) => wrote(C, M))).
fof(beethoven_wrote_symphony, axiom, wrote(beethoven, symphony_no_9)).
fof(vienna_premiered_symphony, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(vienna_is_orchestra, axiom, orchestra(vienna_music_society)).
fof(beethoven_leads_vienna, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [O] : (orchestra(O) => ? [P] : (leads(P, O) & is_conductor(P)))).
fof(conclusion, conjecture, ~is_conductor(beethoven)).