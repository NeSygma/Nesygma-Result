fof(axiom_1, axiom, music_piece(sym9)).
fof(axiom_2, axiom, writes(beethoven, sym9)).
fof(axiom_3, axiom, premiered(vms, sym9)).
fof(axiom_4, axiom, orchestra(vms)).
fof(axiom_5, axiom, leads(beethoven, vms)).
fof(axiom_6, axiom, ! [X] : (orchestra(X) => ? [C] : (conductor(C) & leads(C, X)))).
fof(conjecture, conjecture, conductor(beethoven)).