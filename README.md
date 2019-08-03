# Flower classification with resnet

## About

This is based on the material presented in [Lesson 1: Image
classification](https://course.fast.ai/videos/?lesson=1) and [Lesson 2: Data
cleaning and production; SGD from
scratch](https://course.fast.ai/videos/?lesson=2) (the first half) of the
[Practical Deep Learning for Coders, v3](https://course.fast.ai) course by
fast.ai.

## Notebook

The kernel is available on
[Kaggle](https://www.kaggle.com/nkaretnikov/resnet-flowers).

To view locally:
```
jupyter notebook resnet-flowers.ipynb
```

## App

The `app` directory contains a "Flower classifier" web app, which
utilizes the created model.

As of writing this, the app is running on
[Heroku](https://resnet-flowers.herokuapp.com).

To deploy:
```
./app/scripts/deploy-heroku.sh
```

Heroku-related settings are in `Procfile`, `requirements.txt`, and
`runtime.txt`.  Note that a CPU version of pytorch is used on Linux due to the
[slug size limit](https://devcenter.heroku.com/articles/slug-compiler#slug-size).
