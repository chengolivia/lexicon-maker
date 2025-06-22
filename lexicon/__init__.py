SUPPORTED_LANGUAGES = {
    "german": {
        "display_name": "German",
        "is_modern": True,
        "key": "de_core_news_sm",
        "corpus": None,
    },
    "latin": {
        "display_name": "Latin",
        "is_modern": False,
        "key": "lat",
        "corpus": "lat_models_cltk",
    }
}

from .stemmer import Stemmer
__all__ = ['Stemmer']
