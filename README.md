
# Battling misinformation: A data-driven approach introducing the BERT model  

This GitHub repository was created as part of my Bachelor thesis project on Fake News Detection using BERT (Bidirectional Encoder Representations from Transformers). This thesis has a dual mission: to explore the landscape of fake news and to create a deep-dive explanation of the BERT model for anyone starting in NLP.  

## Original Paper

[Battling misinformation: A data-driven approach introducing the BERT model](https://linktodocumentation)

## Requirements

The models were built and trained on Google Colab Pro with the V100 GPU. There is no installation needed if the program is ran in Google Colab, only downloading the datasets and changing the file paths, if needed, is required.

## Methodology

Two python notebooks were created:
-  [data_exploration_processing.ipynb](https://github.com/halimyoussef/FakeNewsClassifier-BERT/blob/main/data_exploration_processing.ipynb) --> EDA, combination of FEVER and UKPSnopes, data preprocessing, data splitting
-  [model_training_evaluation.ipynb](https://github.com/halimyoussef/FakeNewsClassifier-BERT/blob/main/model_training_evaluation.ipynb) --> Comparison of model training and predictions

Four models are built with "_bert-base uncased_" from the hugging face library and an added dense layer with a softmax activation function for classification, each is trained differently such as :

- Claim-Only model
- ETS-Only model
- Double-Input model
- Double-Input model with frozen BERT parameters

After each epoch (only 11 because of RAM limits), a model checkpoint saved the weights if the AUC increased.

Training and comparing these different models allows us to understand the inpact of training data when it comes to Fake News as well as I understand the impact of fine-tuning BERT's pre-trained embeddings. 

## Dataset

To trained the models, I created one dataset using two corpuses :
- UKPSnopes
- FEVER

Here is an example of one instance :

| label | claim | numerical label | ETS (Evidence text snippets)|
| --- | --- | --- | --- |
| TRUE | gianluigi buffon won an award for goalkeeping. | 1 | he was the first ever goalkeeper to win the golden foot award, and was also named the iffhs world's best goalkeeper a record five times, alongside iker casillas and manuel neuer |
|FALSE|narendra modi is not a member of the bharatiya janata party.|0| he is a member of the bharatiya janata party (bjp) and of the rashtriya swayamsevak sangh (rss), a right wing hindu nationalist paramilitary volunteer organisation|

While the UKPSnopes corpus comes with already fetched ETS created from the fact-cheking website _Snopes_, FEVER's ETS had to be fetched with the Wikipedia library on [ets_extraction.ipynb](https://github.com/halimyoussef/FakeNewsClassifier-BERT/blob/main/ets/ets_extraction.ipynb)

## Results

Here are the results after predictions on unseen claims :

| Model | Accuracy | Precision | Recall | AUC |
|---|---|---|---|---|
| **Claim-Only** | 87.14% | 87.42% | 85.94% | 93.79% |
| **ETS-Only** | 56.02% | 82.73% | 12.16% | 79.04% |
| __**_Double_**__ | ___82.97%___ | ___77.00%___ | ___92.71%___ | ___91.74%___ |
| **Double-Frozen** | 59.36% | 54.84% | 93.45% | 74.21% |

Overall, all non-frozen models overfitted pretty quickly after only a few epochs. While the Double-Input also show signs of over-fiiting, it happened later than Claim-Only. It is also the most versatile between the three. 

We then trained another Double-Input model while freezing BERT's embeddings. This time the model did not show signs of overfitting at all but failed to have high enough precision and accuracy. Maybe with a higher number of epochs we could have seen these values increase however.

## Conclusion

While the BERT seems to to have a pretty good understanf of the language, it does not seem to be capable of linking ETS to unseen claims. This is probabily because claims contains crucial informations, such as the subject name and family name, that sometimes are not present in the ETS, explaining the recall value of the ETS-Only model. Therefore, it is very important to work alongside fact-checkers when training fake news classifier as the training data is absolutely crucial for it to be efficient.
