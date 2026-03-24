"""
Find the correct Azure OpenAI deployment name
"""

from core.config_manager import ConfigManager
import openai

# Load config
config_manager = ConfigManager()
config = config_manager.load_config()

api_key = config.get('OPENAI_API_KEY')
azure_endpoint = config.get('AZURE_OPENAI_ENDPOINT')
api_version = config.get('AZURE_OPENAI_API_VERSION', '2024-02-15-preview')

# Common deployment names to try
deployment_names = [
    'gpt-4',
    'gpt-4-turbo',
    'gpt-4o',
    'gpt-4o-mini',
    'gpt-35-turbo',
    'gpt-35-turbo-16k',
    'gpt4',
    'gpt4o',
    'gpt4o-mini',
    'gpt-4-32k',
]

print("="*80)
print("SEARCHING FOR VALID DEPLOYMENT NAME")
print("="*80)
print(f"Azure Endpoint: {azure_endpoint}")
print(f"API Version: {api_version}")
print("="*80)

client = openai.AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=azure_endpoint
)

print("\nTrying common deployment names...\n")

for deployment in deployment_names:
    try:
        print(f"Testing: {deployment}...", end=" ")
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "user", "content": "Hi"}
            ],
            max_tokens=5
        )
        print(f"✅ FOUND!")
        print(f"\n{'='*80}")
        print(f"SUCCESS! Your deployment name is: {deployment}")
        print(f"{'='*80}")
        print(f"\nUpdate config.env line 26 to:")
        print(f"OPENAI_MODEL={deployment}")
        print(f"{'='*80}")
        break
    except Exception as e:
        error_msg = str(e)
        if "DeploymentNotFound" in error_msg:
            print("❌ Not found")
        elif "quota" in error_msg.lower():
            print("⚠️  Found but quota exceeded")
            print(f"\n{'='*80}")
            print(f"FOUND! Your deployment name is: {deployment}")
            print(f"(Quota exceeded, but deployment exists)")
            print(f"{'='*80}")
            break
        else:
            print(f"❌ Error: {error_msg[:50]}")

print("\n" + "="*80)
print("If no deployment was found, please check Azure Portal:")
print("Azure Portal → payroll-open-ai → Model deployments")
print("="*80)

