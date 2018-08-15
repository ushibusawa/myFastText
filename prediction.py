import sys
import fastText as ft
import MeCab
import re

def main(argv):
    model_name = argv[0]
    classifier = ft.load_model(model_name)

    input_file = argv[1]
    with open(input_file, 'r') as fin:
        qlist = fin.readlines()

    tagger = MeCab.Tagger('-Owakati')
    output_csv = []
    for q in qlist:
        line = tagger.parse(q)
        labels, probs = classifier.predict(line.strip(), k=2)
        output = []
        for label, prob in zip(labels, probs):
            output.append(re.sub('__label__', '', label) + ':' + str(prob))
        output.append(q.strip())
        output_csv.append(','.join(output))
#        print(output_str)
#        print(labels, probs, q.strip())
    output_file = argv[2]
    with open(output_file, 'wt') as fout:
        fout.write('\n'.join(output_csv))

if __name__ == '__main__':
    main(sys.argv[1:])
