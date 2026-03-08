"""
AI Journal Maker - AI Analysis Module
Handles image analysis using LLM providers (OpenRouter, OpenAI, Anthropic, Google)
"""

import os
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional

# Note: In Vercel, environment variables are set automatically
# No need for load_dotenv()


class JournalAIAnalyzer:
    """AI analyzer for journal images"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get('llm_provider', 'openrouter')
        self.model = config.get('model', 'openai/gpt-4o')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2048)
        self.base_url = config.get('base_url', 'https://openrouter.ai/api/v1')

        # Get API key
        api_key_env = config.get('api_key_env', 'OPENROUTER_API_KEY')
        self.api_key = os.getenv(api_key_env)

        if not self.api_key:
            raise ValueError(f"API key not found. Please set {api_key_env} environment variable.")
    
    def analyze_images(self, images: List[Dict[str, str]], title: str, 
                       date: str, time: str, notes: str = "") -> Dict[str, Any]:
        """
        Analyze images and generate a journal report
        
        Args:
            images: List of image data with 'base64' and 'type' keys
            title: Journal entry title
            date: Date of the entry
            time: Time of the entry
            notes: Additional notes from user
            
        Returns:
            Dictionary containing the analysis report
        """
        # Build the prompt
        prompt = self._build_prompt(title, date, time, notes)
        
        # Build message content with images
        content = [
            {"type": "text", "text": prompt}
        ]
        
        for img in images:
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{img['type']};base64,{img['base64']}"
                }
            })
        
        # Call the appropriate API based on provider
        if self.provider == 'openrouter' or self.provider == 'openai':
            response = self._call_openai_api(content)
        elif self.provider == 'anthropic':
            response = self._call_anthropic_api(prompt, images)
        elif self.provider == 'google':
            response = self._call_google_api(prompt, images)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
        
        return {
            'title': title,
            'date': date,
            'time': time,
            'notes': notes,
            'report': response,
            'analysis': True,
            'image_count': len(images)
        }
    
    def _build_prompt(self, title: str, date: str, time: str, notes: str) -> str:
        """Build the analysis prompt"""
        return f"""You are an expert journal analyst. Analyze the provided image(s) and create a detailed, reflective journal entry.

**Journal Entry Context:**
- **Title:** {title}
- **Date:** {date}
- **Time:** {time}
- **Additional Notes:** {notes if notes else "None provided"}

**Your Task:**
1. **Describe what you see** in the image(s) in detail
2. **Identify key elements**, people, objects, settings, or activities
3. **Infer the context** - what might be happening, what occasion this might be
4. **Reflect on the significance** - why this moment might be meaningful
5. **Suggest insights or observations** that could enhance the journal entry

**Format your response as:**
- A warm, personal narrative (2-4 paragraphs)
- Key observations as bullet points
- A reflective conclusion

Write in a thoughtful, engaging tone suitable for a personal journal. Be specific about visual details while also capturing the emotional or contextual significance of the moment."""
    
    def _call_openai_api(self, content: List[Dict[str, Any]]) -> str:
        """Call OpenAI/OpenRouter API for image analysis"""
        import httpx

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                # Print full error for debugging
                if response.status_code != 200:
                    print(f"[ERROR] Status: {response.status_code}")
                    print(f"[ERROR] Response: {response.text}")
                response.raise_for_status()
                result = response.json()
                return result['choices'][0]['message']['content']
        except httpx.HTTPError as e:
            error_msg = f"Error analyzing images: {str(e)}"
            print(f"[ERROR] {error_msg}")
            return error_msg
    
    def _call_anthropic_api(self, prompt: str, images: List[Dict[str, str]]) -> str:
        """Call Anthropic API for image analysis"""
        import httpx
        
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        # Build image blocks for Anthropic
        image_blocks = []
        for img in images:
            image_blocks.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": img['type'],
                    "data": img['base64']
                }
            })
        
        payload = {
            "model": self.model.replace('anthropic/', ''),
            "max_tokens": self.max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *image_blocks
                    ]
                }
            ]
        }
        
        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                return result['content'][0]['text']
        except httpx.HTTPError as e:
            return f"Error analyzing images: {str(e)}"
    
    def _call_google_api(self, prompt: str, images: List[Dict[str, str]]) -> str:
        """Call Google Generative AI API for image analysis"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model_name = self.model.replace('google/', '')
            model = genai.GenerativeModel(model_name)

            # Prepare images
            image_parts = []
            for img in images:
                image_parts.append({
                    "mime_type": img['type'],
                    "data": base64.b64decode(img['base64'])
                })

            response = model.generate_content([prompt] + image_parts)
            
            if response.text:
                return response.text
            else:
                return "No response generated from Gemini. Please try again."

        except Exception as e:
            error_msg = f"Error analyzing images: {str(e)}"
            print(f"[ERROR] {error_msg}")
            return error_msg
