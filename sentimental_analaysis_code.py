

#Removing Useless Data
def clean_data(data):
    b = "*_=][{}1234567890!&@#$,.\";:'?/-|+"
    for i in range(0, len(b)):
        data = data.replace(b[i], " ")
    return data


def make_vocabulary(positive_reviews,negative_reviews):
    vocab = []
    _map_of_words = {}
    for line in positive_reviews:
        words = line.split()
        for word in words:
            if word not in _map_of_words:
               vocab.append(word)
               _map_of_words[word] = 1

    for line in negative_reviews:
         words = line.split()
         for word in words:
             if word not in _map_of_words:
                vocab.append(word)
                _map_of_words[word] = 1

    return vocab


def hash_for_respective_words(reviews):
    _map_of_words = {}
    for lines in reviews:
        words = lines.split()
        for word in words:
            if word not in _map_of_words:
                _map_of_words[word] = 1
            else:
                _map_of_words[word] += 1

    return _map_of_words


def get_count_of_words(_map):
    count = 0
    for i in _map:
        count += _map[i]
    return count


def get_likelihood_for_word(word, hash_for_words, count_of_words, y, vocab_lens):
    count = 0
    if word in hash_for_words:
        count = hash_for_words[word]
    return (count + y)/(count_of_words+vocab_lens)


def get_likelihood(likelihood_for_words, word):
    if word in likelihood_for_words:
        return likelihood_for_words[word]
    else:
        return 0


positive_data = clean_data(open('positive_reviews.txt', 'r').read())
negative_data = clean_data(open('negative_reviews.txt', 'r').read())

positive_reviews = positive_data.split("\n")
negative_reviews = negative_data.split("\n")

number_of_positive_reviews = len(positive_reviews)
number_of_negative_reviews = len(negative_reviews)

prior_positive_probability = number_of_positive_reviews/(number_of_positive_reviews+number_of_negative_reviews)
prior_negative_probability = number_of_negative_reviews/(number_of_positive_reviews+number_of_negative_reviews)

vocabulary = make_vocabulary(positive_reviews, negative_reviews)

hash_for_positive_words = hash_for_respective_words(positive_reviews)
hash_for_negative_words = hash_for_respective_words(negative_reviews)

count_of_positive_words = get_count_of_words(hash_for_negative_words)
count_of_negative_words = get_count_of_words(hash_for_positive_words)

likelihood_for_positive_words = {}
likelihood_for_negative_words = {}

alpha = 1;
vocab_len = len(vocabulary)
for word in vocabulary:
    likelihood_for_positive_words[word] = get_likelihood_for_word(word,hash_for_positive_words,count_of_positive_words,alpha,vocab_len)
    likelihood_for_negative_words[word] = get_likelihood_for_word(word,hash_for_negative_words,count_of_negative_words,alpha,vocab_len)

review = input("Enter Text : ")  #test data
review = clean_data(review)
words = review.split()
positive_likelihood = 1
negative_likelihood = 1
for word in words:
    p_likelihood = get_likelihood(likelihood_for_positive_words,word)
    n_likelihood = get_likelihood(likelihood_for_negative_words,word)
    positive_likelihood *= p_likelihood if p_likelihood != 0 else 1
    negative_likelihood *= n_likelihood if p_likelihood != 0 else 1

positive_probability = prior_positive_probability*positive_likelihood
negative_probability = prior_negative_probability*negative_likelihood

if positive_probability > negative_probability:
    print("POSITIVE REVIEW")
else:
    print("NEGATIVE REVIEW")



