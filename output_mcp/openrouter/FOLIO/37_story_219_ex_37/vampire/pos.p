% Positive version
fof(music_piece_s9, axiom, music_piece(symphony9)).
fof(composer_rule, axiom, ![X] : (composer(X) => ?[Y] : (writes(X,Y) & music_piece(Y)))).
fof(wrote_beethoven, axiom, writes(beethoven, symphony9)).
fof(premiered, axiom, premiered(symphony9, vienna_music_society)).
fof(orchestra_vms, axiom, orchestra(vienna_music_society)).
fof(leads_beethoven, axiom, leads(beethoven, vienna_music_society)).
fof(orchestra_led_by_conductor, axiom, ![O,C] : ((orchestra(O) & leads(C,O)) => conductor(C))).
fof(distinct, axiom, (beethoven != symphony9 & beethoven != vienna_music_society & symphony9 != vienna_music_society)).
fof(goal, conjecture, composer(beethoven)).