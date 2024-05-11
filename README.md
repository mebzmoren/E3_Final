# London Bike-Share Usage Analysis

This is the final project for the E3 - Professional Elective class. 

is a Streamlit app that analyzes and visualizes the usage patterns of the London Bike-Share system. The app provides interactive filters and visualizations to explore the bike-share data.

## Dependencies

The app relies on the following Python libraries:

- Streamlit
- pandas
- Matplotlib
- Seaborn

Make sure you have these libraries installed before running the app. You can install them using pip:

```
pip install requirements.txt
```

## Dataset

The dataset used in this project is the London Bike-Share Usage Dataset, obtained from Kaggle. You can find the dataset at the following link:

[London Bike-Share Usage Dataset](https://www.kaggle.com/datasets/kalacheva/london-bike-share-usage-dataset)

## Usage

1. Make sure you have the `LondonBikeJourneyAug2023.csv` file in the same directory as the `e3_proj.py` file as that file contains the bike-share usage data.

2. Open your terminal or command prompt, navigate to the directory where the `e3_proj.py` file is located, and run the following command:

   ```
   streamlit run <filepath>
   ```

3. The Streamlit app will open in your default web browser.

4. Use the filters in the sidebar to select specific bike models, start stations, end stations, and date ranges. The visualizations and metrics will update based on the selected filters.

5. To stop the app, press `Ctrl + C` in your terminal or command prompt.

