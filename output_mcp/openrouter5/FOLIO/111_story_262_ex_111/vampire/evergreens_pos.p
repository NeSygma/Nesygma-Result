% Positive version: original conclusion as conjecture
% Premise 1: All fir trees are evergreens.
fof(premise1, axiom, ! [X] : (fir_tree(X) => evergreen(X))).
% Premise 2: Some objects of worship are fir trees.
fof(premise2, axiom, ? [X] : (object_of_worship(X) & fir_tree(X))).
% Conclusion: Some evergreens are not objects of worship.
fof(conclusion, conjecture, ? [X] : (evergreen(X) & ~object_of_worship(X))).