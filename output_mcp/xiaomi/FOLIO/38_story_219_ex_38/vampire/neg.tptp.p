fof(symphony_is_music, axiom, music_piece(symphony_no_9)).
fof(composers_write, axiom, ! [X, Y] : ((composer(X) & music_piece(Y)) => writes(X, Y))).
fof(beethoven_wrote_sym9, axiom, writes(beethoven, symphony_no_9)).
fof(vms_premiered_sym9, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(vms_is_orchestra, axiom, orchestra(vienna_music_society)).
fof(beethoven_leads_vms, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [X, Y] : ((orchestra(X) & leads(Y, X)) => conductor(Y))).
fof(goal, conjecture, ~ ? [O, M] : (orchestra(O) & music_piece(M) & premiered(O, M))).