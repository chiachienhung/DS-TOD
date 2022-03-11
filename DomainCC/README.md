# DomainCC 

`DomainCC` is the dataset created for intermediate training purpose. 
It is currently shared under [here](https://drive.google.com/drive/folders/1Apg9iQYtTKD-wtRmIq7wF5y-Iho5vUEC?usp=sharing).
Feel free to download and unzip to use it.

If you would like to crawl your own DomainCC data, 
the scripts in this folder can be modified for your own usage.

The monolingual data can be directly downloaded from [CC-100](https://data.statmt.org/cc-100/), or obtained from `datasets` package:
```
import datasets
def download_cc100(filename, cache_dir='./cc100', lang='en'):
    dataset = datasets.load_dataset(filename, lang=lang, cache_dir=cache_dir)
download_cc100("cc100", cache_dir='./cc100', lang='en')
```

Further modification regarding the selected domain terms, the preprocessing script, can be found under `extract_sent.py` and `split_data.py`.



