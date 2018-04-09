# oneshot-audio
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/zdmc23/oneshot-audio/blob/master/LICENSE)

Experiment with "one-shot learning" techniques to recognize a voice signature. This was my submission and demo for LVTech hack-a-thon 2018

![Alt text](/images/classify-example.png?raw=true "")

#### One-Shot Learning?

"People can learn a new concept from just one or a few examples, making meaningful generalizations that go far beyond the observed data. Replicating this ability in machines has been challenging, since standard learning algorithms require tens, hundreds, or thousands of examples before reaching a high level of classification performance" [1]. (With Deep Learning, the dataset requirement has grown to 100K+).

1. Lake, Lee, et. al. One-shot learning of generative speech concepts. 2014. (https://groups.csail.mit.edu/sls/publications/2014/lake-cogsci14.pdf).

#### Siamese Network

![Alt text](/images/siamese-net.jpeg?raw=true "") 

- G Koch, R Zemel, and R Salakhutdinov. Siamese neural networks for one-shot image recognition. In
ICML Deep Learning workshop, 2015. (http://www.cs.toronto.edu/~zemel/documents/oneshot1.pdf).
