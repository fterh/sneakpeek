import dateutil.parser
import datetime
import time
import re
import requests

from bs4 import BeautifulSoup

from comment import Comment
from difflib import SequenceMatcher
from handlers.AbstractBaseHandler import AbstractBaseHandler, HandlerError
from newspaper import Article
from nltk.util import ngrams
import codecs

class STHandler(AbstractBaseHandler):
    soup = None
    url = None
    title = None
    MAX_DAYS_OFFSET = 2
    MAX_CURLS_ALLOWED = 5
    MIN_PASSING_SCORE = 0.5
    SLEEP_BETWEEN_CURLS = 1
    ST_PUBLISH_CUTOFF_HOUR = 5
    MODERATED_MAX = 0.8 # we don't want perfect scores overwhelming

    @classmethod
    def handle(cls, url):
        cls.url = url
        cls.soup = cls.makeSoup()
        return cls.handlePremium() if cls.isPremiumArticle() else cls.handleNonPremium()

    @classmethod
    def makeSoup(cls):
        html = requests.get(cls.url).text
        soup = BeautifulSoup(html, "html.parser")
        cls.soup = soup
        return soup

    @classmethod
    def isPremiumArticle(cls):
        html = requests.get(cls.url).text
        elem = cls.soup.find(name="div", class_="paid-premium st-flag-1")
        return elem is not None

    @classmethod
    def handleNonPremium(cls):

        article = Article(cls.url)
        article.download()
        article.parse()

        title = article.title
        body = article.text

        return Comment(title, body)

    @classmethod
    def handlePremium(cls):
        cls.title = cls.soup.find(name="meta", property="og:title")['content']
        print(f"article title: {cls.title}")

	# An article may run for multiple days or be published a day or two later
        for days_offset in range(0, cls.MAX_DAYS_OFFSET):
            # Trying to find a scraped article with the closest title/body to the submission
            possibleMatchingArticles = cls.generateTodaysArticles(days_offset)
            closestArticle = cls.getMatchingArticle(possibleMatchingArticles)
            if closestArticle is not None:
                return closestArticle

        print(f"unable to find a suitable article that matches {cls.title}, skipping submission")
        return None

    @classmethod
    def generateTodaysArticles(cls, days_offset):
        articlesList = BeautifulSoup(cls.getArticlesIndex(days_offset), "html.parser")
        articles = articlesList.findAll(name="a")
        scoredArticles = [( article, cls.similar(article.text, cls.title)) for article in articles]

        # sorted such that scoredArticles[0] has the best chance of being the article we want
        scoredArticles =  sorted(scoredArticles, key=lambda x: x[1], reverse=True)

        return scoredArticles

    @classmethod
    def getMatchingArticle(cls, scoredArticles):

        # every article in scoredArticles has a chance of being the article we want
        # with scoredArticles[0] being the most likely and the last element being the least
        # due to rate limits we cannot check all of the articles

        articlesCheckedSoFar = 0
        while articlesCheckedSoFar < cls.MAX_CURLS_ALLOWED and len(scoredArticles) > 0:
            currArticle = scoredArticles.pop(0)
            currComment = cls.makeComment(currArticle[0]['href'])
            previewComment = cls.handleNonPremium()

            if cls.articleBodiesMatch(previewComment.body, currComment.body):
                return currComment

            articlesCheckedSoFar = articlesCheckedSoFar + 1
            time.sleep(cls.SLEEP_BETWEEN_CURLS)

    @classmethod
    def articleBodiesMatch(cls, previewBody, articleBody):
        # the higher the score, the better confidence that previewBody is a subset of articleBody
        score = 0
        for sentence in cls.split_into_sentences(previewBody):
            weight = len(sentence) / float(len(previewBody)) #longer sentences carry more weight
            score = score +  cls.isNeedleInHay(needle=sentence, hay=articleBody) * weight
        return score > cls.MIN_PASSING_SCORE

    @classmethod
    def makeComment(cls, bestCandidate):
        url = f"https://www.pressreader.com{bestCandidate}"
        article = Article(url, browser_user_agent = "Googlebot-News", keep_article_html=True)
        article.download()
        try:
            article.parse()
        except:
            return Comment('','')

        title = article.title.replace("\xad", "") # clean the text
        body = article.text.replace("\xad", "") # clean the text

        print(f"checking the article in this url: {url} with title {title}")
        return Comment(title, body)

    @classmethod
    def getArticlesIndex(cls, days_offset):
        publishedDate = cls.getDate(days_offset)
        userAgent = "Googlebot-News"
        url = f"https://www.pressreader.com/singapore/the-straits-times/{publishedDate}"
        headers = { "User-Agent": userAgent }
        articlesList = requests.get(url, headers=headers).text
        articlesList = articlesList.replace("&#173;", "") # clean the text
        return articlesList


    @classmethod
    def getDate(cls, days_offset):
        elem = cls.soup.find(name="meta", property="article:published_time")
        rawDateTime = elem['content']
        dateTime = dateutil.parser.parse(rawDateTime) + datetime.timedelta(days=days_offset)
        # articles published after the cutoff hour will only appear in the next days index
        if dateTime.hour > cls.ST_PUBLISH_CUTOFF_HOUR:
            dateTime = dateTime + datetime.timedelta(days=1)
        return dateTime.strftime('%Y%m%d')

    # is candidate title "similar" to title?
    # some fuzzy matching is used
    # returns 0 <= score <= 1
    # higher score is more similar
    @classmethod
    def similar(cls, candidate, title):
        title = title.lower()
        candidate = candidate.lower()
        articles = ["a", "an", "the"]
        pronouns = ["all", "another", "any", "anybody", "anyone", "anything", "as", "aught", "both", "each", "each", "other", "either", "enough", "everybody", "everyone", "everything", "few", "he", "her", "hers", "herself", "him", "himself", "his", "idem", "it", "its", "itself", "many", "me", "mine", "most", "my", "myself", "naught", "neither", "no", "one", "nobody", "none", "nothing", "nought", "one", "one", "another", "other", "others", "ought", "our", "ours", "ourself", "ourselves", "several", "she", "some", "somebody", "someone", "something", "somewhat", "such", "suchlike", "that", "thee", "their", "theirs", "theirself", "theirselves", "them", "themself", "themselves", "there", "these", "they", "thine", "this", "those", "thou", "thy", "thyself", "us", "we", "what", "whatever", "whatnot", "whatsoever", "whence", "where", "whereby", "wherefrom", "wherein", "whereinto", "whereof", "whereon", "wherever", "wheresoever", "whereto", "whereunto", "wherewith", "wherewithal", "whether", "which", "whichever", "whichsoever", "who", "whoever", "whom", "whomever", "whomso", "whomsoever", "whose", "whosever", "whosesoever", "whoso", "whosoever", "ye", "yon", "yonder", "you", "your", "yours", "yourself", "yourselves"]
        prepositions = ["of", "with", "at", "from", "into", "during", "including", "until", "against", "among", "throughout", "despite", "towards", "upon", "concerning", "to", "in", "for", "on", "by", "about", "like", "through", "over", "before", "between", "after", "since", "without", "under", "within", "along", "following", "across", "behind", "beyond", "plus", "except", "but", "up", "out", "around", "down", "off", "above", "near"]
        conjunctions = ["for", "and", "nor", "but", "or", "yet", "so", "after", "although", "as", "as", "if", "as", "long", "as", "as", "much", "as", "as", "soon", "as", "as", "though", "because", "before", "by", "the", "time", "even", "if", "even", "though", "if", "in", "order", "that", "in", "case", "lest", "once", "only", "if", "provided", "that", "since", "so", "that", "than", "that", "though", "till", "unless", "until", "when", "whenever", "where", "wherever", "while", "both", "and", "either", "or", "neither", "nor", "not", "only", "but", "also", "whether", "or"]
        redherrings = ["singapore", "singaporeans", "s'pore", "says", "is", "has", "are", "am", "were", "been", "have", "had", "having"]
        blacklist = set(articles + pronouns + prepositions + conjunctions + redherrings)
        score = 0
        wordsScored = 0

        for word in re.compile("[ '.:\;,.!&\"]").split(candidate):
            if word in blacklist:
                continue
            currScore = cls.isNeedleInHay(needle=word, hay=title)
            currScore = (currScore - 0.5) * 2 # ranges 0.5-1, so normalise to 0-1
            if currScore < 0.5:
                continue
            wordsScored = wordsScored + 1
            score = score + currScore
        if wordsScored > 0:
            finalScore = (score / wordsScored)
        else:
            finalScore = 0
        return cls.MODERATED_MAX if finalScore == 1 else finalScore

    #https://stackoverflow.com/a/31433394
    # fuzzily searches for a needle in a haystack and returns the confidence that needle was found
    @classmethod
    def isNeedleInHay(cls, needle, hay):

        needle_length  = len(needle.split())
        max_sim_val    = 0
        max_sim_string = u""

        for ngram in ngrams(hay.split(), needle_length + int(.2*needle_length)):
            hay_ngram = u" ".join(ngram)
            similarity = SequenceMatcher(None, hay_ngram, needle).ratio()
            if similarity > max_sim_val:
                max_sim_val = similarity
                max_sim_string = hay_ngram

        return max_sim_val # how confident are we that needle was found in hay

    #https://stackoverflow.com/a/31505798
    # given a string paragraph, return a list of sentences
    @classmethod
    def split_into_sentences(cls, text):
        alphabets= "([A-Za-z])"
        prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
        suffixes = "(Inc|Ltd|Jr|Sr|Co)"
        starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
        acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
        websites = "[.](com|net|org|io|gov)"
        text = " " + text + "  "
        text = text.replace("\n"," ")
        text = re.sub(prefixes,"\\1<prd>",text)
        text = re.sub(websites,"<prd>\\1",text)
        if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
        text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
        text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
        text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
        text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
        text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
        text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
        if "”" in text: text = text.replace(".”","”.")
        if "\"" in text: text = text.replace(".\"","\".")
        if "!" in text: text = text.replace("!\"","\"!")
        if "?" in text: text = text.replace("?\"","\"?")
        text = text.replace(".",".<stop>")
        text = text.replace("?","?<stop>")
        text = text.replace("!","!<stop>")
        text = text.replace("<prd>",".")
        sentences = text.split("<stop>")
        sentences = sentences[:-1]
        sentences = [s.strip() for s in sentences]
        return sentences
