fof(digital_not_analog, axiom, ! [X] : (digital_media(X) => ~analog(X))).
fof(printed_text_is_analog, axiom, ! [X] : (printed_text(X) => analog(X))).
fof(streaming_is_digital, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(hardcover_is_printed, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(conditional_1984, axiom, streaming_service(1984) => hardcover_book(1984)).
fof(goal_negation, conjecture, ~streaming_service(1984)).