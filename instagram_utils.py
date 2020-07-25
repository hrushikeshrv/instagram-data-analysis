import seaborn as sns
import matplotlib.pyplot as plt
import string
import re

#----------------------------------------------------------------------------------------------------------------------------#

def print_conversation(person, my_username, dms, return_photos = False):
    """
    Takes in a username and prints their conversation as a chat.
    Set return_photos to True if you want the function to return a list containing urls to all the posts and photos
    shared in the chat by all parties involved.
    If return_photos:
        return (posts_sent, posts_recieved, photos_sent, photos_recieved)
    """
    print_chat = 'personal'
    indices, groups = find_person(person, dms, False)
    chat_number = indices[0]
    print(f'Found {len(indices)} chats with {person}.')
    if groups:
        print(f'Found {len(groups)} groupchats with {person}.')
        print_chat = input(f'Enter the chats you want to print - enter "Personal" to print your personal chats with {person} or enter "Group" to print your group chats with {person} - ').lower()

    while print_chat != 'personal' and print_chat != 'group':
        print_chat = input('Got an invalid input. Please either enter "Personal" or "Group"')
    
    if print_chat == 'personal' and len(indices) > 1:
        print(f'\n\nYour personal chats with {person} are at indices {indices}.')
        chat_number = int(input(f'Enter the index of the chat with {person} you want to print. (The higher the index, the older the chat) - '))
    elif print_chat == 'group' and len(groups) > 1:
        print(f'\n\nYour group chats with {person} are at indices {groups}')
        chat_number = int(input(f'Enter the index of the group chat with {person} you want to print. (The higher the index, the older the chat) - '))
    elif print_chat == 'group' and len(groups) == 1:
        chat_number = groups[0]
    
    conversation = reversed(dms['conversation'][chat_number])
    
    prev_day = 0
    sender = 'noone'
    
    #Initialize lists to keep track of photos/posts sent and recieved
    posts_sent = []
    photos_sent = []
    posts_recieved = []
    photos_recieved = []
    
    for i in conversation:
        #Keep track of today's date
        today = i['created_at'].split('T')[0].split('-')[2]
        
        #Check if the day has changed
        if prev_day != today:
            prev_day = today
            print('{:>50}'.format(i['created_at'].split('T')[0]))
            print('-'*100+'\n')
            
        if i['sender'] != sender:
            sender = i['sender']
            print('\n')
            if i['sender'] != my_username:
                print(f'[{i["sender"]}]')
        
        try:        
            #Check if anyone sent a story
            if 'story_share' in i.keys():
                if i['sender'] == my_username:
                    print('{:>100}\n'.format('[' + i["story_share"] + ']'))
                else:
                    print(f'[{i["sender"]} {i["story_share"]}]\n')

            #Check if anyone sent a photo or a post
            if 'media_share_url' in i.keys():
                #Check who sent the photo/post
                if i['sender'] == my_username:
                    print('-'*100)
                    print('{:>100} \n{:>100}\n{:>100}'.format('hrushikeshrv shared a post -',i['media_share_url'],i['media_share_caption']))
                    print('-'*100+'\n')
                    posts_sent.append(i['media_share_url'])
                else:
                    print('-'*100)
                    print('{} shared a post -\n{}\n{}'.format(i['sender'], i['media_share_url'], i['media_share_caption']))
                    print('-'*100+'\n')
                    posts_recieved.append(i['media_share_url'])
            
            #Check if anyone started a video call
            if 'video_call_action' in i.keys():
                print('{:>50}'.format(i['video_call_action']))
            
            #Check if anyone sent a gif
            if 'animated_media_images' in i.keys():
                print('-'*100)
                if i['sender'] == my_username:
                    print('{:>100}\n{}'.format("hrushikeshrv sent a gif -", i["animated_media_images"]["downsized_large"]["url"]))
                else:
                    print(f'{i["sender"]} sent a gif -\n{i["animated_media_images"]["downsized_large"]["url"]}')
                print('-'*100 + '\n')
                
            #Check if anyone sent a picture
            if 'media' in i.keys():
                if i['sender'] == my_username:
                    print('-'*100)
                    print('{:>100} \n{:>100}'.format('hrushikeshrv sent a photo -',i['media']))
                    print('-'*100+'\n')
                    photos_sent.append(i['media'])
                else:
                    print('-'*100)
                    print('{} sent a photo -\n{}'.format(i['sender'], i['media']))
                    print('-'*100+'\n')
                    photos_recieved.append(i['media'])
            if 'media_url' in i.keys():
                if i['sender'] == my_username:
                    print('-'*100)
                    print('{:>100} \n{:>100}'.format('hrushikeshrv sent a photo -',i['media_url']))
                    print('-'*100+'\n')
                    photos_sent.append(i['media_url'])
                else:
                    print('-'*100)
                    print('{} sent a photo -\n{}'.format(i['sender'], i['media_url']))
                    print('-'*100+'\n')
                    photos_recieved.append(i['media_url'])
            
            
            #Check if anyone sent a heart
            if 'heart' in i.keys():
                if i['sender'] == my_username:
                    print('{:>100}'.format(i['heart']))
                else:
                    print('{}'.format(i['heart']))
            
            #Print the text contents of the message
            if 'text' in i.keys():
                if i['sender'] == my_username:
                    print('{:>100}'.format(i["text"]))
                else:
                    print(f'{i["text"]}')
            
            #Check if anyone has liked the meassage
            if 'likes' in i.keys():
                for j in i['likes']:
                    if i['sender'] != my_username:
                        print('[liked by {}]'.format(j['username']))
                    else:
                        print('{:>100}]'.format('[liked by ' + j['username']))
            
            #Check if anyone sent a voice message
            if 'voice_media' in i.keys():
                if i['sender'] == my_username:
                    print('[{:>100}]\n'.format('hrushikeshrv sent a voice message'))
                else:
                    print(f'[{i["sender"]} sent a voice message]\n')
                    
        #Catch exceptions
        except KeyError as e:
            if i['sender'] == my_username:
                print('{:>100} sent some media]\n'.format('['+i['sender']))
                #-----------------------------DEBUG------------------------------#
                print('{:>100}'.format(i.keys()))
                print('ERROR - ' + e)
                #-----------------------------DEBUG------------------------------#
            else:
                print(f'\n[{i["sender"]} sent some media]\n')
                #-----------------------------DEBUG------------------------------#
                print(f'{i.keys()}')
                print('ERROR - ' + e)
                #-----------------------------DEBUG------------------------------#
        
    if return_photos:
        print('\n\n\nReturning lists containing urls to all the media shared in the chat...')
        return posts_sent, posts_recieved, photos_sent, photos_recieved

#----------------------------------------------------------------------------------------------------------------------------#

def frequency_plot(person, dms, weighted_average_days = 3, accuracy = True):
    """
    Takes in a username, finds all the conversations with that person, and plots a graph of the number of messages to and 
    from that person every day over their entire chat history.
    """
    indices, temp = find_person(person, dms, False)
    total_days_talking = []
    
    #Keep count of number of texts each day
    number_of_texts = []
    
    #Iterating through all the chat lists in the dms data frame (i)
    for i in indices:
        conversation = reversed(dms['conversation'][i])
        #initialize the date to 0
        prev_day = 0
        #Iterating through all the messages in a chats in a conversation (message)
        todays_texts = 0
        days_talking = 0
        for message in conversation:
            
            today = message['created_at'].split('T')[0].split('-')[2]
            
            if prev_day == today:
                todays_texts += 1
                
            else:
                prev_day = today
                number_of_texts.append(todays_texts)
                todays_texts = 0
                days_talking += 1
                
        total_days_talking.append(days_talking)
        
    kde = [0]
    beta = 1 - 1/weighted_average_days
    for x in range(1, len(number_of_texts)):
        kde.append((beta*kde[-1] + (1-beta)*number_of_texts[x])/(1-beta**x))
    
    sns.set_context('poster', font_scale = 0.5)
    text_plot = plt.figure()
    ax = text_plot.add_axes([0,0,1.5,1.2])
    ax.set_title('Number of texts vs. days')
    ax.set_xlabel('Days')
    ax.set_ylabel('Texts')
    ax.set_ylim(ymin = -0.017*max(number_of_texts), ymax = 1.15*max(number_of_texts))
    ax.grid(b = True, which = 'major', color = '#444444', linewidth = 0.6)
    if accuracy:
        ax.plot(number_of_texts, color = 'orange', linewidth = 2, label = 'Texts/Day')
        ax.plot(kde, color = 'green', linewidth = 2, label = '{} day average'.format(weighted_average_days))
    else:
        ax.plot(kde, color = 'green', linewidth = 2, label = '{} day average'.format(weighted_average_days))
    ax.legend(loc = 'best')
    
    _ = 0
    for x in total_days_talking:
        _ += x
    print(f'Talked for a total of {_} days.')
    _ = 0
    for x in number_of_texts:
        _ += x
    print(f'In this time, a total of {_} texts were sent')
    print(f'The maximum number of texts in a single day was {max(number_of_texts)}')

#----------------------------------------------------------------------------------------------------------------------------#

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

#----------------------------------------------------------------------------------------------------------------------------#

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
        top_word = words[top_word_index]
        top_word_list.append(words.pop(top_word_index).title())
        top_word_count.append(frequencies.pop(top_word_index))
    
    print(f'You have used a total of {len(frequencies)} unique words with [{person}]')
    print(f'The top {n_top_words} most used words in your chat with [{person}] were - \n')
    for i in range(len(top_word_list)):
        print(f'{i+1}.\t{top_word_list[i]}\t --- used {top_word_count[i]} times.')

    print('\n')

#----------------------------------------------------------------------------------------------------------------------------#

def find_person(person, dms, print_indices = True):
    """
    Takes in the whole series and returns the indices of conversations with the person.
    Primarily meant to be used as a helper function in print_convo(), frequency_plot(), and frequency_analysis()
    """
    group_index = []
    non_group_indices = []
    participants = list(reversed(dms['participants']))
    for i in range(len(participants)):
        if person in participants[i] and len(participants[i]) == 2:
            non_group_indices.append(len(participants) - i - 1)
        elif person in participants[i]:
            group_index.append(len(participants) - i - 1)
    
    if print_indices:
        print(f'Your personal chats with {person} are at indices \n{non_group_indices}.\n[Oldest first]')
        if group_index:
            print(f'Your group chats with {person} are at -\n{group_index}')
            
        
    return non_group_indices, group_index