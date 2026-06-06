% Positive file: Original conclusion as conjecture
% Predicates:
% spills_lot(X) - X spills a lot of food on their clothing
% notably_tidy(X) - X is notably tidy
% clumsy_foodie(X) - X is a clumsy foodie
% goes_out_frequently(X) - X goes out frequently to find new food restaurants
% cleanly(X) - X is cleanly
% values_order_spotless(X) - X values order and spotlessness
% family_prioritizes(X) - X's family prioritizes order and spotlessness

fof(premise1, axiom, ! [X] : (spills_lot(X) => ~notably_tidy(X))).
fof(premise2, axiom, ! [X] : ((clumsy_foodie(X) & goes_out_frequently(X)) => spills_lot(X))).
fof(premise3, axiom, ! [X] : (cleanly(X) => notably_tidy(X))).
fof(premise4, axiom, ! [X] : (values_order_spotless(X) => cleanly(X))).
fof(premise5, axiom, ! [X] : (family_prioritizes(X) => values_order_spotless(X))).
fof(premise6, axiom, ((spills_lot(peter) & cleanly(peter)) | (~spills_lot(peter) & ~cleanly(peter)))).

fof(conclusion, conjecture, ((clumsy_foodie(peter) & goes_out_frequently(peter)) | family_prioritizes(peter))).