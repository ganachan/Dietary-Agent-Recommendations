# Dietary-Agent-Recommendations

This repository contains a Python application that integrates Azure OpenAI, Azure Cosmos DB, and image analysis to provide personalized dietary recommendations based on patient data and food images.

## Features

### Patient Data Management:
- Retrieve patient data (e.g., sugar levels, food sensitivity) from Azure Cosmos DB.
- Dynamic recommendations based on patient-specific health metrics.

### Image Analysis:
- Analyze food items in images using Azure OpenAI's GPT-4V model.
- Generate insights on portion sizes, calorie estimates, and potential impact on blood sugar levels.

### Personalized Recommendations:
- Combine patient health data and food analysis to create tailored dietary suggestions.
- Identify specific recommendations for managing high blood sugar levels based on inputs.

## Prerequisites

Before running the application, ensure you have:
1. **Azure OpenAI Service** with GPT-4V deployment.
2. **Azure Cosmos DB** for storing patient data.
3. **Azure Blob Storage** or a local directory for image storage.
4. **Python 3.8+** installed with required libraries.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/dietary-assistant.git
   cd dietary-assistant
