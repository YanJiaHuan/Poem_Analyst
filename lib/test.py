# import paddlehub as hub
# module = hub.Module(name='chinese-bert-wwm')

import spacy

nlp = spacy.load('zh_core_web_sm')

test_poem = '举头望明月，低头思故乡'
# test_poem = '西门子将努力参与中国的三峡工程建设。'
# test_poem = '李白抬头看到月亮，低头思念家乡'
doc = nlp(test_poem)
for token in doc:
    print(f"{token.text} --- POS: {token.pos_}, {token.tag_}")

print(doc.ents)

for ent in doc.ents:
    print(ent.text, ent.label_)

for token in doc:
    if token.pos_ == 'NOUN':
        print(token.text, token.pos_)