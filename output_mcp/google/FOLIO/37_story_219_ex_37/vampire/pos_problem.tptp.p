fof(music_piece, axiom, is_music_piece(symphony_no_9)).
fof(composer_rule, axiom, ! [C, M] : ((writes(C, M) & is_music_piece(M)) => composer(C))).
fof(beethoven_writes, axiom, writes(beethoven, symphony_no_9)).
fof(vienna_premiered, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(vienna_orchestra, axiom, is_orchestra(vienna_music_society)).
fof(beethoven_leads, axiom, leads(beethoven, vienna_music_society)).
fof(orchestra_rule, axiom, ! [O] : (is_orchestra(O) => ? [C] : (is_conductor(C) & leads(C, O)))).
fof(distinct, axiom, (symphony_no_9 != vienna_music_society & symphony_no_9 != beethoven & vienna_music_society != beethoven)).
fof(goal, conjecture, composer(beethoven)).