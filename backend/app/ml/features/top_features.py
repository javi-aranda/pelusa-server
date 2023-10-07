import numpy as np


def get_available_features():
    return np.array(
        [
            "url_fragments",
            "excessive_subdomains",
            "numeric_domain",
            "domain_length",
            "path_length",
            "percent_chars",
            "at_chars",
            "dash_chars",
            "question_chars",
            "and_chars",
            "equal_chars",
            "underscore_chars",
            "shannon_entropy",
            "suspicious_keywords",
            "shortened_url",
        ]
    )
