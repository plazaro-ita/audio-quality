import os
try:
    from moviepy.editor import VideoFileClip
except ModuleNotFoundError:
    from moviepy import VideoFileClip
import soundfile as sf
import numpy as np
import pyloudnorm as pyln
import matplotlib.pyplot as plt

def get_audio_duration(audio_path):
    """
    Gets the duration of an audio file.
    """
    with sf.SoundFile(audio_path) as f:
        return f.frames / f.samplerate

def analyze_audio(audio_path):
    """
    Analyzes the audio file to determine its quality.
    """
    # Load the audio file
    data, samplerate = sf.read(audio_path)

    # 1. Subtype
    subtype_info = sf.info(audio_path).subtype_info

    # 2. Sample rate
    sample_rate = samplerate

    # 3. Loudness (LUFS)
    meter = pyln.Meter(samplerate) # create loudness meter
    loudness = meter.integrated_loudness(data) # measure loudness

    # 4. Noise Level (simple RMS of silent parts)
    # A simple approach: assume parts with amplitude below a threshold are silence
    silence_threshold = 0.01
    silent_parts = data[np.abs(data) < silence_threshold]
    noise_level = np.sqrt(np.mean(silent_parts**2)) if len(silent_parts) > 0 else 0
    
    # 5. Duration
    duration = get_audio_duration(audio_path)

    return {
        "subtype": subtype_info,
        "sample_rate": sample_rate,
        "loudness (LUFS)": loudness,
        "noise_level": noise_level,
        "duration (s)": duration,
    }

def extract_audio(video_path, audio_path):
    """
    Extracts audio from a video file.
    """
    if not os.path.exists(audio_path):
        print(f"Extracting audio from {video_path}...")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        print(f"Audio extracted to {audio_path}")
    else:
        print(f"Audio file {audio_path} already exists.")

def plot_comparison(quality1, quality2, video1_path, video2_path, results_dir):
    """
    Plots a bar chart comparing the audio quality of two videos.
    """
    labels = ['Loudness (LUFS)', 'Noise Level']
    video1_metrics = [quality1['loudness (LUFS)'], quality1['noise_level']]
    video2_metrics = [quality2['loudness (LUFS)'], quality2['noise_level']]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, video1_metrics, width, label=video1_path)
    rects2 = ax.bar(x + width/2, video2_metrics, width, label=video2_path)

    ax.set_ylabel('Scores')
    ax.set_title('Audio Quality Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()
    chart_path = os.path.join(results_dir, 'audio_quality_comparison.png')
    plt.savefig(chart_path)
    print(f"\nComparison chart saved as {chart_path}")


import argparse

def main():
    """
    Main function to compare audio quality of two videos.
    """
    parser = argparse.ArgumentParser(description='Compare the audio quality of two videos.')
    parser.add_argument('video1', help='Path to the first video file')
    parser.add_argument('video2', help='Path to the second video file')
    args = parser.parse_args()

    video1_path = args.video1
    video2_path = args.video2

    audio1_path = os.path.splitext(video1_path)[0] + ".wav"
    audio2_path = os.path.splitext(video2_path)[0] + ".wav"
    
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Extract audio from videos
    extract_audio(video1_path, audio1_path)
    extract_audio(video2_path, audio2_path)

    # Analyze audio files
    print("\nAnalyzing audio quality...")
    quality1 = analyze_audio(audio1_path)
    quality2 = analyze_audio(audio2_path)

    # Compare and report
    report = "\n--- Audio Quality Comparison ---\n"
    report += f"\nResults for {video1_path}:\n"
    for key, value in quality1.items():
        report += f"  {key}: {value}\n"

    report += f"\nResults for {video2_path}:\n"
    for key, value in quality2.items():
        report += f"  {key}: {value}\n"
    report += "\n--- End of Report ---\n"
    
    print(report)

    results_path = os.path.join(results_dir, 'results.txt')
    with open(results_path, 'w') as f:
        f.write(report)
    print(f"Report saved as {results_path}")

    # Plot comparison
    plot_comparison(quality1, quality2, video1_path, video2_path, results_dir)


if __name__ == "__main__":
    main()
