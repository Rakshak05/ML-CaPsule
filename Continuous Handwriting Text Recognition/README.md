# Continuous Handwriting Text Recognition Pipeline

## Overview

This project focuses on extracting text from images as precisely as possible. This a Deep Learning + Natural Language Processing (NLP) Task. This uses a bidirectional Convolutional Recurrent Neural Network (bi-CRNN) model to identify the handwritten text from the images, combined with NLP enhancing its capability to produce meaningful sentences.

The deep learning model was trained on Teklia/IAM-line dataset.
Dataset link : https://huggingface.co/datasets/Teklia/IAM-line

## Models

The project uses bidirectional Convolutional Recurrent Neural Network (bi-CRNN) to process the sequential text in the image. There are two models trained - bi-LSTM (Bidirectional Long Short Term Memory) model and bi-GRU (Bidirectional Gated Recurrent Network) model. Raw CRNN is not used to tackle the vanishing gradient problem. The models were trained on the Teklia/IAM-line dataset, using techniques like dropout and early stopping to prevent overfitting. 

The Character Error Rate and Word Error Rate of the bi-LSTM model are 8.71% and 29.88% respectively.
The Character Error rate and Word Error Rate of the bi-GRU model are 8.61% and 30.41% respectively.

## Working

- An image with handwritten text is passed as the input. The image preferably has lesser whitespaces.
- The image is preprocessed by inverting the theme to white strokes on black background and further brightening and sharpening the image helping the model determine the text more precisely.
- The trained bi-CRNN models predict the sentence in the image and produce their predictions.
- The predictions of both bi-LSTM and bi-GRU models are combined to produce an optimal output (Ensembling).
- The output produced by the models may still carry ambiguous words with no proper meaning where NLP steps in.
- The produced text is processed using techniques like Predictive word segmentation and Greedy-word Recombination producing legible sentences.

## Outputs
<img width="1134" height="388" alt="image" src="https://github.com/user-attachments/assets/bfe2334a-0179-4ad8-8330-ea385f14a7f5" />

Here, the models process the given image containing the sentence: The commander is a nice person.

However, they are not able to produce the exact text, where NLP steps in to produce as precise and meaningful text as possible.
