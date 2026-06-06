fof(unsupervised_no_labels, axiom,
    ~requires_labeled_data(unsupervised_learning)).

fof(summarization_trained_by_ml, axiom,
    ? [X] : used_to_train(X, state_of_the_art_text_summarization)).

fof(reinforcement_not_used, axiom,
    ~used_to_train(reinforcement_learning, state_of_the_art_text_summarization)).

fof(summarization_requires_labels, axiom,
    ! [X] : (used_to_train(X, state_of_the_art_text_summarization)
             => requires_labeled_data(X))).

fof(ml_categories, axiom,
    ! [X] : (used_to_train(X, state_of_the_art_text_summarization) =>
        (X = supervised_learning | X = unsupervised_learning | X = reinforcement_learning))).

fof(distinct_categories, axiom,
    (supervised_learning != unsupervised_learning &
     supervised_learning != reinforcement_learning &
     unsupervised_learning != reinforcement_learning)).

fof(goal, conjecture,
    used_to_train(supervised_learning, state_of_the_art_text_summarization)).