# 🌿 FarmAssist – Your Go-To Buddy for Farm Matters in Nigeria

**FarmAssist** is a friendly, conversational AI chatbot built to support **smallholder farmers in Nigeria**. Whether you're planting, planning, or pricing, FarmAssist gives you **reliable**, **practical**, and **region-aware** farming tips – all powered by **Google's Gemini** model and presented in a WhatsApp-style chat interface.

## 🚜 What Can FarmAssist Do?

- 🌱 **Farming Tips** – From soil prep to harvest
- 🌾 **Seasonal Crop Recommendations**
- 🐛 **Pest & Disease Management**
- 💧 **Irrigation Guidance**
- 📈 **Market Insight & Demand Trends**
- 🧠 **Remembers Chat History for Context**
- ❌ **Rejects Non-Agricultural or Unethical Requests**
- 🇳🇬 **Only Supports Farmers in Nigeria**

## 🛠️ Tech Stack

| Tool                | Purpose                               |
|---------------------|----------------------------------------|
| [Streamlit](https://streamlit.io)        | Frontend + main logic engine        |
| [Google Gemini API](https://ai.google.dev/) | Conversational AI (LLM)              |
| `dotenv`            | Manage secret API key                 |
| Custom CSS          | Styled similar to WhatsApp chat             |

## 📁 Project Structure

```

FarmAssist/
│
├── app.py               
├── prompts.py           
├── gemini_client.py     
├── config.py           
├── .env                
├── requirements.txt     
└── README.md            

````


## 💻 Local Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/Sholz22/FarmAssist..git
cd FarmAssist
````

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # On macOS/Linux
venv\Scripts\activate        # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Your Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_real_gemini_api_key_here
```

### 5. Run the App

```bash
streamlit run app.py
```


## 🌐 Deployment Options

You can deploy this Streamlit app easily using:

* ✅ [**Streamlit Cloud**](https://streamlit.io/cloud)


## ✨ Future Enhancements

* 🎙 Voice input/output
* 🌍 Local language support (Yoruba, Hausa, Igbo)
* 🌤 Weather + market data APIs
* 📸 Crop image uploads for diagnosis
* 🧑‍🌾 Personal dashboard for farmers


## 🙋 About the Developer

Made with ❤️ for Nigerian farmers by [**Sholz22**](https://github.com/Sholz22)

> *"Farming shouldn't feel like guesswork — let's make it smarter, simpler, and more Naija."* 🇳🇬


## 📄 License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).

