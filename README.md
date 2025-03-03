# Playlist Generator

## Overview
This project is a playlist generator that takes a natural language prompt from the user and creates a playlist using Spotify's Web API. Instead of relying on an external API for the language model (LLM), the project will use a locally installed LLM or a self-hosted cloud-based model to interpret user prompts and generate song selections. The goal is to provide an AI-powered playlist creation experience without incurring API costs for the LLM.

## Features
- Accepts natural language prompts (e.g., "Create a relaxing jazz playlist for reading").
- Uses a locally installed or cloud-hosted LLM to interpret the user's request.
- Retrieves song recommendations based on the interpreted mood, genre, and theme.
- Integrates with Spotify's Web API to create and populate playlists.
- Provides an interactive interface for users to refine their playlists.

## Technology Stack
- **Local LLM Model:** Options may include LLaMA, GPT4All, or other open-source LLMs.
- **Spotify API:** Used for playlist creation and song retrieval.
- **Backend:** Python with Flask or FastAPI for handling API requests.
- **Frontend (Optional):** React or a CLI-based interface for user input.

## TODO List
### 1. Research & Setup
- [ ] **LLM Exploration:**
  - Compare various open-source LLMs for local or self-hosted use.
  - Evaluate hardware/software requirements and plan GPU or CPU utilization.
- [ ] **Spotify API Familiarization:**
  - Read through Spotify Web API documentation and set up a developer account.
  - Understand OAuth2 flow for obtaining access tokens.
- [ ] **Environment Setup:**
  - Choose a backend framework (Flask or FastAPI) and create a basic project structure.
  - Install necessary dependencies for the LLM and Spotify integration.

### 2. Implement LLM Processing
- [ ] **Prompt Parsing:**
  - Write a function to clean and parse user input, extracting genres, moods, or themes.
- [ ] **LLM Integration Module:**
  - Create a standalone module or class to interact with the local LLM.
  - Implement logic to handle generation of relevant keywords or queries from user prompts.
- [ ] **Performance Considerations:**
  - Optimize LLM usage to avoid excessive memory or compute overhead.
  - Cache or store partial results to prevent repeated processing.
- [ ] **Prompt Engineering:**
  - Experiment with different prompt styles to yield more accurate or creative results.

### 3. Integrate with Spotify API
- [ ] **Authentication & Authorization:**
  - Implement OAuth 2.0 flow to acquire and refresh access tokens.
  - Store tokens securely.
- [ ] **Search & Filter:**
  - Based on keywords from LLM output, use the Spotify search endpoint to find tracks.
  - Implement logic to filter by genre, mood, popularity, etc.
- [ ] **Playlist Creation:**
  - Create a new playlist in the user’s account.
  - Add recommended tracks to the newly created playlist.
- [ ] **Error Handling:**
  - Handle exceptions for network issues, invalid tokens, or track not found.
  - Ensure the system gracefully recovers or prompts for re-authentication.

### 4. Build User Interface
- [ ] **CLI Option:**
  - Implement a command-line interface for quick testing and usage.
  - Provide clear instructions on how to input prompts and see playlist results.
- [ ] **Web Interface (Optional):**
  - Set up a React (or other) frontend to collect user input and display playlists.
  - Integrate with the backend API to show feedback when tracks are added to playlists.

### 5. Testing & Deployment
- [ ] **Local Testing:**
  - Test various prompt types to ensure the LLM processes them accurately.
  - Verify Spotify API calls work correctly under different scenarios.
- [ ] **Continuous Integration:**
  - Set up basic CI pipelines (e.g., GitHub Actions) to run tests on each commit.
- [ ] **Performance Optimization:**
  - Profile LLM calls to ensure acceptable response times.
  - Minimize redundant Spotify API calls to avoid rate limit issues.
- [ ] **Deployment Strategy:**
  - Decide on hosting environment (local server, self-hosted cloud VM, Docker, etc.).
  - Document the process for setting up the environment in production.

### 6. Documentation & Future Enhancements
- [ ] **Installation Instructions:**
  - Provide detailed steps for setting up Python environment, installing dependencies, and configuring the LLM.
  - Explain how to set up Spotify API credentials.
- [ ] **Usage Guide:**
  - Include step-by-step examples with sample prompts.
  - Describe optional flags or parameters (if any) for more advanced configurations.
- [ ] **Advanced Personalization:**
  - Potentially incorporate user listening history or personal music library data.
  - Explore ways to leverage Spotify’s recommendation endpoints further.
- [ ] **Additional LLM Features:**
  - Experiment with generating track descriptions, reasons for inclusion, or dynamic transitions.

## How to Run (To be updated)
Instructions on setting up the environment, installing dependencies, and running the project will be added after implementation.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
MIT License

