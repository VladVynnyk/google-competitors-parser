from typing import Optional
from google.cloud import aiplatform
import vertexai
from vertexai.preview.generative_models import GenerativeModel
# from vertexai.language_models import TextGenerationModel

from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request

key_path = "pristine-sphere-422105-n5-b4afd3bed68a.json"
# credentials = Credentials(token=, expiry=None, scopes=['https://www.googleapis.com/auth/cloud-platform'])
credentials = Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])
if credentials.expired:
    credentials.refresh(Request())

PROJECT_ID = "pristine-sphere-422105-n5"
REGION = "europe-west3"

vertexai.init(project=PROJECT_ID, location=REGION, credentials=credentials)


# def init_sample(
#     project: Optional[str] = "pristine-sphere-422105-n5",
#     location: Optional[str] = "europe-west3",
#     experiment: Optional[str] = None,
#     staging_bucket: Optional[str] = None,
#     credentials: Optional[google.auth.credentials.Credentials] = credentials,
#     encryption_spec_key_name: Optional[str] = None,
#     service_account: Optional[str] = "gemini-ai-test@pristine-sphere-422105-n5.iam.gserviceaccount.com",
# )


# Load Gemini Pro
gemini_pro_model = GenerativeModel("gemini-1.0-pro")

model_response = gemini_pro_model.generate_content("Based on name of product 'NOW FOODS VIT D-3 5000IU 120 SGELS' give me '5' the most relevant products from this list.- [NOW Foods високоефективний вітамін D3, 5000 МО, 120 капсул, Now Foods Vitamin D-3 5000 IU 120 softgels біодобавка, NOW Foods високоефективний вітамін D3, 125 мкг (5000 МО), 240 капсул, NOW Foods Вітамін D3, структурна підтримка, 10 мкг (400 МО), 180, NOW Foods Вітамін D3, структурна підтримка, 10 мкг (400 МО), 180, Вітамін D3 50 мкг (2000 МО), NOW Foods, 30 капсул, NOW Foods високоефективний вітамін D3, 50 мкг (2000 МО), 30 капсул, Вітамін D-3 Now Foods 400 МО 180 гелевих капсул]. Don't give any additional information. Structure of content of output must be the next: {list_of_products: [product1, product2, productN, ...]}.")
print("model_response\n",model_response)
