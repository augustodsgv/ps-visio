import pandas as pd

def create_csv():
    dados = [['h264', 'vp8', 200, 1024]]
    df = pd.DataFrame(dados, columns=['source codec', 'destiny codec', 'time (s)', 'size (b)'])
    df.to_csv("./codec_data.csv")
    print(df)

def read_csv():
    df = pd.read_csv("./codec_data.csv")
    print(df)

if __name__ == '__main__':
    read_csv()
    for item in {'fruta' : 'banana', 'lanche' : 'pizza'}.items():
        print(item)