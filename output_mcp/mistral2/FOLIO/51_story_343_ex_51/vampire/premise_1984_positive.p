fof(no_digital_analog_overlap, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(printed_text_is_analog, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(streaming_is_digital, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(hardcover_is_printed, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(conditional_1984, axiom, streaming_service(1984) => hardcover_book(1984)).
fof(conclusion, conjecture, ~streaming_service(1984)).