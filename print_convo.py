from instagram_utils import find_person
def print_convo(person, dms, my_username, return_photos = False):
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