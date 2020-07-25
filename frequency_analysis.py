from instagram_utils import find_person
import string

def frequency_analysis(person, dms, n_top_words = 20, mode = 'top'):
    """
    Takes in the person and makes a frequency table of all the words they used
    
    n_top_words is the number of most frequent words to print out.
    mode is a string which takes either 'top' or 'search'
    search mode is to search for the frequency of a particular word the user enters. The function will return the top n 
    words in either mode
    """
    chat_dictionary = {}
    indices, _ = find_person(person, dms, False)
    
    #To handle a weird special case. No, empty is not '' (the empty string).
    empty = '️'
    
    for i in indices:
        conversation = reversed(dms['conversation'][i])
        for message in conversation:
            if 'text' in message.keys():
                try:
                    words_in_text_preprocessed = message['text'].lower().split()
                    words_in_text = []
                    for w in words_in_text_preprocessed:
                        w_clean = cleaned(w)
                        for x in w_clean:
                            words_in_text.append(x)     
                except:
                    pass
                for word in words_in_text:
                    if word in chat_dictionary.keys() and (word != '' and word != empty and word != "'"):
                        #increment the word count
                        chat_dictionary[word] += 1
                    elif word not in chat_dictionary.keys() and (word != '' and word != empty and word != "'"):
                        #create the key for the word and set it to 1
                        chat_dictionary[word] = 1

    frequencies = list(chat_dictionary.values())
    words = list(chat_dictionary.keys())
    top_word_list = []
    top_word_count = []
    
    if mode == 'search':
        word_to_search = input("Enter the word you want to search for -- ").lower().strip(string.punctuation)
        if word_to_search in words:
            freq = frequencies[words.index(word_to_search)]
            rank = list(sorted(frequencies, reverse = True)).index(freq)+1
            print(f'\nYou have used the word {word_to_search} {freq} times in your chat with {person}.\nIt ranks number {rank}.\n')
        else:
            print(f"You haven't used the word {word_to_search} in a chat with {person}\n")
    
    for i in range(n_top_words):
        top_word_index = frequencies.index(max(frequencies))
        top_word_list.append(words.pop(top_word_index).title())
        top_word_count.append(frequencies.pop(top_word_index))
    
    print(f'You have used a total of {len(frequencies)} unique words with [{person}]')
    print(f'The top {n_top_words} most used words in your chat with [{person}] were - \n')
    for i in range(len(top_word_list)):
        print(f'{i+1}.\t{top_word_list[i]}\t --- used {top_word_count[i]} times.')

    print('\n')