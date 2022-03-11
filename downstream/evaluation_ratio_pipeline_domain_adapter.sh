gpu=$1
model=$2
bert_dir=$3
output_dir=$4
adapter_dir=$5
add1=$6
add2=$7
add3=$8

## DST
for ratio in 0.5 0.7
do
CUDA_VISIBLE_DEVICES=$gpu python main_domain_adapter.py \
    --my_model=BeliefTracker \
    --model_type=${model} \
    --dataset='["multiwoz"]' \
    --task_name="dst" \
    --earlystop="joint_acc" \
    --output_dir=${output_dir}/DST/MWOZ-Ratio/R1_${ratio} \
    --do_train \
    --task=dst \
    --example_type=turn \
    --cache_dir="./save/transformers" \
    --model_name_or_path=${bert_dir} \
    --adapter_name_or_path=${adapter_dir} \
    --save_adapter_path=${output_dir}/DST/MWOZ-Ratio/R1_${ratio}/MLM \
    --batch_size=8 --eval_batch_size=8 \
    --usr_token=[USR] --sys_token=[SYS] \
    --eval_by_step=1000 \
    --train_data_ratio=${ratio} \
    $add1 $add2 $add3
done
