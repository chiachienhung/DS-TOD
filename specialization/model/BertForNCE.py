import torch
from torch import nn, Tensor
from typing import Iterable, Dict
from transformers.modeling_outputs import SequenceClassifierOutput
from transformers import BertPreTrainedModel, BertModel
from torch import nn
from transformers.modeling_utils import (
    PreTrainedModel,
    apply_chunking_to_forward,
    find_pruneable_heads_and_indices,
    prune_linear_layer,
)
from transformers.adapters.model_mixin import ModelWithHeadsAdaptersMixin

from transformers.utils import logging

logger = logging.get_logger(__name__)


class BertForNCE(ModelWithHeadsAdaptersMixin, BertPreTrainedModel):
    def __init__(self, config):
        """
        :param model: Pretrained model
        """
        super().__init__(config)
        self.bert = BertModel(config)
        self.config = config
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, 1)
        self.init_weights()
        
    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        labels=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        pooled_output = self.bert(
            input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
        )
        pooled_output = pooled_output[1]
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output).view(-1, 3)
        loss = None
        if labels is not None:
            labels = labels.view(-1, 3)
            loss_fct = nn.BCEWithLogitsLoss()
            loss = loss_fct(logits, labels)

        return SequenceClassifierOutput(
            loss=loss,
            logits=logits,
            hidden_states=None,
            attentions=None,
        )
