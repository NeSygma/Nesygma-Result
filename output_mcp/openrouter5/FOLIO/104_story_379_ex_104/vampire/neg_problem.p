% Negative version: negated conclusion as conjecture
% Original conclusion: ~multiple_birth(luke) & ~complains_often(luke)
% Negated: ~(~multiple_birth(luke) & ~complains_often(luke))
% i.e., multiple_birth(luke) | complains_often(luke)

fof(premise1, axiom, ! [X] : (multiple_birth(X) => hangs_out(X))).
fof(premise2, axiom, ! [X] : (siblings_together(X) => multiple_birth(X))).
fof(premise3, axiom, ! [X] : (complains_often(X) => siblings_together(X))).
fof(premise4, axiom, ! [X] : (lives_at_home(X) => ~lives_with_strangers(X))).
fof(premise5, axiom, ! [X] : (hangs_out(X) => lives_at_home(X))).
fof(premise6, axiom, 
    ( (multiple_birth(luke) & lives_with_strangers(luke)) 
    | (~multiple_birth(luke) & ~lives_with_strangers(luke)) )).

% Negated conclusion: multiple_birth(luke) | complains_often(luke)
fof(neg_conclusion, conjecture, (multiple_birth(luke) | complains_often(luke))).