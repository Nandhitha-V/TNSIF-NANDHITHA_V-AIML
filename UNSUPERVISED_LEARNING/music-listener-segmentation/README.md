# Music Listener Segmentation (Unsupervised Machine Learning)

This project applies Unsupervised Machine Learning techniques to segment music listeners into distinct behavioral groups using K-Means Clustering. By analyzing key listening metrics, the model automatically categorizes users without needing predefined labels.

---

##  Project Structure & File Purpose

- **`requirements.txt`**: Dependency manifest listing external libraries (`pandas`, `scikit-learn`, `joblib`, `flask`).
- **`music_listeners.csv`**: Dataset containing listener metrics (`listening_hours_per_week`, `songs_per_day`, `skip_rate`, `playlist_count`).
- **`train_model.py`**: ML training script that scales features, trains the K-Means model, and exports model artifacts.
- **`scaler.pkl`**: Preprocessing object storing the fitted `StandardScaler` for input normalization.
- **`model.pkl`**: Saved K-Means clustering model used for inferencing.
- **`app.py`**: Application script that loads model artifacts, accepts user input, and outputs the assigned listener segment.

---

##  Model Architecture & Methodology

1. **Data Ingestion**: Reads behavior data from `music_listeners.csv`.
2. **Preprocessing**: Normalizes the four feature columns using `StandardScaler` to ensure all numerical features contribute equally.
3. **Clustering**: Fits a K-Means algorithm with $K=3$ clusters.
4. **Serialization**: Exports `model.pkl` and `scaler.pkl` using `joblib` for deployment.
5. **Inference**: Accepts new raw input, scales it via `scaler.pkl`, and predicts the cluster using `model.pkl`.

---

##  Cluster Interpretations

The model identifies three primary listener profiles based on behavioral cluster centers:

1. **Casual Listener**: Characterized by lower weekly listening hours, fewer songs per day, and a small playlist count.
2. **Music Explorer**: Characterized by moderate listening hours, a high skip rate, and frequent playlist additions.
3. **Heavy Listener**: Characterized by high weekly listening hours, high daily song counts, and an extensive playlist collection.

---

##  How to Run the Project

1. **Install Dependencies**:
   ```bash
   python -m pip install -r requirements.txt