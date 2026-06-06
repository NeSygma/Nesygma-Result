fof(music_piece_symphony, axiom, music_piece(symphony_no_9)).
fof(composers_write, axiom, ! [X] : (composer(X) => ? [Y] : (writes(X,Y) & music_piece(Y)))).
fof(beethoven_wrote, axiom, writes(beethoven, symphony_no_9)).
fof(vienna_is_orchestra, axiom, orchestra(vienna_music_society)).
fof(beethoven_leads, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [X] : (orchestra(X) => ? [Y] : (leads(Y,X) & conductor(Y)))).
fof(vienna_premiered, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(distinctness, axiom, (beethoven != symphony_no_9 & beethoven != vienna_music_society & symphony_no_9 != vienna_music_society)).
fof(conjecture, conjecture, ~composer(beethoven)).