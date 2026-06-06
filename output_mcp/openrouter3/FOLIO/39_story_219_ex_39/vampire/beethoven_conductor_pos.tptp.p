% Positive file: Original claim as conjecture
fof(symphony_is_music_piece, axiom, music_piece(symphony_no_9)).
fof(composers_write_music, axiom, ! [X] : (composer(X) => ? [Y] : (music_piece(Y) & writes(X, Y)))).
fof(beethoven_wrote_symphony, axiom, writes(beethoven, symphony_no_9)).
fof(vms_premiered_symphony, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(vms_is_orchestra, axiom, orchestra(vienna_music_society)).
fof(beethoven_leads_vms, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [X] : (orchestra(X) => ? [Y] : (conductor(Y) & leads(Y, X)))).
fof(beethoven_is_not_conductor, conjecture, ~conductor(beethoven)).