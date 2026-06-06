fof(all_ml_are_categories, axiom,
    ! [A] : (ml_algo(A) =>
             (category(A, supervised) |
              category(A, unsupervised) |
              category(A, reinforcement)))).

fof(unsupervised_no_labeled, axiom,
    ! [A] : (category(A, unsupervised) => ~requires_labeled_data(A))).

fof(model_trained_with_ml, axiom,
    ? [A] : (ml_algo(A) & trained_with(A, text_sum_model))).

fof(no_reinforcement_for_model, axiom,
    ! [A] : (category(A, reinforcement) => ~trained_with(A, text_sum_model))).

fof(ml_for_model_needs_labeled, axiom,
    ? [A] : (ml_algo(A) & trained_with(A, text_sum_model) & requires_labeled_data(A))).

fof(conclusion_negation, conjecture,
    ~ ? [A] : (category(A, unsupervised) & trained_with(A, text_sum_model))).