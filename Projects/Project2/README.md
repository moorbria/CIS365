# Project 2: Inferring Text Difficulty and Dynamic Augmentation

## Flesh-Kincaid Reading Ease Formula

**How does the readability of literature in a specific category (long-form books, news articles, etc) change over the course of time? Speculate on why this occurs?**

Looking at news articles over time, I found on average the readability went up. I speculate this occured because of the demographic that the news was trying to reach regarding these news articles. The news is trying to reach a larger audience, and can do so by using words with less syllables and using shorter sentences.

**What differences do you notice in readability between modern sources of information? (e.g. news articles, versus long format stories, versus Twitter, etc) Are there differences in the same class of article (e.g. two news sources)? If so, why might this occur? Be careful if trying to draw conclusions from one example.**

When looking at Tweets, we found a large variability in their readability. I speculate this is because you can have tweets that are short but use larger words like "Government" or "Republicans" which will inflate the readability, and there are less one syllable words. There are also tweets that are much easier to read like "I have been much tougher on Russia than Obama, just look at the facts. Total Fake News!" - Don. This tweet has a short average sentence length, and almost every word is one syllable. This will give larger readability score. 

Longer passages, such as news stories or excerpts from novels rarely give a much lower score, and usually average to a mid 70s or low 80s score. This is because a larger amount of data will give less of a chance of a skewed readability level.

**Are there sources that do not make sense to apply?**

Instructional text or recipies did not seem to fit the model well. This is because the format of the text is usually short sentences for instructions, and you also tend to use smaller words like "click", "find", "cup", "ounce", etc. This would give it a high readability score, where in fact it may be a hard instructional set to follow.

## Augmented Text Difficulty

**What strategy did you use to raise or lower the difficulty of an input text.**

After doing a bit of researching on how to tackle this problem, we found the Natural Language Toolkit (NLTK) which allowed us to produce a simple solution to raise and lower the reading difficulty of inputted text. NLTK contains a database of words and their synonyms. We used this to check each word in the text and compare its length to its synonyms. The reading level of a text is determined by the number of words, number of syllabus, and the number of sentences. For a text to have a low reading level, it should contain simple words and short sentences. For a text to have a high reading level, it should contain more complex words and sentences. 

Our approach to reduce the reading level of a text was to check every word against its synonyms provided by NLTK. If our word had a synonym that was shorter than it, we replaced it with that synonym. This allowed us to eliminate complex words from the text and replace them with simpler counterparts. We encountered many problems with the readability of the output text with this method that will be discussed further in question three below.

We also replaced every comma in the text with a period. This eliminated long sentences which helped increase the Flesch-Kincaid score. We also started a list of superfluous words and if a word was in that list, it was deleted. Finally, we experimented with removing “ing” from any word, however this added to problems with the clarity of the output text.

To increase the reading level of a text, we did the opposite of what was explained above. We compared every word to its synonyms and replaced it with the longest synonym we found. This also caused many problems with readability. 

**Describe a situation/application where you could use your approach, or a similar one, to automatically improve the accessibility of text.**

If I had an application that could effectively improve the accessibility and reduce the reading level of a text, I would apply it to professional research papers. Having completed a research project myself, I have read through dozens and dozens of papers. Most of the information I read was incredibly interesting, although it was written in a way that would be confusing to someone who wasn’t familiar with the material. If these journal articles could be rewritten in layman’s terms, they would be accessible to everyone, not just those in the discipline. Having a program that could successfully reduce the reading level of the text while maintaining its readability would be a great tool in rewriting these articles. 

**What difficulties did you run into, if any, while working on this assignment?**

After implementing our plan, we found the results to be less than ideal. Although we were successful in significantly altering the Flesch-Kincaid score of the text, the resulting output ended up being hard to read. The NLTK wordnet interface we used is not comprehensive in the words and synonyms it provides. In addition, many of the words listed as synonyms were either not complete like “anoth”, or were funky and did not make much sense in some contexts. For example, the longest synonym of “hello” is “how-do-you-do”. So, in our program, when we wanted to increase the reading level of a text, every instance of “hello” became “how-do-you-do”. These problems all contributed to the lack of readability of the output text. Some words that should have been changed were not, while some words were changed into words that did not make sense, or incomplete words. Ideally, our program would contain a database of every English word and all its synonyms. It would be able to recognize what a noun, verb, adjective is, and only change words that should be changed. 

NLTK offers ways to accomplish some of these things, but I did not have a chance to implement them. With the wordnet interface, there is a way to check what part of speech the word is, as well as check the similarity of the meaning between two words. By using these tools, a program could attempt to make decisions about which words to change, and then change them into simpler or more complex words with the same meaning. 

**Are there any notable successes, or failures, with your tool?**

The one notable success of our program was its ability to alter the reading level correctly. The more notable failure was its inability to produce readable text. 
