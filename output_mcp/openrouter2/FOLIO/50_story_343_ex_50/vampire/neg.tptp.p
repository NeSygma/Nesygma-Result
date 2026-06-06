fof(no_digital_analog, axiom, ![X] : (digital_media(X) => ~analog_media(X))).
fof(printed_analog, axiom, ![X] : (printed_text(X) => analog_media(X))).
fof(streaming_digital, axiom, ![X] : (streaming_service(X) => digital_media(X))).
fof(hardcover_printed, axiom, ![X] : (hardcover_book(X) => printed_text(X))).
fof(streaming_to_hardcover, axiom, streaming_service(obj_1984) => hardcover_book(obj_1984)).
fof(conjecture, conjecture, ~streaming_service(obj_1984)).