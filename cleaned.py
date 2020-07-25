import string, re

def cleaned(word):
    """
    Takes in a word and returns the cleaned up version of the word.
    
    Can return multiple words or word/emoji combinations. Returns a list. Meant to be used inside the frequency_analysis()
    function.
    
    Removes any punctuation joined to the word, any emojis next to the word, and reduces any 3 letters repeated 
    consecutively to 1.
    """
    word = word.strip(string.punctuation)
    letter_regex = re.compile('\w')
    letters = letter_regex.findall(word)
    
    out_word = []
    prev_count = 0
    prev_letter = ''
    for l in letters:
        if prev_letter != l:
            out_word.append(l)
            prev_letter = l
            prev_count = 0
        else:
            prev_count += 1
            if prev_count < 2:
                out_word.append(l)
    
    out_emoji = []
    
    not_letters = re.compile('\W')
    emoji = not_letters.findall(word)
    prev_count = 0
    prev_emoji = ''
    for l in emoji:
        if prev_emoji != l:
            out_emoji.append(l)
            prev_emoji = l
    
    answer = []
    answer.append(''.join(out_word))
    for i in out_emoji:
        answer.append(i)
    return answer