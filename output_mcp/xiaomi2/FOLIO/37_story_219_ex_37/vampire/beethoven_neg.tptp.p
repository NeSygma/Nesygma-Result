fof(symphony_is_music, axiom, music_piece(symphony_no_9)).
fof(composers_write_music, axiom,
    ! [X, Y] : ((wrote(X, Y) & music_piece(Y)) => composer(X))).
fof(beethoven_wrote_sym9, axiom, wrote(beethoven, symphony_no_9)).
fof(vms_premiered_sym9, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(vms_is_orchestra, axiom, orchestra(vienna_music_society)).
fof(beethoven_leads_vms, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom,
    ! [O, P] : ((orchestra(O) & leads(P, O)) => conductor(P))).
fof(distinct_entities, axiom,
    (beethoven != symphony_no_9 &
     beethoven != vienna_music_society &
     symphony_no_9 != vienna_music_society)).
fof(goal, conjecture, ~composer(beethoven)).