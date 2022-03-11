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
        super(RedditConfig, self).__init__(version=datasets.Version("1.0.0", ""), **kwargs)
        self.domain = domain
        self.data_dir = data_dir

class Reddit(datasets.GeneratorBasedBuilder):
    """Reddit Dataset."""
    VERSION = datasets.Version("1.0.0")
    BUILDER_CONFIGS = [
        RedditConfig(
            name="taxi",
            description="",
            domain="taxi",
            data_dir="../DomainReddit/taxi/all_concat.json",
        ),
        RedditConfig(
            name="attraction",
            description="",
            domain="attraction",
            data_dir="../DomainReddit/attraction/all_concat.json",
        ),
        RedditConfig(
            name="restaurant",
            description="",
            domain="restaurant",
            data_dir="../DomainReddit/restaurant/all_concat.json",
        ),
        RedditConfig(
            name="train",
            description="",
            domain="train",
            data_dir="../domainreddit/train/all_concat.json",
        ),
        RedditConfig(
            name="hotel",
            description="",
            domain="hotel",
            data_dir="../DomainReddit/hotel/all_concat.json",
        ),
        RedditConfig(
            name="hotel-train",
            description="",
            domain="hotel-train",
            data_dir="../DomainReddit/hotel-train/all_concat.json",
        ),
        RedditConfig(
            name="attraction-train",
            description="",
            domain="attraction-train",
            data_dir="../DomainReddit/attraction-train/all_concat.json",
        ),
        RedditConfig(
            name="restaurant-train",
            description="",
            domain="restaurant-train",
            data_dir="../domainreddit/restaurant-train/all_concat.json",
        ),
        RedditConfig(
            name="hotel-restaurant-taxi",
            description="",
            domain="hotel-restaurant-taxi",
            data_dir="../DomainReddit/hotel-restaurant-taxi/all_concat.json",
        ),
        RedditConfig(
            name="hotel-attraction-taxi",
            description="",
            domain="hotel-attraction-taxi",
            data_dir="../DomainReddit/hotel-attraction-taxi/all_concat.json",
        ),
        RedditConfig(
            name="restaurant-attraction-taxi",
            description="",
            domain="restaurant-attraction-taxi",
            data_dir="../DomainReddit/restaurant-attraction-taxi/all_concat.json",
        ),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description="",
            features=datasets.Features(
                {
                    "context": datasets.Value("string"),
                    "response": datasets.Value("string"),
                    "label": datasets.Value("int8"),
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
            label = dial['label']
            yield id_, {"context": context, "response": response, "label": label}