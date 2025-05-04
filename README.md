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
