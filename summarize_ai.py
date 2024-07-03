import re
from openai import OpenAI
import json

client = OpenAI(api_key = "your_API_key")

def break_into_pieces(filename, max_chars=10000):
    with open(filename, 'r') as file:
        content = file.read()
    
    blocks = []
    current_block = ""
    
    for line in content.split('\n'):
                
        if len(current_block) < max_chars:
            current_block += line + '\n'

        else:
            blocks.append(current_block)
            current_block = ""
    
    return blocks


preRequestContent = "The following is a part of conversation (note: this is not a whole conversation): \""

requestContent = "\"\n\nReturn:\n1. Summary of the conversation, in bullet points format, with who said them.\n2. A SHORT summary of the conversation (~10 words).\nAlso add timestamps in parentheses for each bullet point (DO NOT FORGET THAT).\nFor example (use this bullet points format):\n1.\n- Florian Riesenkampf describes his current startup, which focuses on building tooling for working with LLM models. (00:05:15)\n- You share that a former co-founder is also working on a similar concept and mention prior knowledge of competition in the space. (00:12:22)\n2. Short summary:\nYou share your view on Florian's startup."

def summarize(block):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes conversations."},
                {"role": "user", "content": preRequestContent + block + requestContent}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in summarization: {e}")
        return None
    
def connect_summary_transcript(original_blocks, summaries):
    connected_blocks = []
    timestamp_pattern = r'\d{2}:\d{2}:\d{2}'
    
    for block_index, (block, summary) in enumerate(zip(original_blocks, summaries)):
        bullet_points = summary.split('\n')
        all_timestamps = re.findall(timestamp_pattern, block)
        block_start = all_timestamps[0]
        block_end = all_timestamps[-1]
        block_summary = bullet_points[-1]  # Assuming the last line is the short summary

        connected_items = []
        
        for i, point in enumerate(bullet_points[:-1]):  # Exclude the last line (short summary)
            current_match = re.search(timestamp_pattern, point)
            if current_match:
                current_timestamp = current_match.group()
                start_index = block.find(current_timestamp)
                
                if start_index == -1:
                    print("timestamp not found")
                    continue # If the current timestamp is not found, skip this bulletpoint
                
                next_timestamp = None
                if i < len(bullet_points) - 2:  # -2 because we're excluding the last line
                    next_match = re.search(timestamp_pattern, bullet_points[i+1])
                    if next_match:
                        next_timestamp = next_match.group()
                
                if next_timestamp and next_timestamp in block:
                    end_index = block.find(next_timestamp)
                else:
                    end_index = block.rfind(all_timestamps[-1])


 
                transcript_part = block[start_index:end_index].strip()
                
                connected_item = {
                    'timestamp': current_timestamp,
                    'summary_point': point.strip(),
                    'transcript_part': transcript_part
                }
                    
                connected_items.append(connected_item)

        connected_block = {
            'block_summary': block_summary,
            'block_index': block_index,
            'block_start': block_start,
            'block_end': block_end,
            'connected_items': connected_items
        }

        connected_blocks.append(connected_block)
    
    return connected_blocks

def save_to_json(connected_blocks, input_filename):
    # Extract the base name without extension
    base_name = input_filename.rsplit('.', 1)[0]
    output_filename = f"{base_name}_summary.json"
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(connected_blocks, f, ensure_ascii=False, indent=2)
    
    print(f"Data saved to {output_filename}")

def main():
    # Break the transcript into pieces
    input_filename = "text_conversation.txt"
    blocks = break_into_pieces(input_filename)
    
    print(f"Number of blocks: {len(blocks)}")
    for i, block in enumerate(blocks):
        print(f"Block {i+1} length: {len(block)} characters")
        print(f"Block {i+1} starts with: {block[:50]}...")
        print("---")
    
    # Summarize each block
    summaries = [summarize(block) for block in blocks]
    
    # Connect summaries with original transcript
    connected_blocks = connect_summary_transcript(blocks, summaries)
    print(f"Number of connected blocks: {len(connected_blocks)}")

    # Save the connected blocks to a JSON file
    save_to_json(connected_blocks, input_filename)

    # Optionally, print a sample of the results
    if connected_blocks:
        print("\nSample of first connected block:")
        print(json.dumps(connected_blocks[0], indent=2))

if __name__ == "__main__":
    main()
