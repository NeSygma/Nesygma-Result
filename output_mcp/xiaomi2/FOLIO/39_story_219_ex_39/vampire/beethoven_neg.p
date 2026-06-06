fof(p1, axiom, music_piece(symphony_no_9)).
fof(p2, axiom, ! [X, Y] : ((composer(X) & music_piece(Y)) => writes(X, Y))).
fof(p3, axiom, writes(beethoven, symphony_no_9)).
fof(p4, axiom, premieres(vienna_music_society, symphony_no_9)).
fof(p5, axiom, orchestra(vienna_music_society)).
fof(p6, axiom, leads(beethoven, vienna_music_society)).
fof(p7, axiom, ! [X, Y] : ((orchestra(X) & leads(Y, X)) => conductor(Y))).
fof(distinct, axiom, (symphony_no_9 != beethoven & symphony_no_9 != vienna_music_society & beethoven != vienna_music_society)).
fof(goal, conjecture, conductor(beethoven)).