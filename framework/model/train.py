import numpy as np
import os
import json
from ..vocab.vocabulary import load_global_vocabulary, merge_vocabs
from ..config import * 

class ModelTrainer:
    """Class for training a NER model"""
    def __init__(self, model=None, dataset=None):
        self.model = model
        self.dataset = dataset

    def train(self,model, dataset):
#        try:
            # Get the layers of the model and then train
        model_layout = model.get_model()

        model_layout.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        model_layout.fit(np.array(dataset.x_train), np.array(dataset.y_train), validation_split=0.1,
                            batch_size=model.batch_size, epochs=model.epochs)

        self.save_model(model, model_layout, dataset) # store the trained model to disk

        return model_layout
#        except Exception as e:
#            print(e)
#            print("Unable to train model")


    def save_model(self, model_info, trained_model, dataset):
        """
        Need to save the following files
               +-- ModelWeights.h5  -> Weights of the trained model
               +-- Model.json       -> Definition of the model
               +-- Vocabulary.json  -> Mapping of the words used in the model to numerical values
        """
#        save_dir = "extraction/model/models/" + model_info.group + "/" + model_info.name + "/"

        save_dir = config['models-directory'] + model_info.group + "/" + model_info.name + "/"
        print("saving to " + save_dir)

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        model_json = trained_model.to_json()
        with open(save_dir+"Model.json", "w") as json_file:
            json_file.write(model_json)
        trained_model.save_weights(save_dir + "ModelWeights.h5")

        vocab_list = []
        for word,index in dataset.dictionary.items():
            dict_item = {}
            dict_item["word"] = word
            dict_item["index"] = index
            vocab_list.append(dict_item)
        #print(vocab_list)

        vocab_json = json.dumps(vocab_list)
        #vocab_json = json.dumps(vocab_list, load_global_vocabular)

        tags = json.dumps({"categories": list(dataset.categories)})

        with open(save_dir+"Vocabulary.json", "w") as vocab_file:
            vocab_file.write(vocab_json)

        with open(save_dir+"Categories.json", "w") as tags_file:
            tags_file.write(tags)
