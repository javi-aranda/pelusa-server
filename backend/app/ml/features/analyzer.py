import re
import logging
import math
import idna
import tldextract

logger = logging.getLogger(__name__)

SUSPICIOUS_KEYWORDS = [
    'validateaccount', 
    'paymentupdate', 
    'account', 
    'confirm', 
    'accountactivation', 
    'bankingonline', 
    'profile', 
    'confirmemail', 
    'update', 
    'account_recovery', 
    'updateprofile', 
    'account.php', 
    'auth', 
    'verifyaccount', 
    'clientarea', 
    'accountupdate', 
    'appleid', 
    'banking', 
    'accountinfo', 
    'change', 
    'support', 
    'validateinfo', 
    'user', 
    'verifyinfo', 
    'paypal', 
    'validate', 
    'payment', 
    'verifyaccountinfo', 
    'verification', 
    'customer', 
    'recover', 
    'login', 
    'userprofile', 
    'login.php', 
    'verifyuser', 
    'client', 
    'verify', 
    'customercenter', 
    'verifyidentity', 
    'secure.php', 
    'loginvalidate', 
    'validateuser', 
    'authorize', 
    'validate.php', 
    'accountservices', 
    'password', 
    'recover_account', 
    'change_password', 
    'secure', 
    'bank', 
    'billing', 
    'identity', 
    'signin', 
    'authenticate', 
    'redirect', 
    'email_verification', 
    'security', 
    'verifyemail', 
    'securelogin', 
    'transaction', 
    'reset', 
    'signin.php'
]

SUSPICIOUS_KEYWORDS_PATTERN = '|'.join(map(re.escape, SUSPICIOUS_KEYWORDS))

SHORTENED_URL_PATTERN = re.compile(r'https?://(bit\.ly|t\.co|tinyurl\.com|ow\.ly|is\.gd|j\.mp|cli\.gs|v\.gd|tr\.im|su\.pr|fur\.ly|ad\.foc\.us|ff\.im|zz\.gy|x\.co|t2m\.io|to\.ly|twit\.li|u\.to|1url\.com|2\.gly|4\.ms|4sq\.com|7\.ly|8u\.at|amzn\.to|amzn\.com|ar\.gy|azc\.cc|b2l\.me|bacn\.me|bcool\.bz|binged\.it|bizj\.us|bloat\.me|br\.tr|bsa\.ly|budurl\.com|canurl\.com|chilp\.it|cl\.ly|clck\.ru|cliccami\.info|clickthru\.ca|clop\.in|conta\.cc|cort\.as|cot\.ag|crks\.me|ctvr\.us|cutt\.us|dai\.ly|decenturl\.com|dfl8\.me|digbig\.com|digg\.com|dwarfurl\.com|easyurl\.net|eepurl\.com|eweri\.com|fa\.by|fav\.me|fb\.me|fb\.my|flic\.kr|flq\.us|fly2\.ws|fon\.gs|freak\.to|fuseurl\.com|fw\.am|g\.roov\.es|giz\.mo|gl\.am|go2\.do|go2\.me|go2\.pl|goe\.sc|gonze\.com|gr8\.com|gurl\.es|h\.ling\.ca|huff\.to|hulu\.me|hurl\.me|idek\.net|ilix\.in|is\.gd|j\.mp|jijr\.com|kl\.am|klck\.me|korta\.nu|krunchd\.com|l9k\.net|lat\.ms|li\.im|lil\.im|linkbee\.com|link\.to|lnk\.co|lnk\.gs|lnkd\.in|lnk\.ms|lnkmy\.com|loopt\.us|lru\.com|lt\.tl|m\.e|macte\.ch|mash\.to|merky\.de|migre\.me|miniurl\.com|minu\.me|moourl\.com|murl\.com|myloc\.me|myurl\.in|n\.bc|n\.pr|n\.sa|n\.xy|ncane\.com|ning\.com|nn\.nu|notlong\.com|nsfw\.in|nutshellurl\.com|nxy\.in|nyti\.ms|o-x\.fr|oc\.1e\.na|om\.ly|omf\.g\.s|on\.fb\.me|onforb\.es|orz\.se|ow\.ly|ping\.fm|pli\.de|pnt\.me|politi\.co|post\.ly|pp\.gg|profile\.to|pt\.sw|pub\.vu|ql\.nk|qte\.me|qu\.mi|qy\.fi|r\.efer\.me|rb\.g\.s|readthis\.ca|reallytinyurl\.com|redir\.ec|redirects\.ca|retwt\.me|ri\.url|rick\.roll\.fr|rurl\.org|rz\.my|s4c\.in|s7y\.us|safe\.mn|sameurl\.at|sdut\.us|sh\.rt|shar\.es|shink\.in|shorl\.com|short\.ie|short\.to|shorten\.com|shrinkify\.com|shw\.me|simurl\.com|sk\.gy|sk\.im|sk\.ty|slash\.gd|small\.io|smsh\.me|smurl\.name|snipurl\.com|sn\.im|sn\.vc|spedr\.com|srnk\.net|sr\.vc|su\.pr|surl\.co|s\.url\.in|t\.co|t9y\.me|tak\.my|ta\.tc|tbd\.ly|tcrn\.ch|tgr\.pa|tgr\.ph|tight\.url|tik\.ly|tinurl\.us|tiny\.cc|tinyurl\.com|tk\.gd|tl\.gd|tmi\.me|tnij\.org|tnw\.to|tny\.com|to\.ly|totc\.us|to\.purl|tou\.ch|tpm\.ly|tr\.im|tra\.ck\.us|trg\.fr|tr\.im|trunc\.it|twhub\.com|twirl\.at|twit\.ac|twit\.this|twit\.xr|twtr\.to|u\.bb|u\.mavrev\.com|u\.mgeek\.com|u\.mrs\.w|u\.nclic\.io|u\.nu|u\.rl|ub0\.cc|ulu\..lu|updating\.me|ur1\.ca|urlborg\.com|url\.co|urlcover\.com|urlcutter\.com|urld\.it|urlenco\.de|urli\.nl|urls\.im|urlshorteningservicefortwitter\.com|urlvis\.com|urz\.fr|usat\.ly|usefulshortcuts\.com|vb\.ly|vevo\.ly|vgn\.am|vl\.am|vzturl\.com|wapo\.st|wapurl\.co|wipi\.es|wp\.me|x\.co|xrl\.us|xr\.com|xrl\.in|xrl\.us|yfrog\.com|yfrog\.us|yhoo\.it|youtu\.be|yuarel\.com|zen\.gd|zi\.ma|zi\.p\.my|zi\.ud\.com|zud\.us|zurl\.ws|zz\.gd)/[a-zA-Z0-9]+')


class StaticURLAnalyzer:

    def __init__(self, url):
        self.url = url

    def extract_info(self):
        info = {}

        info['url_fragments'] = self.count_url_fragments()
        info['numeric_domain'] = self.has_numeric_domain()
        info['domain_length'] = self.get_domain_length()
        info['path_length'] = self.get_path_length()
        info['percent_chars'] = self.count_percent_chars()
        info['at_chars'] = self.count_at_chars()
        info['dash_chars'] = self.count_dash_chars()
        info['and_chars'] = self.count_and_chars()
        info['equal_chars'] = self.count_equal_chars()
        info['shannon_entropy'] = self.shannon_entropy()
        info['domain_name'] = self.get_domain()
        info['excessive_subdomains'] = self.has_excessive_subdomains()
        info['tld'] = self.get_tld()
        info['punycode'] = self.has_punycode()
        info['question_chars'] = self.count_question_chars()
        info['plus_chars'] = self.count_plus_chars()
        info['underscore_chars'] = self.count_underscore_chars()
        info['suspicious_keywords'] = self.has_suspicious_keywords()
        info['shortened_url'] = self.is_shortened_url()

        return info
    
    
    def get_domain(self):
        if '://' in self.url:
            return self.url.split('://')[1].split('/')[0]
        return self.url.split('/')[0]
    
    def count_url_fragments(self):
        return len(self.url.split('/'))

    def has_numeric_domain(self):
        domain = self.get_domain()
        return bool(re.search(r'\d', domain))
    
    def get_domain_length(self):
        domain = self.get_domain()
        return len(domain)
    
    def get_path_length(self):
        if len(self.url.split('/')) < 4:
            return 0
        return len(self.url.split('/')[3])
    
    def count_percent_chars(self):
        return self.url.count('%')
    
    def count_at_chars(self):
        return self.url.count('@')
    
    def count_dash_chars(self):
        return self.url.count('-')
    
    def count_and_chars(self):
        return self.url.count('&')
    
    def count_equal_chars(self):
        return self.url.count('=')
    
    def shannon_entropy(self):
        domain = self.get_domain()
        if not domain:
            return 0

        prob = [float(domain.count(c)) / len(domain) for c in set(domain)]
        entropy = -sum(p * math.log2(p) for p in prob)
        return entropy
    
    def has_excessive_subdomains(self):
        domain = self.get_domain()
        subdomains = domain.split('.')
        return len(subdomains) >= 3

    def get_tld(self):
        domain = self.get_domain()
        return tldextract.extract(domain).suffix
    
    def has_punycode(self):
        domain = self.get_domain()
        try:
            idna.decode(domain)
            return True
        except (idna.IDNAError, UnicodeError):
            return False
        
    def has_suspicious_keywords(self):
        return bool(re.search(SUSPICIOUS_KEYWORDS_PATTERN, self.url))
    
    def is_shortened_url(self):
        return bool(re.search(SHORTENED_URL_PATTERN, self.url))
    
    def count_question_chars(self):
        return self.url.count('?')
    
    def count_plus_chars(self):
        return self.url.count('+')
    
    def count_underscore_chars(self):
        return self.url.count('_')
