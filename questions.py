import random

question_dict = {
'neutral_general_questions': [	("What do you think about ", "?"),
								("Waht do you feel about ", "?"),
								()],

'positive_general_questions': [("What do you think about ", "? I am a big fan."),
					("", " is interesting. Do you not think?")],

'negative_general_questions': [("What do you think about ", "? I do not like at all."),
					("", " is interesting. Do you not think?")],

'neutral_singular_questions': [("", " is something new to me. Tell me more, what are your thougts?")],

'neutral_plural_questions': [("", " are new to me. Tell me more, what are your thougts?")],

'positive_singular_questions': [("", " is interesting. Tell me more, what are your thougts?")],

'positive_plural_questions': [("", " are interesting. Tell me more, what are your thougts?")],

'negative_singular_questions': [("I do not think that ", " is good. Tell me more, what are your thougts?")],

'negative_plural_questions': [("I do not think that ", " is good. Tell me more, what are your thougts?")],

'neutral_backup_questions': [("What do to think, about the world, in 20 years? what will be different", "?")],

'positive_backup_questions': [("Love takes different forms, as I think, What are the forms of love, you have experienced", "?")],

'negative_backup_questions': [("Humans are destroying the world. Don't you agree?, why", "?")]
}

def get_question_ids(numbers, sentiments):
	global question_dict
	key_name = ''
	list_index = 0
	position_intex = 0
	question_ids = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]

	for number in numbers:
		for  sentiment in sentiments:
			if(sentiment == 'POSITIVE'):
				key_name = key_name + 'positive_'
				list_index = 0
			elif(sentiment == 'NEGATIVE'):
				key_name = key_name + 'negative_'
				list_index = 1
			else:
				key_name = key_name + 'neutral_'
				list_index = 2

			if(number == 'SINGULAR'):
				key_name = key_name + 'singular_'
				position_intex = 0
			elif(number == 'PLURAL'):
				key_name = key_name + 'plural_'
				position_intex = 1
			elif(number == 'BACKUP'):
				key_name = key_name + 'backup_'
				position_intex = 2
			else:
				key_name = key_name + 'general_'
				position_intex = 3

			key_name = key_name + 'questions'
			list_of_questions = question_dict[key_name]
			question_ids[position_intex][list_index] = len(list_of_questions)
			key_name = ''
	return question_ids


def create_question(number, sentiment, question_id=None, word=''):
	global question_dict
	key_name = ''

	if(sentiment == 'POSITIVE'):
		key_name = key_name + 'positive_'
	elif(sentiment == 'NEGATIVE'):
		key_name = key_name + 'negative_'
	else:
		key_name = key_name + 'neutral_'

	if(number == 'SINGULAR'):
		key_name = key_name + 'singular_'
	elif(number == 'PLURAL'):
		key_name = key_name + 'plural_'
	elif(word == None):
		key_name = key_name + 'backup_'
	else:
		key_name = key_name + 'general_'

	key_name = key_name + 'questions'
	list_of_questions = question_dict[key_name]

	if(question_id == None or question_id >= len(list_of_questions)):
		question_id = random.randint(0, len(list_of_questions)-1)
	question_parts = list_of_questions[question_id]
	question = question_parts[0] + word + question_parts[1]

	return question

# sentiments_list = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
# numbers_list = ['SINGULAR', 'PLURAL', 'BACKUP', 'GENERAL']
# question_id_counts = get_question_ids(numbers_list ,sentiments_list)

print(question_id_counts)
print(question_idx)

# test_question = create_question('SINGULAR', 'NEUTRAL', 0, 'cycle')
# print(test_question)

