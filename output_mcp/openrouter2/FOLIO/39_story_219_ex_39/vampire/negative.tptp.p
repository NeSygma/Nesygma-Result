fof(sym_no_9_piece, axiom, music_piece(symphony_no_9)).
fof(beethoven_writes, axiom, writes(beethoven, symphony_no_9)).
fof(vienna_is_orchestra, axiom, orchestra(vienna_music_society)).
fof(beethoven_leads, axiom, leads(vienna_music_society, beethoven)).
fof(orchestra_leads_conductor, axiom, ! [X,Y] : ((orchestra(X) & leads(X,Y)) => conductor(Y))).
fof(distinctness, axiom, (beethoven != symphony_no_9 & beethoven != vienna_music_society & symphony_no_9 != vienna_music_society)).
fof(conjecture, conjecture, conductor(beethoven)).