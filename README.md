## Measuring the Prevalence of Anti-Social Behavior in Online Communities.
##### Joon Sung Park, Joseph Seering, Michael S. Bernstein. 2022. Proceedings of the ACM on Human-Computer Interaction (CSCW ’22) 

### Background
This repository accompanies our CSCW'22 paper, "Measuring the Prevalence of Anti-Social Behavior in Online Communities," by Joon Sung Park, Joseph Seering, and Michael S. Bernstein. In it, we measured how much of the comments on Reddit are "macro-norm" violating and thus likely should have been moderated, and how much of them were actually moderated. We find that around 1 in 20 comments on the 97 most popular subreddits violate at least one of the macro norms, and only 5% of those violating comments are actually moderated. 

This repository includes two ingridients that could help you conduct such measurement studies yourself: 1) the code for gathering the moderated comments and their content from Reddit subcommunities, and 2) the model for classifying "macro-norm" violating comments that are historically moderated in a majority of 100 most popular subreddits (please note that our content moderation classification scheme is meant to only "flag" potentially violating comments, and not to be used as the final say in the moderation process). We will layout how to run the code and model included in this README page. Please consider checking out our paper in the CSCW proceeding or the abstract below to learn more about our work and the method we used: 

> Paper abstract: With increasing attention to online anti-social behaviors such as personal attacks and bigotry, it is critical to have an accurate accounting of how widespread anti-social behaviors are. In this paper, we empirically measure the prevalence of anti-social behavior in one of the world's most popular online community platforms. We operationalize this goal as measuring the proportion of unmoderated comments in the 97 most popular communities on Reddit that violate eight widely accepted platform norms. To achieve this goal, we contribute a human-AI pipeline for identifying these violations and a bootstrap sampling method to quantify measurement uncertainty. We find that 6.25% (95% Confidence Interval [5.36%, 7.13%]) of all comments in 2016, and 4.28% (95% CI [2.50%, 6.26%]) in 2020-2021, are violations of these norms. Most anti-social behaviors remain unmoderated: moderators only removed one in twenty violating comments in 2016, and one in ten violating comments in 2020. Personal attacks were the most prevalent category of norm violation; pornography and bigotry were the most likely to be moderated, while politically inflammatory comments and misogyny/vulgarity were the least likely to be moderated. This paper offers a method and set of empirical results for tracking these phenomena as both the social practices (e.g., moderation) and technical practices (e.g., design) evolve.

### Collecting Moderated Comments From Reddit 
Observing what sorts of content get moderated on various subreddits is important for understanding the moderation norms of these communities, and for building tools that can support their moderation efforts. The code in moderated-comment-collection folder will help you collect the content of these moderated comments, following the general scheme that Eshwar Chandrasekharan et al. used in their [2018 CSCW paper](http://www.eshwarchandrasekharan.com/uploads/3/8/0/4/38043045/eshwar-norms-cscw2018.pdf): 1) we live-stream all comments from the target subreddits to a server we own, and 2) individually verify which of the comments are moderated by querying Reddit's server via praw a day later. 

In moderated-comment-collection folder, there are two subfolders, collector and verifier that are meant to be run on different processes that collectively implements the scheme above: 
* "collector" live-streams all comments to a cloud (S3 AWS) server.
* "verifier" individually checks each of the comments a day later. 

To start run these code, take the following steps: 

1) Place the collector and verifier folder in separate machines (or separate processes in the same machine if the data collection is relatively small in scale).
2) Install the requirements for the collector and verifier. 
pip install -r requirements.txt
3) Fill in the variables in utils.py with your S3, AWS, and praw keys/IDs. 
4) Run collector first to start live-stream all comments from your subreddits of interest (look at the global_variables.py file to see the subreddits that we have used in our analysis -- you can modify this file to specify other subreddits). Run verifier a day later to check which of the comments were removed. 

### Classifying Comments for Macro-Norm Violations 
We define a comment to be macro-norm violating if most communities will choose to moderate it. To reflect this, we imeplement 97 classifers that are each trained on the moderation data of the 97 largest subreddits. You can find the models and their embeddings in the Google Drive here: 
https://drive.google.com/drive/folders/1MYdPMYpUtM4VKNmK5AaCbxS-u3t6QT9Y?usp=sharing

We shared the virtual environment folder as well in this release to make sure some of the libraries are still accessible for you (some of them are deprecated as of now so pip installing them might not get you what you need). Please feel free to download the entire package including the virtual environment, or only download the "src" folder and manually build the environment using the requirements.txt file. 

To classify comments, place your input comments in the "input" folder in "src" (I left an example input csv file in there to show how it should be formatted) and run teh "output_classification" function in the classify.py file. Your output will be put in the "output" folder. 
