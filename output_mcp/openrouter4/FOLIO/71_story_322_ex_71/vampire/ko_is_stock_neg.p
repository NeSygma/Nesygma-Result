fof(premise1, axiom, ! [X] : (growth_stock(X) => profit_appreciation(X))).
fof(premise2, axiom, ! [X] : (profit_appreciation(X) => ~retirement_suitable(X))).
fof(premise3, axiom, ? [X] : (stock(X) & growth_stock(X))).
fof(premise4, axiom, ! [X] : (mature_stock(X) => retirement_suitable(X))).
fof(premise5, axiom, mature_stock(ko)).
fof(conclusion_neg, conjecture, ~stock(ko)).