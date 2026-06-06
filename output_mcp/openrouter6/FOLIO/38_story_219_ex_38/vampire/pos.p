fof(symphony_is_music_piece, axiom, music_piece(symphony_no_9)).
fof(beethoven_is_composer, axiom, composer(beethoven)).
fof(vienna_is_orchestra, axiom, orchestra(vienna_music_society)).
fof(beethoven_wrote_symphony, axiom, writes(beethoven, symphony_no_9)).
fof(vienna_premiered_symphony, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(beethoven_leads_vienna, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [O, P] : (orchestra(O) & leads(P, O) => conductor(P))).
fof(distinct_entities, axiom, (symphony_no_9 != beethoven & symphony_no_9 != vienna_music_society & beethoven != vienna_music_society)).
fof(goal, conjecture, ? [O, M] : (orchestra(O) & music_piece(M) & premiered(O, M))).