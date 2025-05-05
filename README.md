# DocuScribe

Our submission to the Lean AI Solutions Hackathon, with IBM Granite Models, is a web application we call DocuScribe. This web application generates documentation for software projects from the source code and a verbal explanation of the project.

## Models

We run Granite 3.3 Speech-8B on the server to translate and extract speech from an audio clip provided by the user. Then, we pass the source code and transcript to Granite 3.3 Code Instruct to generate the documentation for the project.

## Setup

We leverage the Watsonx API to run foundation models, which means our server needs a developer access token to function.

Simply create an environment file (called `.env`) in the root directory with the following content:
`API_TOKEN=<YOUR TOKEN>`

**Requirements**

- Python 3.11 or higher
- Install packages from `requirements.txt` in `Backend/`
- Node.js 22 or higher
- Run `npm install` from `client/` directory
- ffmpeg is needed for the backend (changing sampling rate of audio)
