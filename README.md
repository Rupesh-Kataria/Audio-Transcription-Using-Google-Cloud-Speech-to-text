# Real-Time Audio Transcription with Google's Live

This project allows you to transcribe audio captured through a microphone in real-time to text using Google Cloud Speech-to-Text service.

## Setup

Follow these steps to set up and run the project:

### 1. Install Required Packages

Make sure you have Python installed on your system. Install the all packages mentioned in requirements.txt file using  pip install -r requirements.txt:


### 2. Set up Google Cloud Service Account

To use the Google Cloud Speech-to-Text service, you need to set up a service account and obtain the necessary credentials:

1. Go to the Google Cloud Console (https://console.cloud.google.com/).
2. Create a new project or use an existing one.
3. Enable speech to text api by going "API & Services">"Library" page.
3. Navigate to the "IAM & Admin" > "Service Accounts" page.
4. Create a new service account with the role "Editor" or provide appropriate permissions.
5. Generate a new private key for the service account and download the JSON file containing your credentials.
6. Rename the JSON file to `audio.json` and place it in the project directory.

### 3. Configure Microphone

Ensure your microphone is properly connected and recognized by your system.

## Usage

Run the `main.py` script to start the real-time audio transcription. The transcribed text will be printed to the console as it becomes available.


## Demonstration

Check out this [video demonstration](link_to_your_video) to see how the code performs on voice.

## Code Structure

The `main.py` script initializes the Google Cloud Speech client, configures recognition and streaming parameters, and starts the audio stream for real-time transcription.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to open an issue or submit a pull request.



