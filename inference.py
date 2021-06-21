from transformers import BartTokenizer, BartForConditionalGeneration
import random
import re
from operator import itemgetter 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from punctuator import Punctuator
from google_nlp import analyze_sentiment, analyze_entities, analyze_syntax

emotion_dict = {'cautious':0, 'joy':1, 'attack':2, 'protect':3}

glove_embedding_dimensions = 100
min_user_input_size = 10
max_user_input_size = 15

sentimet_threshold = 0.3
emotionality_threshold = 0.5

word_embeddings_file = '/home/tharindu/Desktop/black/codes/Black/Dragon_Project/word_embedding/glove.6B/glove.6B.' + str(glove_embedding_dimensions) + 'd.txt'

input_entities  = []



# good_words_old = ['trees', 'love', 'flower', 'house', 'world', 'peace', 'mind', 'hero', 'beaches', 'beach', 'picture', 'victim', 'person', 'happy', 'angry', 'lake', 'grave', 'life', 'death', 'children', 'sweet', 'lane', 'nice', 'sorrow', 'exicted', 'forest', 'road']
# good_words = ['happy', 'love', 'lane', 'unsure', 'anger', 'angry', 'happiness', 'joy', 'caring', 'care', 'loving']
good_words = ['them', 'hang', 'need', 'new', 'above', 'hang', 'floor', 'wait', 'audience', 'out', 'becauase', 'seem', 'meet', 'heart', 'reach',
 'unrest', 'pause', 'curiuos', 'play', 'people', 'tell', 'hear', 'surprise', 'element', 'keep', 'moemory', 'memories', 'thing', 'different',
  'courage', 'there', 'tales', 'many', 'happen', 'trust', 'unknown', 'situation', 'day', 'put',
  'day', 'gone', 'darkness', 'darkness', 'fall', 'children', 'hard', 'blossom', 'world', 'protect', 'thorn', 'outside', 'harsh', 'spikey','retreat', 
  'away', 'any', 'garden', 'secret', 'retaliation', 'home', 'attack', 'trigger', 'provication', 'beware', 'your', 'grow', 'flowers', 'you', 
  'watch', 'comfort', 'calm', 'embrace', 'words', 'offer', 'wonderful', 'around', 'feels', 'warm', 'roses', 'shelter', 'silk', 'take', 'mighty', 'flow', 
  'us', 'butterflies', 'soft', 'let', 'heaven', 'shining', 'summer', 'wonder', 'expression', 'flutter', 'their', 'glittering', 'like', 'full', 
  'weightless', 'morning', 'hope', 'jump', 'bubbles', 'energy', 'run', 'tale', 'explore', 'spark', 'dance', 'fly', 'wings', 'filed', 'sparks', 'fileds', 
  'adventure', 'excited', 'rainbow', 'together', 'side', 'endless', 'have', 'along']

emotion_list = [['cautious', 'peace', 'neutral'], ['happy', 'joy', 'happiness'], 
['anger', 'angry', 'hate', 'lonely', 'sad', 'pain', 'woe', 'sorrow', 'fear'], ['care', 'love', 'affection']]
embeddings_dict = {}


def load_word_embeddings():
	global embeddings_dict
	with open(word_embeddings_file) as f:
		for line in f:
			word, coefs = line.split(maxsplit=1)
			coefs = np.fromstring(coefs, "f", sep=" ")
			embeddings_dict[word] = coefs

def syntax_analysis(text):
	global input_entities
	good_candidate_words_for_question = []
	okay_noun_candidate_words_for_question = []
	okay_verb_candidate_words_for_question = []
	words, word_types, numbers = analyze_syntax(text)
	for word, word_type, number in zip(words, word_types, numbers):
		if(word in input_entities):
			if(word_type is 'NOUN'):
				good_candidate_words_for_question.append((word,number))
		else:
			if(word_type is 'NOUN'):
				okay_noun_candidate_words_for_question.append((word,number))
			elif(word_type is 'VERB'):
				okay_verb_candidate_words_for_question.append((word,number))
	if(len(good_candidate_words_for_question) > 0):
		return good_candidate_words_for_question
	elif(len(okay_noun_candidate_words_for_question) > 0):
		return okay_noun_candidate_words_for_question
	elif(len(okay_verb_candidate_words_for_question) > 0):
		return okay_verb_candidate_words_for_question
	else:
		return []

def generate_question(candidates):
	if(len(candidates) > 0):
		question, number = candidates[0]
		
	else:



def process_input(in_text):
	global input_entities
	total_length = len(in_text)
	entity_words = list(analyze_entities(in_text))
	input_entities = entity_words.copy()
	print(entity_words)
	entity_count = len(entity_words)
	if(entity_count > max_user_input_size):
		random.shuffle(entity_words)
		final_words = entity_words[0:max_user_input_size]
	else:
		final_words = entity_words
	poem_influence_length = random.randint(1,4)
	good_index_list = random.sample(range(len(good_words)), poem_influence_length)
	good_words_list = list(itemgetter(*good_index_list)(good_words))
	print(good_words_list)
	final_words = final_words + good_words_list
	emotional_relevance = random.randint(0,1)
	if(emotional_relevance == 1):
		print("----------------Emotionally Relevant---------------------")
		emotion = emotion_dict[get_emotion(in_text)]
	else:
		emotion = random.randint(0,3)
	emotional_words = emotion_list[emotion]
	print(emotional_words)
	final_words.append(emotional_words[random.randint(0,len(emotional_words)-1)])
	random.shuffle(final_words)
	processed_in_text = ' '.join(final_words)
	print(processed_in_text)
	return processed_in_text


def fix_incomplete_sentences(out_text):
	if(len(re.findall(r'[.]', out_text)) > 0):
		sections = out_text.split('.')[:-1]
		return('.'.join(sections))
	else:
		return out_text

def correct_basic_mistakes(out_text):
	out_text = ' ' + out_text
	out_text = re.sub(" im ", " I\'m ", out_text)
	out_text = re.sub(" imim ", " I\'m ", out_text)
	out_text = re.sub(" ii ", " I ", out_text)
	out_text = re.sub(" ive ", " I have ", out_text)
	return out_text

def not_enough_punctuations(out_text):
	no_of_dots = len(re.findall(r'[.]', out_text))
	no_of_commas = len(re.findall(',', out_text))
	punctuation_count = no_of_dots + no_of_commas
	character_count = len(out_text)
	print("punctuation_count: ", punctuation_count)
	print("character_count: ", character_count)
	if(punctuation_count > character_count/40):
		return False
	else:
		print("not eoungh punctuations..... adding more punctuations")
		return True

def care_or_happy(out_text):
	happiness_metric = len(re.findall('happiness', out_text)) + len(re.findall('happy', out_text)) + len(re.findall('joy', out_text))  + len(re.findall('fun ', out_text)) + len(re.findall('funny ', out_text))  + len(re.findall('fun.', out_text))  + len(re.findall('fun,', out_text))
	love_metric = len(re.findall('love', out_text)) + len(re.findall('care', out_text)) + len(re.findall('caring', out_text)) + len(re.findall('embrac', out_text)) + len(re.findall('affection', out_text))
	if(happiness_metric > love_metric):
		return 'joy'
	else:
		return 'protect'

def get_emotion(text):
	sentiment, emotionality = analyze_sentiment(text)
	print("sentiment: ", sentiment)
	print("emotionality: ", emotionality)
	if(sentiment > sentimet_threshold and emotionality > emotionality_threshold):
		emotion = care_or_happy(text)
	elif(sentiment < 0 - sentimet_threshold and emotionality > emotionality_threshold):
		emotion = 'attack'
	else:
		emotion = 'cautious'
	print("Emotion = ", emotion)
	return emotion


model = BartForConditionalGeneration.from_pretrained('/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/BART_new/output/best')
tokenizer = BartTokenizer.from_pretrained('/home/tharindu/Desktop/black/codes/Black/Dragon_Project/poem_generation/BART_new/output/best')
p = Punctuator('Demo-Europarl-EN.pcl')

while(True):
	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
	in_text = input("Tell Something: ")
	if(in_text == 'q'):
		break
	ARTICLE_TO_SUMMARIZE = process_input(in_text)
	inputs = tokenizer([ARTICLE_TO_SUMMARIZE], return_tensors='pt')

	# Generate Summary
	summary_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=15, max_length=100, early_stopping=True)
	whole_out_text = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
	# print(whole_out_text)
	raw_out_text = ''.join(whole_out_text)
	basic_mistakes_fixed = correct_basic_mistakes(raw_out_text)
	sentece_fragmentation_corrected = fix_incomplete_sentences(basic_mistakes_fixed)
	
	if(not_enough_punctuations(sentece_fragmentation_corrected)):
		final_output = p.punctuate(sentece_fragmentation_corrected)
	else:
		final_output = sentece_fragmentation_corrected
	print("***************************************************************************************************")
	print(raw_out_text)
	print(basic_mistakes_fixed)
	print("***************************************************************************************************")
	print("Emotional Pavilion: ", final_output)
	print("***************************************************************************************************")
	get_emotion(final_output)

	#yesterday was quite hectic. never had a chance to get a good sleep












# def process_input(in_text):
# 	global good_words
# 	# print(good_words)
# 	# print(len(good_words))
# 	in_text = in_text.lower()
# 	in_text = re.sub(r'[^a-z\ ]', '', in_text)
# 	word_list = in_text.split(' ')
# 	stop_words = set(stopwords.words('english') + ['always', 'into', 'can\'t', 'don\'t']) 
# 	stop_words_removed = [word + ' ' for word in word_list if not word in stop_words]
# 	print(stop_words_removed)
# 	in_length = len(stop_words_removed)
# 	user_influence_length = min(max(min_user_input_size, in_length//2), in_length)
# 	poem_influence_length = user_influence_length // 5
# 	index_list = random.sample(range(max(in_length, 1)), user_influence_length)
# 	good_index_list = random.sample(range(len(good_words)), poem_influence_length)
# 	if(in_length>4):
# 		selected_words = list(itemgetter(*index_list)(stop_words_removed))
# 	else:
# 		selected_words = []
# 	good_words_list = list(itemgetter(*good_index_list)(good_words))
# 	# print(good_words_list)
# 	selected_good_words = [word + ' ' for word in good_words_list]
# 	# print(selected_words)
# 	# print(selected_good_words)
# 	all_selected_words = selected_words + selected_good_words
# 	emotion = random.randint(0,3)
# 	emotional_words = emotion_list[emotion]
# 	all_selected_words.append(emotional_words[random.randint(0,len(emotional_words)-1)])
# 	random.shuffle(all_selected_words)
# 	processed_in_text = ''.join(all_selected_words)
# 	print(processed_in_text)
# 	return processed_in_text