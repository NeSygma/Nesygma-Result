tff(digital_media_type, type, digital_media: $i > $o).
tff(analog_type, type, analog: $i > $o).
tff(printed_text_type, type, printed_text: $i > $o).
tff(streaming_service_type, type, streaming_service: $i > $o).
tff(hardcover_book_type, type, hardcover_book: $i > $o).

fof(digital_not_analog, axiom, ! [X: $i] : (digital_media(X) => ~analog(X))).
fof(printed_text_is_analog, axiom, ! [X: $i] : (printed_text(X) => analog(X))).
fof(streaming_is_digital, axiom, ! [X: $i] : (streaming_service(X) => digital_media(X))).
fof(hardcover_is_printed, axiom, ! [X: $i] : (hardcover_book(X) => printed_text(X))).
fof(conditional_1984, axiom, streaming_service(1984) => hardcover_book(1984)).
fof(goal_negation, conjecture, ~streaming_service(1984)).