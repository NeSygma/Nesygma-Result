% Positive version: claim is Beethoven is not a conductor
fof(distinct1, axiom, beethoven != symphony9).
fof(distinct2, axiom, beethoven != vienna_music_society).
fof(distinct3, axiom, symphony9 != vienna_music_society).

fof(music_piece1, axiom, music_piece(symphony9)).
fof(writes1, axiom, writes(beethoven, symphony9)).
fof(premiered1, axiom, premiered(vienna_music_society, symphony9)).
fof(orchestra1, axiom, orchestra(vienna_music_society)).
fof(leads1, axiom, leads(beethoven, vienna_music_society)).

% Rule: any leader of an orchestra is a conductor
fof(rule1, axiom, ! [X,Y] : ((orchestra(Y) & leads(X,Y)) => conductor(X))).

fof(goal, conjecture, ~conductor(beethoven)).