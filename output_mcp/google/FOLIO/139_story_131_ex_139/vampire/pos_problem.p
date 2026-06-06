fof(ml_categories, axiom, ! [X] : (ml_algo(X) <=> (supervised(X) | unsupervised(X) | reinforcement(X)))).
fof(unsupervised_no_labels, axiom, ! [X] : (unsupervised(X) => ~requires_labeled_data(X))).
fof(sota_uses_ml, axiom, ? [X] : (ml_algo(X) & used_for_sota(X))).
fof(sota_not_reinforcement, axiom, ! [X] : (used_for_sota(X) => ~reinforcement(X))).
fof(sota_requires_labels, axiom, ! [X] : (used_for_sota(X) => requires_labeled_data(X))).
fof(goal, conjecture, ? [X] : (unsupervised(X) & used_for_sota(X))).