# Audio Quality Comparison

This repository contains a Python script to analyze and compare the audio quality of two video files.

## Features

- Extracts audio from video files.
- Analyzes audio for:
  - Subtype (encoding, bit depth)
  - Sample Rate
  - Loudness (LUFS)
  - Noise Level
  - Duration (s)
- Generates a comparison report in `results/results.txt`.
- Creates a visual comparison chart in `results/audio_quality_comparison.png`.

## Prerequisites

- Python 3.x
- The Python packages listed in `requirements.txt`.

## How to Use

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the project directory:**
   ```bash
   cd audio-quality
   ```

3. **Run the script with your video files as arguments:**
   ```bash
   python main.py path/to/your/video1.mp4 path/to/your/video2.mp4
   ```
   For example:
   ```bash
   python main.py data/video_with_mic.MP4 data/video_without_mic.MP4
   ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Check the results:**
   - The analysis report will be saved in `results/results.txt`.
   - The comparison chart will be saved in `results/audio_quality_comparison.png`.
