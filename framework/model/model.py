from tensorflow.keras import Input
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense, TimeDistributed, Dropout, Bidirectional, Flatten, Lambda 

class BaseModel:
    def __init__(self, name, group, dataset, input_shape):
        self.name = name # name of the model 
        self.group = group 
        self.dataset = dataset  # Dataset() object
        self.input_shape = input_shape # Input shape

class BiLstm(BaseModel):
    """bi-lstm model information"""
    def __init__(self, name, group, dataset, input_shape, lstm_units, dropout, recurrent_dropout, embedding_output_dimensions, batch_size, epochs):
        """ all information required for training """
        super().__init__(name, group, dataset, input_shape)
        self.lstm_units = lstm_units # todo: write a method for determining units by default
        self.dropout = dropout # dropout layer 
        self.recurrent_dropout = recurrent_dropout # lstm recurrent dropout 
        self.embedding_output_dimensions = embedding_output_dimensions # first embedding layer 
        #self.output_dimensions = output_dimensions # might be a part of dataset 
        # training hyperparameters 
        self.batch_size = batch_size 
        self.epochs = epochs 

    def get_model(self):
        try:
            input = Input(shape=(self.dataset.max_len,))
            embedding = Embedding(input_dim=self.dataset.n_words, output_dim = self.embedding_output_dimensions, input_length = self.dataset.max_len)(input)
            lstm_layer = Bidirectional(LSTM(units=self.lstm_units, return_sequences=True,
                                            recurrent_dropout=self.recurrent_dropout,
                                            dropout=self.dropout))(embedding)
            output_layer = TimeDistributed(Dense(self.dataset.n_tags, activation='softmax'))(lstm_layer)
            model = Model(input, output_layer)
            return model
        except Exception as e:
            print("unable to compile model") # more descriptive errors 
            print(e)

class BiLstm2(BaseModel):
    """bi-lstm model information"""
    def __init__(self, name, group, dataset, input_shape, lstm_units1, lstm_units2, dropout, recurrent_dropout, embedding_output_dimensions, batch_size, epochs):
        """ all information required for training """
        super().__init__(name, group, dataset, input_shape)
        self.lstm_units1 = lstm_units1 # todo: write a method for determining units by default
        self.lstm_units2 = lstm_units2 # todo: write a method for determining units by default
        self.dropout = dropout # dropout layer 
        self.recurrent_dropout = recurrent_dropout # lstm recurrent dropout 
        self.embedding_output_dimensions = embedding_output_dimensions # first embedding layer 
        #self.output_dimensions = output_dimensions # might be a part of dataset 
        # training hyperparameters 
        self.batch_size = batch_size 
        self.epochs = epochs 

    def get_model(self):
        input = Input(shape=(self.dataset.max_len,))
        embedding = Embedding(input_dim=self.dataset.n_words, output_dim = self.embedding_output_dimensions, input_length = self.dataset.max_len)(input)
        lstm_layer = Bidirectional(LSTM(units=self.lstm_units1, return_sequences=True,
                                        recurrent_dropout=self.recurrent_dropout,
                                        dropout=self.dropout))(embedding)
        lstm_layer2 = Bidirectional(LSTM(units=self.lstm_units2, return_sequences=False,
                                         recurrent_dropout=self.recurrent_dropout,
                                         dropout=self.dropout))(lstm_layer)
        output_layer = TimeDistributed(Dense(self.dataset.n_tags, activation='softmax'))(lstm_layer2)
        model = Model(input, output_layer)
        return model
        #except Exception as e:
        #    print("unable to compile model") # more descriptive errors 
        #    print(e)
