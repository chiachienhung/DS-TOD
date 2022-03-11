gpu=$1
bert_dir=$2
output_dir=$3
domain=$4
add1=$5
add2=$6
add3=$7
add4=$8

CUDA_VISIBLE_DEVICES=$gpu python run_rscontrast_adapter.py \
    --model_name_or_path=${bert_dir} \
    --output_dir=${output_dir} \
    --domain=${domain} \
    --cache_dir="./save/transformers" \
    --do_train \
    --do_eval \
    --fp16 \
    --load_best_model_at_end \
    --max_train_samples=200000 \
    --max_val_samples=10000 \
    --learning_rate=1e-5 --evaluation_strategy="epoch"\
    --save_steps=2500 --logging_steps=100 --gradient_accumulation_steps=1\
    --num_train_epochs=30 --save_total_limit 2\
    --per_device_train_batch_size=32 --max_seq_length=256\
    ${add1} ${add2} ${add3} ${add4}
