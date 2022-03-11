import json
import os
import random
import datasets

# _CITATION = """
# """

# _DESCRIPTION = """
# """

class RedditConfig(datasets.BuilderConfig):
    """BuilderConfig for Reddit."""

    def __init__(
        self,
        domain,
        data_dir,
        **kwargs,
    ):
        """BuilderConfig for Reddit.
        Args:
          domain: `string`, which domain in use
          data_dir: `string`, directory to load the file from
          **kwargs: keyword arguments forwarded to super.
        """
        super(RedditConfig, self).__init__(version=datasets.Version("1.0.1", ""), **kwargs)
        self.domain = domain
        self.data_dir = data_dir

class Reddit(datasets.GeneratorBasedBuilder):
    """Reddit Dataset."""
    VERSION = datasets.Version("1.0.1")
    BUILDER_CONFIGS = [
        RedditConfig(
            name="taxi",
            description="",
            domain="taxi",
            data_dir="../DomainReddit/taxi/all_concat_new.json",
        ),
        RedditConfig(
            name="attraction",
            description="",
            domain="attraction",
            data_dir="../DomainReddit/attraction/all_concat_new.json",
        ),
        RedditConfig(
            name="restaurant",
            description="",
            domain="restaurant",
            data_dir="../DomainReddit/restaurant/all_concat_new.json",
        ),
        RedditConfig(
            name="train",
            description="",
            domain="train",
            data_dir="../DomainReddit/train/all_concat_new.json",
        ),
        RedditConfig(
            name="hotel",
            description="",
            domain="hotel",
            data_dir="../DomainReddit/hotel/all_concat_new.json",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description="",
            features=datasets.Features(
                {
                    "context": datasets.Value("string"),
                    "response": datasets.Value("string"),
                    "false_response_hard": datasets.Value("string"),
                    "false_response_soft": datasets.Value("string")
                }
            ),
            supervised_keys=None,
            homepage="",
            citation="",
        )
    
    def _split_generators(self, dl_manager):
        data_file = dl_manager.download_and_extract(self.config.data_dir)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": data_file,
                },),]

    def _generate_examples(self, filepath):
        """Yields examples."""
        with open(filepath,  "r") as f:
            json_reader = json.load(f)
            
        for id_, dial in enumerate(json_reader):
            context = dial['context']
            response = dial['response']
            false_response_hard = dial['false_response'][0]
            false_response_soft = dial['false_response'][1]
            yield id_, {"context": context, "response": response, "false_response_hard": false_response_hard, "false_response_soft": false_response_soft}