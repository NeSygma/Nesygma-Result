fof(symphony_no_9_is_music_piece, axiom, is(symphony_no_9, music_piece)).
fof(composers_write_music_pieces, axiom, ! [C, M] : (is(C, composer) & writes(C, M) => is(M, music_piece))).
fof(beethoven_wrote_symphony_no_9, axiom, wrote(beethoven, symphony_no_9)).
fof(vienna_music_society_premiered_symphony_no_9, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(vienna_music_society_is_orchestra, axiom, is(vienna_music_society, orchestra)).
fof(beethoven_leads_vienna_music_society, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [O, C] : (is(O, orchestra) & leads(C, O) => is(C, conductor))).

fof(conclusion, conjecture, is(beethoven, composer)).