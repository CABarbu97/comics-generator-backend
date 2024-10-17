import replicate
import openai
from config import Config
from PIL import Image
import requests
from io import BytesIO

class ComicService:
    def __init__(self):
        # Initialize API keys from Config
        self.replicate_client = replicate.Client(api_token=Config.REPLICATE_API_TOKEN)
        openai.api_key = Config.OPENAI_API_KEY

    def create_comic(self, environment, characters):
        # Generate the panel descriptions using GPT
        panel_actions = self.generate_panel_descriptions(environment, characters)
        
        # Create the comic prompt
        prompt = (f"Comic with 4 panels: 2 panels on top, 2 panels below. Set in {environment} "
                  f"with {characters}. Keep the style simple, cartoonish, and consistent. "
                  f"Actions: {panel_actions}. Use clear panel separation lines.")

        # Call the function to generate the comic image via Replicate
        return self.generate_comic_flux_pro(prompt)

    def generate_panel_descriptions(self, environment, characters):
        gpt_prompt = (f"Describe actions and simple dialogue for 4 simple comic panels set in {environment} with {characters}. "
                  f"Each panel should show funny or lighthearted interactions and include dialogue.")


        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative assistant helping to generate short comic panel descriptions."},
                {"role": "user", "content": gpt_prompt}
            ]
        )

        panel_actions = gpt_response['choices'][0]['message']['content']
        return panel_actions

    def generate_comic_flux_pro(self, prompt):
        try:
            # Call the Flux Pro model hosted on Replicate
            output = self.replicate_client.run(
                "black-forest-labs/flux-pro",  # Replace with actual model name on Replicate
                input={
                    "steps": 25,
                    "prompt": prompt,
                    "guidance": 4,
                    "interval": 2,
                    "aspect_ratio": "1:1",
                    "output_format": "webp",
                    "output_quality": 30,
                    "safety_tolerance": 4
                }
            )
            return output  # Return the generated image URL
        except replicate.exceptions.ReplicateException as e:
            print(f"Replicate error: {str(e)}")
            return None

    def download_image(self, url):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            return img
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None
