% Positive version: original conclusion as conjecture
% Predicates:
% spills_food(X) - X spills a lot of food on their clothing
% notably_tidy(X) - X is notably tidy
% clumsy_foodie(X) - X is a clumsy foodie
% goes_out_frequently(X) - X goes out frequently to find new food restaurants
% cleanly(X) - X is cleanly
% values_order(X) - X values order and spotlessness
% family_prioritizes_order(X) - X's family prioritizes order and spotlessness

fof(premise1, axiom, ! [X] : (spills_food(X) => ~notably_tidy(X))).
fof(premise2, axiom, ! [X] : ((clumsy_foodie(X) & goes_out_frequently(X)) => spills_food(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(premise4, axiom, ! [X] : (values_order(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritizes_order(X) => values_order(X))).
fof(premise6, axiom, (spills_food(peter) & cleanly(peter)) | (~spills_food(peter) & ~cleanly(peter))).

% Conclusion: Peter is either a clumsy foodie who goes out frequently OR someone whose family prioritizes order and spotlessness
% i.e., (clumsy_foodie(peter) & goes_out_frequently(peter)) | family_prioritizes_order(peter)
fof(conclusion, conjecture, (clumsy_foodie(peter) & goes_out_frequently(peter)) | family_prioritizes_order(peter)).