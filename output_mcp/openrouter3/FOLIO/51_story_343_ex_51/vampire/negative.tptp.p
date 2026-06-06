% Negative file: Premises + negated conclusion as conjecture
fof(no_digital_analog, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(printed_is_analog, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(streaming_is_digital, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(hardcover_is_printed, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(conditional_1984, axiom, streaming_service(nineteen84) => hardcover_book(nineteen84)).
fof(goal_negation, conjecture, streaming_service(nineteen84)).