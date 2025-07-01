from string import digits

PHONE_PUNCTUATION = r".()- "
PHONE_TRANSLATION_TABLE = str.maketrans("", "", PHONE_PUNCTUATION)


def clean_nanp_phone(phone_input, error_to_raise):
    """Validate NANP Telephone Numbers

    https://en.wikipedia.org/wiki/North_American_Numbering_Plan#Modern_plan

    Telephone numbers have the following form: NXX-NXX-XXXX per the "North
    American Numbering Plan"

    - Exactly 10 digits
    - N must be 2-9
    - X may be 0-9 with some exceptions.

    Additional rules:

    - First NXX is the area code.
        - Reserved and non-geographic codes.
            - NXX where the two X are identical, reserved for non-geographic
                use. 911, 988, 800, etc.
            - N90-N99 are reserved for expansion.
            - 370-379, 960-969 are reserved for expansion.
            - 880-889 are reserved for toll-free use.
            - 950 is reserved for usage of prepaid calling cards.
            - 958, 959 are reserved for system testing.
    - Second NXX is the prefix (or exchange).
        - Prefixes of the form N11 were reserved for "Easily Recognizable
            Codes" during the transition to the modern plan and, while we must
            dial with 10 digits now, this rule has stuck around.
        - Prefix 555 has a block of line numbers reserved for fictional use.
            Only two line numbers (1212, 4334) are currently in use, the
            others are reserved until a need is approved by the Industry
            Numbering Committee:
            https://www.nanpa.com/numbering/555-line-numbers. We can reject
            any of these numbers at this time.
    - XXXX is the line number. There are no restrictions.
    """

    GENERAL_ERROR_MSG = (
        "Please enter a 10-digit North American phone number without the 1."
        " Spaces and the following punctuation are allowed: ().-"
    )

    if not isinstance(phone_input, str) or phone_input == "":
        raise error_to_raise(GENERAL_ERROR_MSG)

    if not _is_phone_input_only_allowed_characters(phone_input):
        raise error_to_raise(GENERAL_ERROR_MSG)

    phone_input = _remove_punctuation_and_space(phone_input)

    if len(phone_input) != 10:
        raise error_to_raise(GENERAL_ERROR_MSG)

    area_code = phone_input[:3]
    if not _is_phone_area_code_valid(area_code):
        AREA_CODE_ERROR_MSG = (
            "Please ensure your phone number has a valid area code."
            " Area codes cannot start with 0 or 1,"
            " cannot have the second digit be 9,"
            " and cannot have the second and third digit be the same."
        )
        raise error_to_raise(AREA_CODE_ERROR_MSG)

    prefix = phone_input[3:6]
    if not _is_phone_prefix_valid(prefix):
        PREFIX_ERROR_MESSAGE = (
            "Please ensure your three-digit prefix (exchange) is valid."
            " Prefixes cannot start with 0 or 1, cannot be 555,"
            " and cannot have the second and third digit both be 1."
        )
        raise error_to_raise(PREFIX_ERROR_MESSAGE)

    return phone_input


def _is_phone_input_only_allowed_characters(v):
    return set(v) <= set(PHONE_PUNCTUATION + digits)


def _remove_punctuation_and_space(v):
    return v.translate(PHONE_TRANSLATION_TABLE)


def _is_phone_area_code_valid(v):
    return _is_phone_nanp_n_digit_valid(v) and _is_phone_area_code_geographic(v)


def _is_phone_area_code_geographic(v):
    return not (
        _is_phone_area_code_easily_recognizable(v)
        or v[1] == "9"  # Reserved for 12-digit expansion plan
        or v[:2] in ("37", "88", "96")  # Reserved for non-geographic use
        or v in ("950", "958", "959")  # Reserved for non-geographic use
    )


def _is_phone_area_code_easily_recognizable(v):
    return v[1] == v[2]


def _is_phone_prefix_valid(v):
    return (
        _is_phone_nanp_n_digit_valid(v)
        and not _is_phone_prefix_easily_recognizable(v)
        and not _is_phone_prefix_reserved(v)
    )


def _is_phone_prefix_reserved(v):
    return v == "555"  # Reserved for special use


def _is_phone_prefix_easily_recognizable(v):
    return v[1] == "1" and v[2] == "1"


def _is_phone_nanp_n_digit_valid(v):
    return v[0] not in ("0", "1")
