fof(ml_categories, axiom, ! [X] : (ml_algo(X) <=> (supervised(X) | unsupervised(X) | reinforcement(X)))).
fof(disjoint_categories, axiom, ! [X] : (
    (supervised(X) => (~unsupervised(X) & ~reinforcement(X))) &
    (unsupervised(X) => ~reinforcement(X))
)).
fof(unsupervised_no_labels, axiom, ! [X] : (unsupervised(X) => ~requires_labeled_data(X))).
fof(sota_trained_with_ml, axiom, ? [A] : (ml_algo(A) & trained_with(sota_model, A))).
fof(sota_not_reinforcement, axiom, ! [A] : (trained_with(sota_model, A) => ~reinforcement(A))).
fof(sota_requires_labels, axiom, ! [A] : (trained_with(sota_model, A) => requires_labeled_data(A))).
fof(goal, conjecture, ~? [A] : (trained_with(sota_model, A) & supervised(A))).