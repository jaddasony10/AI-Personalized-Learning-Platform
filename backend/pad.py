import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

actual = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 0])
predicted = np.array([1, 0, 1, 0, 0, 1, 0, 1, 1, 0])

cm = confusion_matrix(actual, predicted, labels=[1, 0])

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['1 (Pred)', '0 (Pred)'], yticklabels=['1 (Actual)', '0 (Actual)'])
plt.title('Confusion Matrix', fontsize=14)
plt.xlabel('Predicted Label', fontsize=12)
plt.ylabel('Actual Label', fontsize=12)
plt.show()

accuracy = accuracy_score(actual, predicted)
precision = precision_score(actual, predicted, pos_label=1)
recall = recall_score(actual, predicted, pos_label=1)
f1 = f1_score(actual, predicted, pos_label=1)

print(f"Accuracy:  {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall:    {recall:.2f}")
print(f"F1 Score:  {f1:.2f}")