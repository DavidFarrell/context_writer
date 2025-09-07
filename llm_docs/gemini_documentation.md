
# The Unofficial Gemini API Developer's Guide (Comprehensive Edition)

This guide provides a comprehensive, structured overview of how to use the Gemini API, covering core capabilities, advanced features, and a dedicated section on mastering the persistent context required for sophisticated applications.

## 1. Getting Started: A Minimal Example

To begin, ensure you have the necessary library installed and your client initialized.

<details>
<summary><b>View Code Examples (Python, JS, Go, REST)</b></summary>

**Python**
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
)
print(response.text)
```
**JavaScript**
```javascript
import { GoogleGenAI } from "@google/genai";
const ai = new GoogleGenAI({});

async function main() {
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "How does AI work?",
  });
  console.log(response.text);
}
main();
```
**Go**
```go
package main
import ("context"; "fmt"; "log"; "google.golang.org/genai")

func main() {
  ctx := context.Background()
  client, err := genai.NewClient(ctx, nil)
  if err != nil { log.Fatal(err) }
  result, _ := client.Models.GenerateContent(ctx, "gemini-2.5-flash", genai.Text("Explain how AI works..."))
  fmt.Println(result.Text())
}
```
**REST**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents": [{"parts": [{"text": "How does AI work?"}]}]}'
```
</details>

## 2. Mastering Context Management

For an application like a writing assistant, managing a large, dynamic context is the central challenge. The following tools provide the fine-grained control needed to build your "context minimap."

### 2.1. The API is Stateless: You Are in Control

Every call to `generate_content` is independent. The API does not remember previous requests. This gives you complete control over the context provided in each turn. You will manually construct the context for each request based on what the user has loaded or enabled in your application's UI.

### 2.2. The File API: Your Context Library

Before using large documents (PDFs, text files) or media (videos, audio), you must upload them using the File API. This creates a durable reference to your file.

**File API Lifecycle:**
1.  **Upload:** Send your file to the API.
2.  **Process:** The API processes the file asynchronously.
3.  **Use:** Once processed, include the file's URI in your prompts.

<details>
<summary><b>View Python Code for Uploading and Using a File</b></summary>

```python
import time
from google import genai

client = genai.Client()

# 1. Upload a file
document_file = client.files.upload(
    path="/path/to/your/research_paper.pdf",
    display_name="Primary Research Article"
)

# 2. Wait for the file to be processed
while document_file.state.name == "PROCESSING":
    print('Waiting for file to be processed.')
    time.sleep(10)
    document_file = client.files.get(document_file.name)

if document_file.state.name == "FAILED":
  raise ValueError(document_file.state.name)

# 3. Use the file in a prompt
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[
        document_file,
        "Summarize the key findings of this research paper."
    ]
)
print(response.text)
```

> **Developer's Note: `display_name` and Your UI**
>
> The `display_name` you provide during upload is the crucial link between the backend `File` object and your frontend UI. When you call `client.files.list()`, you will use this human-readable name to populate the labels in your "context minimap." This allows the user to manage their context by name, while your application uses the corresponding `name` (the unique ID) to interact with the API.

</details>

### 2.3. Context Caching: For High-Frequency, Stable Context

For foundational context that will be used across many API calls (style guides, key research), you can place it in a **cache**. Instead of paying for the tokens in that stable context with every API call, you pay a small fee to create and store the cache, drastically reducing cost and speeding up API calls.

<details>
<summary><b>View Python Code for Context Caching</b></summary>

```python
from google import genai

client = genai.Client()
# This assumes 'document_file' from the previous example exists

# 1. Create a cache with your foundational context
cached_content = client.cache.create(
    model="gemini-2.5-flash",
    display_name="writing_style_and_tone_guide",
    contents=[
        "Rule #1: Always use a professional but approachable tone.",
        document_file
    ]
)

# 2. Use the cache in a new prompt
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Write a short introductory paragraph about AI, keeping our style guide in mind."],
    cached_content=cached_content
)
print(response.text)
```</details>

### 2.3a. Strategy: When to Use Caching vs. the File API

For an advanced application, choosing the right tool for your context is a key strategic decision that impacts performance and cost.

*   **Use the File API for Transient Context:**
    *   **When:** The context is large but will only be used once or a few times in a session.
    *   **Example:** A user uploads a specific article to be summarized or a video to be analyzed *right now*.
    *   **Cost Model:** You pay the full token cost for this context **every time** you include it in an API call.

*   **Use Context Caching for Stable Context:**
    *   **When:** The context is foundational and will be reused across many API calls.
    *   **Example:** A style guide, the user's biography, previous writings that define their tone, or core research that underpins a long writing session.
    *   **Cost Model:** You pay a small, one-time fee to create the cache and a minimal fee for storage. In exchange, you **do not pay the token cost** for the cached content in subsequent API calls, leading to massive savings.
```

***


### 2.4. Proactive Token Management: Powering Your "Minimap"

To build your visual context map, you need to know how many tokens each piece of context consumes. The `count_tokens` method is your primary tool for this.

*   **Gemini 2.5 Pro / Flash Max Context:** 1,048,576 tokens

<details>
<summary><b>View Python Code for Counting Tokens</b></summary>

```python
from google import genai

client = genai.Client()
model = client.models.get("gemini-2.5-pro")

# Assume you have several pieces of context loaded
context_to_send = [
    "This is my new dictation to be cleaned up...",
    client.files.get("files/your-uploaded-pdf-id"),
    client.files.get("files/your-uploaded-video-id")
]

# Calculate the token count for the entire context
response = model.count_tokens(contents=context_to_send)
total_tokens = response.total_tokens

print(f"Total tokens in current context: {total_tokens}")
print(f"Model's maximum input tokens: {model.input_token_limit}")

if total_tokens > model.input_token_limit:
    print("Warning: Context exceeds model's maximum limit.")
```
</details>

***


### 2.5. Managing the Context Lifecycle (List, Get, Delete)

A production application requires the ability to manage context objects over time. These operations are what will power your UI, allowing users to see what's in context and remove items.

#### Listing Your Objects
To populate your "minimap" UI, you can retrieve a list of all your uploaded files or created caches.

```python
# List all uploaded files
for f in client.files.list():
    print(f"File ID: {f.name}, Display Name: {f.display_name}")

# List all created caches
for c in client.cache.list():
    print(f"Cache ID: {c.name}, Display Name: {c.display_name}")
```

#### Retrieving an Object by Name
If you have the ID (the `name` attribute) of a file or cache, you can retrieve it directly without needing to list everything. This is useful for re-using context across sessions.

```python
# Get a specific file
retrieved_file = client.files.get(name="files/your-file-id-123")

# Get a specific cache
retrieved_cache = client.cache.get(name="cachedContents/your-cache-id-abc")
```

#### Deleting an Object
When a user removes an item from their context, you should delete the corresponding object to manage storage and keep your application clean. **Note:** `CachedContent` is immutable and does not have an `update` method. If you need to change a cache, you must delete the old one and create a new one.

```python
# Delete a file from Gemini's storage
client.files.delete(name="files/your-file-id-123")
print("File deleted.")

# Delete a cache
client.cache.delete(name="cachedContents/your-cache-id-abc")
print("Cache deleted.")
```




## 3. Core Capabilities

### 3.1. Text Generation and Chat

#### Standard and Streaming Generation
For interactive applications, use `generate_content_stream` to receive chunks of the response as they are generated.

<details>
<summary><b>View Python Code for Streaming</b></summary>

```python
from google import genai

client = genai.Client()

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=["Explain how AI works"]
)
for chunk in response:
    print(chunk.text, end="")
```
</details>

#### Multi-turn Conversations (Chat)
While the SDK provides a `chat` object for convenience, for full control over your application's context, you will manually manage the conversation history by constructing the `contents` list with alternating `"user"` and `"model"` roles for each API call.

<details>
<summary><b>View REST Example for Manual Chat History</b></summary>

```bash
curl https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "contents": [
      {"role": "user", "parts": [{"text": "Hello"}]},
      {"role": "model", "parts": [{"text": "Hi there! How can I help?"}]},
      {"role": "user", "parts": [{"text": "What is the capital of France?"}]}
    ]
  }'
```
</details>

#### Combining Cached Context with Chat History
For a sophisticated editing workflow, the most powerful pattern is to combine a stable, cached context with the dynamic history of the current conversation. This gives the model both the foundational knowledge (from the cache) and the immediate back-and-forth of the editing process.

The example below shows how to use `cached_content` for the style guide while simultaneously providing the recent chat history in the `contents` list.

<details>
<summary><b>View Python Code for Combined Context</b></summary>

```python
# Assumes 'cached_content' is the cache object holding your style guide
# from Section 2.3

# The user dictates, and the model provides a first draft
conversation_history = [
    {
        "role": "user",
        "parts": ["(User's dictation about AI)... Transcribe this and turn it into a blog post intro."]
    },
    {
        "role": "model",
        "parts": ["Artificial Intelligence is poised to reshape our world... (Version 1 of the text)"]
    }
]

# Now, the user provides feedback. You add their feedback to the history.
user_feedback = "That's a good start, but can you make it more impactful and mention the year 2024?"
conversation_history.append({"role": "user", "parts": [user_feedback]})


# Make the API call with BOTH the cache and the conversation history
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=conversation_history,
    cached_content=cached_content # The model will adhere to the style guide in the cache
)

print("Version 2 of the text:", response.text)
```
</details>
```


#### Structured Output (JSON Mode)
Force the model to output a valid JSON object by setting the `response_mime_type`.

<details>
<summary><b>View Python Code for JSON Output</b></summary>
```python
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="List three fantasy authors and their most famous book.",
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)
print(response.text) # Prints a JSON string
```
</details>

### 3.2. Multimodal Understanding (Image, Video, Audio)

Gemini is natively multimodal. You can include media files in your prompts for analysis, transcription, and summarization. The recommended way to do this is via the File API for larger files.

<details>
<summary><b>View Python Code for Video Understanding</b></summary>
```python
from google import genai
client = genai.Client()

# Upload video via File API and wait for processing...
video_file = client.files.get("your-uploaded-video-file-id")

# Prompt the model with the video
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[video_file, "What is the primary activity shown in this video?"]
)
print(response.text)```
</details>

### 3.3. Multimodal Generation

#### Image Generation (`gemini-2.5-flash-image-preview`)

Create and edit images conversationally. The key to high-quality results is providing detailed, descriptive prompts rather than just keywords.

**Prompting Strategies:**
*   **Photorealistic Scenes:** Use photography terms (e.g., "A photorealistic close-up portrait... captured with an 85mm portrait lens, resulting in a soft, blurred background (bokeh).").
*   **Stylized Illustrations:** Be explicit (e.g., "A kawaii-style sticker of a happy red panda... The design features bold, clean outlines, simple cel-shading... The background must be white.").
*   **Accurate Text:** Specify the text and font style (e.g., "Create a modern, minimalist logo... with the text 'The Daily Grind' in a clean, bold, sans-serif font.").

<details>
<summary><b>View Python Code for Image Editing</b></summary>
```python
from google import genai
from PIL import Image

client = genai.Client()
screenshot = Image.open("/path/to/your/screenshot.png")

response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[
        screenshot,
        "Change the aspect ratio of this image to 16:9 and add a title that says 'Gemini API in Action'."
    ]
)
# Process and save the generated image from the response```
</details>

#### Video Generation (Veo)

Generate 8-second, 720p videos with audio from text prompts. This is an asynchronous operation that requires polling the job status.

<details>
<summary><b>View Python Code for Video Generation</b></summary>
```python
import time
from google import genai

client = genai.Client()
prompt = "A cinematic shot of a majestic lion in the savannah."
operation = client.models.generate_videos(model="veo-3.0-generate-preview", prompt=prompt)

# Poll the operation status until the video is ready.
while not operation.done:
    print("Waiting for video generation...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the video.
video = operation.response.generated_videos
client.files.download(file=video.video)
video.video.save("generated_video.mp4")
```
</details>

#### Audio Generation (Text-to-Speech)
Generate high-quality audio from text, ideal for creating audio versions of articles.

<details>
<summary><b>View Python Code for Text-to-Speech</b></summary>```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-pro-preview-tts",
    contents=["Hello, this is an audio version of my latest article."]
)
with open("generated_audio.mp3", "wb") as f:
    f.write(response.candidates.content.parts.inline_data.data)
```
</details>

## 4. Advanced Features for Building Agents

### 4.1. Function Calling

Connect the model to external systems and APIs. You define functions, and the model can ask to call them to get information or perform actions. This is the foundation for building agents that can interact with the world.

<details>
<summary><b>View Python Code for Function Calling</b></summary>
```python
from google import genai
from google.genai import protos

client = genai.Client()

# Define the tool (function) for the model
find_meeting_tool = protos.Tool(
    function_declarations=[
        protos.FunctionDeclaration(
            name='find_meeting_time',
            description="Find an available meeting time.",
            parameters=protos.Schema(type=protos.Type.OBJECT, properties={})
        )
    ]
)

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="Find a meeting time for me and my team.",
    tools=[find_meeting_tool]
)

# The model returns a request to call your function
function_call = response.candidates.content.parts.function_call
print(function_call)
# Your code would now execute this function and return the result to the model.
```
</details>

### 4.2. Grounding with Google Search

For prompts where factual accuracy is critical (e.g., your fact-checking feature), you can ground the model's response in Google Search. The model will consult search results to generate a higher quality response and provide citations.

<details>
<summary><b>View Python Code for Google Search Grounding</b></summary>
```python
from google import genai
from google.genai import protos

client = genai.Client()
search_tool = protos.Tool(google_search_retrieval=protos.GoogleSearchRetrieval())

response = client.models.generate_content(
    model='gemini-2.5-pro',
    contents="Fact check this statement: The Gemini API was released in 2022.",
    tools=[search_tool]
)
print(response.text) # Will provide a corrected answer with sources
```
</details>

### 4.3. The "Thinking" Feature

Gemini 2.5 Pro and Flash have a "thinking" feature (on by default) that allows them to spend more time reasoning through complex prompts. This improves quality but may increase latency and token cost. For `gemini-2.5-flash`, you can disable it for faster responses when maximum quality is not required by setting `thinking_budget=0`.

## 5. Production-Ready Development

### 5.1. Strategic Model Selection

Use different models for different tasks to balance cost, speed, and quality.
*   **Drafting & Simple Tasks:** `Gemini 2.5 Flash-Lite` (cheapest), `Gemini 2.5 Flash` (fast).
*   **Complex Reasoning & High-Quality Editing:** `Gemini 2.5 Pro`.
*   **Fact-Checking:** `Gemini 2.5 Pro` with Google Search grounding.
*   **Image Generation:** `gemini-2.5-flash-image-preview`.
*   **Text-to-Speech:** `gemini-2.5-pro-preview-tts` (highest quality).

### 5.2. Configuring Safety Settings

You have control over the API's safety filters. Adjust the blocking threshold for categories like Harassment and Hate Speech to suit your application's needs, but be mindful of the responsibility this entails.

<details>
<summary><b>View Python Code for Safety Configuration</b></summary>
```python
from google import genai
from google.generative_ai.types import HarmCategory, HarmBlockThreshold

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="A prompt that might be borderline.",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
)
```
</details>


## 6. Building Advanced Workflows & Production Controls

Moving from a prototype to a production-ready application requires handling the full spectrum of model outputs and building multi-step logic for complex tasks. This section covers the advanced techniques for creating a robust and reliable user experience.

### 6.1. Handling Model Outputs for a Robust UI

A successful API call returns more than just text. The full response object is crucial for debugging and managing the user experience. Always inspect the `finish_reason` to understand *why* the model stopped generating.

*   `STOP`: The model finished its thought naturally. (The ideal case).
*   `MAX_TOKENS`: The model ran out of its output token limit. Your UI should detect this and offer the user a "Continue" button.
*   `SAFETY`: The model's response was blocked by a safety filter. Your UI should detect this and show a generic message like, "I am unable to provide a response to that topic."

<details>
<summary><b>View Python Code for Inspecting the Full Response</b></summary>
```python
from google import genai
import google.generative_ai.types as genai_types

client = genai.Client()

try:
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents="A prompt that might trigger a safety filter or be very long."
    )

    # Always check the finish reason from the first candidate
    if response.candidates.finish_reason != 'STOP':
        print(f"Generation stopped for reason: {response.candidates.finish_reason}")
        # You can inspect safety ratings if the reason was SAFETY
        if response.candidates.finish_reason == 'SAFETY':
            print(f"Safety Ratings: {response.candidates.safety_ratings}")
        # Handle the non-ideal case in your UI here
    else:
        print(response.text)

except genai_types.BlockedPromptException as e:
    # This exception is raised if the *prompt* itself is blocked.
    print(f"Your prompt was blocked. {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

```
</details>

### 6.2. Controlling Creativity with `generationConfig`

You can control the "creativity" of the model's output using the `temperature` parameter. This is essential for switching between precise editing and creative brainstorming.

*   **Low Temperature (e.g., `0.1` - `0.3`):** Produces more deterministic and predictable responses. Ideal for grammar correction, fact extraction, and precise edits.
*   **High Temperature (e.g., `0.7` - `1.0`):** Produces more creative and diverse responses. Ideal for brainstorming, writing first drafts, and suggesting alternative phrasing.

<details>
<summary><b>View Python Code for Controlling Temperature</b></summary>
```python
from google import genai
from google.genai import types

client = genai.Client()

# Low temperature for a factual, direct response
config_direct = types.GenerateContentConfig(temperature=0.2)
response_direct = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Suggest a title for a blog post about time management.",
    config=config_direct
)
print(f"Direct Title Suggestion: {response_direct.text}")

# High temperature for a more creative response
config_creative = types.GenerateContentConfig(temperature=0.9)
response_creative = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Suggest a title for a blog post about time management.",
    config=config_creative
)
print(f"Creative Title Suggestion: {response_creative.text}")
```
</details>

### 6.3. Chaining Calls for Complex Workflows

Truly advanced agentic behavior is achieved by chaining multiple API calls together. The output of one call becomes the input for the next, allowing you to build complex logic.

#### The "Decompose, Execute, Synthesize" Pattern

1.  **Decompose:** Use a first API call to break a large problem into smaller, manageable pieces.
2.  **Execute:** In your application code, loop through these pieces and perform a specific action on each one (often another API call).
3.  **Synthesize:** Use a final API call to take all the intermediate results and consolidate them into a single, coherent output for the user.

**Example: Multi-Claim Fact-Checking an Article**

**Step 1: Decompose (Isolate the Claims)**
Give the model the user's article and ask it to extract verifiable claims into a JSON object.

*   **Prompt:**
    > "You are a fact-checking assistant. Read the following article and extract every distinct, verifiable claim. Return these claims as a JSON array of strings in a `claims` field. If there are no claims, return an empty array."
    >
    > `[Full text of the user's article]`

**Step 2: Execute (Verify Each Claim in a Loop)**
In your application, parse the JSON from Step 1. Then, loop through each claim and make a new API call using the Google Search Grounding tool.

*   **Your Code:** `for claim in claims_from_step_1:`
*   **Prompt (inside the loop):**
    > `Fact check this specific statement: "{claim}"`
    > (This call is made with the Google Search Grounding tool enabled.)

**Step 3: Synthesize (Generate a Final Report)**
Collect all the individual verification results from your loop. Then, make a final API call to consolidate them into a human-readable report.


## 7. Prompting Playbooks for Key Tasks

This section provides focused, practical guides and templates for the most nuanced and creative parts of the Gemini API.

### 7.1. A Mini-Guide for Image Generation (`gemini-2.5-flash-image-preview`)

The fundamental principle of image generation is: **Describe the scene, don't just list keywords.** The model's strength is its deep language understanding. A narrative, descriptive paragraph will almost always produce a better, more coherent image than a list of disconnected words.

---

#### **Use Case 1: Creating a New Image from Text**

This is for generating a brand new image, like a blog post header or a conceptual illustration.

**Prompt Template:**
> A **[Style] [Shot Type]** of a **[Subject]**, who is **[Action or Expression]**. The scene is set in **[Environment/Setting]**. The lighting is **[Lighting Description]**, creating a **[Mood/Atmosphere]**. The composition should emphasize **[Key Detail or Focus]**.

**Example:**
> A **photorealistic wide shot** of an **elderly watchmaker**, who is **hunched over a workbench, meticulously assembling a complex timepiece**. The scene is set in a **cluttered, dusty workshop filled with gears and tools**. The lighting is **a single, warm beam from a desk lamp**, creating a **mood of intense focus and nostalgia**. The composition should emphasize the **delicate details on the watch face**.

---

#### **Use Case 2: Editing an Existing Image (e.g., a Screenshot)**

This is for modifying an image you provide. The model will attempt to match the original's style, lighting, and perspective.

**Prompt Template:**
> Using the provided image of **[Original Subject]**:
>
> 1.  **[Add/Remove/Change]** the **[Element]**.
> 2.  The new element should be **[Description of how it should look or integrate]**.
> 3.  Keep the rest of the image exactly the same.

**Example (for a screenshot of a user interface):**
> Using the provided image of **a mobile app screen**:
>
> 1.  **Change** the text in the main button from "Sign Up" to "Get Started".
> 2.  The new text should use the same font and color as the original.
> 3.  Keep the rest of the image exactly the same.

---

#### **Use Case 3: Composing from Multiple Images**

This is for advanced creation where you combine elements from two or more source images.

**Prompt Template:**
> Create a new image by combining the provided images.
>
> *   From the **first image**, take the **[Element A, e.g., the woman in the red dress]**.
> *   From the **second image**, take the **[Element B, e.g., the Parisian street background]**.
> *   Generate a new, realistic scene where **[Describe how Element A and Element B should interact]**. Adjust lighting and shadows to make the composition look natural.

---

### 7.2. Best Practices for Function Calling and Tool Use

For the agentic parts of your application, the reliability of function calling depends almost entirely on the quality of your tool and function `description` fields. The model uses these descriptions to decide *if* and *how* to use your tools.

**A good description should be:**

*   **Specific and Action-Oriented:** Start with a clear verb. Explain exactly what the function *does*.
*   **Comprehensive:** Mention the key parameters and what they are for.
*   **Contextual:** Briefly explain *when* the tool should be used.

**Example:**

*   **Bad Description:**
    > `description: "gets meeting info"`

*   **Good Description:**
    > `description: "Retrieves the time, attendees, and agenda for a meeting based on a meeting ID. Use this when the user asks for details about a specific upcoming meeting."`


## 8. Reference: Models & Rate Limits

| Model | Max Tokens | Free Tier RPM | Paid Tier 1 RPM |
| :--- | :--- | :--- | :--- |
| **Gemini 2.5 Pro** | 1,048,576 | 5 | 150 |
| **Gemini 2.5 Flash** | 1,048,576 | 10 | 1,000 |
| **Gemini 2.5 Flash-Lite** | 1,048,576 | 15 | 4,000 |
| **Image Preview** | N/A | *Not Published* | 500 |
| **Veo 3** | N/A | *Not Published* | 2 |

