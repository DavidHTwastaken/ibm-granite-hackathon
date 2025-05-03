import requests
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import time
from access import TOKEN

import json
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.foundation_models.utils.enums import DecodingMethods

my_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "api_key": TOKEN,
}
print(TOKEN)
client = APIClient(my_credentials)

gen_parms = {
    GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
    GenParams.MAX_NEW_TOKENS: 100
}
model_id = "ibm/granite-3-8b-instruct"
project_id = "c935f587-0211-4cd0-ac69-fa7f889f8a6a"
space_id = None
verify = False

model = ModelInference(
    model_id=model_id,
    credentials=my_credentials,
    params=gen_parms,
    project_id=project_id,
    space_id=space_id,
    verify=verify,
)

def generate_doc(project, format='markdown', description=''):
    instruction = f'Create a {format} document explaining the following project. The format of the input will be the file path of a file, followed by its content, for each file in the project.'
    if len(description) > 0:
        instruction += f'Here is some additional context: {description}'
    prompt = f'{instruction}\nInput:\n{project}'
    generated_text_response = model.generate_text(
        prompt=prompt, params=gen_parms)

    print("Output from generate_text() method:")
    print(generated_text_response)
    return generated_text_response


def main():
    # start = time.time()
    # project = open('tmp.txt', 'r').read()
    # load_time = time.time() - start

    project = '''
    backend/app.js 
    app.get("/api/login", (req, res) => {
  const params = querystring.stringify({
    client_id: process.env.SPOTIFY_CLIENT_ID,
    response_type: "code",
    redirect_uri: process.env.SPOTIFY_REDIRECT_URI,
    scope: "user-top-read user-read-recently-played",
  });

  res.redirect(`${SPOTIFY_AUTH_URL}?${params}`);
});

app.get("/api/callback", async (req, res) => {
  // console.log(req.query)
  // console.log(req.session)
  const code = req.query.code;
  if (!code) return res.redirect("http://localhost:5173/?error=login_failed");

  try {
    const response = await axios.post(
      SPOTIFY_TOKEN_URL,
      querystring.stringify({
        grant_type: "authorization_code",
        code,
        redirect_uri: process.env.SPOTIFY_REDIRECT_URI,
        client_id: process.env.SPOTIFY_CLIENT_ID,
        client_secret: process.env.SPOTIFY_CLIENT_SECRET,
      }),
      { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
    );
    req.session.access_token = response.data.access_token;
    // console.log(response.data)
    req.session.refresh_token = response.data.refresh_token;
    res.redirect("http://localhost:5173/hof");
  } catch (error) {
    console.error(
      "Error getting tokens:",
      error.response ? error.response.data : error
    );
    res.redirect("http://localhost:5173/?error=token_error");
  }
});
'''
    output = generate_doc(project)

if __name__ == '__main__':
    main()