from fastText import train_supervised
import sys
import os

def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))

def main(argv):
    train_data = os.path.join(os.getenv("DATADIR", ''), argv[0])
    valid_data = os.path.join(os.getenv("DATADIR", ''), argv[1])
    model = train_supervised(
        input=train_data, epoch=1000,
        loss="hs"
    )
    print_results(*model.test(valid_data))
    model.save_model(argv[2])

if __name__ == '__main__':
    main(sys.argv[1:])
