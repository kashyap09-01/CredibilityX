# CredibilityX: Fake News Detection Website

CredibilityX is a website developed to check the credibility of given news articles. Users can input news either as text paragraphs or through news links. The website uses an attention-based LSTM model to perform the classification of the texts, determining whether the news is credible or fake.

## Features

- Input news as text paragraphs or news links
- Uses attention-based LSTM model for classification
- Achieved an accuracy of 88.04% on the test dataset
- Web scraping from Politifact for data collection


## Technologies Used

- Frontend: HTML, CSS, JavaScript
- Backend: Flask
- Model: Attention-based LSTM
- Data Collection: Web scraping using BeautifulSoup and requests

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kashyap09-01/CredibilityX.git
   cd CredibilityX
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the website**:
   ```bash
   python main.py
   ```

5. **Open the website**:
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage
- Enter the news text or link in the provided input field.
- Click on the "Check Credibility" button.
- The website will display whether the news is credible or fake based on the model's prediction.

## Model Training
The LSTM model used for classification was trained using data scraped from the Politifact website over the past 10 years. The training process and model architecture are detailed in the `fakedetect.ipynb` notebook.

## Data
- The dataset used for training and testing the model is stored in `file.csv`.
- Web scraping was conducted using the script in `web_Scrape.py`.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements
- [Politifact](https://www.politifact.com/) for the data used in training the model.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
