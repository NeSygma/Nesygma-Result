fof(no_digital_are_analog, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(every_printed_text_is_analog, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(all_streaming_services_are_digital, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(hardcover_book_is_printed_text, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(streaming_service_1984_implies_hardcover_book, axiom, streaming_service(obj_1984) => hardcover_book(obj_1984)).
fof(conjecture, conjecture, streaming_service(obj_1984)).