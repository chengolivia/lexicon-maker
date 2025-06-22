import string
from cltk import NLP
from cltk.data.fetch import FetchCorpus
import spacy
from . import SUPPORTED_LANGUAGES

class Stemmer:
    def __init__(self, language):
        if language not in SUPPORTED_LANGUAGES:
            raise Exception(f"Unsupported language chosen: {language}")
        self.language = language
        self.is_modern = SUPPORTED_LANGUAGES[self.language]["is_modern"]
        self.model_key = SUPPORTED_LANGUAGES[self.language]["key"]
        self.modeller = self._load_model()
        # Dry run
        self.count_words_from_text("")

    def _parse_text(self, text):
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = text.replace("\n", "")
        text = text.replace(r"\u", "")
        text = text.replace(r"\x", "")
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.digits))
        text = " ".join(text.split())
        return text

    def _count_words(self, text_arr):
        word_counts = {}
        for word in text_arr:
            if word == "" or word in string.punctuation:
                continue
            if word not in word_counts:
                word_counts[word] = 1
            else:
                word_counts[word] += 1
        return word_counts
    
    def _count_above_thresh(self, word_counts, thresh):
        ret = {}
        for word in word_counts:
            if word_counts[word] >= thresh:
                ret[word] = word_counts[word]
        return dict(sorted(ret.items())) # key=lambda i: i[0].lower()
    
    def count_words_from_text(self, text, thresh=1, use_stems=True):
        text = self._parse_text(text)
        if use_stems:
            text_arr = self.modeller(text)
        else:
            text_arr = text.split()
        counts = self._count_words(text_arr)
        return self._count_above_thresh(counts, thresh)
    
    def _modern_modeller(self, text):
        doc = self.model(text)
        return [token.lemma_ for token in doc]
    
    def _classical_modeller(self, text):
        cltk_doc = self.model.analyze(text=text)
        return cltk_doc.lemmata
    
    def _load_model(self):
        if self.is_modern:
            self.model = spacy.load(self.model_key)
            return self._modern_modeller
        else:
            corpus_downloader = FetchCorpus(language=self.model_key)
            corpus_downloader.import_corpus(SUPPORTED_LANGUAGES[self.language]["corpus"])
            self.model = NLP(language=self.model_key, suppress_banner=True)
            self.model.pipeline.processes.pop(-1)
            return self._classical_modeller
