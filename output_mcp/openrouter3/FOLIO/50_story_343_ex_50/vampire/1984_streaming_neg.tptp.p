% Negative file: Premises + negated conclusion as conjecture (TFF version)
tff(item_type, type, item: $tType).
tff(digital_media_decl, type, digital_media: item > $o).
tff(analog_media_decl, type, analog_media: item > $o).
tff(printed_text_decl, type, printed_text: item > $o).
tff(streaming_service_decl, type, streaming_service: item > $o).
tff(hardcover_book_decl, type, hardcover_book: item > $o).
tff(const_1984_decl, type, const_1984: item).

tff(no_digital_analog, axiom, ! [X: item] : (digital_media(X) => ~analog_media(X))).
tff(printed_is_analog, axiom, ! [X: item] : (printed_text(X) => analog_media(X))).
tff(streaming_is_digital, axiom, ! [X: item] : (streaming_service(X) => digital_media(X))).
tff(hardcover_is_printed, axiom, ! [X: item] : (hardcover_book(X) => printed_text(X))).
tff(conditional_1984, axiom, streaming_service(const_1984) => hardcover_book(const_1984)).
tff(goal_negation, conjecture, ~streaming_service(const_1984)).