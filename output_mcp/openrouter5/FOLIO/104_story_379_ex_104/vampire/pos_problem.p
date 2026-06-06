% Positive version: original conclusion as conjecture
% Conclusion: Luke is neither born in a multiple birth nor complains often about annoying siblings.
% i.e., ~multiple_birth(luke) & ~complains_often(luke)

% Predicates:
% multiple_birth(X) - X was born in a multiple birth
% siblings_together(X) - X has siblings who were born together
% hangs_out(X) - X spends a lot of time hanging out with and playing with siblings
% complains_often(X) - X complains often about annoying siblings
% lives_at_home(X) - X lives at home
% lives_with_strangers(X) - X lives with strangers

fof(premise1, axiom, ! [X] : (multiple_birth(X) => hangs_out(X))).
fof(premise2, axiom, ! [X] : (siblings_together(X) => multiple_birth(X))).
fof(premise3, axiom, ! [X] : (complains_often(X) => siblings_together(X))).
fof(premise4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise5, axiom, ! [X] : (hangs_out(X) => lives_at_home(X))).
fof(premise6, axiom, 
    ( (multiple_birth(luke) & lives_with_strangers(luke)) 
    | (~multiple_birth(luke) & ~lives_with_strangers(luke)) )).

% Conclusion: Luke is neither born in a multiple birth nor complains often about annoying siblings.
% i.e., ~multiple_birth(luke) & ~complains_often(luke)
fof(conclusion, conjecture, (~multiple_birth(luke) & ~complains_often(luke))).