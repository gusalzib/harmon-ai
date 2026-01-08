# HarmonAI
Brought to you by **Team 3** 🥳

## Description
Do you like a song and want to play it on your instrument, but don't know the chords? HarmonAI has your back! Upload an mp3 file and let our AI transcribe the chords for you, or search our database and see if the song you're looking for has already been transcribed! 🎶

### Wiki
Information about requirements can be found in the [Wiki](https://git.chalmers.se/courses/dit826/2025/team3/-/wikis/home), and the corresponding issues can also be found in the [issues page](https://git.chalmers.se/courses/dit826/2025/team3/-/issues). For information about meetings and tasks/responsibilities, there is a section for that on a [separate section of the Wiki](https://git.chalmers.se/courses/dit826/2025/team3/-/wikis/home/Meetings)

## Gaining Access
**Our project is available on the cloud! Follow this link to visit our website:** http://34.51.250.115.nip.io/

### Creating an account
To unlock the full potential of our project, you can create an account with us! It comes with a **massive range of benefits**, specifically:
- None 🎉

### Administrator accounts
Not everyone can manage or create an administrator account. Security is a very important aspect to keep in mind on today's internet, so these are created internally. But, we're sure you'd like to try out some of the functionality yourself, so we've set up an account for you - the reader, literally anyone with access to this page - as well! 🤗

**Functionality of administrator accounts:**
- Upload new training data and trigger the training of a new model
- Choose which version of the model is active
- Look at model performance statistics and compare them side by side

If you promise you can be discrete 🤫, we'll share a **set of credentials with you**! 😊<br>
```
username: fran
password: fran
```

## Config Files Required to Build & Deploy
If you want to deploy the project yourself, either locally or on Google Cloud, you'll need to do some setup of your own. This is guaranteed to work for local deployment, with some features being unavailable, e.g. deploying a new model. Some scattered instructions on deploying with Minikube can be found at `team3/server/using-minikube.md`, but in addition to this you'll need to create some config files:

### Google credentials
Location(s):
- `team3/server/validation_training_service/HarmonAI_storage.json`
- `team3/server/prediction_service/HarmonAI_storage.json`
```
{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": "",
  "universe_domain": "googleapis.com"
}

```

### DB connection string
Location(s):
- `team3/server/users_project/.env`
```
DB_CONNECTION_STRING=<MongoDB database URL w/ username + password>
```

### Client top domain URL
Location(s):
- `team3/client/harmonai_frontend/.env.production`
```
VITE_API_URL=<URL/address to where the site will be hosted>
```

### 
Location(s):
- `team3/client/harmonai_frontend/.env`
```
VITE_GCS_BUCKET_NAME=
VITE_GCS_CLIENT_ID=
VITE_GCS_SCOPE=
VITE_API_URL=<URL/address to where the site will be hosted>
```