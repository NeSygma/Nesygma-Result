tff(digital_media_type, type, digital_media: $int > $o).
tff(analog_media_type, type, analog_media: $int > $o).
tff(printed_text_type, type, printed_text: $int > $o).
tff(streaming_service_type, type, streaming_service: $int > $o).
tff(hardcover_book_type, type, hardcover_book: $int > $o).

fof(no_digital_analog_overlap, axiom, ! [X: $int] : (digital_media(X) => ~analog_media(X))).
fof(printed_text_is_analog, axiom, ! [X: $int] : (printed_text(X) => analog_media(X))).
fof(streaming_is_digital, axiom, ! [X: $int] : (streaming_service(X) => digital_media(X))).
fof(hardcover_is_printed, axiom, ! [X: $int] : (hardcover_book(X) => printed_text(X))).
fof(conditional_1984, axiom, streaming_service(1984) => hardcover_book(1984)).
fof(negated_conclusion, conjecture, streaming_service(1984)).