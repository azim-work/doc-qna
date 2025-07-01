def chunk_text(full_text: str, tokenizer, target_chunk_size: int = 300):
    paragraphs = full_text.split("\n ")
    chunks = []
    cur_chunk = ""
    cur_chunk_size = 0

    for para in paragraphs:
        # Strip leading and trailing whitespace from the paragraph
        para = para.strip()

        # Skip empty paragraphs
        if not para:
            continue

        # Number of tokens in the paragraph
        para_size = len(tokenizer.encode(para))

        if para_size > target_chunk_size:
            # Skip paragraphs that are larger than the target chunk size for now
            continue

        # If adding the paragraph exceeds the target chunk size, save the current chunk and start a new one with the current paragraph
        if cur_chunk_size + para_size > target_chunk_size:
            if cur_chunk:
                # Append the current chunk to the list of chunks
                chunks.append(cur_chunk.strip())

            # Start a new chunk with the current paragraph
            cur_chunk = para
            cur_chunk_size = para_size

        # Otherwise, add the paragraph to the current chunk
        else:
            cur_chunk += "\n\n" + para
            cur_chunk_size += para_size

    # Add the last chunk if it exists
    if cur_chunk:
        chunks.append(cur_chunk.strip())

    return chunks
