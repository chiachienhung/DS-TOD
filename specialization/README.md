# Domain Specialization

For domain specialization, here are multiple methods you can implement for your own usage:

- **MLM (DomainCC)**
```
./run_tod_intermediate_mlm.sh 0 "TODBERT/TOD-BERT-JNT-V1" save/domain_eval/taxi/TOD-BERT_MLM ../DomainCC/train/taxi_200K_prep.txt ../DomainCC/test/taxi_10K_prep.txt --overwrite_output_dir --patience 3
```

- **MLM-adapter (DomainCC)**

```
./run_tod_intermediate_mlm_adapter.sh 0 "TODBERT/TOD-BERT-JNT-V1" save/domain_eval/taxi/TOD-BERT_MLM_adapter ../DomainCC/train/taxi_200K_prep.txt ../DomainCC/test/taxi_10K_prep.txt --overwrite_output_dir --patience 3
```

- **RS-Class (DomainReddit)**
```
./run_tod_intermediate_rsclass.sh 0 "TODBERT/TOD-BERT-JNT-V1" save/domain_eval/taxi/TOD-BERT_RSClass "taxi" --overwrite_output_dir --patience 3
```

- **RS-Class-adapter (DomainReddit)**
```
./run_tod_intermediate_rsclass_adapter.sh 0 "TODBERT/TOD-BERT-JNT-V1" save/domain_eval/taxi/TOD-BERT_RSClass_adapter "taxi" --overwrite_output_dir --patience 3
```

- **RS-Contrast (DomainReddit)**
```
./run_tod_intermediate_rscontrast.sh 0 "TODBERT/TOD-BERT-JNT-V1" save/domain_eval/taxi/TOD-BERT_RSContrast "taxi" --overwrite_output_dir --patience 3
```

- **RS-Contrast-adapter (DomainReddit)**
```
./run_tod_intermediate_rscontrast_adapter.sh 0 "TODBERT/TOD-BERT-JNT-V1" save/domain_eval/taxi/TOD-BERT_RSContrast_adapter "taxi" --overwrite_output_dir --patience 3
```
