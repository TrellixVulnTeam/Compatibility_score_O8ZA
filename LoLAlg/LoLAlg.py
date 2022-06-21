import easygui as eg
import matplotlib
import matplotlib.pyplot as plt
import sys
#attribute table
    #a dictionary containing the attributes one looks for in a partner, as well as their weights
    # example: 'emotional support' : 200
#preference_code
    #a users attribute table from a previous round

attribute_table = {}
preference_code = ''

def generate_table():
    intro = "For the following \'attributes\', assign points" \
            " depending on how important each attribute is to you " \
            "in a love interest. Think carefully, and take your time!"
    if not eg.msgbox(intro, title):
        sys.exit(0)

    basic_attributes = ['Intelligence', 'Physical appearance', 'Emotional support', 'Friendship', 'Independence'];

    for item in basic_attributes:
        intro = 'How important is this to you in a love interest? \'' + item + '\'';
        response = eg.choicebox(intro, title, ["not important", "50", "100", "150", "200"])
        if not response == "not important": attribute_table[item] = int(response)

    intro = "Now, add any \'attributes\' you look for in a love interest that you didn't see listed. This part is important! " \
            "The more information you provide, the more accurate your results will be."
    if not eg.msgbox(intro, title):
        sys.exit(0)
    intro = "Enter your custom attribute, press cancel when finished"
    custom_attributes = []
    while True:
        response = eg.enterbox(intro, title)
        if response == None:
            break
        if len(str(response)) >= 1:
            custom_attributes.append(response);

    if len(custom_attributes) != 0:
        for item in custom_attributes:
            response = eg.choicebox(item, title, ["50", "100", "150", "200"])
            attribute_table[item] = float(response)

#uses a preference code to fill the attribute_table
def fill_table(p_code):
    preference_code = p_code.split('-')
    try:
        preference_code.remove('')
        preference_code.remove(' ')
    except:
        ValueError
    i=0
    while i<len(preference_code):
        attribute = preference_code[i]
        score = float(preference_code[i+1])
        attribute_table[attribute] = score
        i+=2



title = "Compatibility Score"
intro = "This is a game that uses a little math to help you figure out how compatible you and your love interest are. " \
        "This could be someone you are dating right now, have dated in the past, or even someone you just met"
if not eg.msgbox(intro, title):
    sys.exit(0)

intro = "If you have played this game before, paste your preference code below. If not, select \'No\'"
response = eg.buttonbox(intro, choices = ['Yes', 'No'])
if response == 'No':
    generate_table()
elif response == 'Yes':
    intro = "Enter your preference code below"
    preference_code = eg.enterbox(intro, title)
    fill_table(preference_code)


else:   sys.exit(0);
intro = "Alright, now that you have determined what you look for in a partner, It's time to score your love interest"
if not eg.msgbox(intro,title):
    sys.exit(0)
final_score_table = {}
intro = "What is the name of your love interest?"
name = eg.enterbox(intro, title)
max_score_table = {}
missing_points = 0
total_points = 0 # to calculate the % missing info
for item in attribute_table:
    total_points += attribute_table.get(item)
    intro = name + "\'s Score: " + '\'' + item + '\''
    response = eg.choicebox(intro, title, ["I don\'t know", "100", "200", "300", "400", "500"])
    if not response == "I don\'t know":
        final_score_table[item] = float(response) * .002 * attribute_table.get(item) #add a percentage of the max points based on response
        max_score_table[item] = attribute_table.get(item) #used to calculate max score (excludes IDK attributes)
    elif response == "I don\'t know":
        missing_points += attribute_table.get(item) #sum up the missing points to calculate 'percent missing'


score = 0
max_score = 0   # to calculate the % match
for item in final_score_table: # calculate final score
    score += final_score_table.get(item)
for item in max_score_table:    # calculate max score
    max_score += max_score_table.get(item)
percent_missing = missing_points/total_points * 100 # calculate percent missing

plt.bar([name], [score], color='pink', width=.05, alpha=.65, label=str(score))  # visualize using bar graph
plt.ylim( (0,max_score))
ax = plt.gca()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
t = name + '\'s score out of ' + str(max_score) + '! (Close to continue)'
plt.title(t)
plt.legend()
plt.show()

if score != 0 and max_score != 0:  #avoid 'divide by 0' error
    intro = name+ '\'s Score: ' + str(score/max_score*100) +'% Match, ' + 'Missing info: ' + str(percent_missing) + '%'
else:
    intro = name + '\'s Score: 0% Match, ' + 'Missing info: ' + str(percent_missing) + '%'
if not eg.msgbox(intro,title):
    sys.exit(0)
preference_save = ''
for item in attribute_table:
    preference_save += item + '-' + str(attribute_table.get(item)) + '-'
intro = "Copy this code using \'Ctrl+c\' in order to store your preferences for next time: " + preference_save
if not eg.msgbox(intro, title):
    sys.exit(0)
