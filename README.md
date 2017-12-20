# dike
[CS492] May the justice w/ you.

![](http://imgd.rgcdn.nl/c1b2c416dd5248fc8022f08ad93f4f55/opener/Justitie-zegt-in-een-brief-aan-de-informateur-meer-geld-nodig-te-hebben-foto-pixabay-com.jpg)

We aim to paraphrase written judgment to enhance readability by crowdsourcing workflow. We introduce Split-Polish-Connect-Revise workflow for the paraphrasing. It doesn’t require experts for paraphrasing, which could reduce the cost to make more readable written judgments.

We support three tasks : (1) People can contribute to paraphrase statements in written judgment, (2) People can see which part of written judgment is hard to understand, and (3) People can browse the paraphrased written judgment, which usually has better readability. Below shows how we proceed each task in our platform.

### Description

- In main django project `dike/`,
  - webdike app (incl. models, views, urls, natural_selection) is in `dike/webdike/`.
  - templates (.html) are in `dike/templates`.
  - static files (.css, .js, .png) are in `dike/webdike/static`.
- A judgement (.txt) for deploy is in `data/`.
- LICENSE, README, requirements.txt are in `root`.

### [Paper](https://github.com/todoaskit/dike/blob/master/jung2017dike.pdf)

