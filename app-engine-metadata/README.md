App Engine example to access project metadata.

Replace YOUR-GOOGLE-PROJECT-ID-HERE in app.yaml with your project id

To add/update metadata, run the following gcloud command

```
$ gcloud compute project-info add-metadata --metadata <VAR-NAME>=<VAR-VALUE>
```
