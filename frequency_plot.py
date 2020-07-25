from instagram_utils import find_person
import seaborn as sns
import matplotlib.pyplot as plt

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