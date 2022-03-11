gpu=$1
model=$2
bert_dir=$3
output_dir=$4
add1=$5
add2=$6
add3=$7

for ratio in 0.5 0.7
do
CUDA_VISIBLE_DEVICES=$gpu python main_domain.py \
    --my_model=BeliefTracker \
    --model_type=${model} \
    --dataset='["multiwoz"]' \
    --task_name="dst" \
    --earlystop="joint_acc" \
    --output_dir=${output_dir}/DST/MWOZ-Ratio/R1_${ratio} \
    --do_train \
    --task=dst \
    --cache_dir="./save/transformers" \
    --example_type=turn \
    --model_name_or_path=${bert_dir} \
    --batch_size=8 --eval_batch_size=8 \
    --usr_token=[USR] --sys_token=[SYS] \
    --eval_by_step=1000 \
    --train_data_ratio=${ratio} \
    $add1 $add2 $add3
done
