fof(multiple_birth_implies_hangs_out, axiom, ! [X] : (multiple_birth(X) => hangs_out_with_siblings(X))).
fof(has_sibling_implies_multiple_birth, axiom, ! [X] : (has_sibling(X) => multiple_birth(X))).
fof(complains_annoying_siblings_implies_has_sibling, axiom, ! [X] : (complains_annoying_siblings(X) => has_sibling(X))).
fof(lives_at_home_implies_not_lives_with_strangers, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(hangs_out_implies_lives_at_home, axiom, ! [X] : (hangs_out_with_siblings(X) => lives_at_home(X))).
fof(luke_situation, axiom, ( (baby(luke) & multiple_birth(luke) & lives_with_strangers(luke)) | ( ~baby(luke) & ~multiple_birth(luke) & ~lives_with_strangers(luke) ) ) ).
fof(conclusion, conjecture, ~hangs_out_with_siblings(luke)).