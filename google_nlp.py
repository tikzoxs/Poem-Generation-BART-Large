#  export GOOGLE_APPLICATION_CREDENTIALS="/home/tharindu/Desktop/black/GoogleCloudProjects/dragon/dragon-project-313222-28d7d9fd60f0.json"

from google.cloud import language_v1

def analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    # Get overall sentiment of the input document
    # print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    # print(
    #     u"Document sentiment magnitude: {}".format(
    #         response.document_sentiment.magnitude
    #     )
    # )

    # Get sentiment for all sentences in the document
    # for sentence in response.sentences:
    #     print(u"Sentence text: {}".format(sentence.text.content))
    #     print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
    #     print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # # Get the language of the text, which will be the same as
    # # the language specified in the request or, if not specified,
    # # the automatically-detected language.
    # print(u"Language of the text: {}".format(response.language))
    return(response.document_sentiment.score, response.document_sentiment.magnitude)


def analyze_syntax(text_content):
    """
    Analyzing Syntax in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'This is a short sentence.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_syntax(request = {'document': document, 'encoding_type': encoding_type})

    words = []
    word_types = []
    numbers = []
    # Loop through tokens returned from the API
    for token in response.tokens:
        # Get the text content of this token. Usually a word or punctuation.
        text = token.text
        # print(u"Token text: {}".format(text.content))
        # print(
        #     u"Location of this token in overall document: {}".format(text.begin_offset)
        # )
        # Get the part of speech information for this token.
        # Parts of spech are as defined in:
        # http://www.lrec-conf.org/proceedings/lrec2012/pdf/274_Paper.pdf
        part_of_speech = token.part_of_speech
        POS = str(language_v1.PartOfSpeech.Tag(part_of_speech.tag).name)
        NUMBER = str(language_v1.PartOfSpeech.Number(part_of_speech.number).name)
        if(POS == 'NOUN' or POS == 'VERB'):
            words.append(text.content)
            word_types.append(POS)
            numbers.append(NUMBER)
        # Get the tag, e.g. NOUN, ADJ for Adjective, et al.
        # print(
        #     u"Part of Speech tag: {}".format(
        #         language_v1.PartOfSpeech.Tag(part_of_speech.tag).name
        #     )
        # )
        # Get the voice, e.g. ACTIVE or PASSIVE
        # print(u"Voice: {}".format(language_v1.PartOfSpeech.Voice(part_of_speech.voice).name))
        # Get the tense, e.g. PAST, FUTURE, PRESENT, et al.
        # print(u"Tense: {}".format(language_v1.PartOfSpeech.Tense(part_of_speech.tense).name))
        # See API reference for additional Part of Speech information available
        # Get the lemma of the token. Wikipedia lemma description
        # https://en.wikipedia.org/wiki/Lemma_(morphology)
        # print(u"Lemma: {}".format(token.lemma))
        # Get the dependency tree parse information for this token.
        # For more information on dependency labels:
        # http://www.aclweb.org/anthology/P13-2017
        dependency_edge = token.dependency_edge
        # print(u"Head token index: {}".format(dependency_edge.head_token_index))
        # print(
        #     u"Label: {}".format(language_v1.DependencyEdge.Label(dependency_edge.label).name)
        # )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    # print(u"Language of the text: {}".format(response.language))
    # print(nouns)
    return words, word_types, numbers


def analyze_entities(text_content):
    """
    Analyzing Entities in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})

    # Loop through entitites returned from the API
    entity_words = []
    for entity in response.entities:
        entity_words.append(entity.name)
        # print(u"Representative name for the entity: {}".format(entity.name))

    #     # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        # print(u"Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))

    #     # Get the salience score associated with the entity in the [0, 1.0] range
        # print(u"Salience score: {}".format(entity.salience))

    #     # Loop over the metadata associated with entity. For many known entities,
    #     # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
    #     # Some entity types may have additional metadata, e.g. ADDRESS entities
    #     # may have metadata for the address street_name, postal_code, et al.
    #     for metadata_name, metadata_value in entity.metadata.items():
    #         print(u"{}: {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        # for mention in entity.mentions:
        #     print(u"Mention text: {}".format(mention.text.content))

        #     # Get the mention type, e.g. PROPER for proper noun
        #     print(
        #         u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name)
        #     )

    # # Get the language of the text, which will be the same as
    # # the language specified in the request or, if not specified,
    # # the automatically-detected language.
    # print(u"Language of the text: {}".format(response.language))
    return set(entity_words)


# print(analyze_sentiment("Let us watch the flowers grow. The soft leaves will shelter and comfort you. Watch the butterflies around you."))
# print(analyze_syntax("I experience a significant part of world through my ears. I love listening to the different sounds in the environment, be it traffic or the birds. In my opinion there is so much to listen to in this world that tells us a lot about it."))
# print(analyze_entities("I experience a significant part of world through my ears. I love listening to the different sounds in the environment, be it traffic or the birds. In my opinion there is so much to listen to in this world that tells us a lot about it."))
