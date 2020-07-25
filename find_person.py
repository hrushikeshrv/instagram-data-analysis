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