fof(music_piece, axiom, is_music_piece(symphony_no_9)).
fof(composers_write, axiom, ! [C, M] : (writes(C, M) => is_music_piece(M))).
fof(beethoven_wrote, axiom, writes(beethoven, symphony_no_9)).
fof(vienna_premiered, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(vienna_is_orchestra, axiom, is_orchestra(vienna_music_society)).
fof(beethoven_leads, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [O, C] : ((is_orchestra(O) & leads(C, O)) => is_conductor(C))).
fof(distinct, axiom, (beethoven != vienna_music_society & beethoven != symphony_no_9 & vienna_music_society != symphony_no_9)).
fof(goal, conjecture, ~is_conductor(beethoven)).