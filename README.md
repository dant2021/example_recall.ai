# Meeting Summary Generator

## Overview

This project is a Meeting Summary Generator that works with the Recall.ai Universal API for Meeting Bots. It takes meeting transcripts, summarizes them, and retains the link between the summarized text and the original transcript. The summarized data is structured for easy storage in a non-relational database like Firebase, allowing for fast and flexible retrieval in user applications.

## Features

- Breaks long transcripts into manageable chunks
- Generates summaries for each chunk using OpenAI's GPT-3.5-turbo model
- Maintains the connection between summary points and corresponding transcript sections
- Outputs a JSON file that can be easily stored in a non-relational database

## Getting Started

### Prerequisites

- Python 3.7 or higher
- OpenAI API key
- (Future implementation) Recall.ai API key
- (Future implementation) Firebase account and configuration

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/meeting-summary-generator.git
   cd meeting-summary-generator
   ```

2. Install the required packages:
   ```
   pip install openai requests
   ```

3. Set up your OpenAI API key:
   - Open `summarize_ai.py`
   - Replace `"your_API_key"` with your actual OpenAI API key

### Usage

1. Prepare your input:
   - Currently, the script uses a text file named `text_conversation.txt` as input
   - Place your transcript in this file in the project directory

2. Run the script:
   ```
   python summarize_ai.py
   ```

3. The script will generate a JSON file named `text_conversation_summary.json` containing the summarized data

### Output Structure

The output JSON file contains an array of "connected blocks", each representing a summarized chunk of the transcript. Each block includes:

- `block_summary`: A short summary of the entire block
- `block_index`: The index of the block in the transcript
- `block_start` and `block_end`: Timestamps for the start and end of the block
- `connected_items`: An array of items, each containing:
  - `timestamp`: The timestamp for this part of the conversation
  - `summary_point`: A bullet point summarizing this part
  - `transcript_part`: The corresponding part of the original transcript

## Future Improvements

- Implement direct integration with Recall.ai API for real-time transcript processing
- Add Firebase integration for database storage and retrieval
- Implement more robust error handling and retrying for failed API requests
- Add unit tests to ensure reliability of summarization and connection processes
- Create a user interface for easier interaction with the summarization tool

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
