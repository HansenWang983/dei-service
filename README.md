# Serverless Framework Python Flask API on AWS

Develop and deploy flask based DEI service API running on AWS Lambda using the traditional Serverless Framework.




## Anatomy of the project

This project configures a single function, `api`, which is responsible for handling all incoming requests thanks to configured `httpApi` events. To learn more about `httpApi` event configuration options, please refer to [httpApi event docs](https://www.serverless.com/framework/docs/providers/aws/events/http-api/). As the events are configured in a way to accept all incoming requests, `Flask` framework is responsible for routing and handling requests internally. The implementation takes advantage of `serverless-wsgi`, which allows you to wrap WSGI applications such as Flask apps. To learn more about `serverless-wsgi`, please refer to corresponding [GitHub repository](https://github.com/logandk/serverless-wsgi). Additionally, the template relies on `serverless-python-requirements` plugin for packaging dependencies from `requirements.txt` file. For more details about `serverless-python-requirements` configuration, please refer to corresponding [GitHub repository](https://github.com/UnitedIncome/serverless-python-requirements).



### Enviroment

- Customize the ethnicolr API and use `census_ln(df, namecol, year=2010)` & `pred_wiki_name(df, namecol, num_iter=100, conf_int=0.9)`for race inference
- Use python:3.8-slim as base image and build a docker image from Dockerfile
- the output catagory can be mapped into 5 general ethnicities:
  - White
  - Hispanic/Latino
  - Black
  - Asian
  - Other



## Usage

### Prerequisites

1. Push the image built from Dockerfile in this repo to a private docker image repository in ECR.

   AWS CLI setup:

   - If have 2FA enabled, update aws credentials with received AccessKeyId, SecretAccessKey, and SessionToken. AWS recommends having either cron job to refresh token. You can increase sessions by providing -duration-seconds but only up to 36 hours. A good explanation can be found at [authenticate-mfa-cli](https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/).

   Then, 

   ```bash
   # Retrieve an authentication token and authenticate the Docker client to your registry.
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 
   ECR_REGISTRY_REPO_URL
   
   # Build the Docker image.
   docker build -t IMAGE_NAME .
   
   # After the build completes, tag and push the image to this repository.
   docker tag IMAGE_NAME ECR_REGISTRY_REPO_URL
   
   # Run the following command to push this image to the newly created AWS repository:
   docker push ECR_REGISTRY_REPO_URL
   ```

​		

2. In serverless.yaml, change the name of image in function configuration to the uri of image in ECR repository.



### Deployment

In order to deploy with serverless dashboard, you need to first login with:

```
serverless login
```

install dependencies with:

```
npm install
```

and then perform deployment with:

```
serverless deploy
```

After running deploy, you should see output similar to:

```bash
Deploying aws-python-flask-api-project to stage dev (us-east-1)

✔ Service deployed to stack aws-python-flask-api-project-dev (182s)

endpoint: ANY - https://xxxxxxxx.execute-api.us-east-1.amazonaws.com
functions:
  api: aws-python-flask-api-project-dev-api (1.5 MB)
```

_Note_: In current form, after deployment, the API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [httpApi event docs](https://www.serverless.com/framework/docs/providers/aws/events/http-api/).



### Invocation

After successful deployment, you can call the created application via HTTP:

```bash
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev/
```

Which should result in the following response:

```
{"message":"Hello from root!"}
```

Calling the `/hello` path with:

```bash
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev/hello
```

Should result in the following response:

```bash
{"message":"Hello from path!"}
```

If you try to invoke a path or method that does not have a configured handler, e.g. with:

```bash
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev/nonexistent
```

You should receive the following response:

```bash
{"error":"Not Found!"}
```



DEI Service API:

```
curl --location --request POST 'https://xxxxxxx.execute-api.us-east-1.amazonaws.com/dev/analyze' \
--header 'Content-Type: application/json' \
--data-raw '{
    "uuid": "12345",
    "names": [
        {
            "last_name": "ramsey",
            "first_name": "joel"
        },
        {
            "last_name": "hurst",
            "first_name": "robin"
        },
        {
            "last_name": "bast",
            "first_name": "kelvin"
        },
        {
            "last_name": "davis",
            "first_name": "c grier"
        },
        {
            "last_name": "deangelus",
            "first_name": "alfred"
        },
        {
            "last_name": "brewer",
            "first_name": "herbert"
        }
	]
}'
```



### Test with 100 names

response time: 10-20 seconds without a GPU setup.

inputs are from app/ethnical/data/input-with-header.csv

results in test_response.json



### Local development

Thanks to capabilities of `serverless-wsgi`, it is also possible to run your application locally, however, in order to do that, you will need to first install `werkzeug` dependency, as well as all other dependencies listed in `requirements.txt`. It is recommended to use a dedicated virtual environment for that purpose. You can install all needed dependencies with the following commands:

```bash
pip install werkzeug
pip install -r requirements.txt
```

At this point, you can run your application locally with the following command:

```bash
serverless wsgi serve
```

For additional local development capabilities of `serverless-wsgi` plugin, please refer to corresponding [GitHub repository](https://github.com/logandk/serverless-wsgi).	
