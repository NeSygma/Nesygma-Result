% Negative version: negated conclusion as conjecture

% Predicates:
% spill_food(X) - X spills a lot of food on their clothing
% tidy(X) - X is notably tidy
% clumsy_foodie(X) - X is a clumsy foodie who goes out frequently to find new food restaurants to try
% cleanly(X) - X is cleanly
% values_order(X) - X values order and spotlessness
% family_prioritizes(X) - X's family prioritizes order and spotlessness

% Premise 1: If people spill a lot of food on their clothing, then they are not notably tidy.
fof(p1, axiom, ! [X] : (spill_food(X) => ~tidy(X))).

% Premise 2: All clumsy foodies who go out frequently to find new food restaurants to try are people who spill a lot of food on their clothing.
fof(p2, axiom, ! [X] : (clumsy_foodie(X) => spill_food(X))).

% Premise 3: If people are cleanly, then they are notably tidy.
fof(p3, axiom, ! [X] : (cleanly(X) => tidy(X))).

% Premise 4: If people value order and spotlessness, then they are cleanly.
fof(p4, axiom, ! [X] : (values_order(X) => cleanly(X))).

% Premise 5: All people whose families prioritize order and spotlessness themselves value order and spotlessness.
fof(p5, axiom, ! [X] : (family_prioritizes(X) => values_order(X))).

% Premise 6: Peter is either a person who spills a lot of food on his clothing and is cleanly, or a person who does not spill a lot of food on his clothing and is not cleanly.
fof(p6, axiom, ( (spill_food(peter) & cleanly(peter)) | (~spill_food(peter) & ~cleanly(peter)) )).

% Negated conclusion: It is NOT the case that (clumsy_foodie(peter) & family_prioritizes(peter)) | (~clumsy_foodie(peter) & ~family_prioritizes(peter))
% Which is equivalent to: (clumsy_foodie(peter) & ~family_prioritizes(peter)) | (~clumsy_foodie(peter) & family_prioritizes(peter))
fof(neg_conclusion, conjecture, ~( ( (clumsy_foodie(peter) & family_prioritizes(peter)) | (~clumsy_foodie(peter) & ~family_prioritizes(peter)) ) )).