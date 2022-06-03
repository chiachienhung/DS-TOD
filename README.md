# DS-TOD: Efficient Domain Specialization for Task Oriented Dialog

Authors: Chia-Chien Hung, Anne Lauscher, Simone Paolo Ponzetto, Goran Glavaš 

ACL 2022. Findings: https://aclanthology.org/2022.findings-acl.72/

## Introduction
Recent work has shown that self-supervised dialog-specific pretraining on large conversational datasets yields substantial gains over traditional language modeling (LM) pretraining in downstream task-oriented dialog (TOD). These approaches, however, exploit general dialogic corpora (e.g., Reddit) and thus presumably fail to reliably embed domain-specific knowledge useful for concrete downstream TOD domains. In this work, we investigate the effects of domain specialization of pretrained language models (PLMs) for TOD. Within our **DS-TOD** framework, we first automatically extract salient domain-specific terms, and then use them to construct *DomainCC* and *DomainReddit* -- resources that we leverage for domain-specific pretraining, based on (i) masked language modeling (MLM) and (ii) response selection (RS) objectives, respectively. We further propose a resource-efficient and modular domain specialization by means of **domain adapters**. Our experiments with prominent TOD tasks -- dialog state tracking (DST) and response retrieval (RR) -- encompassing five domains from the MultiWOZ benchmark demonstrate the effectiveness of DS-TOD. Moreover, we show that the light-weight adapter-based specialization (1) performs comparably to full fine-tuning in single domain setups and (2) is particularly suitable for multi-domain specialization, where besides advantageous computational footprint, it can offer better TOD performance.

Overview of DS-TOD framework:

<img src="/img/DS-TOD.png" width="1000"/>

## Citation
If you use any source codes, or datasets included in this repo in your work, please cite the following paper:
<pre>
@inproceedings{hung-etal-2022-ds,
    title = "{DS}-{TOD}: Efficient Domain Specialization for Task-Oriented Dialog",
    author = "Hung, Chia-Chien  and
      Lauscher, Anne  and
      Ponzetto, Simone Paolo and
      Glava{\v{s}}, Goran",
    booktitle = "Findings of the Association for Computational Linguistics: ACL 2022",
    month = may,
    year = "2022",
    address = "Dublin, Ireland",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2022.findings-acl.72",
    pages = "891--904",
}
</pre>

## Pretrained Models
The pre-trained models can be easily loaded using huggingface [Transformers](https://github.com/huggingface/transformers) or Adapter-Hub [adapter-transformers](https://github.com/Adapter-Hub/adapter-transformers) library using the **AutoModel** function. Following pre-trained versions are supported:
* `TODBERT/TOD-BERT-JNT-V1`: TOD-BERT pre-trained using both MLM and RCL objectives 
* `bert-base-cased`

The scripts for downstream tasks are mainly modified from [here](https://github.com/jasonwu0731/ToD-BERT), where there might be slight version differences of the packages, which are noted down in the `requirements.txt` file.

## Datasets
Two datasets **DomainCC** and **DomainReddit** are created for intermediate training purpose, in order to encode knowledge via the domain-specific corpus.
You can simply download the data from [DomainCC](https://drive.google.com/drive/folders/1Apg9iQYtTKD-wtRmIq7wF5y-Iho5vUEC?usp=sharing) and [DomainReddit](https://drive.google.com/drive/folders/1mHQVjwawehL4OxbKzifbztXzVuB_I3_h?usp=sharing). Or you can modify the scripts for your own usage.

## Structure
The dialog_datasets in use of our paper are from MultiWOZ-2.1, which we further followed the preprocessing step from [here](https://github.com/jasonwu0731/ToD-BERT), and split the five domains into different subfiles. The full dialog_datasets can be found under [here](https://drive.google.com/file/d/1j8ZpC8Rl2GQPmMAgj1AHBZiYmRhjZdj3/view?usp=sharing).

This repository is currently under the following structure:
```
.
└── DomainReddit
└── DomainCC
└── downstream
    └── models
    └── utils
    └── dialog_datasets
└── specialization
    └── model
└── img
└── README.md
```
