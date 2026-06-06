% Negative file: negated claim as conjecture
% Negated conclusion: Beethoven is a conductor.

fof(distinct, axiom, (
    beethoven != symphony_no_9 &
    beethoven != vienna_music_society &
    symphony_no_9 != vienna_music_society
)).

fof(a1, axiom, music_piece(symphony_no_9)).
fof(a2, axiom, ! [X, Y] : (composer(X) & music_piece(Y) & writes(X, Y) => composer_writes_piece(X, Y))).
fof(a3, axiom, composer(beethoven)).
fof(a4, axiom, writes(beethoven, symphony_no_9)).
fof(a5, axiom, premiered(vienna_music_society, symphony_no_9)).
fof(a6, axiom, orchestra(vienna_music_society)).
fof(a7, axiom, leads(beethoven, vienna_music_society)).
fof(a8, axiom, ! [X, Y] : (orchestra(Y) & leads(X, Y) => conductor(X))).

fof(goal_neg, conjecture, conductor(beethoven)).