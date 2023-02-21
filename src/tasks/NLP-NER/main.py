text = """I extend a warm welcome to you all in 'Mann ki Baat', once again. This programme is the 
95th episode which is held in Delhi prime minister PMO. We are fast moving towards the century of 'Mann ki Baat'. This programme is another medium 
for me to connect with 130 crore countrymen. Before every episode, reading letters from villages and cities,
listening to audio messages from children to elders; it is like a spiritual experience for me.programme 
referring to a unique gift. There is a weaver brother in Rajanna Sircilla district of Telangana–Yeldhi 
Hariprasad. He has sent me this G20 logo woven with his own hands and which is situated in Delhi. I was surprised to see this wonderful 
gift. Hariprasad ji is such an expert in his art that he attracts everyone's attention. Hariprasad ji has 
also sent me a letter along with this handwoven G20 logo. In this, he has written that it is a matter of 
great pride for India to host the G20 Summit next year. Amid the joy of this achievement of the country, 
he has Gujrat prepared this logo of G20 with his own hands.He has inherited this wonderful talent of weaving from
his father and today, he is engaged in it with full passion.Friends, a few days ago I had the privilege of 
launching the G20 logo and the website of the Presidency of India. I live in Kolkata. And G20 basically started in different cities like Madhya Pradesh, 
Utter Pradesh and Gujarat, Kharagpur"""
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
named_entities = []
nes = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(text)))
for ne in nes:
  if type(ne) is nltk.tree.Tree:
    if (ne.label() == 'GPE' or ne.label() == 'PERSON'
        or ne.label() == 'ORGANIZATION'):
      l = []
      for i in ne.leaves():
        l.append(i[0])
      s = u' '.join(l)
      if not (s in named_entities):
        named_entities.append(s)
print(named_entities)