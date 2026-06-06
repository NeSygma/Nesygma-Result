fof(is_music_piece_s9, axiom, is_music_piece(symphony_no_9)).
fof(composers_write_pieces, axiom, ! [C, M] : (composes(C, M) => is_music_piece(M))).
fof(beethoven_wrote_s9, axiom, wrote(beethoven, symphony_no_9)).
fof(vienna_premiered_s9, axiom, premiered_by(symphony_no_9, vienna_music_society)).
fof(vienna_is_orchestra, axiom, is_orchestra(vienna_music_society)).
fof(beethoven_leads_vienna, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [O, C] : (is_orchestra(O) & leads(C, O) => led_by(O, C))).
fof(goal_negation, conjecture, ~ (? [O, M] : (is_orchestra(O) & premiered_by(M, O)))).