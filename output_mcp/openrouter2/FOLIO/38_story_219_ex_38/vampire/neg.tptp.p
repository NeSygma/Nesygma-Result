fof(symphony_piece, axiom, music_piece(symphony_no_9)).
fof(composer, axiom, composer(beethoven)).
fof(writes, axiom, writes(beethoven, symphony_no_9)).
fof(orchestra, axiom, orchestra(vienna_music_society)).
fof(premiered, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(leads, axiom, leads(beethoven, vienna_music_society)).
fof(orchestra_leads, axiom, ![Z] : (orchestra(Z) => ?[C] : (led_by(Z,C) & conductor(C)))).
fof(leads_implies_led_by, axiom, ![Y,Z] : (leads(Y,Z) => led_by(Z,Y))).
fof(conductor, axiom, conductor(beethoven)).
fof(distinct, axiom, (symphony_no_9 != beethoven & symphony_no_9 != vienna_music_society & beethoven != vienna_music_society)).
fof(goal, conjecture, ~(?[O,M] : (orchestra(O) & premiered(O,M) & music_piece(M)))).