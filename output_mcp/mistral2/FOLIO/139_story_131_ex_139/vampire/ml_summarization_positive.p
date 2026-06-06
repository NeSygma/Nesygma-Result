fof(categorization, axiom,
    ! [A] : (ml_algorithm(A) =>
             (supervised_learning(A) | unsupervised_learning(A) | reinforcement_learning(A)))).

fof(unsupervised_no_labeled_data, axiom,
    ! [A] : (unsupervised_learning(A) => ~requires_labeled_data(A))).

fof(state_of_the_art_trained_with_ml, axiom,
    ? [A] : (ml_algorithm(A) & is_trained_with(A, state_of_the_art_summarization_model))).

fof(no_reinforcement_learning_used, axiom,
    ! [A] : (reinforcement_learning(A) => ~is_trained_with(A, state_of_the_art_summarization_model))).

fof(ml_requires_labeled_data, axiom,
    ! [A] : (is_trained_with(A, state_of_the_art_summarization_model) => requires_labeled_data(A))).

fof(conjecture, conjecture,
    ? [A] : (unsupervised_learning(A) & is_trained_with(A, state_of_the_art_summarization_model))).