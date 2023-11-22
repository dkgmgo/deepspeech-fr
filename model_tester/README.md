# front

### Project setup

```
cd front
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

# back

### trainings

If you run the model locally, your training results are saved in a trainings folder in the root directory. If this is not the case, create it and put your results in it.

### change directory to root

```
cd deepspeech-fr
```

### run the api with gunicorn

```
gunicorn model_tester.back.api:app
```
