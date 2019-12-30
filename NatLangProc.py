import utilities

def parse_story(file_name):
    """
    Input:
    (String) -> List(String)
    Returns an ordered list of words from input text with white space and bad characters (As defined by bad_chars in utilities) removed.
    >>>parse_story('test_text_parsing.txt') 
    ['the', 'code', 'should', 'handle', 'correctly', 'the', 'following', ':',
    'white', 'space', '.', 'sequences', 'of', 'punctuation', 'marks', '?', '!', '!',
    'periods', 'with', 'or', 'without', 'spaces', ':', 'a', '.', '.', 'a', '.', 'a',
    "don't", 'worry', 'about', 'numbers', 'like', '1', '.', '5', 'remove', 'capitalization']
    """
    with open(file_name , 'r') as input_file:
         words = []   
         for line in input_file:
             whole_line = line.strip()
             whole_line = whole_line.lower()
             for r in whole_line:
                if r in utilities.BAD_CHARS:
                    
                    strtorep = " " + r + " "
                    whole_line = whole_line.replace(r, strtorep)
                elif r in utilities.VALID_PUNCTUATION:
                    
                    strtorep = " " + r + " "
                    whole_line = whole_line.replace(r, strtorep)
             wl_withoutspaces = whole_line.split(" ")
             words += wl_withoutspaces
         words_withoutspaces = []
         for r in words:
            if (not(r in utilities.BAD_CHARS)) and r != "":
                words_withoutspaces.append(r)
         return(words_withoutspaces)
        
def get_prob_from_count(intcount):
    """
    Input:
    List(Num) -> List(Num)
    Returns list of probabilities derived from a list of counts and occurences of a token.
    >>> get_prob_from_count([10, 20, 40, 30])
    [0.1, 0.2, 0.4, 0.3]
    """
    x = 0
    for r in intcount:
        x += r
    for a in range(0,len(intcount)):
        intcount[a] = intcount[a]/x
    return intcount

def build_ngram_counts(p, n):
    """
    Input:
    (List(string), num) -> Dictionary
    Returns a dictionary of Ngrams. Also records which words follow the ngram and how many duplicates there are
    >>> words = [‘the’, ‘child’, ‘will’, ‘go’, ‘out’, ‘to’, ‘play’, ‘,’, ‘and’, ‘the’, ‘child’, ‘can’, ‘not’, ‘be’, ‘sad’, ‘anymore’, ‘.’]
    >>> build_ngram_counts(words, 2)
    { (‘the’, ‘child’): [[‘will’, ‘can’], [1, 1]], (‘child’, ‘will’): [[‘go’], [1]],
    (‘will’, ‘go’): [[‘out’], [1]],  (‘go’, out’): [[‘to’], [1]], (‘out’, ‘to’): [[‘play’], [1]],
    (‘to’, ‘play’): [[‘,’], [1]],  (‘play’, ‘,’): [[‘and’], [1]],  (‘,’, ‘and’): [[‘the’], [1]],
    (‘and’, ‘the’): [[‘child’], [1]],  (‘child’, ‘can’): [[‘not’], [1]],  (‘can’, ‘not’): [[‘be’], [1]],
    (‘not’, ‘be’): [[‘sad’], [1]],  (‘be’, ‘sad’): [[‘anymore’], [1]], (‘sad’, ‘anymore’): [[‘.’], [1]] } 
    """
    dict1 = {}
    for k in range(len(p)-n):
        tempstor = p[k:k+n]
        tk = tuple(tempstor)
        dict1[tk] = [[],[]]
        c = -1
        while c <= len(p)-n-1:
            c += 1
            if tk == tuple(p[c:c+n]):
                if not(p[c+n] in dict1[tk][0]):
                    a = dict1[tk][1]
                    b = dict1[tk][0]
                    b.append(p[c+n])
                    a.append(1)
                else:
                    a = dict1[tk][1]
                    b = dict1[tk][0]
                    a[b.index(p[c+n])] += 1
                   
    return dict1
        

def prune_ngram_counts(count, prune_len):
   """
   Type Contract:
   (dictionary(strings, num) , num) -> dictionary(strings,num)
   Given a dictionary of n-grams, keeps prune_len number of highest frequency words.
   In case of a tie, both words are kept
   >>>ngram_counts = { (‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’, ‘no’], [20, 20, 10, 2]],
   (‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]], ('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]] }
   >>> prune_ngram_counts(ngram_counts, 3)
   { (‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [20, 20, 10]], (‘u’, ‘r’): [[‘cool’, ‘nice’, ‘lit’, 'kind’],
   [8, 7, 5, 5]], ('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]] } 
   """
   pl = prune_len
   c = count
   for k in c:
       c[k][1], c[k][0] = (list(x) for x in zip(*sorted(zip(c[k][1], c[k][0]))))
   for k in c:
        if not len(c[k][1]) <= pl:
            if (c[k][1][0] == c[k][1][1]):
                while len(c[k][0]) > (pl + 1):
                    c[k][1].pop(0)
                    c[k][0].pop(0)
                    c[k][1].reverse()
                    c[k][0].reverse()
                    
            else:
                 while len(c[k][0]) > pl:
                    c[k][1].pop(0)
                    c[k][0].pop(0)
                    c[k][1].reverse()
                    c[k][0].reverse()
        else:
            c[k][1].reverse()
            c[k][0].reverse()
   return(c)

def probify_ngram_counts(counts):
    """
    Type Contract:
    (dictionary(string, int)) -> dictionary(string, int)
    Takes dictionary of ngrams and counts and converts the counts to probabilities.
     ngram_counts = { (‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [20, 20, 10]], (‘u’, ‘r’):
     [[‘cool’, ‘nice’, ‘lit’, 'kind’], [8, 7, 5, 5]], ('toronto’, ‘is’): [[‘six’, ‘drake’], [2, 3]] }
     >>> probify_ngram_counts(ngram_counts)
     { (‘i’, ‘love’): [[‘js’, ‘py3’, ‘c’], [0.4, 0.4, 0.2]], (‘u’, ‘r’):
     [[‘cool’, ‘nice’, ‘lit’, 'kind’], [0.32, 0.28,  0.2, 0.2]], ('toronto’, ‘is’): [[‘six’, ‘drake’], [0.4, 0.6]] }
    """
    keys = counts.keys()
    keys = list(keys)
    for key in keys:
        sum = 0
        nums = counts[key][1]
        for num in nums:
            sum += num
        
        for ind in range(0,len(nums)):
            counts[key][1][ind] = counts[key][1][ind] / sum
    return(counts)

def build_ngram_model(words, n):
    """
    Type Contract:
    (List(strings) , num) -> dictionary(string, int)
    Takes list of strings and converts it to a dictionary of Ngrams.
    This dictionary is pruned and counts are turned into probabilities, and the resultant dictionary is returned.
    >>> words = [‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘can’, ‘the’, ‘child’, ‘will’, ‘the’, ‘child’, ‘may’, ‘go’, ‘home’, ‘.’]
    >>> build_ngram_model(words, 2)
    { (‘the’, ‘child’): [[‘will’, ‘can’, ‘may’], [0.5, 0.25,  0.25]],
    (‘child’, ‘will’): [[‘the’], [1.0]], (‘will’, ‘the’): [[‘child’],
    [1.0]], (‘child’, ‘can’): [[‘the’], [1.0]], (‘can’, ‘the’): [[‘child’],
    [1.0]], (‘child’, ‘may’): [[‘go’], [1.0]], (‘may’, ‘go’): [[‘home’], [1.0]],
    (‘go’, ‘home’): [[‘.’], [1.0]] } 
    """
    return(probify_ngram_counts(prune_ngram_counts(build_ngram_counts(words, n),15)))
    
if __name__ == "__main__":
    
    print('After this cs lab, if there is a god he will have to beg for my forgiveness')
    
