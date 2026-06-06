fof(symphony_is_music_piece, axiom, is_music_piece(symphony_no_9)).
fof(composer_beethoven, axiom, composer(beethoven)).
fof(beethoven_wrote_symphony, axiom, writes(beethoven, symphony_no_9)).
fof(vienna_premiered_symphony, axiom, premieres(vienna_music_society, symphony_no_9)).
fof(vienna_is_orchestra, axiom, orchestra(vienna_music_society)).
fof(beethoven_leads_vienna, axiom, leads(beethoven, vienna_music_society)).
fof(orchestras_led_by_conductors, axiom, ! [O] : (orchestra(O) => ? [C] : leads(C, O))).

fof(conclusion, conjecture, ? [O, M] : (orchestra(O) & is_music_piece(M) & premieres(O, M))).