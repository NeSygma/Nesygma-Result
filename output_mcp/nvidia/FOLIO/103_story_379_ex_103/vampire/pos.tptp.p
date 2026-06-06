% Axiom 1
fof(axiom1, axiom, ! [X] : ( ? [Y] : born_together(X, Y) => hang_out_with_siblings(X) ) ).
% Axiom 2
fof(axiom2, axiom, ! [X] : ( ? [Y] : born_together(X, Y) => multiple_birth(X) ) ).
% Axiom 3
fof(axiom3, axiom, ! [X] : ( complain_often_about_annoying_siblings(X) => ? [Y] : born_together(X, Y) ) ).
% Axiom 4
fof(axiom4, axiom, ! [X] : ( live_at_home(X) => ~ live_with_strangers(X) ) ).
% Axiom 5
fof(axiom5, axiom, ! [X] : ( hang_out_with_siblings(X) => often_live_at_home(X) ) ).
% Axiom 6
fof(luke_case, axiom, ( (baby_multiple_birth(luke) & live_with_strangers(luke)) | ( ~baby_multiple_birth(luke) & ~live_with_strangers(luke) ) ) ).
% Conjecture
fof(goal, conjecture, complain_often_about_annoying_siblings(luke) ).