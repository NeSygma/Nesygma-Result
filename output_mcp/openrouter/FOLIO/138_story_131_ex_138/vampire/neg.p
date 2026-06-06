fof(cat_exhaustive, axiom, ! [A] : (supervised(A) | unsupervised(A) | reinforcement(A))).
fof(cat_exclusive1, axiom, ! [A] : (supervised(A) => ~unsupervised(A))).
fof(cat_exclusive2, axiom, ! [A] : (supervised(A) => ~reinforcement(A))).
fof(cat_exclusive3, axiom, ! [A] : (unsupervised(A) => ~reinforcement(A))).
fof(unsup_no_label, axiom, ! [A] : (unsupervised(A) => ~requires_labeled_data(A))).
fof(exist_trains, axiom, ? [A] : trains(sota_model, A)).
fof(reinf_not_used, axiom, ! [A] : (reinforcement(A) => ~trains(sota_model, A))).
fof(trains_requires_label, axiom, ! [A] : (trains(sota_model, A) => requires_labeled_data(A))).
fof(goal, conjecture, ~(? [A] : (supervised(A) & trains(sota_model, A)))).