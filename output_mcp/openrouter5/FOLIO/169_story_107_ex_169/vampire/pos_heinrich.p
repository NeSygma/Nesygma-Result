% Positive version: original conclusion as conjecture
% Conclusion: No politicians are part of the Nazi Reichstag.
% i.e., ! [X] : (politician(X) => ~member_of_nazi_reichstag(X))

fof(premise_1, axiom, german_politician(heinrich_schmidt)).
fof(premise_2, axiom, member_of_prussian_parliament(heinrich_schmidt)).
fof(premise_3, axiom, member_of_nazi_reichstag(heinrich_schmidt)).

% If Heinrich Schmidt is a German politician, then he is a politician.
fof(politician_def, axiom, ! [X] : (german_politician(X) => politician(X))).

% Conclusion: No politicians are part of the Nazi Reichstag.
fof(goal, conjecture, ! [X] : (politician(X) => ~member_of_nazi_reichstag(X))).