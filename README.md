# SimpleLearning
Deep Lens Simple Learning
DeepLens Simple Learning Overview

Simple Learning provides out-of-the-box learning capability for DeepLens. It is a tool that allows users to train and perform recognition rapidly. 
It was borne out of my own experience of customizing deep lens for object detection. 

DeepLens is optimized for Apache MXNet, a scalable deep learning framework. SqueezeNet is a model that runs on the MXNet framework and performs categorization. SqueezeNet is trained on the image-net.org image set. Specifically, it was trained to identify 1000 image-net categories. SqueezeNet is used by the hotdog or no hotdog example, where a probability is returned that the object recognized is a hot dog. SqueezeNet can provide recognition when the camera sees images which closely match one of the 1000 categories it was trained on. Hog dogs are one of those categories. So are goldfish, bottlecap, canoe, mailbag, and four-poster bed. But what if the object you want to detect does not fall into one of these 1000 categories? 

One solution is to train your own model. SageMaker provides capabilities that can assist in this area. Creating your own model involves providing a large number of source images and the training process is computationally intense. But is there a simpler way to get started using deep lens in a practical way?

Let me back up for a moment and say I intended to use deep lens to identify whether a raccoon was eating out of our cat bowl. We have an outdoor cat who prefers eating outside. I would like to see if deep lens could notify me when a large animal, such as a raccoon or opossum was at the bowl. But I don’t want to be notified if our cat is eating at the bowl. So how do I do this? First, I looked up ‘raccoon’ in the list of 1000 image-net categories in the hope this would be a simple solution. But raccoon is not listed.  Then I got the idea that if deep lens saw a raccoon it might return a category match for something else, which is close enough to a raccoon to perform recognition. So I brought up photos of raccoons on my iPad and showed it to deep lens. The result. It responded with a high probability that it was an arctic fox!  Now since I don’t expect many arctic foxes in my backyard here in suburban New Jersey, I figured it was safe to recategorize arctic fox as raccoon. This ran successfully during training, but I soon found that different images of raccoons produced different results. When I provided a closeup of the raccoon image to deep lens it recognized it as a hamster. When I provided partially blocked images, it was a grey fox. So how to reconcile this inconsistency?

My approach was to collect a list of category matches that the model recognized as a racoon. Then I would overwrite the entry in the list of 1000 categories and insert the word Raccoon. There were just a handful. This worked fairly well.  Whenever deep lens recognized one of them, I would send a notification  to my cell phone using the Simple Notification Service (SNS)  with an image and a custom message. The image came from an S3 bucket. 
So I’ve customized the recognition for raccoons. Now what about oposums? I did the same for opossums. Now I can recognize two distinct animals. 
But it’s a lot of work to train and edit the lambda functions. Is there a general case where I can train for anything?

The answer is letting deep lens observe a background scene. Then perform detection on the differences. Simple Learning lets the model run, detecting high probability category matches and storing them in a list in an S3 bucket. During this time, normal motion is encouraged. You can walk past the frame, let the cat eat at the bowl, or allow whatever motion would be considered normal. Then switch to detection mode. Simple learning observes the frame, compares high probability category matches to the list created during training. And if a new category match is found, it notifies the user with SNS. This can be done with an SMS text message or an email. Notification include a link to the image, and some details on the object detected. You can also customize the text message based on the category found. 

Deep Lens requires power and an internet connection. But it can be portable using an AC Power Supply. So you can place it anywhere. 

Even outside. And if you use your phone as a hotspot, you can take it anywhere there is a cell phone signal.

Oh, and one more thing …

Alexa, tell deep lens to start training.

Alexa, tell deep lens to start detection.

You can customize the Alexa intents and sample utterances to suit your needs.

So that’s Deep Lens Simple Learning. It provides an easy way to get started with Deep lens. Customize it today, and build your own Simple Learning solution.



It turns out if you let deep lens observe a scene it comes up with a set of high probability matches for features within its view. If you collect those matches you create a background. 
The simple learning software on deep lens sends the image to the S3 bucket, constructs a JSON message with recognition details, including the URL, and publishes to an MQTT topic. 
This worked very well. But only when I showed deep lens images on my iPad. Why won’t this work in the general sense? The reason comes from the nature of deep learning. Deep learning performs feature extraction. It analyzes edges and gradients using a set of filters. It looks at an  image and asks “What is the probability that the features in this image match each of the 1000 categories?” So the result will be something like:

Arctic Fox:	52%
Hamster:	18%
Grey Fox:	10%
.
.
.
Mosquito Net: 0.01%

But images from an iPad are not real life. The edges and gradients will be different. The categories that match could be very different. So how do we solve this? 

The answer is to place the deep lens camera in the location where recognition will take place and let it train on the background. In my case, this means placing the camera so it views the back porch with the cat food bowl in the frame. Then I run the training and collect the categories where the probability exceeded a threshold (arbitrarily set to 50%). The camera is producing several frames/sec and deep lens is performing an analysis on each frame. If a subsequent frame produces a result where the probability of another category exceeds the threshold, I add that category to the list of background categories. During this time normal motion is encouraged. The cat should come and go, and if a person would normally walk by in the frame, they should do so during training. Essentially, you are capturing normal life. This is background capture. These are categories which will NOT produce a text message to your phone.
Training tends to produce no new results after a minute or so. Although it can be run longer to capture a wider variety of background categories. The training results are written to your S3 bucket in the admin folder. 
The raw results of the top 5 recognized categories are also written to the <bucket>/admin/raw_results folder.

Now that we have the background captured, how do we let deep lens detect what we are interested in? There are two ways:
1.	The simplest is to perform Simple Detection. Simple detection performs an analysis of each frame and if the probability of a category match exceeds a threshold, it compares it to the background category list. If the category is not in the background, then detection has occurred. The image is stored in an S3 bucket and notification sent to the user. An extension of this approach is subsetting. This involved culling the 1000 categories to only those which have a high possibility of being relevant. For example, if you were looking for a raccoon, you might add the addition constraint that you don’t want to be notified unless the category fits (Arctic Fox, Hamster, Grey Fox, or other animal categories). This manual curation of the list varies based on the desired results. In all cases, the threshold is arbitrary and better results may be obtained by adjusting this value. 
2.	The second way is positive training. In other words, let the raccoon have a good meal at your expense, and let deep lens capture the set of high probability categories during this session. Positive training is best since future visits by a raccoon will be very similar. The analysis of positive training results includes differentiation with background category results. In other words, that chair in the background was there whether the raccoon was eating or not. Background categories are filtered out of detection results. Currently, they are eliminated. A more realistic result should be applying a reduced probability when finding a background category in a detection frame. 

So what can you do with Simple Learning? In its most basic form, Simple Learning performs Simple Detection of categories which were not in the background training set. This is useful if changes in the environment must be detected but you don’t know in advance what those changes might be. It is far more than a motion detector, since normal motion is captured during training and will be filtered out during detection. Positive training involves a second step and is useful when the object you wish to detect is available for training.
In my raccoon example, simple training may alert me when either a raccoon or opossum approaches the cat bowl. But it also detects when a neighbor’s cat (who looks significantly different from my cat) eats at the bowl. It is a catch-all. And may provide false positives. It all depends on what you are looking for. The refinement (or culling) of the 1000 categories into just a subset may provide just opossums and raccoons and ignore the neighbor’s cat, if that is what you are interested in. Of course, these examples are meant as illustrations of what you can do with deep lens. The point is that deep lens can distinguish between categories. The use of this technology can be applied to any situation where detection of a category is desired. This can be a known category, such as the 1000 image-net categories, or something in between, which has elements of several categories. Essentially, we are mapping a real-world image to a set of image-net categories. It is helpful to view the categories not as hamsters, mittens, or milk cans. But as patterns of edges and gradients. These patterns match real-world objects with a certain probability. For example, an opossum is not listed in the list of 1000 categories. But it may be viewed as 52% hamster, 15% mitten, 10% milk can, and so forth. Capturing the probability for each category, in a sense, creates a new category. In other words, after training, deep lens now recognizes an object which is 52% hamster, 15% mitten and 10% milk can as an opossum. 

For best results, deep lens should have both training and detection runs performed from the same location. It is best to control for variables such as lighting and background motion when possible. In other words, it is best to train in the same lighting and with the same location as detection is performed. The camera should be kept in one spot.

