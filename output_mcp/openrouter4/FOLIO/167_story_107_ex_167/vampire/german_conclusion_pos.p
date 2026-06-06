% Positive file: original claim as conjecture
% Premise 1: Heinrich Schmidt was a German politician
fof(premise1, axiom, german_politician(heinrich_schmidt)).
% If someone is a German politician, they are German
fof(german_politician_implies_german, axiom, ! [X] : (german_politician(X) => german(X))).
% Premise 2: He was a member of the Prussian State Parliament and the Nazi Reichstag
fof(premise2a, axiom, member_of(heinrich_schmidt, prussian_parliament)).
fof(premise2b, axiom, member_of(heinrich_schmidt, nazi_reichstag)).
% Conclusion: Heinrich Schmidt was German or Russian or both
fof(conclusion, conjecture, (german(heinrich_schmidt) | russian(heinrich_schmidt))).