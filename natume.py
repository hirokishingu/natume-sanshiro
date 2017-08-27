from janome.tokenizer import Tokenizer
from gensim.models import word2vec
import re
import os.path

binarydata = open("sanshiro.txt", "rb").read()

text = binarydata.decode("shift_jis")
text = re.split(r"\-{5,}", text)[2]
# print(text)
text = re.split(r"底本：", text)[0]
# print(text + "\n")

t = Tokenizer()
lines = text.split("\r\n")
results = []

wakachigaki_file = "sanshiro.wakachi"

if not os.path.exists(wakachigaki_file):
	for line in lines:
		s = line
		s = s.replace(r"|", "")
		s = re.sub(r"《.+?》", "", s)
		s = re.sub(r"［＃.+?］", "", s)
		tokens = t.tokenize(s)
		r = []
		for token in tokens:
			if token.base_form == "*":
				w = token.surface
			else:
				w = token.surface
			ps = token.part_of_speech
			# print(ps)
			hinshi = ps.split(",")[0]
			if hinshi in ["名詞", "形容詞", "動詞", "記号"]:
				r.append(w)
		rl = (" ".join(r)).strip()
		results.append(rl)
		print(rl)
	with open(wakachigaki_file, "w", encoding="utf-8") as fp:
		fp.write("\n".join(results))

	data = word2vec.LineSentence(wakachigaki_file)
	model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)
	model.save("sanshiro.model")
	print("sanshiro model completed")


data = word2vec.LineSentence(wakachigaki_file)
model = word2vec.Word2Vec(data, size=200, window=10, hs=1, min_count=2, sg=1)

print("\n三四郎にない単語はエラーのもと")

while True:
	print("\n終了は 'q' をおしてね \n")
	search = input("三四郎に出てくる単語の類似度を測るよ>> ")
	if search == ("q" or "ｑ"):
		print("\nbye bye")
		break
	print()
	print(model.most_similar(positive=[search]))

