fof(symphony_is_music_piece, axiom, is_music_piece(symphony_no_9)).
fof(write_implies_composer, axiom, ! [X, Y] : (writes(X, Y) & is_music_piece(Y) => composer(X))).
fof(beethoven_wrote_symphony, axiom, writes(beethoven, symphony_no_9)).
fof(vienna_premiered_symphony, axiom, premieres(vienna_music_society, symphony_no_9)).
fof(vienna_is_orchestra, axiom, is_orchestra(vienna_music_society)).
fof(beethoven_leads_vienna, axiom, leads(beethoven, vienna_music_society)).
fof(orchestra_has_conductor, axiom, ! [X] : (is_orchestra(X) => ? [Y] : leads(Y, X))).
fof(distinct_constants, axiom, beethoven != vienna_music_society & beethoven != symphony_no_9 & vienna_music_society != symphony_no_9).
fof(beethoven_is_not_composer, conjecture, ~composer(beethoven)).