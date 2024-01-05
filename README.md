# Magic Autocomplete
## This is a Magic: the Gathering decklist autocompletion tool
### Made by Julien Audet, not affiliated in any way to Magic: the Gathering nor to Wizards of the Coast

This project was made as my CEGEP integrator project. It has been made over the course of 20 weeks and 100+ hours of
research and work. A paper detailing the development process and results of the first version is available at: 
https://docs.google.com/document/d/1LHNd_-JQrEzRyDKt-MnAX0Gg7qHPufJPXdoyU1dHDbQ/edit?usp=sharing. 

This project aims to predict Magic: the Gathering decklists from subsets of those lists, as a player would do when
facing an opponent. A demo of the working tool is available on 
https://drive.google.com/file/d/1zIPOR6mSmvFgz_L1QG9-KxZphI7PVPhe/view?usp=sharing


## Organization
The project is divided in five main parts: data acquisition (scraping), data preprocessing, model training,
model evaluation, and model 


## How can I replicate the results?
  If you want to reuse the lists I did, simply run local_training.py to train a new model:
  
 ```python local_training.py```
 
Select the desired command line arguments in the file. By default, the number of epochs is set to 60. This takes me ~10 min to train on tf-cpu on a Ryzen 5 5600x. The best model yet was trained on 300 epochs, but very good results are obtained at 60+ epochs.
 
If you want to load your own lists, you'll first have to download all of the ones you want, place them in the data/unf_lists directory, and run report_code/format.py This will format all the lists. You can then run the second version of the code by calling local_training.py (make sure to first change the VOCAB_SIZE appropriately, in main_package/scripts/metadata.py)

## Usage
### 1) Gathering data
You can either use the lists present in the `data_21_01_2022` folder or dowload your own.
The lists should be placed in a folder named `./data`.
The unformatted lists have the default format from dowloading text lists on [MTG Goldfish](https://www.mtggoldfish.com)
Unformatted lists should be placed under `./data/unformatted_lists`. Each list should be under its
respective archetype folder, as is done in `data_21_01_2022/unformatted_lists`, e.g. `data_21_01_2022/unformatted_lists/Affinity/0.txt`.

If Magic, the Gathering decklists need to be downloaded, a web scraper (provided) can be used.


### What about the first version?
Either use the included lists or your own, see paragraph above. If you are using your own lists, make sure to run vectorize.py to create the vector embeddings. 
The types of model used are detailed in the paper (LS and LV), run the desired training code (train_LS or train_LV). train_LS.py will yield better results but take longer to train. 


# Versions
TODO


### If you like the project or find something that could be made better, please let me know! I'd love to hear what you think!

### Edit (04_2023):
* Added usage documentation