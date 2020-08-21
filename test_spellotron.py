from spellotron import *

#############################################################################
#Testing zone
#############################################################################
def test_extra():
    alpha = alphabet()
    lib = library()
    print("Testing extra()")
    print("wore" == extra("worde", lib, alpha))
    print('word' == extra('fword', lib, alpha))
    print(('') == extra('', lib, alpha))
    print(('c') == extra('c', lib, alpha))
    print(('a') == extra('ca', lib, alpha))
    print(('help') == extra('help', lib, alpha))
    print(('brewer') == extra('.brewer', lib, alpha))

def test_missing():
    alpha = alphabet()
    lib = library()
    print("Testing missing()")
    print(("word") == missing("word", lib, alpha))
    print(('ward') == missing('wrd', lib, alpha))
    print(( 'a') == missing('', lib, alpha))
    print(( 'c') == missing('c', lib, alpha))
    print(( 'Zsimony') == missing('Zsimony', lib, alpha))
    print(( 'brewer') == missing('rewer', lib, alpha))

def test_adjacent():
    alpha = alphabet()
    lib = library()
    print("Testing adjacency()")
    print(("word") == adjacency("word", lib, alpha))
    print(( "word") == adjacency("worf", lib, alpha))
    print(( "wordl") == adjacency("wordl", lib, alpha))
    print(( "") == adjacency("", lib, alpha))
    print(( "ant") == adjacency("abt", lib, alpha))
        
def test_combine_letters():
    print("Testing combine_letters()")
    lst = []
    lst+= "abcdef"
    print("abcdef" == combine_letters(lst))
    print("" == combine_letters([]))

def test_combine_words():
    print("Testing combine_words()")
    lst = []
    quote = "@makes sense.!!!!"
    lst += quote.strip().split()
    print("@makes sense.!!!!" == combine_words(lst))

def test_library():
    print("Testing library()")
    s = library()
    print(("sex" in s) == True)
    print(("lab" in s) == True)
    print(("A's" in s) == True)
    print(("a" in s) == True)
    print(("lib" in s) == True)
    print(("bitc" in s) == False)

def test_punctuation_removal():
    print("testing_punctuation_removal()")
    t = "....word..."
    dct = dict()
    dct['....'] = [0]
    dct['...'] = [2]
    print((dct, 'word') == punctuation_removal(t))
    t1 = 'word...'
    dct1 = dict()
    dct1['...'] = [1]
    print( (dct1, 'word') == punctuation_removal(t1))
    t2 = 'word'
    dct2 = dict()
    print( (dct2, 'word') == punctuation_removal(t2))

def test_punctuation_adder():
    print("Testing punctuation_addition()")
    dct = dict()
    dct1 = dict()
    dct['...'] = [0]
    dct['?'] = [2]
    print("...hey?" == punctuation_addition(dct, "hey"))
    dct1["'"] = [1]
    print("hey'" == punctuation_addition(dct1, "hey"))
    dct2 = dict()
    print("hey" == punctuation_addition(dct2, "hey"))

def test_upper():
    print("Testing upper()")
    print("Abc" == upper("abc"))
    print("ABC" == upper("aBC"))
    print("" == upper(""))

def test_lower():
    print("Testing lower()")
    print("abc" == lower("Abc"))
    print("aBC" == lower("ABC"))
    print("" == lower(""))
    
def test_alpha():
    print("Testing alphabet()")
    print(alphabet())

def test_spell_check():
    print("Testing spell_check()")
    a = "I want a cookie!"
    lst = list()
    lst = a.split(" ")
    print(([], [], ['I', 'want', 'a', 'cookie!']) == spell_check(lst))
    b = "I bte.... an ana@"
    lst = list()
    lst = b.split(" ")
    print((['bte....', 'ana@'], [], ['I', 'bye....', 'an', 'aha@']) ==\
          spell_check(lst))
    lst = []
    lst.append("aasdfsadfdaskfsadfasga")
    print(([], ["aasdfsadfdaskfsadfasga"], ["aasdfsadfdaskfsadfasga"]) ==\
          spell_check(lst))

def test_words():
    print("Testing words()")
    a = "I want some cookies!"
    lst = list()
    lst = a.strip().split()
    words(lst)

def test_lines():
    print("Testing lines()")
    a = "HEy You, come here!"
    lst = list()
    lst = a.strip().split()
    lines(lst)

def test_remove_newline():
    print("Testing remove_newline_and_tab():")
    a = "\n hey \t"
    print(" hey " == remove_newline_and_tab(a))
    a = "\t hey \t"
    print(" hey " == remove_newline_and_tab(a))
    a = "t"
    print("t" == remove_newline_and_tab(a))
    
def test_all():
    test_library()
    test_alpha()
    test_combine_letters()
    test_combine_words()
    test_adjacent()
    test_missing()
    test_extra()
    test_punctuation_removal()
    test_punctuation_adder()
    test_upper()
    test_lower()
    test_spell_check()
    test_lines()
    test_words()
    test_remove_newline()
    
test_all()

