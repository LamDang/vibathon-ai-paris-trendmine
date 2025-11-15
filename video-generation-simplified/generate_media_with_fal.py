import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import fal_client
import requests

# Load environment variables
load_dotenv()

# Configure APIs
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
FAL_API_KEY = os.getenv('FAL_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
os.environ["FAL_KEY"] = FAL_API_KEY

# ============================================================================
# SECTION PROMPTS - MODIFIEZ ICI POUR CHANGER LE STYLE DES IMAGES/VIDEOS
# ============================================================================

VISUAL_DESIGNER_PROMPT = """You are an expert visual designer specialized in creating realistic, high-end product images for technology and gaming hardware.
Your role is to transform each user input into a clear, visually grounded, photorealistic image concept.

Style guidelines:
- Prioritize realism over abstraction.
- Focus on believable lighting, materials, textures, and environments.
- Highlight the hardware or the experience in a way a real photographer would: controlled lighting, shallow depth of field, detailed close-ups, natural shadows.
- Use modern, minimal, premium aesthetics similar to Apple, Nvidia, Samsung, or Sony product photography.
- Avoid surreal effects, metaphors, fantasy elements, or exaggerated sci-fi visuals.
- No text inside the image.

Transformations:
- Convert technical statements into real-world visual scenes.
- Emphasize physical hardware, user experience, or environment when appropriate.
- Produce concise, well-structured prompts that image generators can render accurately.

Examples:

Input: "The new architecture ensures smoother gameplay with higher frame rates."
Output: "A photorealistic gaming setup with a high-end monitor displaying ultra-fluid gameplay at high frame rates, crisp motion, minimal blur. Modern GPU tower with LED accents softly illuminating a clean desk. Natural lighting, realistic reflections."

Input: "DLSS 3.0 technology brings AI-powered upscaling for crisp, clear images."
Output: "Close-up shot of a gaming monitor showing a sharp, high-resolution image, side-by-side with improved clarity. Modern GPU visible in the setup. Realistic color accuracy, no exaggeration."

Input: "NVIDIA's New GPU: Gaming Revolution Unleashed"
Output: "Premium product photography of a next-generation NVIDIA GPU graphics card on a minimalist dark surface, dramatic studio lighting with soft shadows, sharp focus on the GPU cooler and LED elements, professional tech photography style, ultra-realistic materials and textures."

Now transform the following text into a photorealistic image/video prompt:"""

# ============================================================================


def transform_text_to_prompt(text, context=""):
    """
    Use Gemini to transform script text into photorealistic prompts.

    Args:
        text: The text to transform
        context: Optional context about the video topic

    Returns:
        A photorealistic prompt string
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')

        full_prompt = VISUAL_DESIGNER_PROMPT + f"\n\n"
        if context:
            full_prompt += f"Context: {context}\n"
        full_prompt += f"Text: {text}\n\nPhotorealistic prompt:"

        response = model.generate_content(full_prompt)

        if response.text:
            return response.text.strip()
        else:
            return f"Photorealistic product photography: {text}"

    except Exception as e:
        print(f"  Warning: Could not transform with Gemini: {e}")
        return f"High-end product photography style: {text}"


def generate_image_with_fal(prompt, filename, width=1080, height=1920):
    """
    Generate an image using FAL AI.

    Args:
        prompt: The image generation prompt
        filename: Output filename for the image
        width: Image width
        height: Image height

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"  Generating image...")
        print(f"  Prompt: {prompt[:100]}...")

        # Use FAL's Flux model for high-quality images
        result = fal_client.subscribe(
            "fal-ai/flux/dev",
            arguments={
                "prompt": prompt,
                "image_size": {
                    "width": width,
                    "height": height
                },
                "num_inference_steps": 28,
                "guidance_scale": 3.5,
                "num_images": 1,
                "enable_safety_checker": True
            }
        )

        # Download the generated image
        if result and 'images' in result and len(result['images']) > 0:
            image_url = result['images'][0]['url']
            response = requests.get(image_url)

            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"  [OK] Image saved: {filename}")
                return True
            else:
                print(f"  [ERROR] Failed to download image")
                return False
        else:
            print(f"  [ERROR] No image generated")
            return False

    except Exception as e:
        print(f"  [ERROR] Error generating image: {e}")
        return False


def generate_video_with_fal(prompt, filename, duration=5):
    """
    Generate a video using FAL AI.

    Args:
        prompt: The video generation prompt
        filename: Output filename for the video
        duration: Video duration in seconds

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"  Generating video (this may take 1-2 minutes)...")
        print(f"  Prompt: {prompt[:100]}...")

        # Use FAL's video generation model
        result = fal_client.subscribe(
            "fal-ai/ltx-video",
            arguments={
                "prompt": prompt,
                "num_frames": duration * 25,  # 25 FPS
                "num_inference_steps": 30,
                "guidance_scale": 3.0,
                "enable_safety_checker": True
            }
        )

        # Download the generated video
        if result and 'video' in result:
            video_url = result['video']['url']
            response = requests.get(video_url)

            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"  [OK] Video saved: {filename}")
                return True
            else:
                print(f"  [ERROR] Failed to download video")
                return False
        else:
            print(f"  [ERROR] No video generated")
            return False

    except Exception as e:
        print(f"  [ERROR] Error generating video: {e}")
        return False


def generate_media_from_script(json_file_path, output_folder='media_output'):
    """
    Generate images and videos for each component of the video script.

    Args:
        json_file_path: Path to the JSON file containing the script
        output_folder: Folder where media will be saved
    """
    # Create output folder
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Process each script
    for script in data.get('scripts', []):
        script_num = script.get('script_number', 1)
        topic = data.get('topic', 'video').replace(' ', '_')

        # Create subfolder for this script
        script_folder = Path(output_folder) / f"{topic}_script_{script_num}"
        script_folder.mkdir(parents=True, exist_ok=True)

        print("\n" + "="*70)
        print(f"Processing Script {script_num}: {script['title']}")
        print("="*70)

        context = f"Topic: {data.get('topic', '')}. Video Title: {script['title']}"

        # Counter for elements
        element_count = 0

        # 1. TITLE - Image + Video
        element_count += 1
        print(f"\n[{element_count}] Processing TITLE...")
        title_prompt = transform_text_to_prompt(script['title'], context)

        # Save prompt
        with open(script_folder / f"{element_count:02d}_title_prompt.txt", 'w', encoding='utf-8') as f:
            f.write(f"Original: {script['title']}\n\n")
            f.write(f"Transformed Prompt:\n{title_prompt}\n")

        # Generate image
        generate_image_with_fal(
            title_prompt,
            str(script_folder / f"{element_count:02d}_title.png"),
            width=1080,
            height=1920
        )

        # Generate video
        generate_video_with_fal(
            title_prompt,
            str(script_folder / f"{element_count:02d}_title.mp4"),
            duration=3
        )

        # 2. KEY POINTS - Image + Video for each
        for i, key_point in enumerate(script['key_points'], 1):
            element_count += 1
            print(f"\n[{element_count}] Processing KEY POINT {i}/{len(script['key_points'])}...")

            keypoint_prompt = transform_text_to_prompt(key_point, context)

            # Save prompt
            with open(script_folder / f"{element_count:02d}_keypoint_{i:02d}_prompt.txt", 'w', encoding='utf-8') as f:
                f.write(f"Original: {key_point}\n\n")
                f.write(f"Transformed Prompt:\n{keypoint_prompt}\n")

            # Generate image
            generate_image_with_fal(
                keypoint_prompt,
                str(script_folder / f"{element_count:02d}_keypoint_{i:02d}.png"),
                width=1080,
                height=1920
            )

            # Generate video
            generate_video_with_fal(
                keypoint_prompt,
                str(script_folder / f"{element_count:02d}_keypoint_{i:02d}.mp4"),
                duration=3
            )

        # 3. CTA - Image + Video
        element_count += 1
        print(f"\n[{element_count}] Processing CTA...")
        cta_prompt = transform_text_to_prompt(script['cta'], context)

        # Save prompt
        with open(script_folder / f"{element_count:02d}_cta_prompt.txt", 'w', encoding='utf-8') as f:
            f.write(f"Original: {script['cta']}\n\n")
            f.write(f"Transformed Prompt:\n{cta_prompt}\n")

        # Generate image
        generate_image_with_fal(
            cta_prompt,
            str(script_folder / f"{element_count:02d}_cta.png"),
            width=1080,
            height=1920
        )

        # Generate video
        generate_video_with_fal(
            cta_prompt,
            str(script_folder / f"{element_count:02d}_cta.mp4"),
            duration=3
        )

        # Create summary info file
        info_file = script_folder / "00_info.txt"
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(f"Script: {script['title']}\n")
            f.write(f"Total elements generated: {element_count}\n\n")
            f.write(f"1. Title\n")
            for i in range(len(script['key_points'])):
                f.write(f"{i+2}. Key Point {i+1}\n")
            f.write(f"{element_count}. CTA\n\n")
            f.write(f"Hashtags: {' '.join(script['hashtags'])}\n")
            f.write(f"Target Audience: {script['target_audience']}\n")

        print("\n" + "="*70)
        print(f"[SUCCESS] Generated {element_count * 2} files ({element_count} images + {element_count} videos)")
        print(f"[SUCCESS] Location: {script_folder}")
        print("="*70)


def main():
    print("="*70)
    print("FAL AI Media Generator - Images & Videos")
    print("="*70)

    # Find the most recent script file
    script_files = list(Path('user_request').glob('scripts_*.json'))

    if not script_files:
        print("\n[ERROR] No script files found in user_request folder!")
        return

    # Use the most recent file
    latest_script = max(script_files, key=lambda p: p.stat().st_mtime)
    print(f"\nProcessing: {latest_script}")

    generate_media_from_script(str(latest_script))

    print("\n" + "="*70)
    print("[SUCCESS] All media generated successfully!")
    print("Check the 'media_output' folder for your files.")
    print("="*70)


if __name__ == "__main__":
    main()
