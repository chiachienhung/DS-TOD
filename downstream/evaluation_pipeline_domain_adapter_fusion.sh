gpu=$1
model=$2
bert_dir=$3
output_dir=$4
adapter_dir=$5
adapter_dir_2=$6
add1=$7
add2=$8
add3=$9

## DST
CUDA_VISIBLE_DEVICES=$gpu python main_domain_adapter_fusion.py \
    --my_model=BeliefTracker \
    --model_type=${model} \
    --dataset='["multiwoz"]' \
    --task_name="dst" \
    --earlystop="joint_acc" \
    --output_dir=${output_dir}/DST/MWOZ_stack_full/ \
    --do_train \
    --task=dst \
    --example_type=turn \
    --cache_dir="./save/transformers" \
    --model_name_or_path=${bert_dir} \
    --adapter_name_or_path=${adapter_dir} \
    --adapter_name_or_path_2=${adapter_dir_2} \
    --save_adapter_path=${output_dir}/DST/MWOZ_stack_full/RS \
    --batch_size=6 --eval_batch_size=6 \
    --usr_token=[USR] --sys_token=[SYS] \
    --eval_by_step=1000 \
    $add1 $add2 $add3

    
### Response Retrieval
#CUDA_VISIBLE_DEVICES=$gpu python main_domain_adapter_fusion.py \
#    --my_model=dual_encoder_ranking \
#    --do_train \
#    --task=nlg \
#    --task_name=rs \
#    --example_type=turn \
#    --model_type=${model} \
#    --model_name_or_path=${bert_dir} \
#    --output_dir=${output_dir}/RR/MWOZ_stack_full/ \
#    --cache_dir="./save/transformers" \
#    --adapter_name_or_path=${adapter_dir} \
#    --adapter_name_or_path_2=${adapter_dir_2} \
#    --save_adapter_path=${output_dir}/RR/MWOZ_stack_full/RS \
#    --batch_size=15 --eval_batch_size=100 \
#    --usr_token=[USR] --sys_token=[SYS] \
#    --fix_rand_seed \
#    --eval_by_step=1000 \
#    --max_seq_length=256 \
#    $add1 $add2 $add3
