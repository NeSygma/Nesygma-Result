% Negative: prove streaming_service(1984)
fof(no_digital_are_analog, axiom, ! [X] : (digital_media(X) => ~analog_media(X))).
fof(every_printed_is_analog, axiom, ! [X] : (printed_text(X) => analog_media(X))).
fof(all_streaming_are_digital, axiom, ! [X] : (streaming_service(X) => digital_media(X))).
fof(hardcover_implies_printed, axiom, ! [X] : (hardcover_book(X) => printed_text(X))).
fof(streaming_implies_hardcover, axiom, streaming_service(year_1984) => hardcover_book(year_1984)).
fof(goal, conjecture, streaming_service(year_1984)).