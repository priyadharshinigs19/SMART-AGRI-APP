import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier

# Load dataset
data = pd.read_csv("Crop_recommendation.csv")

# Features & Target
X = data.drop('label', axis=1)
y = data['label']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 🔹 Step 1: Train with GridSearch
params = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5]
}

rf = RandomForestClassifier(random_state=42)

grid = GridSearchCV(rf, params, cv=5)
grid.fit(X_train, y_train)

# 🔹 Step 2: Get best model
model = grid.best_estimator_

# 🔹 Step 3: Proper cross-validation (NEW model with best params)
rf_final = RandomForestClassifier(**grid.best_params_)

scores = cross_val_score(rf_final, X, y, cv=5)

accuracy = round(scores.mean() * 100, 2)

print("Model Accuracy:", accuracy)
print("Cross-validation scores:", scores)

# 🔹 Prediction function
def predict_crop(input_data):
    import pandas as pd
    
    columns = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    
    input_df = pd.DataFrame([input_data], columns=columns)
    
    return model.predict(input_df)[0]
import pickle

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)