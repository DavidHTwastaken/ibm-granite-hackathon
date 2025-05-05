import React from 'react';

export function About() {
  return (
    <div>
      <h1>About Us</h1>
      <p>Our submission to the Lean AI Solutions Hackathon, with IBM Granite Models, is a web application we call DocuScribe. This web application generates documentation for software projects from the source code and a verbal explanation of the project.</p>
      <p>We run Granite 3.3 Speech-8B on the server to translate and extract speech from an audio clip provided by the user. Then, we pass the source code and transcript to Granite 3.3 Code Instruct to generate the documentation for the project.</p>
    </div>
  );
}

export default About;